import os
from dotenv import load_dotenv
import io
import json
import requests
import PIL
from PIL import Image, ImageSequence


data = open('attributes.json')

pfp_atts = json.load(data)

gif_folder = 'gifs/'
pfp_folder = 'clean_pfps/'
save_img_folder = 'dressed_pfps/'
no_background_folder = 'no_background/'
welcome_folder = 'Welcome_gif/'
gifs = ["gm", "gn", "welcome"]


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
        print(frame)
    frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                   '.gif', save_all=True, append_images=frames[1:],  loop=0)

    return


def make_gif_nb(gif, pfp_id):
    gif_string = gif.lower()

    animated_gif = Image.open(gif_folder + gif_string + '.gif')
    frames = []

    for f in ImageSequence.Iterator(animated_gif):

        frame = f.convert("RGBA")
        # monke = m.copy()
        m = Image.open(no_background_folder + str(pfp_id) + '.png')

        m.paste(frame, mask=frame)
        # print(monke)
        frames.append(m)
    frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                   '.gif', save_all=True, append_images=frames[1:],  loop=0)

    return


def welcome_gif(im1, im2, im3, im4, im5, im6, im7):
    one = Image.open(welcome_folder + im1 + '.png')
    two = Image.open(welcome_folder + im2 + '.png')
    three = Image.open(welcome_folder + im3 + '.png')
    four = Image.open(welcome_folder + im4 + '.png')
    five = Image.open(welcome_folder + im5 + '.png')
    six = Image.open(welcome_folder + im6 + '.png')
    seven = Image.open(welcome_folder + im7 + '.png')

    frames = [one,  two,  three,  four,
              five,  six,  seven, seven, seven]

    frames[0].save(gif_folder + 'welcome' +
                   '.gif', save_all=True, append_images=frames[1:],  loop=0, optimize=False, duration=500)


# welcome_gif('1', '2', '3', '4', '5', '6', '7')
