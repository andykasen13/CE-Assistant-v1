# ---------- time imports -----------
import asyncio
from datetime import datetime, timedelta
import datetime
import functools
import time
import typing

# ----------- discord imports ---------
import discord
from discord import app_commands
import random
from typing import Literal

# ----------- json imports ------------
import json
import psutil

# --------- web imports ---------
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# --------- other file imports ---------
from Web_Interaction.curator import loop
from Web_Interaction.scraping import get_achievements, get_games


# --------------------------------------------------- ok back to the normal bot ----------------------------------------------
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

intents.message_content = True

# Grab information from json file
with open('Jasons/secret_info.json') as f :
    localJSONData = json.load(f)

discord_token = localJSONData['discord_token']
guild_ID = localJSONData['guild_ID']

# Add the guild ids in which the slash command will appear. 
# If it should be in all, remove the argument, but note that 
# it will take some time (up to an hour) to register the command 
# if it's for all guilds.
    

# ------------------------------------------------------------------------------------------------------------------------------ #
# ---------------------------------------------------------HELP COMMAND--------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------ #
@tree.command(name="help", description="help", guild=discord.Object(id=guild_ID))
async def help(interaction) :
    # Defer the message
    await interaction.response.defer()

    # Create the view (will be used for buttons later)
    view = discord.ui.View(timeout=600)

    helpInfo = {
        "Rolls" : "This bot has the ability to roll random games for any event in the Challenge Enthusiast server. P.S. andy reminder to get autofill to work!",
        "/get_rolls" : "Use this command to see your current (and past) rolls, or the rolls of any other user in the server.",
        "steam_test" : "Get general information about any STEAM game.",
        "Curator" : "The bot will automatically check to see if any new entries have been added to the CE curator (within three hours)."
    }

    embeds=[]
    pageNum = 1
    
    for page in list(helpInfo):
        embed=discord.Embed(color=0x000000, title=page, description=helpInfo[page])
        embed.set_footer(text=(f"Page {pageNum} of {len(list(helpInfo))}"))
        embed.timestamp=datetime.datetime.now()
        embeds.append(embed)
        pageNum+=1

    await get_buttons(view, embeds)

    await interaction.followup.send(embed=embeds[0], view=view)


# ------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------------ROLL COMMAND --------------------------------------------------------- # 
# ------------------------------------------------------------------------------------------------------------------------------- #
events = Literal["One Hell of a Day", "One Hell of a Week", "One Hell of a Month", "Two Week T2 Streak", 
          "Two 'Two Week T2 Streak' Streak", "Never Lucky", "Triple Threat", "Let Fate Decide", "Fourward Thinking",
          "Russian Roulette"]

