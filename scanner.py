import imutils.perspective
import numpy as np
import cv2
import matplotlib.pyplot as mp
import imutils

def main():#pipeline: open image -> resize image -> process image -> locate corners -> crop points -> save image
    #opening image
    original_image = cv2.imread("./images/033.jpg")
    #displaying image file
    cv2.imshow("original_image", original_image)

    #resized image
    resized_image = resize_image(original_image, 1000)

    processed_image = image_processing(resized_image)
    #outling edges on image
    four_points = getCornerPoints(processed_image)
    cv2.drawContours(resized_image, [four_points], -1, (255, 0, 0), 3)
    cv2.imshow("outline_image", resized_image)

    #cropped image
    ratio = original_image.shape[0] / resized_image.shape[0]
    four_points_for_original = (ratio * four_points).astype(int)
    cropped_image = imutils.perspective.four_point_transform(original_image, four_points_for_original)
    cv2.imshow("Cropped_image", cropped_image)

    #saving an image
    cv2.imwrite(".\\output_images\\cropped_image.png", cropped_image)

    #closing all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#image resizing function
def resize_image(image, new_width):
    old_height, old_width, channel = image.shape
    aspect_ratio = old_height / old_width
    new_height = int(aspect_ratio * new_width)
    image_new_size = (new_width, new_height)

    image = cv2.resize(image, image_new_size)
    return image

def image_processing(resized_image):
    #turned graycale
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    #blurred
    blured_image = cv2.GaussianBlur(gray_image,(5, 5), 0)

    #detecting edges
    edge_detected_image = cv2.Canny(blured_image, 50, 200)

    #broadning edges
    seed = np.ones((4, 4), np.uint8)
    dialated_image = cv2.dilate(edge_detected_image, seed)

    #closing small gaps
    no_gap_image = cv2.morphologyEx(dialated_image, cv2.MORPH_CLOSE, seed)

    return no_gap_image

def getCornerPoints(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key = cv2.contourArea, reverse = True) #puts largest area first

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

        if len(approx) == 4: #found largest closed area with 4 corners
            return np.squeeze(approx)

if __name__ == "__main__":
    main()
