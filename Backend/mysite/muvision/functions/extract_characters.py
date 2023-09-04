import cv2
import numpy as np
from . import border_crop as bc


# Extracting Contours
def add_background(img, b_color, cntrs):
    mask_image = img.copy()
    mask_value = 255
    b_mask = np.zeros(img.shape[:-1]).astype(np.uint8)
    cv2.drawContours(b_mask, [cntrs], -1, (255, 255, 255), thickness=-1)

    selection = b_mask != mask_value
    mask_image[selection] = b_color

    cv2.drawContours(mask_image, cntrs, -1, (int(b_color[0]), int(b_color[1]), int(b_color[2])), 1)

    return mask_image


def extract_contours(img, cntrs, common_color):
    channels = None
    if len(img) < 2:
        channels = img.shape[2]
    else:
        channels = 1
    arr = []
    bounding_box = []

    for cntr in cntrs:
        mask = np.full((img.shape[0], img.shape[1], 3), (0, 0, 0), dtype=np.uint8)
        ignore_mask = (255,) * channels
        cv2.drawContours(mask, [cntr], -1, (255, 255, 255), thickness=-1)

        mask_image = cv2.bitwise_and(img, mask)
        x, y, w, h = cv2.boundingRect(cntr)
        box = (x, y, w, h)

        bounding_box.append(box)

        filled_image = add_background(mask_image, common_color, cntr)

        # Crop the image
        cropped_line = filled_image[y:y + h, x:x + w]
        # cv2.imshow(cropped_line)

        arr.append(cropped_line)
    return arr, bounding_box


def identify_letter_helper(single_bounding_box, x1, y1, resize, iter):
    return_box = []
    for i in range(len(single_bounding_box)):
        bound_box = (x1 + single_bounding_box[i][0] / pow(resize, iter),
                     y1 + single_bounding_box[i][1] / pow(resize, iter),
                     x1 + single_bounding_box[i][0] / pow(resize, iter) + single_bounding_box[i][2] / pow(resize, iter),
                     y1 + single_bounding_box[i][1] / pow(resize, iter) + single_bounding_box[i][3] / pow(resize, iter))
        return_box.append(bound_box)
    return return_box


def clean_cntrs(cntrs, dimensions):
    return_tuple = []
    for i in range(len(cntrs)):
        x, y, w, h = cv2.boundingRect(cntrs[i])
        if h > dimensions[0] * 0.01 and w > dimensions[1] * 0.01:
            return_tuple.append(cntrs[i])
    return return_tuple


def identify_letter(image, line_images, single_bounding_box, x1, y1, iter, dmx, dmy, b_color):
    resize_factor = 3
    if not hasattr(image, 'shape'):
        return
    # To enhance the image
    image = cv2.resize(image, (image.shape[1] * resize_factor, image.shape[0] * resize_factor),
                       interpolation=cv2.INTER_AREA)

    # Creating the sharpening kernel
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])

    # Applying the sharpening kernel
    sharpened = cv2.filter2D(image, -1, kernel)

    (dilation, inverted_dilation) = bc.prepare_image(sharpened, (dmx, dmy))
    cntrs_line, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_NONE)
    # cntrs_line = sorted(cntrs_line, key=lambda ctr: cv2.boundingRect(ctr)[0])

    sharpened_copy = image.copy()
    # cntrs_line = clean_cntrs(cntrs_line, (image.shape[1] * resize, image.shape[0] * resize))

    if len(cntrs_line) == 1:
        # Base case
        return_image = []
        return_box = []
        x, y, w, h = cv2.boundingRect(cntrs_line[0])
        box = (
          x1 + x / pow(resize_factor, iter), y1 + y / pow(resize_factor, iter), x1 + x / pow(resize_factor, iter) + w /
          pow(resize_factor, iter), y1 + y / pow(resize_factor, iter) + h / pow(resize_factor, iter))
        return_image.append(sharpened_copy)
        return_box.append(box)

        return return_image, return_box
    else:
        # Extract contours gets the width
        (arr, single_bound_box) = extract_contours(sharpened_copy, cntrs_line, b_color)
        # Need to base the contour coordinates based on x1, x2, y1, y2 values.
        single_bound_box = identify_letter_helper(single_bound_box, x1, y1, resize_factor, iter)
        for i in range(len(arr)):
            (tmp_line_images, tmp_box) = identify_letter(arr[i], line_images, single_bounding_box,
                                                         single_bound_box[i][0],
                                                         single_bound_box[i][1], iter + 1, 1, 20, b_color)
            if len(tmp_line_images) > 1:
                line_images = tmp_line_images
                single_bounding_box = tmp_box

            else:
                line_images = line_images + tmp_line_images
                single_bounding_box = single_bounding_box + tmp_box

    return line_images, single_bounding_box


def resize(img, width, height, background_colour):
    new_img = None
    # max_size denotes the shape of the square image, which would be max_size x max_size
    max_size = max(img.shape[0], img.shape[1])
    if max_size == img.shape[0]:
        to_add = int((max_size - img.shape[1]) / 2)
        # top bottom
        new_img = cv2.copyMakeBorder(img, 0, 0, to_add, to_add, borderType=cv2.BORDER_CONSTANT,
                                     value=(
                                     int(background_colour[0]), int(background_colour[1]), int(background_colour[2])))
    else:
        to_add = int((max_size - img.shape[0]) / 2)
        # right left
        new_img = cv2.copyMakeBorder(img, to_add, to_add, 0, 0, borderType=cv2.BORDER_CONSTANT,
                                     value=(
                                     int(background_colour[0]), int(background_colour[1]), int(background_colour[2])))
    resized = cv2.resize(new_img, (max_size, max_size), interpolation=cv2.INTER_AREA)
    return resized
