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


# Returns JSON object as a dictionary
pfp_atts = json.load(data)


def get_pfp_img_url(id):
    for pfp in pfp_atts:
        if id == pfp['number']:
            return pfp['Image']


# Downloads the pfp from the image URL and saves it in a directory

def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)

# Combines the pfp image with a transparent png of the attribute  and saves it to an output directory


def get_dressed(fit: str, pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return


def make_b_w(pfp_id):
    url = (get_pfp_img_url(str(pfp_id)))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    monke = pfp.convert("L")
    monke.save(save_img_folder + 'bw' + str(pfp_id) + '.png')
    return


make_b_w(5001)
