from inference_module import llm_inference,extract_json
import random


def decision_maker_start(personality_definition,current_context,storyline,curr_clock_time,sociability,threshold):
    prompt = """
You are an expert story teller and good at simulating behaviour of fictional personalities and understanding their thought processes. Think from the characters POV

You will be given a personalities description and the context of the conversation they had before. You will also be given the storyline of what the user was doing during that time

You need to give emphasis on the timing while you consider this.
From the perspective of the character answer if the character will be in the mood to have a conversation witht he user in the scale of : "Absolutely No" , "No" , "Maybe" , "Yes" , "Absolutely Yes"


PERSONALITY DEFINITION:
{personality_defintion}

CURRENT CHAT HISTORY and CONTEXT :
{current_context}

CURRENT STORYLINE :
{storyline}

CURRENT TIME:
{curr_clock_time}

OUTPUT FORMAT"
The output as specified should be one of : "Absolutely No" , "No" , "Maybe" , "Yes" , "Absolutely Yes"
This should be based on all the information shown earlier to simulate how such a personality would respond under the specified cicumstances

The output should be in json format as below:

{{
"answer": the answer as a single string of text
}}
    """.format(personality_defintion=personality_definition,current_context=current_context,storyline=storyline,curr_clock_time=curr_clock_time)


    score_mapping = {
        "Absolutely No" : 0.2,
        "No" : 0.4,
        "Maybe" : 0.6,
        "Yes" : 0.8,
        "Absolutely Yes" : 1.0
    }
    
    context_based_weight = score_mapping[extract_json(llm_inference(prompt))["answer"]]
    rand_num = random.uniform(0.0, 1.0)
    
    final_score = (context_based_weight * (rand_num + sociability) > threshold)

    return final_score

def decision_maker_terminator(personality_definition,current_context,storyline,curr_clock_time,sociability,threshold):
    prompt = """
You are an expert story teller and good at simulating behaviour of fictional personalities and understanding their thought processes. Think from the characters POV

You will be given a personalities description and the context of the conversation they had before. You will also be given the storyline of what the user was doing during that time

You need to give emphasis on the timing while you consider this.

There is a conversationg on going between the user and character. You need to determine if its time to end the conversation based on the chat history

From the perspective of the character answer if the character will be in the mood to have a conversation witht he user in the scale of : "Absolutely No" , "No" , "Maybe" , "Yes" , "Absolutely Yes"

Absolutely No here indicates that the character would like to stop the conversation as it either got boring for it or the character is tired or the character is busy with her storyline. This should be done with consideration to the personality defined

PERSONALITY DEFINITION:
{personality_defintion}

CURRENT CHAT HISTORY and CONTEXT :
{current_context}

CURRENT STORYLINE :
{storyline}

CURRENT TIME:
{curr_clock_time}

OUTPUT FORMAT"
The output as specified should be one of : "Absolutely No" , "No" , "Maybe" , "Yes" , "Absolutely Yes"
This should be based on all the information shown earlier to simulate how such a personality would respond under the specified cicumstances

The output should be in json format as below:

{{
"answer": the answer as a single string of text
}}
    """.format(personality_defintion=personality_definition,current_context=current_context,storyline=storyline,curr_clock_time=curr_clock_time)


    score_mapping = {
        "Absolutely No" : 0.2,
        "No" : 0.4,
        "Maybe" : 0.6,
        "Yes" : 0.8,
        "Absolutely Yes" : 1.0
    }
    
    context_based_weight = score_mapping[extract_json(llm_inference(prompt))["answer"]]
    rand_num = random.uniform(0.0, 1.0)
    
    final_score = (context_based_weight * (rand_num + sociability) > threshold)

    return final_score