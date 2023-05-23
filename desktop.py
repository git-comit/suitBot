import os
from dotenv import load_dotenv
import io
import json
import requests
import PIL
from PIL import Image


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
# Returns JSON object as a dictionary
pfp_atts = json.load(data)


# list of the various outfits you want to offer. these should match the filename on the outfit pngs

outfits = ["bandito_santa_full", "bandito_santa", "blue", "cape", "daovote", "elf", "ghost", "halo", "horns", "masters", "portugal",
           "portugalsolana", "pumpkin", "santa_hat", "santa", "shotta", "sombrero", "stronger", "suit-blk", "suit-pink", "vote", "votebrero", "vr"]

wc_kits = ["argentina", "australia", "belgium", "brazil", "canada", "costarica", "croatia", "england", "france",
           "germany", "italy", "mexico", "mexico+", "netherlands", "portugal", "serbia", "southkorea", "spain", "usa"]
# Search for the pfp id in the JSON dictionary and return the image URL associated with that id. You'll need to update the keys to match what's in your JSON delattr

sombreros = ["black", "blacktie", "cinco", "easter", "october", "pink"]

phone_backgrounds = ["all_black", "black_fade", "black_stack",  "blue_stack", "blue",
                     "green_icons", "green_md", "green_stack", "green", "white_blue_md", "white_icons", "yellow"]

pfp_backgrounds = ["blue", "green", "red"]

banners = ["black", "blue_bananas", "blue_green_wave", "blue", "green_bananas", "green_wave", "green",
           "monkeDAO_green", "monkeDAO1", "monkeDAO2", "white_bananas", "wordmark_blue", "wordmark_green", "yellow_blue"]


# Need to add error handling

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


def make_smol(pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')
    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    pfp_bg_color = pfp.convert('RGB')
    r, g, b = pfp_bg_color.getpixel((300, 300))
    smol_im = pfp.resize((int(pfp.width/3), int(pfp.height/3)))

    smol = Image.new('RGB', (384, 384), (r, g, b))
    smol.paste(smol_im, (128, 256), mask=smol_im)

    smol.save(save_img_folder + 'smol' + str(pfp_id) + '.png')

    return


def make_desktop(w, h, pfp_id):
    url = get_pfp_img_url(pfp_id)
    download_image(url, pfp_folder + str(pfp_id) + '.png')
    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    pfp_bg_color = pfp.convert('RGB')
    r, g, b = pfp_bg_color.getpixel((300, 300))
    background = Image.new('RGB', (w, h), (r, g, b))
    i = 0
    while i < w:
        j = 0

        while j < h:
            background.paste(pfp, (i, j), mask=pfp)
            j += 1000

        i += 1000
    background.save(save_img_folder + 'desktop' + str(pfp_id) + '.png')

    return


# make_banner("black", "4470", "5001", "3", "443", "2232")
# make_banner("yellow_blue", "4470", "5001", "3", "443", "2232")
make_desktop(1080, 1920, "4470")
