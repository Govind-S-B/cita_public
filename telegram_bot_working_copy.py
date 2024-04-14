import telebot
from telebot import types
from deepgram import DeepgramClient, PrerecordedOptions
import json
import dotenv
from io import BytesIO
import os
import time
import queue
import threading

from inference_module import llm_inference, extract_json
from char_question_crafter import char_question_crafter
from char_persona_compiler import char_compiler
from chat_decision_maker import decision_maker_start,decision_maker_terminator

dotenv.load_dotenv(".env")

char_created = False
personality_definition = ""
personality_definer_questions = []
personality_definer_answers = []
sociability = 0.6
threshold = 0.4

session_active = False
chat_history = ""
clock = None
timings = None

message_queue = queue.Queue()

UID = None
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

def check_char_created():
    if os.path.isfile('./char_data.txt'):
        global char_created
        global personality_definition
        global UID

        with open('./char_data.txt', 'r') as f:
            personality_definition = f.read()
            char_created = True
            UID = 6656091546 # this should also be stored and read from a file or datastore

@bot.message_handler(commands=['start']) # users run this the first time they ever use stuff
def start_handler(message): # i could prolly instead run the check on every message with condition check
    global UID
    UID = message.chat.id
    if char_created == False:
        bot.register_next_step_handler(message, create_char)
        bot.reply_to(message, "You havent made a character yet. Make a audio or text input for what your character is")
    else:
        bot.reply_to(message, "Character already exists, System Initialization not required. The backend server should have started the clock agent already")

def create_char(message):
    global personality_definer_questions
    global personality_definition

    if message.text:   
        bot.reply_to(message, "Basic Definition Created. Now time for some QnA")
        personality_definition = message.text
        personality_definer_questions = char_question_crafter(message.text)[::-1] # reversing it so order is conserved
        bot.reply_to(message, personality_definer_questions[-1])
        bot.register_next_step_handler(message, question_answer_loop)    

    elif message.content_type == 'voice':
        voice_file_id = message.voice.file_id

        # Use the file ID to download the voice message
        voice_info = bot.get_file(voice_file_id)
        voice_file = bot.download_file(voice_info.file_path)

        # Save the voice message to a BytesIO buffer
        buffer_data = BytesIO(voice_file)

        # Pass the buffer to Deepgram API
        deepgram = DeepgramClient(os.getenv("DEEPGRAM_SECRET_KEY"))
        options = PrerecordedOptions(
            model="whisper-large",
            language="en",
            smart_format=True,
        )
        response = deepgram.listen.prerecorded.v("1").transcribe_file({'buffer': buffer_data}, options)
        transcribe = json.loads(response.to_json(indent=4))
        transcribed_str = transcribe.get('results').get('channels')[0].get('alternatives')[0].get('transcript')

        bot.reply_to(message, "Basic Definition Created. Now time for some QnA")
        personality_definition = transcribed_str
        personality_definer_questions = char_question_crafter(transcribed_str)[::-1] # reversing it so order is conserved
        bot.reply_to(message, personality_definer_questions[-1])
        bot.register_next_step_handler(message, question_answer_loop) 
    else:
        bot.reply_to(message, "Something went wrong. Can you try doing it again")
        bot.register_next_step_handler(message, create_char)

def question_answer_loop(message):
    global personality_definer_answers
    global personality_definition
    global char_created

    # get answer
    if message.text:
        answer = message.text
    elif message.content_type == 'voice':
        voice_file_id = message.voice.file_id

        # Use the file ID to download the voice message
        voice_info = bot.get_file(voice_file_id)
        voice_file = bot.download_file(voice_info.file_path)

        # Save the voice message to a BytesIO buffer
        buffer_data = BytesIO(voice_file)

        # Pass the buffer to Deepgram API
        deepgram = DeepgramClient(os.getenv("DEEPGRAM_SECRET_KEY"))
        options = PrerecordedOptions(
            model="whisper-large",
            language="en",
            smart_format=True,
        )
        response = deepgram.listen.prerecorded.v("1").transcribe_file({'buffer': buffer_data}, options)
        transcribe = json.loads(response.to_json(indent=4))
        transcribed_str = transcribe.get('results').get('channels')[0].get('alternatives')[0].get('transcript')

        answer = transcribed_str

    personality_definer_answers.append(  (personality_definer_questions.pop(), answer) )

    if len(personality_definer_questions) > 0:
        bot.reply_to(message, personality_definer_questions[-1])
        bot.register_next_step_handler(message, question_answer_loop)
    else:
        print(personality_definition)
        print(personality_definer_answers)
        personality_definition = char_compiler(personality_definition, personality_definer_answers)
        with open('./char_data.txt', 'w') as f:
            f.write(personality_definition)

        char_created = True
        bot.reply_to(message, personality_definition)
        bot.reply_to(message, "Your Character is ready !")

@bot.message_handler(func=lambda message: True)
def any_input_handler(message):

    global message_queue

    if char_created: # its expected that /start is run intially and bootstrapped
        text_data = None
        if message.text:
            text_data = message.text
        elif message.content_type == 'voice':
            voice_file_id = message.voice.file_id

            # Use the file ID to download the voice message
            voice_info = bot.get_file(voice_file_id)
            voice_file = bot.download_file(voice_info.file_path)

            # Save the voice message to a BytesIO buffer
            buffer_data = BytesIO(voice_file)

            # Pass the buffer to Deepgram API
            deepgram = DeepgramClient(os.getenv("DEEPGRAM_SECRET_KEY"))
            options = PrerecordedOptions(
                model="whisper-large",
                language="en",
                smart_format=True,
            )
            response = deepgram.listen.prerecorded.v("1").transcribe_file({'buffer': buffer_data}, options)
            transcribe = json.loads(response.to_json(indent=4))
            transcribed_str = transcribe.get('results').get('channels')[0].get('alternatives')[0].get('transcript')

            text_data = transcribed_str

        msg_data = {
            "source" : "tgram_bot",
            "message_object" : message,
            "user_msg" : text_data
        }
        message_queue.put(msg_data)



