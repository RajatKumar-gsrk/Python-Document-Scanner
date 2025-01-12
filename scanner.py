import imutils.perspective
import numpy as np
import cv2
import matplotlib.pyplot as mp
import imutils

def main():#pipeline: open image -> resize image -> process image -> locate corners -> crop points -> save image
    #opening images
    image_paths = take_image_paths()
    image_names = find_names(image_paths)
    original_images = read_images_from_path(image_paths)

    #resized images
    resized_images = resize_images(original_images, 1000)

    #processing the images
    processed_images = image_processing(resized_images)
    
    #outling edges on image
    four_points_list = getCornerPoints(processed_images)
    add_outlines(four_points_list, resized_images)
    draw_images(resized_images, "outlined_image")

    #cropped image
    ratios = find_ratios(original_images, resized_images)
    four_points_for_original_list = shift_points(ratios, four_points_list)
    cropped_images = crop_images(original_images, four_points_for_original_list)
    draw_images(cropped_images, "Cropped_image")

    #saving images
    save_images(".\\output_images\\",image_names, cropped_images)

    #closing all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#asks user for image paths
def take_image_paths():
    print("Enter (CORRECT) paths for each image on new line, type 'end' to stop giving input: ")
    paths = []
    while True:
        x = input()
        if x == 'end':
            break
        paths.append(x)
    return paths

def find_names(image_paths):
    names = []
    for path in image_paths:
        name = path.split("/")[-1]
        names.append(name)
    return names

#return images from paths
def read_images_from_path(image_paths):
    images = []
    for path in image_paths:
        images.append(cv2.imread(path))
    return images

#draws image in window
def draw_images(images, window_name = "image"):
    i = 0
    for image in images:
        cv2.imshow(f"{window_name} {i}", image)
        i += 1


#image resizing function
def resize_images(images, new_width):
    resized_images = []
    for image in images:
        old_height, old_width, channel = image.shape
        aspect_ratio = old_height / old_width
        new_height = int(aspect_ratio * new_width)
        image_new_size = (new_width, new_height)

        image = cv2.resize(image, image_new_size)
        resized_images.append(image)
    return resized_images

#process the image
def image_processing(resized_images):#grayscale -> blur -> edge detection -> give room for error -> close small gaps ->return
    processed_images = []
    for resized_image in resized_images:
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
        processed_images.append(no_gap_image)

    return processed_images

#returns corner points for image
def getCornerPoints(images):#find contour -> sort by area -> return largest are with 4 points
    four_points_list = []
    for image in images:
        contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True) #puts largest area first

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

            if len(approx) == 4: #found largest closed area with 4 corners
                four_points_list.append(np.squeeze(approx))
                break
    
    return four_points_list

#adds out line to images
def add_outlines(four_points_list, resized_images):
    i = 0
    for four_points in four_points_list:
        cv2.drawContours(resized_images[i], [four_points], -1, (255, 0, 0), 3)
        i += 1

#finds resolution ratio between 2 images
def find_ratios(original_images, resized_images):
    ratios = []
    for i in range(len(original_images)):
        ratio = original_images[i].shape[0]/resized_images[i].shape[0]
        ratios.append(ratio)
    
    return ratios

#shift ponits by ratios
def shift_points(ratios, four_points_list):
    shifted_four_points = []
    for i in range(len(ratios)):
        shifted_four_points.append((ratios[i] * four_points_list[i]).astype(int))
    
    return shifted_four_points

#crops required images by crop points
def crop_images(original_images, four_points_for_original_list):
    cropped_images = []
    for i in range(len(four_points_for_original_list)):
       cropped_image =  imutils.perspective.four_point_transform(original_images[i], four_points_for_original_list[i])
       cropped_images.append(cropped_image)
    
    return cropped_images

#saves images in desiered path
def save_images(path, names,cropped_images):
    for i in range(len(cropped_images)):
        cv2.imwrite(f"{path}{names[i]}", cropped_images[i])
        i += 1
        

if __name__ == "__main__":
    main()
