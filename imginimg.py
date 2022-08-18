from PIL import Image, ImageOps
from time import perf_counter
import sys

def get_digits(val):
    d1, d2, d3 = map(int, list(f"{val:03}"))  # eg: 23 => 0,2,3
    if not d1 and not d2 and not d3:  # converting 0,0,0 to 0,0,1
        d3 = 1
    return [d1, d2, d3]  # splitting and returning each digit in val

def get_encoded_rgb(val, digits):
    # Changing last digit of rgb value | eg: (123, 231, 211) , [2,4,1] ==> (122, 234, 211)
    final = []
    RGB = [i % 10 for i in val]
    for i in zip(RGB, digits, val):
        if i[0] != i[1]:
            if abs(i[1] - i[0]) <= 5 and (t := i[2] + (i[1] - i[0])) <= 255:
                temp = t

            elif (i[1] - i[0]) > 0 and (t := i[2] - (10 - (i[1] - i[0]))) > 0:
                temp = t

            elif(i[1] - i[0]) < 0:
                temp = i[2] + (10 - abs(i[1] - i[0]))

            else:
                temp = i[2] + (i[1] - i[0])
        else:
            temp = i[2]

        final.append(temp)

    return tuple(final)


def encode(imgcover, imghide):
    filename = f"{imgcover.filename.split('/')[-1].split('.')[0]}_{imghide.filename.split('/')[-1].split('.')[0]}"

    imgcover = imgcover.convert('RGB')
    imghide = ImageOps.grayscale(imghide)
    imghide.thumbnail(imgcover.size, Image.ANTIALIAS)

    pix_main = imgcover.load()
    pix_hide = imghide.load()

    for i in range(imghide.size[0]):
        for j in range(imghide.size[1]):
            # Detecting corner pixels
            if i == imghide.size[0]-1 and j == imghide.size[1]-1 or i == 0 and j == imghide.size[1]-1:
                pix_main[i, j] = get_encoded_rgb(pix_main[i, j], [0, 0, 0])  # Changing corner pixel LSB to 0
                break

            pix_main[i, j] = get_encoded_rgb(pix_main[i, j], get_digits(pix_hide[i, j]))
             # print(f"rgb={pix_main[i, j]} i={i} j={j}")

    imgcover.save(f"{filename}.png")

def decode(img,savetype='png'):
    bg = ImageOps.grayscale(img)
    pix_clr = img.load()
    pix_bg = bg.load()

    w, h = img.size
    br = 0

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if not j < h:
                break
            val = int(f"{pix_clr[i,j][0]%10}{pix_clr[i,j][1]%10}{pix_clr[i,j][2]%10}")  # brightness value from rgb
            pix_bg[i, j] = val
            # print(f"i={i} j={j} val={val}")
            if not val:  # finding resolution with black pixels
                if br == 0:  # first corner
                    h = j + 1
                elif br == 1:  # second corner
                    w = i + 1
                br += 1
                pix_bg[i, j] = pix_bg[i, j-1]  # covering the black pixel
        if br == 2:
            break

    crop = bg.crop((0, 0, w, h))
    crop.save(f"{img.filename.split('/')[-1].split('.')[0]}_decoded.{savetype}")


def main():
    filetype = 'png'
    skip = False
    if len(sys.argv) > 1:
        skip = True
        if sys.argv[1] == '/e':
            ch = 1
            try:
                cover_img = sys.argv[2]
                hid_img = sys.argv[3]
            except Exception as e:
                print("image path not specified\n")
                print(f"Usage:\npython {sys.argv[0]} /e cover_image hide_image")
                exit(0)
        elif sys.argv[1] == '/d':
            ch = 2
            try:
                dec_img = sys.argv[2]
                if len(sys.argv) == 4:
                    filetype = sys.argv[3]
            except Exception as e:
                print("image path not specified\n")
                print(f"Usage:\npython {sys.argv[0]} /d decode_image savefile_type(default : png)")
                exit(0)
        else:
            print('Wrong command\n')
            print(f"Usage:\npython {sys.argv[0]} /e cover_image hide_image")
            print(f"python {sys.argv[0]} /d decode_image savefile_type(default : png)")
            exit(0)
    else:
        ch = int(input("1. Encode\n2. Decode\n0. Exit\n"))

    if ch == 0:
        exit(0)

    if ch == 1:
        if not skip:
            cover_img = input("Path of the cover image : ")
            hid_img = input("\nPath of image to hide : ")

        image_cover = Image.open(cover_img)
        image_hide = Image.open(hid_img)
        print('encoding...')
        s = perf_counter()
        encode(image_cover, image_hide)
        f = perf_counter()

    if ch == 2:
        if not skip:
            dec_img = input("Path of the image to decode : ")
        image_decode = Image.open(dec_img)
        print('decoding...')
        s = perf_counter()
        decode(image_decode, filetype)
        f = perf_counter()

    print(f"finished in {round(f-s)} seconds")

# 26/3/2022
# Aswin Koroth
main()