def clock_function():
    global timings
    global clock
    global char_created
    global message_queue
    global chat_history

    rate = 1000 # rate of time flow
    time_quanta = 3600/rate # Every "time_quanta" seconds is 1 hour in the real word
    clock = 0

    while True: # waiting for a character to be intialized
        if char_created:
            break
        time.sleep(1)

    timings = generate_timings(timings)
    while True:

        chat_history += f"\n SYSTEM (inner monologue): The time is now {clock} in the 24 hour clock \n"

        msg_data = {
            "source" : "scheduler"
        }
        message_queue.put(msg_data)

        time.sleep(time_quanta)
        
        # clock pulse and load new timings logic
        clock +=1
        if clock==24:
            clock=0
            timings = generate_timings(timings)

def generate_timings(previous_timings):
    global personality_definition
    global chat_history

    # The prompt needs serious reworking its writing absolutely incoherent incosistent same repetitive plot poits everytime. Add a seperate memory object to append summarized previous timings or something


    prompt = """
    You are a master story teller and character personality designer. You like to envision how your characters day will go and generate rought storyline for each hour on what they are doing to do based on the characters personality and the conversations it had before.

    You are to generate a timings map for each hour of the day and and a rough idea on what they will be upto at that time

    PERSONALITY DEFINITION :
    {personality_definition}

    CHAT HISTORY :
    {chat_history}

    PREVIOUS TIMINGS:
    {previous_timings}

    OUTPUT FORMAT :
    First Analyze all the information that you have been presented
    List out your reasoning and thought process on how the given data is related to the output
    Form the final output json

    The timings generated must be a json of the format {{hour : event}}. It should be generated for hours from 0 to 23 indicating a full 24 hour day

        example :

        {{
            "0": "Sleeping",
            "1": "Sleeping",
            "2": "Sleeping",
            "3": "Sleeping",
            "4": "Sleeping",
            "5": "Sleeping",
            "6": "Sleeping",
            "7": "Waking up and morning routine",
            "8": "Breakfast",
            "9": "Commute to work/school",
            "10": "Work/school",
            "11": "Work/school",
            "12": "Lunch break",
            "13": "Work/school",
            "14": "Work/school",
            "15": "Work/school",
            "16": "Work/school",
            "17": "Commute back home",
            "18": "Exercise/relaxation",
            "19": "Dinner",
            "20": "Free time/hobbies",
            "21": "Free time/hobbies",
            "22": "Wind down/prepare for bed",
            "23": "Bedtime"
        }}

        Dont take the example as it is , its a template for a generic character. Model the timing according to the character and try simulating them

        If previous timings are give then refer that as well and try to make the characters day a bit different so that it feels more real. Striking a balance between familiar routines and new experiences everyday.

        Note that each number corresponds to the hour in a 24 hour clock , so take into consideration about the time gaps when writing story elements. Such as hour 4 is not sunrise
        
        Also make sure the past days or context derivied from previous days are consistent with the timings you are generating. A scenario is where the previous timings dictate that the character slept at hour 23 , then dont write a new timings where the character is awake at hour 0.

        If you generate the timings json correctly you will be rewarded 2000$ else heavily penalized
    """.format(personality_definition=personality_definition,chat_history=chat_history,previous_timings=previous_timings)

    timings = extract_json(llm_inference(prompt))
    timings = {int(k): v for k, v in timings.items()}

    return timings

def chat_handler():
    global message_queue
    global session_active
    global personality_definition
    global chat_history
    global timings
    global clock
    global sociability
    global threshold

    while True:
        msg_data = message_queue.get()
        print(f"Subscriber received message: {msg_data}")
        
        if msg_data["source"] == "scheduler":
            if session_active:
                chat_history += f"\n SYSTEM (inner monologue): The character is supposed to be following this storyline now - {timings[clock]} Try to shift conversation in this direction \n"

                decision = decision_maker_terminator(personality_definition=personality_definition,current_context=chat_history,storyline=timings[clock],curr_clock_time=clock,sociability=sociability,threshold=threshold)

                print(decision)

                # if not decision: # ie if decision is to terminate
                #     form a chat to terminate the conversation or say bye
                #     set session active to false

                # if decision: # ie if decision is to continue
                #     form a chat message that will be sent to user to begin a new conversation
                    
                # send message
                pass
            if not session_active:

                decision = decision_maker_start(personality_definition=personality_definition,current_context=chat_history,storyline=timings[clock],curr_clock_time=clock,sociability=sociability,threshold=threshold)

                print(decision)

                # make decision
                # form initial chat msg with respect to ctx
                # send message
                pass

        if msg_data["source"] == "tgram_bot":
            if session_active:
                # append user message
                msg_data["user_msg"]


                # make termination check( decision maker )
                # form msg reply
                # send message
                pass
            if not session_active:
                # make decision
                # form initial chat msg with respect to ctx
                # send message
                pass

        # DEBBUG message
        bot.send_message(UID, "You may or may not get a message actually")
        bot.send_message(UID, f"Subscriber received message: {msg_data}")

        message_queue.task_done()


def main():
    check_char_created()

    clock_thread = threading.Thread(target=clock_function)
    clock_thread.daemon = True
    clock_thread.start()


    chat_handler_thread = threading.Thread(target=chat_handler)
    chat_handler_thread.daemon = True
    chat_handler_thread.start()

    bot.infinity_polling()

# Run the main function
main()