@tree.command(name="roll", description="Participate in Challenge Enthusiast roll events!", guild=discord.Object(id=guild_ID))
async def roll_command(interaction, event: events) -> None:
    await interaction.response.defer()

    # Open file
    tier_one_file = open("faket1list.txt", "r")
    data = tier_one_file.read()
    data_into_list = data.split("\n")
    tier_one_file.close()

    view = discord.ui.View(timeout=600)
    game = "error"

    #  -------------------------------------------- One Hell of a Day  --------------------------------------------
    if event == "One Hell of a Day" :
        # Pick a random game from the list
        game = random.choice(data_into_list)
        print("Rolled game: " + game)

        # Create the embed
        embed = getEmbed(game, interaction.user.id)
        embed.add_field(name="Roll Requirements", value = 
            "You have one day to complete " + embed.title + "."    
            + "\nMust be completed by <t:" + str(int(time.mktime((datetime.datetime.now()+timedelta(1)).timetuple())))
            + ">\nOne Hell of a Day has a two week cooldown."
            + "\nCooldown ends on <t:" + str(int(time.mktime((datetime.datetime.now()+timedelta(14)).timetuple())))
            + ">\n[insert link to cedb.me page]", inline=False)
        embed.set_author(name="ONE HELL OF A DAY", url="https://example.com")

    # -------------------------------------------- Two week t2 streak --------------------------------------------
    elif event == "Two Week T2 Streak" :
        # two random t2s
        print("received two week t2 streak")
        games = []
        embeds = []

        # ----- Grab two random games -----
        i=0
        while(i != 2) :
            games.append(random.choice(data_into_list))
            i += 1
        game = games[0] + " and " + games[1]

        # ----- Create opening embed -----
        embeds.append(discord.Embed(
            color=0x000000,
            title="Two Week T2 Streak",
            description="games lol"))
        embeds[0].set_footer(text="Page 1 of 3")
        i=1
        for gamer in games:
            embeds[0].description += "\n" + str(i) + ". " + gamer
            i+=1
        embeds[0].add_field(name="Roll Requirements", value =
            "You have two weeks to complete " + embeds[0].title + "."
            + "\nMust be completed by <t:" + str(int(time.mktime((datetime.datetime.now()+timedelta(14)).timetuple())))
            + ">\nTwo Week T2 Streak has no cooldown."
            + "\n[insert link to cedb.me page]", inline=False)
        embeds[0].set_author(name = "TWO WEEK T2 STREAK", url="https://example.com")

        # ----- Create the embeds for each game -----
        #currentPage = 1
        page_limit = 3
        i=0
        for gamer in games :
            embeds.append(getEmbed(gamer, interaction.user.id))
            embeds[i+1].set_footer(text=(f"Page {i+2} of {page_limit}"))
            embeds[i+1].set_author(name="TWO WEEK T2 STREAK")
            i+=1

        # ----- Set the embed to send as the first one ------
        embed = embeds[0]
       
        # ----- Create buttons -----
        await get_buttons(view, embeds)



    # -------------------------------------------- One Hell of a Week --------------------------------------------
    elif event == "One Hell of a Week" :
        # t1s from each category
        embed = discord.Embed(title=f"you ave week")

    # -------------------------------------------- One Hell of a Month --------------------------------------------
    elif event == "One Hell of a Month" : 
        # five t1s from each category
        embed = discord.Embed(title=f"you have month")

    # -------------------------------------------- Two "Two Week T2 Streak" Streak --------------------------------------------
    elif event == "Two 'Two Week T2 Streak' Streak" :
        # four t2s
        embed = discord.Embed(title=("two two week t2 streak streak"))

    # -------------------------------------------- Never Lucky --------------------------------------------
    elif event == "Never Lucky" :
        # one t3
        embed = discord.Embed(title=("never lucky"))

    # -------------------------------------------- Triple Threat --------------------------------------------
    elif event == "Triple Threat" :
        # three t3s
        embed = discord.Embed(title=("triple threat"))
         
    # -------------------------------------------- Let Fate Decide --------------------------------------------
    elif event == "Let Fate Decide" :
        # one t4
        embed = discord.Embed(title=("let fate decide"))

    # -------------------------------------------- Fourward Thinking --------------------------------------------
    elif event == "Fourward Thinking" :
        # idk
        embed = discord.Embed(title=("fourward thinking"))

    # -------------------------------------------- Russian Roulette --------------------------------------------
    elif event == "Russian Roulette" :
        # choose six t5s and get one at random
        embed = discord.Embed(title=("russian roulette"))

    # -------------------------------------------- kill yourself --------------------------------------------
    else : embed=discord.Embed(title=(f"'{event}' is not a valid event."))

    # open the json file
    with open('Jasons/users.json', 'r') as f :
        userInfo = json.load(f)
    
    # find the location of the user
    i = 0
    while userInfo['users'][i]['ID'] != interaction.user.id :
        i += 1
        
    # append the roll to the user's current rolls array
    # userInfo['users'][i]['current_rolls'].append({"event_name" : "One Hell of a Day", 
    #                                               "games" : [{"name" : embed.title, "completed" : False}], 
    #                                               "end_time" : "" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    # dump the info
    with open('Jasosns/users.json', 'w') as f :
        json.dump(userInfo, f, indent=4)
    # ---------------------------------------------
    # ------------------ Co-ops -------------------
    # Destiny Alignment: You and another player roll games
    #   from the other's library, and both must complete them
    # Soul Mates: You and another player agree on a tier, 
    #   and then a game is rolled (time limit based on tier)

    # Finally, send the embed
    await interaction.followup.send(embed=embed, view=view)
    print("Sent information on rolled game: " + game)


# -------------------------------------------------------------------------------------------------- #
# -------------------------------------------- BUTTONS --------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #

async def get_buttons(view, embeds):
    currentPage = 1
    page_limit = len(embeds)
    buttons = [discord.ui.Button(label=">", style=discord.ButtonStyle.green, disabled=False), discord.ui.Button(label="<", style=discord.ButtonStyle.red, disabled=True)]
    view.add_item(buttons[1])
    view.add_item(buttons[0])

    async def hehe(interaction):
        return await callback(interaction, num=1)

    async def haha(interaction):
        return await callback(interaction, num=-1)

    async def callback(interaction, num):
        nonlocal currentPage, view, embeds, page_limit, buttons
        currentPage+=num
        if(currentPage >= page_limit) :
            buttons[0].disabled = True
        else : buttons[0].disabled = False
        if(currentPage <= 1) :
            buttons[1].disabled = True
        else : buttons[1].disabled = False
        await interaction.response.edit_message(embed=embeds[currentPage-1], view=view)

    buttons[0].callback = hehe
    buttons[1].callback = haha


