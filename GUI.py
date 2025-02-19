import os
from pathlib import Path

import tkinter
from tkinter import filedialog #needs seprate importing
from PIL import Image, ImageTk

import imutils.perspective
import numpy
import cv2

def main():
    root = tkinter.Tk()
    root.geometry("480x640")
    root.resizable(width=False, height=False)
    root.title("DocumentScanner by RajatKumar-gsrk")
    root.iconbitmap("./contract.ico")
    lbl_head = tkinter.Label(text="DocumentScanner", fg = "white", bg = "gray", font=("Futura", 30))
    lbl_head.pack(fill="x")#setting width = x;
    lbl_head = tkinter.Label(text="RajatKumar-gsrk", fg = "#1c3ad4", bg = "gray", font=("ROBOTO BOLD", 15))
    lbl_head.place(x = 0, y = 40, relwidth=1)#relwidth takes width of parent element, width = 480, pixels
    
    def openImageBox():
        nonlocal image_labels, image_names, lbl_noImage
        file_paths = filedialog.askopenfilenames(initialdir="./input" , title="Select Images to be Processed", filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))

        if file_paths:
            lbl_noImage.pack_forget()
            lbl_noImage.destroy()
            for image_label in image_labels:
                image_label.grid_forget()
                image_label.destroy()
            image_labels = [] #resets old images if new selected
            image_names = []

            for widget in iamgeFrame.winfo_children():
                widget.destroy()

            # ADDING scrollable images to Frames

            canvas = tkinter.Canvas(iamgeFrame, width=400, height=400, background="gray")
            canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

            scrollbar_y = tkinter.Scrollbar(iamgeFrame, orient=tkinter.VERTICAL, command=canvas.yview)
            scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)

            canvas.config(yscrollcommand=scrollbar_y.set)

            thumbnail_frame = tkinter.Frame(canvas, background="gray")  # Frame for thumbnails
            canvas.create_window((0, 0), window=thumbnail_frame)


            def configure_canvas(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            thumbnail_frame.bind("<Configure>", configure_canvas)

            iamgeFrame.configure(borderwidth=4, relief="sunken")

            for imagePath in file_paths:
                image = Image.open(imagePath)
                image.thumbnail((125,125))
                image = ImageTk.PhotoImage(image)
                image_names.append(imageName(imagePath))
                lbl_inFrame = tkinter.Label(master=thumbnail_frame, image=image, text=f"{image_names[-1]}", width=125, borderwidth=1, relief="solid")#compound=tkinter.TOP to show lable at bottom
                lbl_inFrame.image = image
                image_labels.append(lbl_inFrame)
            
            images_added = 0
            for image_label in image_labels:
                image_label.grid(row = int(images_added/3), column = int(images_added%3), sticky = "",padx = 2, pady = 1)
                images_added += 1

            enOutputName = tkinter.Entry(master=root, font=("Consolas", 20))
            def on_entry_focus_in(event):
                if enOutputName.get() == "Output":  # Check if it's the placeholder
                    enOutputName.delete(0, tkinter.END)  # Clear the entry

            def on_entry_focus_out(event):
                if enOutputName.get() == "":  # Check if it's empty
                    enOutputName.insert(0, "Output")  # Insert the placeholder
            enOutputName.bind("<FocusIn>", on_entry_focus_in)
            enOutputName.bind("<FocusOut>", on_entry_focus_out)
            enOutputName.insert(0, "Output")
            enOutputName.pack(pady=5, fill="x")
            btnConvert = tkinter.Button(master=root, text="Convert To Doxument PDF", command=lambda:convertImagesToPdf(file_paths, enOutputName.get()))
            btnConvert.pack(pady=5)
        else:
            return
    
    def imageName(imagePath):
        return imagePath.split("/")[-1]

    btn_selectImages = tkinter.Button(text="Select Images", command=openImageBox)
    btn_selectImages.pack(pady=25)#now we have paths for all the selected images

    image_labels, image_names = [], []
    iamgeFrame = tkinter.Frame(master=root, width=400, height=500, background="gray")
    iamgeFrame.pack(pady=5)# image frame is ready now


    lbl_noImage = tkinter.Label(master=iamgeFrame, text="No Image Selected", font=("TKDefaultFont", 30, "bold"))#when no image selected
    lbl_noImage.pack()




    root.mainloop()

def convertImagesToPdf(imagePaths, nameOfOutput):
    cv2ImageList = read_images_from_path(imagePaths)
    resizedCv2ImageList = resize_images(cv2ImageList, 500)
    processedCv2ImageList = image_processing(resizedCv2ImageList)

    cornerPoints = getCornerPoints(processedCv2ImageList)
    aspectRatios = find_ratios(cv2ImageList, resizedCv2ImageList)

    cornerPointsOriginalImageList = shift_points(aspectRatios, cornerPoints)

    croppedCv2Images = crop_images(cv2ImageList, cornerPointsOriginalImageList)

    save_to_pdf(f".\\output\\{nameOfOutput}.pdf", croppedCv2Images)

    openFolder(".\\output")



def read_images_from_path(image_paths):
    images = []
    for path in image_paths:
        images.append(cv2.imread(path))
    return images

def resize_images(images, new_width):
    resized_images = []
    for image in images:
        old_height, old_width = get_height(image), get_width(image)
        aspect_ratio = find_ratio(old_height , old_width)
        new_height = int(aspect_ratio * new_width)
        image_new_size = (new_width, new_height)

        image = cv2.resize(image, image_new_size)
        resized_images.append(image)
    return resized_images

def get_height(image):
    return image.shape[0]

def get_width(image):
    return image.shape[1]

def find_ratio(num1, num2):
    return num1/num2

def image_processing(resized_images):#grayscale -> blur -> edge detection -> give room for error -> close small gaps ->return
    processed_images = []
    for resized_image in resized_images:
        #turned graycale
        gray_image = image_to_grayscale(resized_image)
        #blurred
        blured_image = image_to_blur(gray_image)
        #detecting edges
        edge_detected_image = image_to_canny(blured_image)
        #broadning edges
        seed = numpy.ones((4, 4), numpy.uint8)
        dialated_image = cv2.dilate(edge_detected_image, seed)
        #closing small gaps
        no_gap_image = cv2.morphologyEx(dialated_image, cv2.MORPH_CLOSE, seed)
        processed_images.append(no_gap_image)

    return processed_images

#turn cv2 image to grayscale
def image_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#apply blur to cv2 image
def image_to_blur(image):
    return cv2.GaussianBlur(image,(5, 5), 0)

def image_to_canny(image):
    return cv2.Canny(image, 50, 200)

def getCornerPoints(images):#find contour -> sort by area -> return largest are with 4 points
    four_points_list = []
    for image in images:
        contours = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0] #ignore heirarchies
        contours = sorted(contours, key = cv2.contourArea, reverse = True) #puts largest area first

        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

            if len(approx) == 4: #found largest closed area with 4 corners
                four_points_list.append(numpy.squeeze(approx))
                break
    
    return four_points_list

