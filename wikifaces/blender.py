import cv2
import numpy as np
from wikifaces import patern_filler
from wikifaces import photo_scraper
from wikifaces import wiki_scraper
import os
from datetime import datetime
import secrets

def mask_maker(person, uploaded_img):
    #== Parameters mask_maker===========================================================
    BLUR = 21
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 90   #200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (0.0,0.0,0.0) # In BGR format

    #== Processing =======================================================================
    #-- Read image -----------------------------------------------------------------------
    search_filters = '+face+high+res+portrait' #+grayscale #

    if len(uploaded_img) > 50:
        path = uploaded_img
    else:
        path = photo_scraper.scraper(person, search_filters, uploaded_img)

    print("MASK MAKER", path)

    img = cv2.imread(path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #-- Edge detection -------------------------------------------------------------------
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    #-- Find contours in edges, sort by area ---------------------------------------------
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    #-- Create empty mask, draw filled polygon on it corresponding to largest contour ----
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #-- Smooth mask, then blur it --------------------------------------------------------
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices,
    img         = img.astype('float32') / 255.0                 #  for easy blending
    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit
    #cv2.imshow('img', masked)                                   # Display
    #cv2.waitKey()
    #cv2.imwrite('C:/Temp/person-masked.jpg', masked)           # Save
    cv2.imwrite(uploaded_img[:46] + '/ripped_face.jpg', masked)
    # print(uploaded_img[:46])
    os.remove(path)

#=====================================================================================
#=====================================================================================

def name_stripper(url):
    "Gets persons name from the wiki URL"
    name = url[url.find('wiki/')+5:]
    name = name.replace('_', ' ') if name.find('_') != -1 else name
    print(f"Making Wikiface of: {name}")
    return name


def image_resizing(uploaded_img):
    "resizes images appropriately, respects ratio"
    img1 = Image.open(uploaded_img + '/ripped_face.jpg')
    width, height = img1.size
    ratio =  width/height

    if ratio >= 0.8 and ratio <= 1.2:
        img1 = img1.resize(( 1100, 1100), Image.ANTIALIAS) #1100
    elif ratio <= 1:
        img1 = img1.resize(( round(1500*ratio), 1500), Image.ANTIALIAS) #1400
    elif ratio > 1:
        img1 = img1.resize((1500, round(1500/ratio)), Image.ANTIALIAS)  #1400

    h , w = img1.size
    return img1, h, w, ratio


#== Processing blending_face_text ====================================================
# Importing Image and ImageChops module from PIL package
from PIL import Image, ImageChops, ImageOps, ImageEnhance
import validators
def blending_face_text(name, uploaded_img):
    now1 = datetime.now()
    url_status = 'no'
    # print("BLENDER",name, uploaded_img)

    print("person, uploaded_img",name, uploaded_img)
    if len(uploaded_img) > 46 and uploaded_img[-8:]!= 'file.jpg':
        uploaded_img = uploaded_img[:-20]

    if os.path.exists(uploaded_img + '/ripped_face.jpg') == True:
        if validators.url(name) == True:
            url_status = 'yes'
        pass
    elif validators.url(name) == True:
        mask_maker(name_stripper(name), uploaded_img)
        url_status = 'yes'
    else:
        mask_maker(name, uploaded_img)

    uploaded_img = uploaded_img[:46]
    img1, h, w, ratio = image_resizing(uploaded_img)
    print("BLENDER, name, url_status", name, url_status)
    word_dict = wiki_scraper.main(name, url_status)
    img2 = patern_filler.words_to_canvas((h, w), word_dict)
    del word_dict

    #==== Color settings =================================================#
    "IMAGE=============================================="
    enhancer = ImageEnhance.Brightness(img1)
    factor = 1    #0.2
    img1 = enhancer.enhance(factor)

    enhancer = ImageEnhance.Contrast(img1)
    factor = 1   #8.0
    img1 = enhancer.enhance(factor)


    enhancer = ImageEnhance.Color(img1)
    factor = .1    #5.0
    img1 = enhancer.enhance(factor)

    #img1.show()

    enhancer = ImageEnhance.Sharpness(img1)
    factor = 1    # 0.0
    img1 = enhancer.enhance(factor)


    "TEXT==========================================="
    enhancer = ImageEnhance.Brightness(img2)
    factor = 0.2
    img2 = enhancer.enhance(factor)

    enhancer = ImageEnhance.Contrast(img2)
    factor = 4.0
    img2 = enhancer.enhance(factor)


    enhancer = ImageEnhance.Color(img2)
    factor = 0.0    # 5 cool
    img2 = enhancer.enhance(factor)

    #img2.show()

    enhancer = ImageEnhance.Sharpness(img2)
    factor = 0.0
    img2 = enhancer.enhance(factor)


    "FINAL IMAGE=================================================="
    img3 = ImageChops.multiply(img1, img2)
    #img1.show()

    enhancer = ImageEnhance.Contrast(img3)
    factor = 2.0
    img3 = enhancer.enhance(factor)


    enhancer = ImageEnhance.Color(img3)
    factor = 1.0     # 5 cool
    img3 = enhancer.enhance(factor)

    enhancer = ImageEnhance.Brightness(img3)
    factor = 1.0
    img3 = enhancer.enhance(factor)


    enhancer = ImageEnhance.Sharpness(img3)
    factor = 1.0
    img3 = enhancer.enhance(factor)


    ###############################################################################
    img3 = img3.resize((2000, round(2000/ratio)), Image.ANTIALIAS)

    if uploaded_img[-1] == "\\" or uploaded_img[-1] == "/":
        uploaded_img = uploaded_img[:-1]

    saving_path = uploaded_img + uploaded_img[-17:] + '.jpg'
    print("saving_path",saving_path)
    img3.save(saving_path)
    now2 = datetime.now()
    print(f"Time passed: {now2 - now1}" )
    if validators.url(name) == True:
        name = name_stripper(name)

    return img3,saving_path, name
