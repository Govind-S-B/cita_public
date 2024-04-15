May god help you navigate the code cause this is cursed

Hey this is my attempt 0 at building a conversation initiating agent
Its a telegram bot cause I cant be bothered to create a UI when telegram already has a beautiful UI. Stop reinventing the wheel. Especially since its an OSS project

I cant show u the commit history cause its in my private repo and i accidentally commited my key in there.
So yeah this is a publicly available cleaned up repo.

# Some stuff from my presentation
## Some diagrams to help out


## Additional Improvements to be made
- Its all 3 threads and not modularized properly
- No prompt injection protection (im already making a ton of calls )
- Refactoring is required very much
- Add random offsets to time to simulate imperfection
- Increase Resolution of internal clock ( hours -> minutes -> seconds )
- Improve all the prompts and experimenting with better EQ focused finetune models
- Using multiple models for varying specialized tasks
- Optimizing for speed
- Data Stores are now ephemeral , make it persistent and load on system init
- RAG for more related context for old contexts ( NA for hackathon )

## References
Generative Agents Paper : https://arxiv.org/pdf/2304.03442.pdf
