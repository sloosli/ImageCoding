#!/usr/bin/python3
import os.path
from PIL import Image, ImageDraw


def compare_images(im1, im2):
    if im1.size != im2.size:
        "Image sizes must be equal"
    counter = 0
    pix1 = im1.load()
    pix2 = im2.load()
    for i in range(im1.size[0]):
        for j in range(im1.size[1]):
            if pix1[i, j] != pix2[i,j]:
                counter += 1

    return counter


def char_to_binary(char):
    return "{0:08b}".format(ord(char))


def open_image(image_name):
    try:
        image = Image.open(image_name)
        return image
    except FileNotFoundError:
        print("Image %s not found" % image_name)
        return None


def open_image_dialog():
    image = None
    while image is None:
        print("Input path to image")
        image_name = input(">>> ")
        image_name = image_name.replace('"', '').replace("'", "")
        image_name = image_name.strip()
        image = open_image(image_name)
        if image is None:
            print("Cannot open this image try another one")
    return image


def compare_bits(pixel):
    return pixel[0] % 2 == pixel[1] % 2 == pixel[2] % 2


def binary_to_image(image, binary):
    width, height = image.size
    if len(binary) > width * height:
        print("Text is too long")
    draw = ImageDraw.Draw(image)
    pixels = image.load()

    def draw_bit(bit, x, y):
        bit = int(bit)
        new_color = lambda color : color + (color % 2 - bit)
        red, green, blue = pixels[x, y]
        draw.point((x, y), (
            new_color(red),
            new_color(green),
            new_color(blue))
        )
        p = image.load()

    for i, bit in enumerate(binary):
        draw_bit(bit, i % width, i // width)
    del draw


def image_to_binary(image):
    width, height = image.size
    pixels = image.load()
    x, y, i = 0, 0, 0
    bitstring = ""

    while compare_bits(pixels[x, y]):
        bitstring += str(pixels[x, y][0] % 2)
        i += 1
        x = i % width
        y = i // width

    return bitstring


def text_to_binary(text):
    binary_text = ""
    for ch in text:
        binary_ch = char_to_binary(ch)
        if len(binary_ch) > 8:
            print("Non ASCII symbol:", ch)
            return None
        binary_text += binary_ch
    return binary_text


def binary_to_text(binary_text):
    text = ""
    for i in range(0, len(binary_text), 8):
        binary_ch = binary_text[i:i + 8]
        int_ch = int(binary_ch, 2)
        text += chr(int_ch)
    return text


def decode_image_dialog():
    image = open_image_dialog()
    binary = image_to_binary(image)
    text = binary_to_text(binary)
    image.close()
    print(text)


def encode_text_dialog():
    image = open_image_dialog()
    print("Input text")
    text = input(">>> ")
    binary = text_to_binary(text)
    if binary is None:
        return

    binary_to_image(image, binary)
    filename = "new_" + os.path.basename(image.filename)
    image.save(filename, "PNG")
    image.close()
    print("%i symbols recorded" % len(text))
    print("File saved: ", filename)
    print("Done")


def compare_images_dialog():
    im1 = open_image_dialog()
    im2 = open_image_dialog()

    counter = compare_images(im1, im2)
    print("Количество различных пикселей: ", counter)


def main():
    answer = '1'
    while True:
        print("1) Decode image",
              "2) Encode text",
              "3) Compare two images",
              "0) Exit",
              sep="\n")
        answer = input(">>> ")

        if answer == '0':
            break
        elif answer == '1':
            decode_image_dialog()
        elif answer == '2':
            encode_text_dialog()
        elif answer == '3':
            compare_images_dialog()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
