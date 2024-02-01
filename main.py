import disnake
import os
import random
from functions import roll_dice, format_roll_input
from functions import gather_spell_data, format_response
from disnake.ext import commands
from keep_alive import keep_alive

#Defines the bot
bot = commands.InteractionBot(
    test_guilds=[1055087390521307228, 1032978996813643776, 996085683594727424])
"""
Parameters: String in the form of XdY+-Z
Returns: Response containing the total and the individual rolls
"""


@bot.slash_command(
    description="Rolls X dice of size Y and adds or subtracts Z (XdY+Z || XdY-Z)"
)
async def roll(inter, details: str):
    try:
        #Formats the user data
        dice_cnt, dice_size, dice_mod = format_roll_input(details)

        #Error traps extraneous input
        if dice_cnt > 1000 or dice_cnt <= 0 or dice_size <= 1:
            raise Exception("Extraneous Input")

        #Rolls dice, updates response
        rolls = roll_dice(dice_size, dice_cnt)
        response = f"> **Total:** {sum(rolls)+dice_mod}\n> **Details:** ({details}) {rolls}"

    #If invalid, update response, sends response
    except:
        response = "> Invalid Input"
    await inter.response.send_message(response)


"""
Parameters: N/A
Returns: 6 stats containing the sum and three individual rolls followed by a total
"""


@bot.slash_command(description="Generates Stats for 5th Ed DND character")
async def statmaster(inter):
    response, total = "> ***__Results:__***\n", 0
    for x in range(1, 7):

        #Roll 4 dice and take highest 3
        rolls = roll_dice(6, 4)
        rolls.sort()
        rolls.pop(0)

        #Adds the results to the response
        response += f"> **Stat {x}:** {sum(rolls)} {rolls}\n"
        total += sum(rolls)

    #Adds the total, sends response
    response += f"> **Total:** {total}"
    await inter.response.send_message(response)


"""
Parameters: String of the creature name and a int of the number of creatures
Returns: Generates proposed loot based on the creature and the number of creatures
"""


@bot.slash_command(
    description="Determines random loot from a given creature name")
async def loot(inter, creature_name: str):

    #Creates the file name
    file_name = "loot_tables/" + creature_name.lower() + ".txt"

    #Generates random line
    i = random.randint(1, 12)

    #Reads all the data from the file
    with open(file_name) as file:
        lines = file.readlines()

    #Sends response
    #await inter.response.send_message("> " + lines[i])
    await inter.response.send_message("In progress")


"""
Parameters: Spell Name
Returns: The Spell Info
"""

@bot.slash_command(
    description="Given a spell name returns data about that spell")
async def spellinfo(inter, spell_name: str):

    try:
        #Gathers spell info and formats
        link = f"http://dnd5e.wikidot.com/spell:{spell_name}"
        spell_info = gather_spell_data(link)

        #Formats and sends response
        response = format_response(spell_info, spell_name)
        await inter.response.send_message(response)
    except:
        await inter.response.send_message("Spell Not Found")


#Runs the bot
keep_alive()
bot.run(os.environ["TOKEN"])
