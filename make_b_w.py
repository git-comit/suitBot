import os
import io
import discord
from discord.ext import commands
import json
import requests
import PIL
from PIL import Image, ImageSequence
from dotenv import load_dotenv

port = int(os.environ.get('PORT', 33507))
# discord bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)

# Opening JSON file with pfps. Add your open file and update it to match the name here
data = open('attributes.json')

# Folder locations for clean pfps, completed pfps, and outfits

save_img_folder = 'dressed_pfps/'
pfp_folder = 'clean_pfps/'
outfits_folder = 'outfits/'
no_background_folder = 'no_background/'
wc_folder = 'wc_kits/'
sombrero_folder = 'sombreros/'
wallpaper_folder = 'wallpapers/'
pfp_background_folder = 'pfp_backgrounds/'
banner_folder = 'banners/'
gif_folder = 'gifs/'
watch_folder = 'watchfaces/'

# Returns JSON object as a dictionary
pfp_atts = json.load(data)


def make_watch(bg, pfp_id):
    background = Image.open(watch_folder + bg.lower() + '.png')
    monke = Image.open(no_background_folder + str(pfp_id) + '.png')
    monke = monke.resize((int(monke.width*2.3), int(monke.height*2.3)))
    background.paste(monke, (-40, 85), mask=monke)
    background.save(save_img_folder + bg.lower() + str(pfp_id) + '.png')

    return


make_watch("blue", "4432")
