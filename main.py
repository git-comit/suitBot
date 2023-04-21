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


# list of the various outfits you want to offer. these should match the filename on the outfit pngs

outfits = ["bandito_santa_full", "bandito_santa", "blue", "cape", "daovote", "elf", "ghost", "halo", "horns", "masters", "portugal",
           "portugalsolana", "pumpkin", "santa_hat", "santa", "shotta", "sombrero", "stronger", "suit-blk", "suit-pink", "vote", "votebrero", "vr"]

wc_kits = ["argentina", "australia", "belgium", "brazil", "canada", "costarica", "croatia", "england", "france",
           "germany", "italy", "mexico", "mexico+", "netherlands", "portugal", "serbia", "southkorea", "spain", "usa"]
# Search for the pfp id in the JSON dictionary and return the image URL associated with that id. You'll need to update the keys to match what's in your JSON delattr

sombreros = ["black", "blacktie", "cinco",
             "easter", "october", "pink", "solana"]

phone_backgrounds = ["all_black", "black_fade", "black_stack",  "blue_stack", "blue",
                     "green_icons", "green_md", "green_stack", "green", "white_blue_md", "white_icons", "yellow"]

pfp_backgrounds = ["blue", "green", "red"]

banners = ["black", "blue_bananas", "blue_green_wave", "blue", "green_bananas", "green_wave", "green_white",
           "green", "white_bananas", "white_green", "white", "wordmark_blue", "wordmark_green", "yellow_blue"]

gifs = ["gm", "gm2", "gn", "gn2"]

watches = ["black_stack", "blue_bananas", "blue_stack", "blue", "green_bananas",
           "green_monke", "green_stack", "green", "white_bananas", "white"]

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


def get_dressed(fit: str, pfp_id):
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


def make_watch(bg, pfp_id):
    background = Image.open(watch_folder + bg.lower() + '.png')
    monke = Image.open(no_background_folder + str(pfp_id) + '.png')
    monke = monke.resize((int(monke.width*2.3), int(monke.height*2.3)))
    background.paste(monke, (-40, 85), mask=monke)
    background.save(save_img_folder + bg.lower() + str(pfp_id) + '.png')

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

    pfp.paste(brero, (0, 0), mask=brero)
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


def pfp_background(background, pfp_id: int):
    pfp = Image.open(pfp_background_folder + background.lower() + '.png')
    monke = Image.open(no_background_folder + str(pfp_id) + '.png')

    pfp.paste(monke, (0, 0), mask=monke)

    pfp.save(save_img_folder + background.lower() + str(pfp_id) + '.png')

    return


