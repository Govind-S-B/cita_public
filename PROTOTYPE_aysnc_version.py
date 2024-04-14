import asyncio

# https://betterprogramming.pub/solve-common-asynchronous-scenarios-fire-and-forget-pub-sub-and-data-pipelines-with-python-asyncio-7f20d1268ade

def generate_timings():
    
    timings = {
        0: "Sleeping",
        1: "Sleeping",
        2: "Sleeping",
        3: "Sleeping",
        4: "Sleeping",
        5: "Sleeping",
        6: "Sleeping",
        7: "Waking up and morning routine",
        8: "Breakfast",
        9: "Commute to work/school",
        10: "Work/school",
        11: "Work/school",
        12: "Lunch break",
        13: "Work/school",
        14: "Work/school",
        15: "Work/school",
        16: "Work/school",
        17: "Commute back home",
        18: "Exercise/relaxation",
        19: "Dinner",
        20: "Free time/hobbies",
        21: "Free time/hobbies",
        22: "Wind down/prepare for bed",
        23: "Bedtime"
    }

    return timings


###

# session is a consumer function and during each pulse it checks if actions exist before proceeding with a conversation
# ie check if queue has some request
# then proceeds with telegram bot
# the telegram bot and session is very intertwined
# session is either active or inactive
# session object should exposed methods to get status
# methods to add things to queue
# process queue if exist and if session active continue chat on eery pulse ( use a similar clock tick approach 0)


# TELEGRAM BOT ( SESSION HANDLER COMPONENT )
# if text receive check if session is active
# if session is not active , set active and pass user message to session service
# session service can also call the function in tgram bot to send a message
# the session  


#### EXPERIMENTAL DEFINTIONS

def check_session_exist(): # checks if session exist
    pass

def session_context_injector(): # trigger to inject hourly context to an ongoing session if exist
    pass

def user_chat_chat_initiator():
    
    # triggered when user sends a chat while session not exist ( this should be checked on telegrams ide)
    
    pass

####

async def process_task(description): 
    # takes in current hour's description
    # takes in other personality and history artifacts
    # makes a decision  based on those factors and if session already exist
    # if things are clear make a new chat session if not discard ( optimally have a way to push this to context )
    print(description)
    await asyncio.sleep(2)

async def scheduler(time_quanta):
    clock = 0
    timings = generate_timings()
    while True:
        print(timings[clock])
        await asyncio.sleep(time_quanta)  # Every "time_quanta" seconds is 1 hour in the real word
        
        # clock pulse and load new timings logic
        clock +=1
        if clock==24:
            clock=0
            timings = generate_timings()

# Main function
async def main():
    rate = 5 * 1000 # rate of time flow
    time_quanta = 3600/rate
    await scheduler(time_quanta)

# Run the main function
asyncio.run(main())