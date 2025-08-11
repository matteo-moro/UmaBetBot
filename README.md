# UmaBetBot
Bot done with discord.py for a friendly umamusume race to enable betting with a fake currecy  

Functions include:
1. Registering users into a database to mantain their balance
2. Saving the details of races and the bets inside a .yaml file
3. Distributing the wins to players once race results are declared
4. Giving details on specified races

Races are saved in .yaml file with a specific template and are assigned an ID made of 6 ints, starting from 100000 and finishing at 999999  

Future features / WIP:  
- [ ] Capacity of generating race .yaml files from scratch
- [ ] Improvements to the race details embed message
- [ ] Player profiles
- [ ] General bug fixing and ecception handling

### Additional notes:
I am aware this is some of the most ugly python code I have ever written, I am busy and have had no time to think about what i wanted to write in code. Maybe one day this will be fixed if this bot sees any use.  

On another note, the project uses a SQLite database to store player info and PyYaml to manage yaml files
