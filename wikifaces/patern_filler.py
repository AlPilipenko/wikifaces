from shapely.geometry import Polygon
import json
import random
from PIL import Image, ImageDraw, ImageFont

#== Functions =======================================================================
def font_calculator(rat):
    """ Determines behaiviour of fonts """
    if  rat > 0.993:
        return 86
    elif  rat > 0.983:
        return 70
    elif  rat > 0.92:
        return 40
    elif  rat > 0.88:
        return 30
    elif  rat > 0.81:
        return 25
    elif  rat > 0.75:
        return 23
    elif  rat > 0.65:
        return 21
    elif  rat > 0.45:
        return 18
    elif  rat > 0.20:
        return 16
    else:
         return 14


def text_to_canvas(x,y,img,d,fnt,img_size, max_font):
    """Prints words to canvas with adjustment to font size and word len"""
    word_length = len(y[0])
    if  x[1][0] - x[0][0] < x[2][1] - x[1][1]:
        img = img.rotate(-90, resample=0, expand=1, center=None, translate=None)
        d = ImageDraw.Draw(img)
        x1 = img_size[1] - x[2][1] #- w
        y1 = x[0][0]

        if word_length == 3 and max_font > 35:
            d.text((x1+10, y1-10), y[0], font=fnt )
        elif word_length == 4 and max_font > 35:
            d.text((x1+5, y1), y[0], font=fnt )
        elif word_length <= 6 and max_font > 50:
            d.text((x1+15, y1), y[0], font=fnt )
        elif word_length > 6 and max_font > 50:
            d.text((x1, y1+5), y[0], font=fnt )
        else:
            d.text((x1, y1), y[0], font=fnt )
        img = img.rotate(90, resample=0, expand=1, center=None, translate=None)
        d = ImageDraw.Draw(img)

    else:
        if word_length <= 3 and max_font > 70:
            d.text((x[0][0]+30,x[0][1] -20), y[0], font=fnt )
        elif word_length <= 3 and max_font > 50:
            d.text((x[0][0]+20,x[0][1] -10), y[0], font=fnt )
        elif word_length <= 3 and max_font > 35:
            d.text((x[0][0]+10,x[0][1] -10), y[0], font=fnt )
        elif word_length <= 4 and max_font > 69:
            d.text((x[0][0]+30,x[0][1] -15), y[0], font=fnt )
        elif word_length <= 5 and max_font > 69:
            d.text((x[0][0]+20,x[0][1] -15), y[0], font=fnt )
        elif word_length <= 5 and max_font > 50:
            d.text((x[0][0]+25,x[0][1] -15), y[0], font=fnt )
        elif word_length >= 6 and word_length <= 9 and max_font > 50:
             d.text((x[0][0]+10,x[0][1]-10), y[0], font=fnt )
        else:
            d.text(x[0], y[0], font=fnt )

    return d,img


def fitting_words(x,y, max_font,font_style):
    "Adjust font size wnen word differs a lot from the spot its placed"
    if y[0] == "York":
        y = list(y)
        y[0] = "New York"
    if y[0] == "Los":
        y = list(y)
        y[0] = "Los Angeles"
    if y[0] == "Las":
        y = list(y)
        y[0] = "Las Vegas"

    temp_font = max_font
    fnt = ImageFont.truetype(font_style, max_font)
    h,w = fnt.getsize(y[0])

    if Polygon(x).area / (h*w) < 0.75:
        while Polygon(x).area /(h*w) < 0.70:
            temp_font -=2
            fnt = ImageFont.truetype(font_style, temp_font)
            h,w = fnt.getsize(y[0])
        temp_font = max_font

    elif Polygon(x).area / (h*w) >= 1.05:
        while Polygon(x).area / (h*w) >= 1.05:
            temp_font +=3

            fnt = ImageFont.truetype(font_style, temp_font)
            h,w = fnt.getsize(y[0])
        temp_font = max_font

    return fnt,y

#== Processing =======================================================================
def words_to_canvas(img_size, word_dict):
    "alocates wikipedia words to black image"
    font_style = 'impact.ttf'
    img = Image.new('RGB', img_size, color = (0, 0, 0))
    d = ImageDraw.Draw(img)

    "To control dencity of the words on the canvas"
    max_words = round((img_size[0] * img_size[1]) / 1500) + 1500
    inverted_list = list(word_dict.items())[::-1][:max_words]

    """In case of having not enough words on wikipage"""
    if len(inverted_list) < max_words:
        inverted_list = inverted_list * round(max_words/len(inverted_list))
        print("not enough words, making new!")

    curent_word = max_words

    with open('wikifaces/word_templates.json', 'r') as f:
        alist = json.load(f)
        template = random.randint(0,100)
        template_list = alist.get(str(template))


    for x, y  in zip(template_list,inverted_list):
        if x[0][0] > img_size[0] or x[0][1] > img_size[1]:
            continue

        ratio = curent_word/max_words
        curent_word -= 1
        max_font = font_calculator(ratio)
        fnt,y = fitting_words(x,y, max_font,font_style)
        d,img = text_to_canvas(x,y,img,d,fnt,img_size,max_font)

    return img
