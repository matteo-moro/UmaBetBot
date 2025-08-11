import discord
from discord import app_commands
from typing import Literal
import dbfunc
import yamlfunc

TEST_GUILD = discord.Object(id=<testing guild ID>)

class BotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    
    async def setup_hook(self):
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

intents = discord.Intents.default()
client = BotClient(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("---------")
    await dbfunc.DBInit()


@client.tree.command()
async def register(interaction: discord.Interaction):
    """Registers user to betting database"""
    result = await dbfunc.DBRegister(interaction.user.name)
    if result == True:
        await interaction.response.send_message(f"Registration complete for {interaction.user.mention}")
    elif result == False:
        await interaction.response.send_message(f"Registration failed, if you are not already registered contact unochesiannoia")


@client.tree.command()
@app_commands.describe(
    username="username of the user to modify the bal of",
    modifier="number of carats to use in the operation",
    operation="operation to use on the bal"
)
@app_commands.default_permissions()
async def change_bal(interaction: discord.Interaction, username: str, modifier: int, operation: Literal["Add", "Subtract", "Multiply", "Divide"]):
    """changes the bal of an user"""
    await interaction.response.send_message(f"Modified the balance of {username} by {modifier} with operation {operation}")
    await dbfunc.DBBalMod(username, operation, modifier)

@client.tree.command()
async def addbet(interaction: discord.Interaction, race_id: int, amount: int, jockey_number: int):
    """Adds a bet of the specified amount to the jockey with the specified number"""
    await interaction.response.send_message(f"Added a bet of {amount} carats to jockey number {jockey_number} by {interaction.user.mention}")
    await yamlfunc.add_bet(race_id, interaction.user.name, amount, jockey_number)

@client.tree.command()
async def raceinfo(interaction: discord.Interaction, race_id: int):
    """gives information on the specified race"""
    jockeys = await yamlfunc.GetRaceJockeys(race_id)
    rates = await yamlfunc.GetRaceBetRates(race_id)
    bets = await yamlfunc.GetUsersBets(race_id)

    embed_message = discord.Embed(title = "Race Info", description = "ID = {}".format(race_id))

    jockey_string = ""
    for n in range(jockeys[0]):
        jockey_string += "{}. Name: {}\t|\tHorse: {}\n".format(n + 1, jockeys[1][n][0], jockeys[1][n][1])
    embed_message.add_field(name="Jockeys:", value=jockey_string)

    rates_string = ""
    for n in range(len(rates)):
        rates_string += "{}. {}\n".format(n + 1, rates[n])
    embed_message.add_field(name="Rates:", value=rates_string)

    bets_string = ""
    for n in range(len(bets)):
        bets_string += "Jockey {}:\n".format(n + 1)
        for x in range(len(bets[n])):
            bets_string += "\t{} = {}\n".format(bets[n][x][0], bets[n][x][1])
    embed_message.add_field(name="Bets:", value=bets_string)

    await interaction.response.send_message(embed=embed_message)

@client.tree.command()
@app_commands.default_permissions()
async def declare_results(interaction: discord.Interaction, race_id: int, winner: int):
    """declares if a race was won or lost"""
    rates = await yamlfunc.GetRaceBetRates(race_id)
    bets = await yamlfunc.GetUsersBets(race_id)
    for bet in bets[winner - 1]:
        await dbfunc.DBBalMod(bet[0], "Add", bet[1] * rates[winner - 1])
    await interaction.response.send_message("Race with ID {} has concluded, with the winner being jockey number {}!\nBets have been processed".format(race_id, winner))


client.run("<client id>")
