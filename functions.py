import random
import requests
from requests import request
import re
from bs4 import BeautifulSoup

#Rolls a dice of a given size (dice_size) a number of times equal to count
#Returns a list containing the rolls
def roll_dice(dice_size, count = 1):
    if count < 1: raise Exception("Number of rolls must be above 1")
    rolls = []
    for x in range(count):
        rolls.append(random.randint(1, dice_size))
    return rolls

#Takes details in form of XdY+-Z and returns X, Y, and Z
def format_roll_input(details):
    
    #Gets number of dice to roll
    X, excess_details = details.lower().split('d')
    if X == "":
      X = 1
    else: X = int(X)

    #Determines if there is a + or - modifier in the
    plus, minus = -1, -1
    try:
        plus = excess_details.index("+")
    except: pass
    try:
        minus = excess_details.index("-")
    except: pass

    #If there is a modifier then get the first one for indexing
    i = 0
    if plus != -1:
        i = plus
    if minus != -1 and i > minus:
        i = minus

    #Evaluates the excess details
    if i != 0: Y, Z = int(excess_details[:i]), eval(excess_details[i:])
    else: Y, Z = int(excess_details), 0

    return X, Y, Z

#Give a link to the spell webpage gather the needed data
def gather_spell_data(link):

    #Get request and checked for spell
    r = requests.get(link)
    if r.status_code != 200: return "Spell Not Found"

    #Gathers spell data if found and returns tuple of data
    soup = BeautifulSoup(r.text, "html.parser")
    return re.findall(r"Source: (.*)\n(.*)\nCasting Time: (.*)\nRange: (.*)\nComponents: (.*)\nDuration: (.*)\n((.|\n)*(?=Spell Lists.))Spell Lists\. (.*)", soup.find(id="page-content").text)[0]

#Given the spell_info create a string to send to chat
def format_response(spell_info, spell_name):
    if spell_info == "Spell Not Found": return "> Spell Not Found"
    response = f"> **__{spell_name.title()}__:**\n"
    response += f"> *{spell_info[1]}*\n"
    response += f"> ***Source:** {spell_info[0]}*\n"
    response += f"> **Casting Time:** {spell_info[2]}\n"
    response += f"> **Range:** {spell_info[3]}\n"
    response += f"> **Components** {spell_info[4]}\n"
    response += f"> **Duration** {spell_info[5]}\n"

    #Formats the spell description and details
    data = spell_info[6].split('\n')
    data.pop(-1)
    response += f"> **Details:** {data[0]}\n"
    for d in data[1:]:
        response += f"> \t{d}\n"
    response += f"> **Castable by:** *{spell_info[8]}*"
    
    return response