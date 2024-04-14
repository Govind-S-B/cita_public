from inference_module import llm_inference,extract_json

def char_question_crafter(char_desc):
    prompt_template = """
    You are a story teller / character designer. You are to frame questions to ask the user to help them design a character for a chat based very personal slice of life. Daily Life simulation game.
    So you need to gather information about how the character behaves and what thier day looks like , what motivates them and what they do for a living. You will also need to ask about the character personality and how they handle stress and adversity. How talkative they are. Relevant questions about their backstory that makes them who they are. And many other such questions to get a feel for who the character is on a personal level. Enough to deeply understand the person and simulate the person in a conversation.

    Given below is the base level character description:
    <start>
    {char_desc}
    </stop>

    Note that each question must be independant of the other and can be asked in any order.
    You can only ask 10 questions within that you try to understand the character and simulate them. Use questions wisely therefore.

    A general flow you can take is First write out your reasoning and general understanding for the user and the world they reside in. And then try to think through how to flesh out the character and define them better. Then form questions relevant to building this character.

    OUTPUT FORMAT :
    Your reasoning and understanding and thought process in plain text.
    Then your questions in the following json format :
    {{
    "questions": [ list of questions as strings ]
    }}

    If you complete your task correctly you will be rewarded 2000$ and recognition for work in a global scale.
    """

    prompt = prompt_template.format(char_desc=char_desc)

    return extract_json(llm_inference(prompt))["questions"]