def high_quality(pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    monke = pfp.resize((int(pfp.width*5), int(pfp.height*5)))
    monke.save(save_img_folder + 'hq' + str(pfp_id) + '.png')

    return


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


def make_smoller(pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')
    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    pfp_bg_color = pfp.convert('RGB')
    r, g, b = pfp_bg_color.getpixel((300, 300))
    smol_im = pfp.resize((int(pfp.width/6), int(pfp.height/6)))

    smol = Image.new('RGB', (384, 384), (r, g, b))
    smol.paste(smol_im, (160, 320), mask=smol_im)

    smol.save(save_img_folder + 'smol' + str(pfp_id) + '.png')

    return


def make_banner(ban, pfp_id, pfp2=None, pfp3=None, pfp4=None, pfp5=None):
    banner_string = ban.lower()
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')
    background = Image.open(banner_folder + banner_string + '.png')

    if banner_string == "yellow_blue" or banner_string == "blue_green_wave":

        monke = Image.open(pfp_folder + str(pfp_id) + '.png')
        monke = monke.resize(
            (int(monke.width*2.60416666667), int(monke.height*2.60416666667)))
        if pfp2:
            m2 = Image.open(no_background_folder + str(pfp2) + '.png')
            m2 = m2.resize((int(m2.width*1.5), int(m2.height*1.5)))
            background.paste(m2, (1500, 424), mask=m2)
            background.save(save_img_folder + banner_string +

                            str(pfp_id) + '.png')

        if pfp3:
            m3 = Image.open(no_background_folder + str(pfp3) + '.png')
            m3 = m3.resize((int(m3.width*1.5), int(m3.height*1.5)))
            background.paste(m3, (1100, 424), mask=m3)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')
        if pfp4:
            m4 = Image.open(no_background_folder + str(pfp4) + '.png')
            m4 = m4.resize((int(m4.width*1.5), int(m4.height*1.5)))
            background.paste(m4, (700, 424), mask=m4)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        if pfp5:
            m5 = Image.open(no_background_folder + str(pfp5) + '.png')
            m5 = m5.resize((int(m5.width*1.5), int(m5.height*1.5)))
            background.paste(m5, (300, 424), mask=m5)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        background.paste(monke, (2040, 0), mask=monke)
        background.save(save_img_folder + banner_string + str(pfp_id) + '.png')

    elif banner_string == "black" or banner_string == "blue" or banner_string == "green":
        monke = Image.open(no_background_folder + pfp_id + '.png')
        monke = monke.resize((int(monke.width*1.5), int(monke.height*1.5)))

        if pfp2:
            m2 = Image.open(no_background_folder + str(pfp2) + '.png')
            m2 = m2.resize((int(m2.width*1.5), int(m2.height*1.5)))
            background.paste(m2, (1100, 424), mask=m2)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')
        if pfp3:
            m3 = Image.open(no_background_folder + str(pfp3) + '.png')
            m3 = m3.resize((int(m3.width*1.5), int(m3.height*1.5)))
            background.paste(m3, (700, 424), mask=m3)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        if pfp4:
            m4 = Image.open(no_background_folder + str(pfp4) + '.png')
            m4 = m4.resize((int(m4.width*1.5), int(m4.height*1.5)))
            background.paste(m4, (300, 424), mask=m4)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')
        if pfp5:
            m5 = Image.open(no_background_folder + str(pfp5) + '.png')
            m5 = m5.resize((int(m5.width*1.5), int(m5.height*1.5)))
            background.paste(m5, (-100, 424), mask=m5)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        background.paste(monke, (1500, 424), mask=monke)
        background.save(save_img_folder + banner_string + str(pfp_id) + '.png')

    else:

        monke = Image.open(no_background_folder + pfp_id + '.png')
        monke = monke.resize((int(monke.width*1.5), int(monke.height*1.5)))

        if pfp2:
            m2 = Image.open(no_background_folder + str(pfp2) + '.png')
            m2 = m2.resize((int(m2.width*1.5), int(m2.height*1.5)))
            background.paste(m2, (1600, 424), mask=m2)
            background.save(save_img_folder + banner_string +

                            str(pfp_id) + '.png')

        if pfp3:
            m3 = Image.open(no_background_folder + str(pfp3) + '.png')
            m3 = m3.resize((int(m3.width*1.5), int(m3.height*1.5)))
            background.paste(m3, (1200, 424), mask=m3)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')
        if pfp4:
            m4 = Image.open(no_background_folder + str(pfp4) + '.png')
            m4 = m4.resize((int(m4.width*1.5), int(m4.height*1.5)))
            background.paste(m4, (800, 424), mask=m4)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        if pfp5:
            m5 = Image.open(no_background_folder + str(pfp5) + '.png')
            m5 = m5.resize((int(m5.width*1.5), int(m5.height*1.5)))
            background.paste(m5, (400, 424), mask=m5)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        background.paste(monke, (2000, 424), mask=monke)
        background.save(save_img_folder + banner_string + str(pfp_id) + '.png')

    return


def make_gif(gif, pfp_id):
    gif_string = gif.lower()
    url = (get_pfp_img_url(str(pfp_id)))
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
    frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                   '.gif', save_all=True, append_images=frames[1:],  loop=0)

    return


def make_gif_nb(gif, pfp_id):
    gif_string = gif.lower()

    animated_gif = Image.open(gif_folder + gif_string + '.gif')
    frames = []

    for f in ImageSequence.Iterator(animated_gif):
        m = Image.open(no_background_folder + str(pfp_id) + '.png')

        frame = f.convert("RGBA")
        monke = m.copy()
        monke.paste(frame, mask=frame)
        # print(monke)
        frames.append(monke)
    frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                   '.gif', save_all=True, append_images=frames[1:],  loop=0)

    return


def high_quality_no_background(pfp_id):

    pfp = Image.open(no_background_folder + str(pfp_id) + '.png')
    monke = pfp.resize((int(pfp.width*5), int(pfp.height*5)))
    monke.save(save_img_folder + 'hq' + str(pfp_id) + '.png')

    return


