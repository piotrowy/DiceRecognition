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
            elif image[i][j] > 0.8:
                image[i][j] = 1
            else:
                image[i][j] = 0.5
    return image


def convert_image(image):
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


def point_distance(point1, point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))

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

    fig, ax = plt.subplots()
    ax.imshow(image, interpolation='nearest', cmap=plt.cm.gray)

    sum = 0.0
    for n, contour in enumerate(contours):
        sum += contour.shape[0]
    avg = sum/len(contours)

    count = 0
    circles = []

    for n, contour in enumerate(contours):
        cc = circle_center(contour)
        avgr = avg_radius(contour, cc)
        accuracy = check_circle(contour, cc, avgr)
        if float(contour.shape[0]) < avg and accuracy > 0.95:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
            count = count + 1
            circles.append(cc)
    # float(contour.shape[0]) - 0.1*float(contour.shape[0]) <= avg <= float(contour.shape[0]) + 0.1*float(contour.shape[0])

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    # plt.show()

    return circles


def unified_length_to_rest(sixCircles):
    result = []
    for center in sixCircles[1:]:
        result.append(point_distance(sixCircles[0], center))
    return sorted([x/min(result) for x in result])


def arrays_probably_match(length, perfect_values, param):
    for i, distance in enumerate(length):
        if abs(distance - perfect_values[i]) > param:
            return 0
    return 1


def are_proper_dice_six(six_circles):
    length = unified_length_to_rest(six_circles)
    perfect_for_corner = [1.0, 1.6, 1.88, 2.0, 2.56]
    perfect_for_side = [1.0, 1.0, 1.6, 1.88, 1.88]
    if arrays_probably_match(length, perfect_for_corner, 0.05):
        return 1
    if arrays_probably_match(length, perfect_for_side, 0.05):
        return 1
    return 0


def get_from_binary_coded(circles, binary):
    result = []
    for index, char in enumerate(reversed(binary)):
        if char == '1':
            result.append(circles[len(circles)-(index + 1)])
    return result


def find_six(circles):

    if len(circles) < 6:
        return 0

    for i in range(0, (2**len(circles))):
        if bin(i).count('1') == 6:
            if are_proper_dice_six(get_from_binary_coded(circles, bin(i))):
                return 1

    return 0

def main():
    image = load_image(1)
    image = convert_image(image)
    circles = draw_contours(image)
    if find_six(circles):
        print(6)
        exit(0)

    # io.imshow(image);
    # io.show()

if __name__ == '__main__':
    main()
