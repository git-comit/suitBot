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
gen3 = open('gen3Attributes.json')

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
gifs = ["gm", "gm2", "gn", "gn2", "welcome"]
# Returns JSON object as a dictionary
pfp_atts = json.load(data)
gen3_atts = json.load(gen3)


def get_gen3_pfp_img_url(id):
    for pfp in gen3_atts:
        if id == pfp['id']:
            return pfp['image']
# Downloads the pfp from the image URL and saves it in a directory


def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)


def make_gif_gen3(gif, pfp_id):
    gif_string = gif.lower()
    url = (get_gen3_pfp_img_url(str(pfp_id)))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

    animated_gif = Image.open(gif_folder + gif_string + '.gif')
    frames = []
    m = Image.open(pfp_folder + str(pfp_id) + '.png')

    for f in ImageSequence.Iterator(animated_gif):

        frame = f.convert("RGBA")
        monke = m.copy()
        monke.paste(frame, mask=frame)
        # print(monke)
        frames.append(monke)

    if gif_string == 'welcome':
        frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                       '.gif', save_all=True, append_images=frames[1:],  loop=0, duration=500)
    else:
        frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                       '.gif', save_all=True, append_images=frames[1:],  loop=0)
    return


make_gif_gen3('gm', 2)