def delete_gif(gif, pfp_id):
    gif_string = gif.lower()
    os.remove(save_img_folder + gif_string + str(pfp_id) + '.gif')


def delete_hq(pfp_id):
    os.remove(save_img_folder + 'hq' + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')


def delete_smol(pfp_id):
    os.remove(save_img_folder + 'smol' + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')


def make_b_w(pfp_id):
    url = (get_pfp_img_url(str(pfp_id)))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    monke = pfp.convert("LA")
    monke.save(save_img_folder + 'bw' + str(pfp_id) + '.png')

    return


def delete_bw(pfp_id):
    os.remove(save_img_folder + 'bw' + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# !newfit command executes the get_dressed function and returns the resulting image. It accepts a value between 1 and 5000. Update this to use the command name you want and the values to fit the range of your project


@bot.command(name="newfit", brief='Dress your pfp see `?fits`', description='This command will let you apply new fits to your pfp')
async def newfit(ctx, fit: str, pfp_id: int):
    # try:
    if fit.lower() in outfits:
        if 0 < pfp_id <= 5001:
            get_dressed(fit, str(pfp_id))
            await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
            deleteDressed(str(pfp_id))
        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')

    else:
        await ctx.send('Please enter a valid fit. Check ?fits for options')
    # except:
    # await ctx.send('Please enter a valid number between 1 and 5000.')


@bot.command(name="gif", brief='Dress your pfp see `?list_gifs`', description='This command will let you apply new fits to your pfp')
async def gif(ctx, gif: str, pfp_id: int):
    # try:
    if gif.lower() in gifs:
        if 0 < pfp_id <= 5001:
            make_gif(gif, pfp_id)
            await ctx.send(file=discord.File(save_img_folder + gif + str(pfp_id) + '.gif'))
            delete_gif(gif, pfp_id)
        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')

    else:
        await ctx.send('Please enter a valid fit. Check ?gifs for options')


@bot.command(name="bw", brief='make a black and white monke', description='makes black and white monke')
async def bw(ctx, pfp_id):
    # try:
    if 0 < int(pfp_id) <= 5001:
        make_b_w(pfp_id)
        await ctx.send(file=discord.File(save_img_folder + 'bw' + str(pfp_id) + '.png'))
        delete_bw(pfp_id)
    else:
        await ctx.send('Please enter a valid number between 1 and 5000.')


@bot.command(name="watch", brief='watch face', description='makes watch faces')
async def watch(ctx, bg, pfp_id):
    # try:
    if bg.lower() in watches:
        if 0 < int(pfp_id) <= 5001:
            make_watch(bg, pfp_id)
            await ctx.send(file=discord.File(save_img_folder + bg.lower() + str(pfp_id) + '.png'))
            deleteDressed(bg, pfp_id)
        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')
    else:
        await ctx.send('Please enter a valid fit. Check `?watch_faces` for options')


@bot.command(name="gif_nb", brief='Dress your pfp see `?list_gifs`', description='This command will let you apply new fits to your pfp')
async def gifnb(ctx, gif: str, pfp_id: int):
    # try:
    if gif.lower() in gifs:
        if 0 < pfp_id <= 5001:
            make_gif_nb(gif, pfp_id)
            await ctx.send(file=discord.File(save_img_folder + gif + str(pfp_id) + '.gif'))
            delete_gif(gif, pfp_id)
        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')

    else:
        await ctx.send('Please enter a valid fit. Check ?gifs for options')


@bot.command(name="newbrero", brief='new sombrero for your monke', description='This command will let you apply new sombrero to your pfp')
async def newbrero(ctx, fit: str, pfp_id: int):
    try:
        if fit.lower() in sombreros:
            if 0 < pfp_id <= 5001:
                get_brero(fit, str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
                deleteDressed(str(pfp_id))

            else:
                await ctx.send('Please enter a valid number between 1 and 5000.')
        else:
            await ctx.send('Please enter a valid fit. Check ?sombrero for options')
    except:
        await ctx.send('something went wrong')

# Lists the different "fits" available. This just returns the outfits list on new lines


@bot.command(brief='List avaiable fits', description='This command will list the different outfits available to you')
async def fits(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(outfits))


@bot.command(brief='List avaiable watch faces', description='This command will list the different watch faces available to you')
async def watch_faces(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(watches))


@bot.command(brief='List avaiable gifs', description='This command will list the different outfits available to you')
async def list_gifs(ctx):
    await ctx.send('**List of gifs (please choose from one of the below)**\n\n' + "\n".join(gifs))


@bot.command(brief='show docs', description='help document')
async def docs(ctx):
    await ctx.send("https://monkedao.gitbook.io/welcome-to-monkedao/monke-outfits")


@bot.command(brief='List avaiable World Cup kits', description='This command will list the different World Cup kits available to you')
async def kits(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(wc_kits))


@bot.command(brief='List avaiable sombreros', description='This command will list the different outfits available to you')
async def sombrero(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(sombreros))


@bot.command(brief='List avaiable wallpaper backgrounds', description='This command will list the different wallpaper backgrounds available to you')
async def wallpapers(ctx):
    await ctx.send('**List of wallpapers (please choose from one of the below)**\n\n' + "\n".join(phone_backgrounds))


@bot.command(brief='List avaiable holiday backgrounds', description='This command will list the different backgrounds')
async def holiday_bg(ctx):
    await ctx.send('**List of backgrounds (please choose from one of the below)**\n\n' + "\n".join(pfp_backgrounds))


@bot.command(brief='List avaiable banners', description='This command will list the different banners')
async def list_banners(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(banners))

# Lets user know when they enter an invalid command


@bot.command(name="nb", brief="this will return the chosen monke with no background")
async def nb(ctx, pfp_id: int):
    try:
        if 0 < pfp_id <= 5001:
            await ctx.send(file=discord.File(no_background_folder + str(pfp_id) + '.png'))

        else:
            await ctx.send('Please enter a number between 1 and 5000')

    except:
        await ctx.send("unknow error")


@bot.command(name="wc", brief='World Cup Kits', description='This command will let you apply select wc kits to your monke, type `?kits` to see available countries')
async def wc(ctx, fit: str, pfp_id: int):
    try:
        if fit.lower() in wc_kits:
            if 0 < pfp_id <= 5001:
                get_kit(fit, str(pfp_id))
                await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
                deleteDressed(fit, str(pfp_id))

            else:
                await ctx.send('Please enter a valid number between 1 and 5000.')
        else:
            await ctx.send('Please enter a valid kit. Check ?kits for options')
    except:
        await ctx.send('something went wrong')


@bot.command(name="wcnb", brief='World Cup Kits no background', description='This command will let you apply select wc kits to your monke, and return them without a background. type `?kits` to see available countries')
async def wc_nb(ctx, fit: str, pfp_id: int):
    # try:
    if fit.lower() in wc_kits:
        if 0 < pfp_id <= 5001:
            no_background_wc(fit, str(pfp_id))
            await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
            deleteDressed(fit, str(pfp_id))

        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')

    else:
        await ctx.send('Please enter a valid kit. Check ?kits for options')
    # except:
    #     await ctx.send('Please enter a valid number between 1 and 5000.')


@bot.command(name="newfitnb", brief='new fits no background', description='This command will let you apply fits, and return them without a background. type `?fits` to see available fits')
async def fit_nb(ctx, fit: str, pfp_id: int):
    # try:
    if fit.lower() in outfits:
        if 0 < pfp_id <= 5001:
            no_background_fit(fit, str(pfp_id))
            await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
            deleteDressed(fit.lower(), str(pfp_id))

        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')

    else:
        await ctx.send('Please enter a valid kit. Check ?kits for options')
    # except:
    #     await ctx.send('Please enter a valid number between 1 and 5000.')


@bot.command(name="wallpaper", brief='Phone Wallpaper', description='This command will let make a phone wallpapere, type `?wallpapers` to see available backgrounds')
async def wallpaper(ctx, wallpaper: str, pfp_id: int):
    # try:
    if wallpaper.lower() in phone_backgrounds:
        if 0 < pfp_id <= 5001:
            make_wallpaper(wallpaper.lower(), str(pfp_id))
            await ctx.send(file=discord.File(save_img_folder + wallpaper.lower() + str(pfp_id) + '.png'))
            deleteDressed(wallpaper.lower(), str(pfp_id))

        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')
    else:
        await ctx.send('Please enter a valid wallpaper. Check ?wallpapers for options')
    # except:
    # await ctx.send('Please enter a valid number between 1 and 5000.')


@bot.command(name="hq", brief='High Resolution Monke', description='This command will return an upscaled version of your monke 1920 x 1920')
async def hq(ctx, pfp_id: int):
    # try:

    if 0 < pfp_id <= 5001:
        high_quality(str(pfp_id))
        await ctx.send(file=discord.File(save_img_folder + 'hq' + str(pfp_id) + '.png'))
        delete_hq(pfp_id)
    else:
        await ctx.send('Please enter a valid number between 1 and 5000')
    # except:
    #     await ctx.send('something went wrong')


@bot.command(name="hqnb", brief='High Resolution Monke No Background', description='This command will return an upscaled version of your monke 1920 x 1920')
async def hqnb(ctx, pfp_id: int):
    # try:

    if 0 < pfp_id <= 5001:
        high_quality_no_background(str(pfp_id))
        await ctx.send(file=discord.File(save_img_folder + 'hq' + str(pfp_id) + '.png'))
        delete_hq(pfp_id)
    else:
        await ctx.send('Please enter a valid number between 1 and 5000')
    # except:
    # await ctx.send('Something went wrong')


@bot.command(name="smol", breif='A smol monke', description='will return a smol monke')
async def smol(ctx, pfp_id):
    if 0 < int(pfp_id) <= 5001:
        make_smol(pfp_id)
        await ctx.send(file=discord.File(save_img_folder + 'smol' + str(pfp_id) + '.png'))
        # delete_smol(pfp_id)
    else:
        await ctx.send('Please enter a valid number between 1 and 5000')


@bot.command(name="smoller", breif='A smol monke', description='will return a smol monke')
async def smoller(ctx, pfp_id):
    if 0 < int(pfp_id) <= 5001:
        make_smoller(pfp_id)
        await ctx.send(file=discord.File(save_img_folder + 'smol' + str(pfp_id) + '.png'))
        # delete_smol(pfp_id)
    else:
        await ctx.send('Please enter a valid number between 1 and 5000')


@bot.command(name='holiday', breif='Holiday monkes', description='backgrounds for monkes \n takes 1 command `holiday blue 4470` ')
async def holiday(ctx, background: str, pfp_id: int):
    if background.lower() in pfp_backgrounds:

        if 0 < pfp_id <= 5001:
            pfp_background(background, pfp_id)
            await ctx.send(file=discord.File(save_img_folder + background.lower() + str(pfp_id) + '.png'))
            deleteDressed(background, str(pfp_id))

        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')

    else:
        await ctx.send('Please enter a valid background. Check `?holiday_bg` for options')
    # except:
        # await ctx.send('Please enter a valid number between 1 and 5000.')


@bot.command(name="banner", brief='Twitter banner for your Monke', description='will create a custom banner for twitter')
async def banner(ctx, fit: str, pfp_id: int, pfp2=None, pfp3=None, pfp4=None, pfp5=None):
    if fit.lower() in banners:
        if 0 < pfp_id <= 5001:

            if pfp5:
                make_banner(fit, str(pfp_id), str(pfp2),
                            str(pfp3), str(pfp4), str(pfp5))
            elif pfp4:
                make_banner(fit, str(pfp_id), str(pfp2), str(pfp3), str(pfp4))
            elif pfp3:
                make_banner(fit, str(pfp_id), str(pfp2), str(pfp3))
            elif pfp2:
                make_banner(fit, str(pfp_id), str(pfp2))
            else:
                make_banner(fit, str(pfp_id))

            await ctx.send(file=discord.File(save_img_folder + fit.lower() + str(pfp_id) + '.png'))
            deleteDressed(str(pfp_id))

        else:
            await ctx.send('Please enter a valid number between 1 and 5000.')
    else:
        await ctx.send('Please enter a valid fit. Check ?list_banners for options')
    # except:
    #     await ctx.send('something went wrong')


@bot.event
async def on_command_error(ctx, error):
    # or discord.ext.commands.errors.CommandNotFound as you wrote
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command, please check `?help` for a list of available commands")

load_dotenv()

bot.run(os.getenv('TOKEN'))
