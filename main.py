import os
import io
import discord
from discord.ext import commands
import json
import requests
import PIL
from PIL import Image
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
wc_folder= 'wc_kits/'
sombrero_folder = 'sombreros/'
wallpaper_folder = 'wallpapers/'
# Returns JSON object as a dictionary
pfp_atts = json.load(data)


# list of the various outfits you want to offer. these should match the filename on the outfit pngs

outfits = ["cape", "blue", "daovote", "ghost","halo", "horns","portugal", "portugalsolana","pumpkin", "sombrero", "suit-blk", "suit-pink", "vote","votebrero", "vr"]

wc_kits = ["argentina", "australia", "belgium", "brazil", "canada", "costarica", "croatia", "england", "france", "germany", "italy", "mexico", "mexico+", "netherlands", "portugal", "serbia", "southkorea", "spain", "usa"]
# Search for the pfp id in the JSON dictionary and return the image URL associated with that id. You'll need to update the keys to match what's in your JSON delattr

sombreros = ["black", "blacktie", "cinco", "easter", "october", "pink"]

phone_backgrounds = ["black_stack", "blue_stack", "blue", "green_icons", "green_md", "green_stack", "green", "white_blue_md", "white_icons", "yellow"]

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


def get_dressed(fit, pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return

def make_wallpaper(wallpaper, pfp_id):
    background = Image.open(wallpaper_folder + wallpaper.lower() + '.png')
    monke = Image.open(no_background_folder + pfp_id + '.png')
    monke = monke.resize((int(monke.width*5), int(monke.height*5)))
    background.paste(monke, (0, 1920), mask=monke)
    background.save(save_img_folder + wallpaper.lower() + str(pfp_id) + '.png')

    return

def deleteDressed(fit, pfp_id):
    os.remove(save_img_folder + fit.lower() + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')

def get_kit(fit, pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    outfit = Image.open(wc_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return

def get_brero(fit, pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    brero = Image.open(sombrero_folder + fit.lower() + '.png')

    pfp.paste(brero, (0,0), mask=brero)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return

def no_background_wc(fit, pfp_id):
    pfp = Image.open(no_background_folder + str(pfp_id) + '.png')
    outfit = Image.open(wc_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return

def no_background_fit(fit, pfp_id):
    pfp = Image.open(no_background_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return

def brero_no_background(fit, pfp_id):
    pfp = Image.open(no_background_folder + str(pfp_id) + '.png')
    outfit = Image.open(sombrero_folder + str(pfp_id) + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return

def high_quality(pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

    pfp = pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    pfp.resize((int(pfp.width*5), int(pfp.height*5)))
    pfp.save(save_img_folder + 'hq' + str(pfp_id) + '.png')

    return

def delete_hq(pfp_id):
    os.remove(save_img_folder + 'hq' + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# !newfit command executes the get_dressed function and returns the resulting image. It accepts a value between 1 and 5000. Update this to use the command name you want and the values to fit the range of your project


@bot.command(name="newfit", brief='Dress your pfp', description='This command will let you apply new fits to your pfp')
async def newfit(ctx, fit: str, pfp_id: int):
    try:
        if fit.lower() in outfits:
            if 0 <= pfp_id <= 5000:
                get_dressed(fit, str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
                deleteDressed(str(pfp_id))
        else:
            await ctx.send('Please enter a valid fit. Check ?fits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 5000.')


@bot.command(name="newbrero", brief='new sombrero for your monke', description='This command will let you apply new sombrero to your pfp')
async def newbrero(ctx, fit: str, pfp_id: int):
    try:
        if fit.lower() in sombreros:
            if 0 <= pfp_id <= 5000:
                get_brero(fit, str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
                deleteDressed(str(pfp_id))
        else:
            await ctx.send('Please enter a valid fit. Check ?sombrero for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 5000.')

# Lists the different "fits" available. This just returns the outfits list on new lines


@bot.command(brief='List avaiable fits', description='This command will list the different outfits available to you')
async def fits(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(outfits))

@bot.command(brief='List avaiable World Cup kits', description='This command will list the different World Cup kits available to you')
async def kits(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(wc_kits))

@bot.command(brief='List avaiable sombreros', description='This command will list the different outfits available to you')
async def sombrero(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(sombreros))

@bot.command(brief='List avaiable wallpaper backgrounds', description='This command will list the different wallpaper backgrounds available to you')
async def wallpapers(ctx):
    await ctx.send('**List of wallpapers (please choose from one of the below)**\n\n' + "\n".join(phone_backgrounds))

# Lets user know when they enter an invalid command

@bot.command(name="nobackground", brief="this will return the chosen monke with no background")
async def nobackground(ctx, pfp_id: int):
    try:
        if 0 < pfp_id <=5000:
            await ctx.send(file=discord.File(no_background_folder + str(pfp_id) + '.png'))

        else: await ctx.send('Please enter a number between 1 and 5000')

    except:
        await ctx.send("unknow error")

@bot.command(name="wc", brief='World Cup Kits', description='This command will let you apply select wc kits to your monke, type `?kits` to see available countries')
async def wc(ctx, fit: str, pfp_id: int):
    try:
        if fit.lower() in wc_kits:
            if 0 <= pfp_id <= 5000:
                get_kit(fit, str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
                deleteDressed(fit, str(pfp_id))
        else:
            await ctx.send('Please enter a valid kit. Check ?kits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 5000.')

@bot.command(name="wcnb", brief='World Cup Kits no background', description='This command will let you apply select wc kits to your monke, and return them without a background. type `?kits` to see available countries')
async def wc_nb(ctx, fit: str, pfp_id: int):
    try:
        if fit.lower() in wc_kits:
            if 0 <= pfp_id <= 5000:
                no_background_wc(fit, str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
                deleteDressed(fit, str(pfp_id))
        else:
            await ctx.send('Please enter a valid kit. Check ?kits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 5000.')

@bot.command(name="newfitnb", brief='new fits no background', description='This command will let you apply fits, and return them without a background. type `?fits` to see available fits')
async def fit_nb(ctx, fit: str, pfp_id: int):
    try:
        if fit.lower() in outfits:
            if 0 <= pfp_id <= 5000:
                no_background_fit(fit, str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
                deleteDressed(fit, str(pfp_id))
        else:
            await ctx.send('Please enter a valid kit. Check ?kits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 5000.')

@bot.command(name="wallpaper", brief='Phone Wallpaper', description='This command will let make a phone wallpapere, type `?wallpapers` to see available backgrounds')
async def wallpaper(ctx, wallpaper: str, pfp_id: int):
    try:
        if wallpaper.lower() in phone_backgrounds:
            if 0 <= pfp_id <= 5000:
                make_wallpaper(wallpaper, str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + wallpaper.lower() + str(pfp_id) + '.png'))
                deleteDressed(wallpaper, str(pfp_id))
        else:
            await ctx.send('Please enter a valid wallpaper. Check ?wallpapers for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 5000.')

@bot.command(name="hq", brief='High Resolution Monke', description='This command will return an upscaled version of your monke 1920 x 1920')
async def hq(ctx, pfp_id: int):
    try:

            if 0 <= pfp_id <= 5000:
                high_quality(str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + 'hq' + str(pfp_id) + '.png'))
                delete_hq(pfp_id)
            else:
                await ctx.send('Please enter a valid number between 1 and 5000')
    except:
        await ctx.send('Please enter a valid number between 1 and 5000.')


@bot.event
async def on_command_error(ctx, error):
    # or discord.ext.commands.errors.CommandNotFound as you wrote
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command, please check `?help` for a list of available commands")

load_dotenv()

bot.run(os.getenv('TOKEN'))
