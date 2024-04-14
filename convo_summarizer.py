from inference_module import llm_inference, extract_json

def convo_summarizer(convo_sample):
    prompt = """
  You are an expert story teller and good at summarizing conversations in dense summaries so that someone can pick up what their conversation was about without having to read through the entire conversation.
  This is done so that the context about what was being discussed is not lost but not super extensive as well.

  You can remove the unneccsary context from the conversation and only pick up on the key points that you think will be remembered a week later as well.

  The conversation to summarize is 
  ---
  {convo_sample}
  ---

  The output should be in json format as below:
  {{
    "summary": the dense summary as a single string of text about what the conversation was about
  }}
    """.format(convo_sample=convo_sample)

    return extract_json(llm_inference(prompt))["summary"]


if __name__ == "__main__":
  convo_sample = """
User: Hey Cita, what's up? I was hoping you could tell me more about this whole magic thing you're always going on about.

Cita: Ooh girl, you have no idea what you're in for! This magic stuff is seriously wild. But in the best way possible, you know?

User: Haha yeah, I've noticed you getting pretty into it lately. So spill the details - what's it all about?

Cita: Okay, okay, buckle up! So the deal with magic in this realm is that it comes from the world's natural energy. We mages can channel that power through all sorts of spells and incantations.

It's like...harnessing the elements themselves. I've been focusing a lot on evocation - you know, fire, lightning, that kind of thing. The power is just, wow, it's insane.

User: Woah, that sounds intense! But I bet it's not all sunshine and rainbows, is it? What kind of challenges have you been facing?

Cita: Ugh, don't even get me started! There's just so much to learn, it's crazy. Like, the different schools of magic, the intricate hand movements, keeping your focus during a spell...it's a lot, you know?

And don't even get me started on the physical toll. I'm wiped out after even the simplest rituals sometimes. Plus, there's always the risk of a spell going haywire. It's all very humbling, let me tell you.

User: Yikes, that does sound super tough. But you seem pretty determined to keep at it. What's keeping you motivated through all the hard work?

Cita: Haha, yeah, I'm not gonna lie - some days I just want to throw in the towel. But then I remember the sheer power of it all, you know? The ability to shape the very elements themselves? It's like nothing else.

And the more I learn, the more I realize how much more there is to discover. Magic is this endless well of possibility. I can't just walk away from that! Even with all the challenges, the thrill of it keeps pulling me back.

User: I can totally see why. You've definitely got me intrigued now. Any advice for a newbie mage like myself who wants to get in on the action?

Cita: Ooh girl, I thought you'd never ask! Okay, listen up - discipline and focus are key. You gotta train that mind of yours, through meditation and all sorts of mental exercises.

And practice, practice, practice. Spellcasting is not something that comes naturally, even for us prodigies. You're gonna have to put in the time to really master those incantations and gestures.

But most importantly, stay curious! Don't be afraid to experiment and push the boundaries of what you know. That's where the real magic happens. You got this, girl!

User: Awesome, thanks so much Cita! Can't wait to give it all a try. Maybe you can even teach me a thing or two sometime?

Cita: Haha, you know it! Anytime, my friend. The arcane arts await - let's go show 'em what we've got!
"""

  print(convo_summarizer(convo_sample))

