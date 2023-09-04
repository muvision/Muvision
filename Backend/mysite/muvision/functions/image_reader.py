import cv2
import numpy as np
import pandas as pd
from . import border_crop as bc
from . import extract_characters as ec
from . import special_characters as sc
from . import identify_characters as ic
from IPython.display import display
from . import latex
from . import classification


def common_color(_img):
    unq, count = np.unique(_img.reshape(-1, 3), axis=0, return_counts=True)
    back_color = [0, 0, 0]
    back_color[0], back_color[1], back_color[2] = unq[np.argmax(count)]

    return back_color


def image_reader(image):
    image = np.asarray(image)
    cropped_image = bc.prepare_crop(image)

    cropped_image = bc.binarize_img(cropped_image)
    cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_GRAY2RGB)

    c_color = common_color(cropped_image)

    if c_color == [0, 0, 0]:
        w_mask = np.full((cropped_image.shape[0], cropped_image.shape[1], 3), (255, 255, 255), dtype=np.uint8)
        cropped_image = cv2.bitwise_xor(cropped_image, w_mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    cropped_image = cv2.erode(cropped_image, kernel, iterations=1)

    # Cropping the borders by 1% if case any there was unclean cropping of image
    height_diff = int(cropped_image.shape[0] * 0.01)
    width_diff = int(cropped_image.shape[1] * 0.01)

    cropped_image = cropped_image[height_diff:cropped_image.shape[0] - height_diff,
                    width_diff:cropped_image.shape[1] - width_diff]

    dilation, inverted_dilation = bc.prepare_image(cropped_image, (100, 5))

    im2 = cropped_image.copy()
    cntrs = bc.get_contours(dilation, inverted_dilation)

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    b_color = common_color(cropped_image)

    (cropped_lines, bounding_box) = ec.extract_contours(cropped_image, cntrs, b_color)

    boxcoords = pd.DataFrame([], )
    label = ['x', 'y', 'x1', 'y1', 'image']

    for i in range(len(bounding_box)):
        boxcoords = pd.concat([boxcoords, pd.DataFrame(
            [bounding_box[i][0], bounding_box[i][1], bounding_box[i][0] + bounding_box[i][2],
             bounding_box[i][1] + bounding_box[i][3], cropped_lines[i]])], axis='columns')

    boxcoords = boxcoords.transpose()
    boxcoords.columns = label
    boxcoords = boxcoords.reset_index()

    boxcoords = boxcoords.sort_values('y1', ascending=[True])

    line_info = []

    for i in range(len(boxcoords.index)):
        img_shape = boxcoords['image'].iloc[i].shape
        line_images = []
        single_bounding_box = []
        (line_images, single_bounding_box) = ec.identify_letter(boxcoords['image'].iloc[i], line_images,
                                                             single_bounding_box, 0, 0, 1, 1, 100, b_color)

        line_coords = pd.DataFrame([], )
        line_label = ['x', 'y', 'x1', 'y1', 'image', 'shape']
        for i in range(len(line_images)):
            resized_img = ec.resize(line_images[i], 45, 45, b_color)
            line_coords = pd.concat([line_coords, pd.DataFrame(
                [single_bounding_box[i][0], single_bounding_box[i][1], single_bounding_box[i][2],
                 single_bounding_box[i][3], resized_img, img_shape])], axis='columns')

        if len(line_coords) > 1:
            line_coords = line_coords.transpose()
            line_coords.columns = line_label
            line_coords = line_coords.reset_index()

            line_coords = line_coords.sort_values('x', ascending=[True])
            line_coords = line_coords.reset_index()
            line_coords = line_coords.drop(columns=['level_0', 'index'])

            median_y = []
            area = []

            for i in range(len(line_coords)):
                median_y.append((line_coords['y'].iloc[i] + line_coords['y1'].iloc[i]) / 2)
                area.append(abs(line_coords['y'].iloc[i] - line_coords['y1'].iloc[i]) * abs(line_coords['x'].iloc[i] - line_coords['x1'].iloc[i]))
            line_coords['median_y'] = median_y
            line_coords['area'] = area
            line_info.append(line_coords)

    for i in range(len(line_info)):
        std = np.std(line_info[i]['median_y'])
        median_mean = np.average(line_info[i]['median_y'])
        type_list = sc.determine_special_functions(line_info[i], std, median_mean)
        line_info[i]['character type'] = type_list

        # Used for equal signs and division
        line_info[i]['std'] = std
        line_info[i]['median_mean'] = median_mean

        display(line_info[i])

    document = ic.identify_lines(line_info)

    print(document)

    return document
    # Call


#img = cv2.imread('C:/Users/Richard/Pictures/Muvision Images/daa6ccaa-5a64-4a61-99b9-87ab1dd34ec31.jpg')
#lines = image_reader(img)
#
# latex.write_latex(lines)
#
# # print(classification.classify(img))
