#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from matplotlib import pyplot as plt
from skimage import io
from skimage import filter
from skimage.filter import threshold_otsu
from skimage.draw import polygon
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


def main():
    image = io.imread('kostka.jpg', as_grey=True);
    image = dilation(image, square(15))
    image = filter.gaussian_filter(image, 0.99)
    image = erosion(image, selem=square(20))
    print(image)
    image = tresh(image);
    contours = measure.find_contours(image, level = 0)
    print(len(contours))
    #print(contours)
    io.imshow(image);

    io.show()



if __name__ == '__main__':
    main()
