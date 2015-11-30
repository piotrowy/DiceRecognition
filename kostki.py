#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from random import randint
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import filter
from skimage import measure
from skimage import data, color
from skimage.filter import canny
from skimage.transform import hough_circle
from skimage.draw import circle_perimeter
from skimage.feature import peak_local_max
from skimage.morphology import disk, erosion, square, dilation


def tresh(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j] < 0.3:
                image[i][j] = 0
            else:
                image[i][j] = 1
    return image


def convert_image(image):
    # image = dilation(image, square(15))
    # image = filter.gaussian_filter(image, 0.99)
    # image = filter.rank.median(image, disk(3))
    # image = erosion(image, selem=square(20))
    # image = filter.canny(image)
    image = tresh(image)
    image = filter.rank.median(image, disk(18))
    return image


def load_image(i):
    try:
        if i < 10:
            image = io.imread('kostki_ex/' + 'kostka_0' + str(i) + '.JPG', as_grey=True)
        else:
            image = io.imread('kostki_ex/' + 'kostka_' + str(i) + '.JPG', as_grey=True)
        return image
    except FileNotFoundError:
        blank_image = np.zeros((50, 50), np.uint8)
        return blank_image


def load_all_from_range(start, end):
    images = []
    for i in range(start, end):
        image = load_image(i)
        images.append(image)
    return images


def circle_center(contour):
    x = 0
    y = 0
    for i in range(len(contour)):
        x += contour[i][0]
        y += contour[i][1]
    return [x/len(contour), y/len(contour)]


def radius(point, center):
    return math.sqrt(math.pow(center[0] - point[0], 2) + math.pow(center[1] - point[1], 2))


def avg_radius(contour, center):
    r = 0
    for i in range(len(contour)):
        r += radius(contour[i], center)
    return r/len(contour)


def check_circle(contour, center, avgr):
    hits = 0
    for i in range(len(contour)):
        r = radius(contour[i], center)
        if avgr + 0.1*avgr >= r >= avgr - 0.1*avgr:
            hits += 1
    return hits/len(contour)


def draw_contours(image):
    contours = measure.find_contours(image, level=0)
    print(len(contours))

    fig, ax = plt.subplots()
    ax.imshow(image, interpolation='nearest', cmap=plt.cm.gray)

    sum = 0.0
    for n, contour in enumerate(contours):
        sum += contour.shape[0]
    avg = sum/len(contours)

    for n, contour in enumerate(contours):
        cc = circle_center(contour)
        avgr = avg_radius(contour, cc)
        accuracy = check_circle(contour, cc, avgr)
        print(cc, avgr, accuracy)
        if float(contour.shape[0]) < avg and accuracy > 0.95:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


def main():
    image = load_image(6)
    image = convert_image(image)
    draw_contours(image)


    # io.imshow(image);
    # io.show()

if __name__ == '__main__':
    main()
