May god help you navigate the code cause this is cursed

Hey this is my attempt 0 at building a conversation initiating agent
Its a telegram bot cause I cant be bothered to create a UI when telegram already has a beautiful UI. Stop reinventing the wheel. Especially since its an OSS project

I cant show u the commit history cause its in my private repo and i accidentally commited my key in there.
So yeah this is a publicly available cleaned up repo.

# Some stuff from my presentation

## Some diagrams to help out
![Cita is the thing doe (4)](https://github.com/Govind-S-B/cita_public/assets/62943847/8d9c0d77-bc7a-4d02-a5df-bf3711ccf1d9)
![Cita is the thing doe](https://github.com/Govind-S-B/cita_public/assets/62943847/9687940d-bf0d-49e4-8935-f02b81a6a9e5)
![Cita is the thing doe (1)](https://github.com/Govind-S-B/cita_public/assets/62943847/2b57a0bc-0131-4c51-9226-12e20e311408)
![Cita is the thing doe (2)](https://github.com/Govind-S-B/cita_public/assets/62943847/8cc0c6ce-b5e2-4ea0-9c87-7a00d74a75fe)
![Cita is the thing doe (3)](https://github.com/Govind-S-B/cita_public/assets/62943847/72678a8c-d694-49e5-a922-5b6dec1d8d1a)


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
