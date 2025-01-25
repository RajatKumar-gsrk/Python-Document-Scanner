# Python Document Scanner
#### Description:
**WHAT THIS CODE DOES -->**
<br>It takes jpg or jpeg images with document and process them, it then crops the document from image and save it either as an image file or a PDF file.
<br>
<br>
**BASIC PIPE LINE -->**
<br>Asks user to put all input files in input folder
<br>Reads file paths for all the .jpg and .jpeg files
<br>Open those images and store in a list
<br>resize all the images in list, for better processing
<br>process all the resized images
<br>Locate 4 points on image that represent document corner, for all images
<br>Shift those points to match the original images
<br>Crop the images
<br>Save as images or a PDF file based on user input
<br>
<br>
**Working of Project -->**
<br>*Tasks of main(): takes no argument*
<br>Making calls to various functions in ordered manner
<br>Functions called -->
<br>take_image_paths()
<br>find_names()
<br>read_images_from_path()
<br>resize_images()
<br>image_processing()
<br>getCornerPoints()
<br>find_ratios()
<br>shift_points()
<br>crop_images()
<br>save_images() or save_to_pdf() based on user choice
<br>
<br>*Task of take_image_paths(input_folder): takes path to input folder as string*
<br>Asks user to Press ENTER after puting images in input directory
<br>With help of pathlib.Path searches all the files and sub-directories and returns list of all the .jpg and .jpeg files
<br>
<br>*Task of find_names(image_paths): takes path of images as list*
<br>Extracts name of each file and returns as list of string
<br>
<br>*Task of read_images_from_path(image_paths): takes path of images as list*
<br>Returns List of cv2 image files(numpy arrays)
<br>
<br>*Task of resize_images(images, new_width): takes cv2 images as list, new width as integer*
<br>Loops through images
<br>Finds aspect ratio and resize each image to new width maintaining the aspect ratio
<br>Returns list of resized cv2 images
<br>
<br>*Task of get_height(image): takes cv2 image*
<br>Returns height of image as int
<br>
<br>*Task of get_width(image): takes cv2 image*
<br>Returns image width as int
<br>
<br>*Task of image_processing(resized_images):takes resized cv2 images as list*
<br>Loops through images
<br>Grayscale's image for better contrast and detection
<br>Blur's image to reduce noise
<br>Detects Edges in the image
<br>Dialate those edges to give room for error
<br>closes small gaps between detected edges
<br>returns list of processed cv2 images
<br>
<br>*Task of image_to_grayscale(image): takes cv2 image*
<br>Returns grayscale version of cv2 image
<br>
<br>*Task of image_to_blur(image): takes cv2 image*
<br>Returns blurred version of cv2 image
<br>
<br>*Task of image_edge_detection: takes cv2 image*
<br>Returns canny/Edge detected version of image
<br>
<br>*Task of getCornerPoints(images): takes cv2 canny images as list*
<br>loops through images
<br>finds all the contours of image
<br>Sorts them by area in reverse so Largest area comes first
<br>Detects largest area with 4 point in it(the document)
<br>Returns list of 4 points for all the images
<br>
<br>*task of find_ratios(original_images, resized_images): takes original cv2 image as list, and resized cv2 images as list*
<br>Loops through images
<br>Finds size ratio between them
<br>Returns list of ratios
<br>
<br>*Task of find_ratio(num1, num2): takes 2 numbers*
<br>Returns their ratio
<br>
<br>*Task of shift_points(ratios, four_points_list): takes ratios as list, 4 corners of documents as list*
<br>Loops through ratios
<br>Shifts 4 corner points by ratio
<br>Returns list of shifted 4 points
<br>
<br>*Task of crop_images(original_images, four_points_for_original_list): takes original cv2 images as list, shifted 4 points as list*
<br>Loops through list of points
<br>Crop images by the points(extracting document out of it)
<br>Returns list of cropped images
<br>
<br>*Task of save_images(path, names,cropped_images):takes output path as string, names of cv2 images as list, cropped cv2 images as list*
<br>Loops though images
<br>Saves image
<br>Display success message
<br>
<br>*Task of save_to_pdf(pdf_path, cv2_image_list): takes output path as string, cropped cv2 images as list*
<br>Asks user for output file name
<br>Resizes each image to width of 1920
<br>Loops through cv2 images
<br>Converts cv2 images to PIL images
<br>save as PDF file
<br>Displays success message
<br>
<br>
<br>**Testing instructions -->**
<br>Images used for teting as in for_testing directory, don't forget to include those
<br>
<br>
##THANKS
