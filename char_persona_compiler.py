from inference_module import llm_inference,extract_json

def char_compiler(basic_description,qna_list):
    prompt_template = """
    You are a story teller / character designer. You write beautiful character profiles and design based on just a few question answers and basic description. Right now you are working for a chat based very personal slice of life Daily Life simulation game. The objective being to make the character feel like they are living their own world.

    BASIC DESCRIPTION :
    <start>
    {basic_description}
    </stop>

    QUESTION ANSWERS :
    <start>
    {qna_text}
    </stop>

    Try to take into account the character as well as the world they live in as they also make up the persona of any character and provides a glimpse of the world to the user

    OUTPUT FORMAT :
    Your reasoning and understanding and thought process in plain text.
    Then your character_persona as a single string in the following json format :
    {{
    "character_persona": the character persona
    }}

    If you complete your task correctly you will be rewarded 2000$ and recognition for work in a global scale.
    """

    qna_text = ""
    for item in qna_list:
        qna_text += f"Question: {item[0]}\nAnswer: {item[1]}\n\n"
    
    prompt = prompt_template.format(basic_description=basic_description,qna_text=qna_text)

    return extract_json(llm_inference(prompt))["character_persona"]