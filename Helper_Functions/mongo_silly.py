# --------- web imports ---------
import json
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Literal
from bson import ObjectId
import time
import datetime
from datetime import timedelta
from Helper_Functions.end_time import months_to_days
from typing import overload

"""
####################################################################
############       THE WHOLE POINT OF THIS       ###################
##############        FILE IS TO HOLD        #######################
#######      HELPER FUNCTIONS AND OTHER VARIABLES       ############
####################################################################
"""

# ---------------------------------------------variables-----------------------------------------------------------------
_in_ce = True
"""Determines if you'd like to run the CE Bot or a test bot."""

# ------------- mongo variables -------------
mongo_ids = {
    "name_old" : ObjectId('64f8d47f827cce7b4ac9d35b'),
    "tier" : ObjectId('64f8bc4d094bdbfc3f7d0050'),
    "curator" : ObjectId('64f8d63592d3fe5849c1ba35'),
    "tasks" : ObjectId('64f8d6b292d3fe5849c1ba37'),
    "user" : ObjectId('64f8bd1b094bdbfc3f7d0051'),
    "unfinished" : ObjectId('650076a9e35bbc49b06c9881'),
    "name" : ObjectId('6500f7d3b3e4253bef9f51e6'),
    "steamhunters" : ObjectId('65f64af8ba6efd911038594c')
}
"""The :class:`ObjectID` values stored under the `_id` value in each document."""
_uri = "mongodb+srv://andrewgarcha:KUTo7dCtGRy4Nrhd@ce-cluster.inrqkb3.mongodb.net/?retryWrites=true&w=majority"
_mongo_client = AsyncIOMotorClient(_uri)
_mongo_database = _mongo_client['database_name']
collection = _mongo_client['database_name']['ce-collection']
"""The MongoDB collection used to pull and push all the databases."""

# ------------- image icons -------------
ce_mountain_icon = "https://i.imgur.com/4PPsX4o.jpg"
"""The mountain icon used most commonly by CE."""
ce_hex_icon = "https://i.imgur.com/FLq0rFQ.png"
"""The hex icon used by CE's banner."""
ce_james_icon = "https://i.imgur.com/fcdHTvx.png"
"""The icon made by James that was previously used."""
final_ce_icon = "https://i.imgur.com/O9J7fg2.png"
"""The icon made by @crappy for CE Assistant."""

# ------------- discord channel numbers -------------
# ce ids
_ce_log_old_id = 1208259110638985246         # old log
_ce_log_id = 1218980203209035938             # current log
_ce_casino_test_id = 1208259878381031485     # fake casino
_ce_casino_id = 1080137628604694629          # real casino
_ce_game_additions_id = 949482536726298666   # game additions
_ce_private_log_id = 1208259110638985246     # private log
# bot test ids
_test_log_id = 1141886539157221457
_test_casino_id = 811286469251039333
_test_game_additions_id = 1128742486416834570
# go-to channels 
# NOTE: replace these with the ids as needed
if _in_ce:
    game_additions_id = _ce_game_additions_id
    casino_id = _ce_casino_id
    log_id = _ce_log_id
    private_log_id = _ce_private_log_id
else :
    game_additions_id = _test_game_additions_id
    casino_id = _test_casino_id
    log_id = _test_log_id
    private_log_id = _test_log_id

# ------------- emoji icons -------------
icons = {
    # tiers
    "Tier 0" : '<:tier0:1126268390605070426>',
    "Tier 1" : '<:tier1:1126268393725644810>',
    "Tier 2" : '<:tier2:1126268395483037776>',
    "Tier 3" : '<:tier3:1126268398561677364>',
    "Tier 4" : '<:tier4:1126268402596585524>',
    "Tier 5" : '<:tier5:1126268404781809756>',
    "Tier 6" : '<:tier6:1126268408116285541>',
    "Tier 7" : '<:tier7:1126268411220074547>',

    # genres
    "Action" : '<:CE_action:1126326215356198942>',
    "Arcade" : '<:CE_arcade:1126326209983291473>',
    "Bullet Hell" : '<:CE_bullethell:1126326205642190848>',
    "First-Person" : '<:CE_firstperson:1126326202102186034>',
    "Platformer" : '<:CE_platformer:1126326197983383604>',
    "Strategy" : '<:CE_strategy:1126326195915591690>',

    # others
    "Points" : '<:CE_points:1128420207329816597>',
    'Arrow' : '<:CE_arrow:1126293045315375257>',

    # ranks
    "A Rank" : '<:rank_a:1126268299504795658>',
    "B Rank" : '<:rank_b:1126268303480979517>',
    "C Rank" : '<:rank_c:1126268305083215913>',
    "D Rank" : '<:rank_d:1126268307813715999>',
    "E Rank" : '<:rank_e:1126268309730512947>',
    "S Rank" : '<:rank_s:1126268319855562853>',
    "SS Rank" : '<:rank_ss:1126268323089367200>',
    "SSS Rank" : '<:rank_sss:1126268324804833280>',
    "EX Rank" : '<:rank_ex:1126268312842666075>',
    "P Rank" : '<:rank_p:1126268315279564800>',
    "Q Rank" : '<:rank_q:1126268318081364128>',

    # miscellaneous
    "Casino" : '<:CE_casino:1128844342732263464>',
    "Diamond" : '<:CE_diamond:1126286987524051064>',
    "All" : '<:CE_all:1126326219332399134>',
    "Rank Omega" : '<:rank_omega:1126293063455756318>',
    "Hexagon" : '<:CE_hexagon:1126289532497694730>',
    "Site Dev" : '<:SiteDev:963835646538027018>',

    # reactions
    "Shake" : '<:shake:894912425869074462>',
    "Safety" : '<:safety:802615322858487838>'
}
"""All of the CE emojis that CE Assistant uses."""

