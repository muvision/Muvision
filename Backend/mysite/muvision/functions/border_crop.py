import cv2
import numpy as np


def prepare_image(image, dimension_size):
    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img_th = cv2.GaussianBlur(img_gray, (5, 5), 0)

    ret, thresh1 = cv2.threshold(img_th, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, dimension_size)
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    inverted_image = cv2.bitwise_not(img_th)
    ret1, thresh2 = cv2.threshold(inverted_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    inverted_dilation = cv2.dilate(thresh2, rect_kernel, iterations=1)

    return dilation, inverted_dilation


def prepare_crop(image):
    dilation, inverted_dilation = prepare_image(image, (1, 1))
    cntrs = get_contours(dilation, inverted_dilation)
    return border_fix(image, dilation, inverted_dilation)


def border_fix(image, dilation, inverted_mask):
    # Initializing temporary variables to be used
    final_contours = None
    counter = 0
    cropped_image = image.copy()

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    # Finding contours inverse
    contours_mask, hierarchy = cv2.findContours(inverted_mask, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)

    contour_len = len(contours)
    contour_mask_len = len(contours_mask)
    # Determines the maximum contour length of both
    final_contours_length = max(contour_len, contour_mask_len)

    ''' If the contour length is greater than 1 for both not inverted and inverted,
  then we assume that one of the masks does not include any borders. The problem
  before is that the contours would be found, but it would just end up finding the
  contours of a border
  '''
    while final_contours_length <= 1 and counter < 16:

        if (contour_len and contour_mask_len) <= 1:

            x1, y1, w1, h1 = cv2.boundingRect(contours[0])
            x2, y2, w2, h2 = cv2.boundingRect(contours_mask[0])

            if w1 * h1 <= w2 * h2:
                src = np.array([[x1, y1], [x1, y1 + h1], [x1 + w1, y1 + h1], [x1 + w1, y1]], np.float32)
                dst = np.array([[0, 0], [0, h1], [w1, h1], [w1, 0]], np.float32)

                # Getting the linear transformation to be used to warp the image
                MT = cv2.getPerspectiveTransform(src, dst)

                # Remove any rotations, warping issues with the image
                cropped_image = cv2.warpPerspective(cropped_image, MT, (w1, h1))
                dilation = cv2.warpPerspective(dilation, MT, (w1, h1))
                inverted_mask = cv2.warpPerspective(inverted_mask, MT, (w1, h1))

                final_contours = contours
            else:
                src = np.array([[x2, y2], [x2, y2 + h2], [x2 + w2, y2 + h2], [x2 + w2, y2]], np.float32)
                dst = np.array([[0, 0], [0, h2], [w1, h2], [w2, 0]], np.float32)
                # Getting the linear transformation to be used to warp the image
                MT = cv2.getPerspectiveTransform(src, dst)

                # Remove any rotations, warping issues with the image
                cropped_image = cv2.warpPerspective(cropped_image, MT, (w2, h2))
                dilation = cv2.warpPerspective(dilation, MT, (w2, h2))
                inverted_mask = cv2.warpPerspective(inverted_mask, MT, (w2, h2))

                final_contours = contours_mask

        counter += 1

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        # Finding contours inverse
        contours_mask, hierarchy = cv2.findContours(inverted_mask, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)
        contour_len = len(contours)
        contour_mask_len = len(contours_mask)

        final_contours_length = max(contour_len, contour_mask_len)

    return cropped_image


def get_contours(dilation, inverted_dilation):
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    # Finding contours inverse
    contours_mask, hierarchy = cv2.findContours(inverted_dilation, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_NONE)
    if len(contours) > len(contours_mask):
        cntrs = contours
    else:
        cntrs = contours_mask

    return cntrs


def binarize_img(img):
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    th, im_otsu = cv2.threshold(im_gray, 192, 255, cv2.THRESH_OTSU)
    return im_otsu