# ----------------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------- MY_ROLLS COMMAND --------------------------------------------------------- # 
# ----------------------------------------------------------------------------------------------------------------------------------- #
@tree.command(name="check_rolls", description="Check the active rolls of anyone on the server", guild=discord.Object(id=guild_ID))
async def checkRolls(interaction, user: discord.Member=None) :
    # defer the message
    await interaction.response.defer()

    # if no user is provided default to sender
    if user is None :
        user = interaction.user

    #open the json file and get the data
    with open('Jasons/users.json', 'r') as f :
        userInfo = json.load(f)

    #iterate through the json file until you find the
    #designated user
    userNum = 0
    while userInfo['users'][userNum]['ID'] != user.id :
        if(userNum + 1 == len(userInfo['users'])) : return await interaction.followup.send("This user does not exist.")
        else: userNum += 1

    # set up this bullshit
    currentrollstr = ""
    completedrollstr = ""

    # grab all current rolls
    for x in userInfo['users'][userNum]['current_rolls'] :
        end_time = time.mktime(datetime.strptime(str(x['end_time']), "%Y-%m-%d %H:%M:%S").timetuple())
        currentrollstr = currentrollstr + "- __" + x['event_name'] + "__ (complete by <t:" + str(int(end_time)) + ">):\n"
        gameNum = 1
        for y in x['games'] :
            if(y['completed']) :
                currentrollstr += (" " + str(gameNum) + ". " + y['name'] + " (completed)\n")
            else : currentrollstr += (" " + str(gameNum) + ". " + y['name'] + " (not completed)\n")
            gameNum += 1
    
    # account for no current rolls
    if(currentrollstr == "") :
        currentrollstr = f"{user.name} has no current rolls."

    # grab all completed rolls
    for x in userInfo['users'][userNum]['completed_rolls'] :
        end_time = time.mktime(datetime.strptime(str(x['completed_time']), "%Y-%m-%d %H:%M:%S").timetuple())
        completedrollstr += "- __" + x['event_name'] + "__ (completed on <t:" + str(int(end_time)) + ">):\n"
        gameNum = 0
        for y in x['games'] :
            completedrollstr += (" " + str(gameNum) + ". " + y['name'] + "\n")
            gameNum += 1
    
    # account for no completed rolls
    if(completedrollstr == "") :
        completedrollstr = f"{user.global_name} has no completed rolls."
    
    # make the embed that you're going to send
    embed = discord.Embed(
    colour=0x000000,
    timestamp=datetime.datetime.now())
    embed.add_field(name="User", value = "<@" + str(user.id) + ">", inline=False)
    embed.add_field(name="Current Rolls", value=currentrollstr, inline=False)
    embed.add_field(name="Completed Rolls", value=completedrollstr, inline=False)
    embed.set_thumbnail(url=user.avatar.url)
    embed.set_footer(text="CE Assistant",
        icon_url="https://cdn.discordapp.com/attachments/639112509445505046/891449764787408966/challent.jpg")

    # send the embed
    await interaction.followup.send(embed=embed)



# ---------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------- THREADING ------------------------------------------------------------ #
# ---------------------------------------------------------------------------------------------------------------------------------- #

def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------- SCRAPING --------------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------- #

@to_thread
def scrape_thread_call():
    get_games()

@tree.command(name="scrape", description="run through each game in the CE database and grab the corresponding data", guild=discord.Object(id=guild_ID))
async def scrape(interaction):
    await interaction.response.defer()
    await scrape_thread_call()
    await interaction.followup.send("scraped")


# ---------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- COMMAND RESOURCE TESTING ---------------------------------------------------- #
# ---------------------------------------------------------------------------------------------------------------------------------- #

@tree.command(name="resource_testing", description="runs function while recording ram and time", guild=discord.Object(id=guild_ID))
async def resource_testing(function):
    ram_usage = []
    time = []
    ram_before = psutil.virtual_memory()[3]/1000000000
    time_before = datetime.datetime.now()
    await function
    ram_after = psutil.virtual_memory()[3]/1000000000
    time_after = datetime.datetime.now()
    ram_usage.append(ram_after-ram_before)
    time.append((time_after-time_before).total_seconds())

    print('ram usage (GB): ' + str(sum(ram_usage)/len(ram_usage)))
    print('time taken (s):' + str(sum(time)/len(time)))