# ------ genres ------
all_genres = ["Action", "Arcade", "Bullet Hell", "First-Person", "Platformer", "Strategy"]
_game_to_id = {
    '- Challenge Enthusiasts -' : "76574ec1-42df-4488-a511-b9f2d9290e5d",
    '- Puzzle Games - ' : "27578157-10b2-4f29-acee-452c2dc59477",
    'clown town 1443' : "09f100aa-caa7-4154-a224-1c3e9277eea4",
    'RetroArch' : "5144e054-d64e-465f-9d0e-3c517a0fe92b"
}

ce_squared_id = "76574ec1-42df-4488-a511-b9f2d9290e5d"
"""The CE ID for the game `- Challenge Enthusiasts -`."""



# ---------------------------------------------functions-----------------------------------------------------------------


# -------- get and set mongo databases --------
_mongo_names = Literal["name_old", "tier", "curator", "user", "tasks", "unfinished", "name", "steamhunters"]
async def get_mongo(title : _mongo_names):
    """Returns the MongoDB associated with `title`."""
    _db = await collection.find_one({'_id' : mongo_ids[title]})
    del _db['_id']
    return _db

async def dump_mongo(title : _mongo_names, data) :
    """Dumps the MongoDB given by `title` and passed by `data`."""
    if "_id" not in data : data["_id"] = mongo_ids[title]
    return await collection.replace_one({'_id' : mongo_ids[title]}, data)


# ----- get unix timestamp for x days from now -----
# NOTE: this is technically wrong. old_unix should technically
#       start the cooldown  from the time the roll STARTS, not when it ends.
def get_unix(days = 0, minutes = -1, months = -1, old_unix = -1) -> int:
    """Returns a unix timestamp for `days` days (or `minutes` minutes, or `months` months) from the current time.
    \nAdditionally, `old_unix` can be passed as a parameter to get `days` days (or `minutes` minutes, or `months` months) from that unix."""
    # -- old unix passed --
    if(old_unix != -1) :
        if (minutes != -1) : return int(minutes * 60) + old_unix
        elif (months != -1) : return (months_to_days(months))*(86400) + old_unix
        else : return days * 86400 + old_unix

    # -- old unix NOT passed --
    # return right now
    if(days == "now") : return int(time.mktime((datetime.datetime.now()).timetuple()))
    # return minutes
    elif (minutes != -1) : return int(time.mktime((datetime.datetime.now()+timedelta(minutes=minutes)).timetuple()))
    # return months
    elif (months != -1) : return get_unix(months_to_days(months))
    # return days
    else: return int(time.mktime((datetime.datetime.now()+timedelta(days)).timetuple()))

# ----- convert ce timestamp to unix timestamp -----
def timestamp_to_unix(timestamp : str) -> int :
    """Takes in the CE timestamp (`"2024-02-25T07:04:38.000Z"`) and converts it to unix timestamp (`1708862678`)"""
    return int(time.mktime(datetime.datetime.strptime(str(timestamp[:-5:]), "%Y-%m-%dT%H:%M:%S").timetuple()))

# ------ check if a t0 is valid ------
def is_valid_t0(name : str) -> bool:
    """Takes in a T0 and checks to see if it's one of the permanent ones (CE, Puzzle, clown town, Retro)."""
    return name in ['- Challenge Enthusiasts -', '- Puzzle Games -', 'clown town 1443', 'RetroArch']

# ------ get a ce-id from a discord id ------
#@overload
async def get_ce_id(discord_id : str) -> str | None:
    """(ASYNC) Takes in a Discord ID (`347900490668965888`) and returns their CE ID (`835afaad-0059-4e39-b24f-24b2c76b1d08`), or `None` if they aren't registered."""
    database_user = await get_mongo("user")
    for user in database_user :
        if database_user[user]['Discord ID'] == discord_id :
            return user
    
    del database_user
    return None
#@overload
def get_ce_id_normal(discord_id : str, database_user) -> str | None :
    """(SYNC) Takes in a Discord ID (`347900490668965888`) and returns their CE ID (`835afaad-0059-4e39-b24f-24b2c76b1d08`), or `None` if they aren't registered."""
    for user in database_user:
        if database_user[user]['Discord ID'] == discord_id : return user

    return None

# ------ get a specific api page ------
_ce_api_types = Literal["game", "user"]
def get_api(type : _ce_api_types, id : str) -> dict | None:
    """Return the CE-api page of any user or game."""
    try:
        response = requests.get(f"https://cedb.me/api/{type}/{id}")
        data = json.loads(response.text)
        del response
    except Exception as e:
        print(e)
        data = None
    
    return data


# ----------------------------------------------------------------------------------------------------------------------------