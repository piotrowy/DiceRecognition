#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from skimage import io
from skimage import filter
from skimage.morphology import disk, erosion, square, dilation
from skimage import measure

def tresh(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j] < 50:
                image[i][j] = 0
            else:
                image[i][j] = 1
    return image


def convert_image(image):
    image = dilation(image, square(15))
    image = filter.gaussian_filter(image, 0.99)
    image = erosion(image, selem=square(20))
    image = tresh(image)
    return image


def main():
    images = []
    for i in range(0, 11):
        if i < 10:
            image = io.imread('kostki_ex/' + 'kostka_0' + str(i) + '.JPG', as_grey=True)
            images.append(image)
        else:
            image = io.imread('kostki_ex/' + 'kostka_' + str(i) + '.JPG', as_grey=True)
            images.append(image)

    image = convert_image(images[0])
    contours = measure.find_contours(image, level = 0)
    print(len(contours))

    io.imshow(image);
    io.show()

if __name__ == '__main__':
    main()
