#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from skimage.transform._hough_transform import probabilistic_hough_line


def tresh(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j] < 0.3:
                image[i][j] = 0
            else:
                image[i][j] = 1
    return image


def convert_image(image):
    #image = dilation(image, square(15))
    #image = filter.gaussian_filter(image, 0.99)
    #image = filter.rank.median(image, disk(3))
    #image = erosion(image, selem=square(20))
    image = tresh(image)
    image = filter.rank.median(image, disk(18))
    # image = filter.canny(image)
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


def find_circles(image):
    edges = filter.canny(image, sigma=3, low_threshold=10, high_threshold=50)

    fig, ax = plt.subplots(ncols=1, nrows=1)

    # Detect two radii
    hough_radii = np.arange(15, 30, 2)
    hough_res = hough_circle(edges, hough_radii)

    centers = []
    accums = []
    radii = []

    for radius, h in zip(hough_radii, hough_res):
        # For each radius, extract two circles
        num_peaks = 2
        peaks = peak_local_max(h, num_peaks=num_peaks)
        centers.extend(peaks)
        accums.extend(h[peaks[:, 0], peaks[:, 1]])
        radii.extend([radius] * num_peaks)

    # Draw the most prominent 5 circles
    image = color.gray2rgb(image)
    for idx in np.argsort(accums)[::-1][:5]:
        center_x, center_y = centers[idx]
        radius = radii[idx]
        cx, cy = circle_perimeter(center_y, center_x, radius)
        image[cy, cx] = (220, 20, 20)

    ax.imshow(image, cmap=plt.cm.gray)
    plt.show()


def draw_contours(image):
    contours = measure.find_contours(image, level=0)
    print(len(contours))

    fig, ax = plt.subplots()
    ax.imshow(image, interpolation='nearest', cmap=plt.cm.gray)

    sum = 0

    for n, contour in enumerate(contours):
        sum += contour.shape[0]

    avg = sum/len(contours)

    for n, contour in enumerate(contours):
        if float(contour.shape[0]) < avg:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


def probabilistic_hough(image):
    edges = canny(image, 2, 1, 25)
    lines = probabilistic_hough_line(edges, threshold=10, line_length=5,
                                     line_gap=3)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8,4), sharex=True, sharey=True)

    ax1.imshow(image, cmap=plt.cm.gray)
    ax1.set_title('Input image')
    ax1.set_axis_off()
    ax1.set_adjustable('box-forced')

    ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.set_title('Canny edges')
    ax2.set_axis_off()
    ax2.set_adjustable('box-forced')

    ax3.imshow(edges * 0)

    for line in lines:
        p0, p1 = line
        ax3.plot((p0[0], p1[0]), (p0[1], p1[1]))

    ax3.set_title('Probabilistic Hough')
    ax3.set_axis_off()
    ax3.set_adjustable('box-forced')
    plt.show()


def main():
    image = load_image(6)
    image = convert_image(image)
    # probabilistic_hough(image)
    draw_contours(image)


    # io.imshow(image);
    # io.show()

if __name__ == '__main__':
    main()