def find_ratios(original_images, resized_images):
    ratios = []
    for i in range(len(original_images)):
        ratio = find_ratio(get_height(original_images[i]), get_height(resized_images[i]))
        ratios.append(ratio)
    
    return ratios

def shift_points(ratios, four_points_list):
    shifted_four_points = []
    for i in range(len(ratios)):
        shifted_four_points.append((ratios[i] * four_points_list[i]).astype(int))
    
    return shifted_four_points

def crop_images(original_images, four_points_for_original_list):
    cropped_images = []
    for i in range(len(four_points_for_original_list)):
       cropped_image =  imutils.perspective.four_point_transform(original_images[i], four_points_for_original_list[i])
       cropped_images.append(cropped_image)
    
    return cropped_images

def save_to_pdf(pdf_path, cv2_image_list):
    cv2_image_list = resize_images(cv2_image_list, 1920)
    pil_images = []
    for image in cv2_image_list:
        #cv2 images are in BGR format
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)) #cv2 image is in form of array need to convert to PIL image format
        pil_images.append(pil_image)
    
    pil_images[0].save(pdf_path, "PDF", save_all = True, resolution = 100, append_images = pil_images[1:]) #methods from PIL library


def openFolder(pathToFolder):
    folder_path = Path(pathToFolder)
    try:
        if folder_path.is_dir():  # Check if it's a directory
            os.startfile(str(folder_path)) # If it is windows, use os.startfile
        else:
            print(f"Error: '{folder_path}' is not a directory.")

    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()