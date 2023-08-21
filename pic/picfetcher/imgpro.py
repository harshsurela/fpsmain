import cv2 as cv
import numpy as np
import sys

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def apply_high_pass_filter(image, kernel_size):
    if kernel_size % 2 == 0:
        kernel_size += 1
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    filtered = cv.filter2D(image, -1, kernel)
    filtered = image.astype('float32') - filtered.astype('float32')
    filtered = filtered + 127 * np.ones(image.shape, np.uint8)
    filtered = filtered.astype('uint8')
    return filtered

def adjust_black_point(image, black_point):
    adjusted_image = map_range(image.astype('int32'), black_point, 255, 0, 255)
    _, adjusted_image = cv.threshold(adjusted_image, 0, 255, cv.THRESH_TOZERO)
    adjusted_image = adjusted_image.astype('uint8')
    return adjusted_image

def adjust_white_point(image, white_point):
    _, adjusted_image = cv.threshold(image, white_point, 255, cv.THRESH_TRUNC)
    adjusted_image = map_range(adjusted_image.astype('int32'), 0, white_point, 0, 255)
    adjusted_image = adjusted_image.astype('uint8')
    return adjusted_image

def apply_black_and_white_conversion(image):
    lab = cv.cvtColor(image, cv.COLOR_BGR2LAB)
    (l, a, b) = cv.split(lab)
    bw_image = cv.add(cv.subtract(l, b), cv.subtract(l, a))
    return bw_image

def main(input_image_path, output_image_path):
    image = cv.imread(input_image_path)
    black_point = 25
    white_point = 225
    mode = "SMODE"

    if mode == "GCMODE":
        image = apply_high_pass_filter(image, kernel_size=51)
        white_point = 127
        image = adjust_white_point(image, white_point)
        image = adjust_black_point(image, black_point)
    elif mode == "RMODE":
        image = adjust_black_point(image, black_point)
        image = adjust_white_point(image, white_point)
    elif mode == "SMODE":
        image = adjust_black_point(image, black_point)
        image = adjust_white_point(image, white_point)
        image = apply_black_and_white_conversion(image)

    cv.imwrite(output_image_path, image)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_image_path output_image_path")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        main(input_path, output_path)