# ----------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------- STEAM TEST COMMAND ------------------------------------------------------ #
# ----------------------------------------------------------------------------------------------------------------------------------- #

@tree.command(name="steam_game", description="Get information on any steam game", guild=discord.Object(id=guild_ID))
async def steam_command(interaction, game_name: str):

    # Log the command
    print("Recieved steam_game command with parameter: " + game_name + ".")

    # Defer the interaction
    await interaction.response.defer()

    # Get the embed
    embed = getEmbed(game_name, interaction.user.id)
    embed.set_author(name="REQUESTED STEAM GAME INFO ON '" + game_name + "'")
    embed.remove_field(1)
    embed.add_field(name="Requested by", value="<@" + str(interaction.user.id) + ">", inline=True)
    embed.add_field(name="CE Status", value="Not on CE / x Points", inline=True)
    embed.add_field(name="CE Owners", value="[insert]", inline=True)
    embed.add_field(name="CE Completions", value="[insert]", inline=True)

    # Finally, send the embed
    await interaction.followup.send(embed=embed)

    # And log it
    print("Sent information on requested game " + game_name + "\n")


# ----------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------- GET EMBED FUNCTION ------------------------------------------------------ #
# ----------------------------------------------------------------------------------------------------------------------------------- #
def getEmbed(game_name, authorID):

    #TODO add error exceptions
    #TODO turn this into a class with getters and setters for wider versatility

    game_word_lst = game_name.split(" ")
    for name in game_word_lst:
        if len(name) != len(name.encode()):
            game_word_lst.pop(game_word_lst.index(name))


    searchable_game_name = " ".join(game_word_lst)

    payload = {'term': searchable_game_name, 'f': 'games', 'cc' : 'us', 'l' : 'english'}
    response = requests.get('https://store.steampowered.com/search/suggest?', params=payload)

    divs = BeautifulSoup(response.text, features="html.parser").find_all('div')
    ass = BeautifulSoup(response.text, features="html.parser").find_all('a')
    options = []
    for div in divs:
        try:
            if div["class"][0] == "match_name":
                options.append(div.text)
        except:
            continue
    

        correct_app_id = ass[0]['data-ds-appid']

    for i in range(0, len(options)):
        if game_name == options[i]:
            correct_app_id = ass[i]['data-ds-appid']

# --- DOWNLOAD JSON FILE ---

    # Open and save the JSON data
    payload = {'appids': correct_app_id, 'cc' : 'US'}
    response = requests.get("https://store.steampowered.com/api/appdetails?", params = payload)
    jsonData = json.loads(response.text)
    
    # Save important information
    gameTitle = jsonData[correct_app_id]['data']['name']
    imageLink = jsonData[correct_app_id]['data']['header_image']
    gameDescription = jsonData[correct_app_id]['data']['short_description']
    if(jsonData[correct_app_id]['data']['is_free']) : 
        gamePrice = "Free"
    else: gamePrice = jsonData[correct_app_id]['data']['price_overview']['final_formatted']
    gameNameWithLinkFormat = game_name.replace(" ", "_")

# --- CREATE EMBED ---

    # and create the embed!
    embed = discord.Embed(title=f"{gameTitle}",
        url=f"https://store.steampowered.com/app/{correct_app_id}/{gameNameWithLinkFormat}/",
        description=(f"{gameDescription}"),
        colour=0x000000,
        timestamp=datetime.datetime.now())

    embed.add_field(name="Price", value = gamePrice, inline=True)
    embed.add_field(name="User", value = "<@" + str(authorID) + ">", inline=True)
    
    embed.set_author(name="[INSERT ROLL EVENT NAME HERE]", url="https://example.com")
    embed.set_image(url=imageLink)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/639112509445505046/891449764787408966/challent.jpg")
    embed.set_footer(text="CE Assistant",
        icon_url="https://cdn.discordapp.com/attachments/639112509445505046/891449764787408966/challent.jpg")
    return embed


# --------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------TEST COMMAND------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------- #

@tree.command(name="test_command", description="test", guild=discord.Object(id=guild_ID))
async def test(interaction) :
    await interaction.response.defer()
    print(get_achievements("-SPROUT-"))
    await interaction.followup.send("achievements achieved")

# ----------------------------------- LOG IN ----------------------------
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_ID))
    print("Ready!")
    await loop.start(client)

client.run(discord_token)