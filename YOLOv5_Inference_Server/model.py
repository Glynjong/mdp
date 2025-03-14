import os
import shutil
import time
import glob
import torch
from PIL import Image
from ultralytics import YOLO
import cv2
import random
import string
import numpy as np
import yolov5
import pathlib



def get_random_string(length):
    """
    Generate a random string of fixed length 

    Inputs
    ------
    length: int - length of the string to be generated

    Returns
    -------
    str - random string

    """
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

def load_model():
    """
    Load the model from the local directory
    """
    # Nat model load
    # temp = pathlib.PosixPath
    # pathlib.PosixPath = pathlib.WindowsPath
    # file_path = r"C:\Users\DELL G15\Desktop\SCHOOL\MDP\mdp\Weights\best_yolo5_2024_10_18.pt"
    # yolov5_path = r"C:\Users\DELL G15\Desktop\SCHOOL\MDP\mdp\yolov5"  # Explicit full path

    # print(f"Loading YOLOv5 from: {yolov5_path}")
    
    # model = torch.hub.load(yolov5_path, 'custom', path=file_path, source='local', force_reload=True)

    # print("✅ Model Loaded Successfully!")
    # model = YOLO(file_path)  
    #model.conf = 0.6  # confidence threshold

    
    model = YOLO("../Weights/best_plsplspls.pt")
    # model = YOLO("../Weights/bestv3_nat.pt")
    # model = YOLO("../Weights/best_e205v8.pt")
    # model = YOLO("../Weights/best_kev.pt")
    # print("Model Classes:", model.names)
    return model

def draw_own_bbox(img,x1,y1,x2,y2,label,color=(36,255,12),text_color=(0,0,0)):
    """
    Draw bounding box on the image with text label and save both the raw and annotated image in the 'own_results' folder

    Inputs
    ------
    img: numpy.ndarray - image on which the bounding box is to be drawn

    x1: int - x coordinate of the top left corner of the bounding box

    y1: int - y coordinate of the top left corner of the bounding box

    x2: int - x coordinate of the bottom right corner of the bounding box

    y2: int - y coordinate of the bottom right corner of the bounding box

    label: str - label to be written on the bounding box

    color: tuple - color of the bounding box

    text_color: tuple - color of the text label

    Returns
    -------
    None

    """
    # create the own/results file
    if not os.path.exists('own_results'):
        os.makedirs('own_results')


    name_to_id = {
        "NA": 'NA',
        "Bullseye": 0,
        "one": 11,
        "two": 12,
        "three": 13,
        "four": 14,
        "five": 15,
        "six": 16,
        "seven": 17,
        "eight": 18,
        "nine": 19,
        "A": 20,
        "B": 21,
        "C": 22,
        "D": 23,
        "E": 24,
        "F": 25,
        "G": 26,
        "H": 27,
        "S": 28,
        "T": 29,
        "U": 30,
        "V": 31,
        "W": 32,
        "X": 33,
        "Y": 34,
        "Z": 35,
        "up": 36,
        "down": 37,
        "right": 38,
        "left": 39,
        "circle": 40
    }

    # name_to_id = {
    #     "NA": 'NA',
    #     "Bullseye-id10": 0,
    #     "one_id11": 11,
    #     "two_id12": 12,
    #     "three_id13": 13,
    #     "four_id14": 14,
    #     "five_id15": 15,
    #     "six_id16": 16,
    #     "seven_id17": 17,
    #     "eight_id18": 18,
    #     "nine_id19": 19,
    #     "A_id20": 20,
    #     "B_id21": 21,
    #     "C_id22": 22,
    #     "D_id23": 23,
    #     "E_id24": 24,
    #     "F_id25": 25,
    #     "G_id26": 26,
    #     "H_id27": 27,
    #     "S_id28": 28,
    #     "T_id29": 29,
    #     "U_id30": 30,
    #     "V_id31": 31,
    #     "W_id32": 32,
    #     "X_id33": 33,
    #     "Y_id34": 34,
    #     "Z_id35": 35,
    #     "up_id36": 36,
    #     "down_id37": 37,
    #     "right_id38": 38,
    #     "left_id39": 39,
    #     "stop-id40": 40
    # }
    # name_to_id = {
    #     "NA": 'NA',
    #     "0": 0,
    #     "11": 11,
    #     "12": 12,
    #     "13": 13,
    #     "14": 14,
    #     "15": 15,
    #     "16": 16,
    #     "17": 17,
    #     "18": 18,
    #     "19": 19,
    #     "20": 20,
    #     "21": 21,
    #     "22": 22,
    #     "23": 23,
    #     "24": 24,
    #     "25": 25,
    #     "26": 26,
    #     "27": 27,
    #     "28": 28,
    #     "29": 29,
    #     "30": 30,
    #     "31": 31,
    #     "32": 32,
    #     "33": 33,
    #     "34": 34,
    #     "35": 35,
    #     "36": 36,
    #     "37": 37,
    #     "38": 38,
    #     "39": 39,
    #     "40": 40,
    #     "41": 41,
    # }
    # Reformat the label to {label name}-{label id}
    label_id = name_to_id.get(label, 'NA')
    label = label + "-" + str(label_id)
    # Convert the coordinates to int
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    # Create a random string to be used as the suffix for the image name, just in case the same name is accidentally used
    rand = str(int(time.time()))

    # Save the raw image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f"own_results/raw_image_{label}_{rand}.jpg", img)

    # Draw the bounding box
    img = cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    # For the text background, find space required by the text so that we can put a background with that amount of width.
    (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
    # Print the text  
    img = cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), color, -1)
    img = cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1)
    # Save the annotated image
    cv2.imwrite(f"own_results/annotated_image_{label}_{rand}.jpg", img)


def predict_image(image, model, signal):
    try:
        # Load the image
        img = Image.open(os.path.join('images', image))

        # Predict the image using the model
        results = model(img)  # Returns a list of Results objects

        # Ensure the 'runs' folder exists
        if not os.path.exists('runs'):
            os.makedirs('runs')

        # Save each detection as a separate image
        if len(results) > 0:
            print(f"Detections found: {len(results)}")
            timestamp = int(time.time())
            for i, result in enumerate(results):
                # Get the annotated image
                annotated_img = result.plot()  # Returns an image with bounding boxes

                unique_filename = f"runs/detection_{image.split('.')[0]}_{timestamp}_{i}.jpg"
                # Save the annotated image
                cv2.imwrite(unique_filename, annotated_img)
                print(f"Saved detection image: {unique_filename}")
        else:
            print("No detections found.")

        # Extract detection results from the first result object
        if len(results) > 0:
            result = results[0]  # Use the first result
            boxes = result.boxes  # Access detection boxes

            # Extract bounding box coordinates, confidence scores, and class labels
            bbox_data = []
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()  # Bounding box coordinates
                conf = box.conf.item()  # Confidence score
                cls = box.cls.item()  # Class label
                name = model.names[int(cls)]  # Class name
                bbox_data.append({
                    'xmin': x1,
                    'ymin': y1,
                    'xmax': x2,
                    'ymax': y2,
                    'confidence': conf,
                    'name': name
                })

            # Convert to a DataFrame-like structure (optional)
            import pandas as pd
            df_results = pd.DataFrame(bbox_data)

            # Calculate the height, width, and area of the bounding box
            df_results['bboxHt'] = df_results['ymax'] - df_results['ymin']
            df_results['bboxWt'] = df_results['xmax'] - df_results['xmin']
            df_results['bboxArea'] = df_results['bboxHt'] * df_results['bboxWt']

            # Sort by bounding box area (largest first)
            df_results = df_results.sort_values('bboxArea', ascending=False)

            # Filter out Bullseye
            pred_list = df_results[df_results['name'] != 'Bullseye']
            # pred_list = df_results[df_results['name'] != 'Bullseye-id10']

            # Initialize prediction to NA
            pred = 'NA'

            # If only one label is detected and it's not Bullseye
            if len(pred_list) == 1:
                if pred_list.iloc[0]['name'] != 'Bullseye':
                # if pred_list.iloc[0]['name'] != 'Bullseye-id10':
                    pred = pred_list.iloc[0]

            # If more than one label is detected
            elif len(pred_list) > 1:
                # Filter by confidence and area
                pred_shortlist = []
                current_area = pred_list.iloc[0]['bboxArea']
                for _, row in pred_list.iterrows():
                    if row['name'] != 'Bullseye' and row['confidence'] > 0.5 and (
                    # if row['name'] != 'Bullseye-id10' and row['confidence'] > 0.5 and (
                        (current_area * 0.8 <= row['bboxArea']) or
                        (row['name'] == 'One' and current_area * 0.6 <= row['bboxArea'])
                    ):
                        pred_shortlist.append(row)
                        current_area = row['bboxArea']

                # If only one prediction remains after filtering
                if len(pred_shortlist) == 1:
                    pred = pred_shortlist[0]

                # If multiple predictions remain, use signal to filter further
                else:
                    pred_shortlist.sort(key=lambda x: x['xmin'])
                    if signal == 'L':
                        pred = pred_shortlist[0]
                    elif signal == 'R':
                        pred = pred_shortlist[-1]
                    else:
                        for i in range(len(pred_shortlist)):
                            if pred_shortlist[i]['xmin'] > 250 and pred_shortlist[i]['xmin'] < 774:
                                pred = pred_shortlist[i]
                                break
                        if isinstance(pred, str):
                            pred_shortlist.sort(key=lambda x: x['bboxArea'])
                            pred = pred_shortlist[-1]

            # Draw the bounding box on the image
            if not isinstance(pred, str):
                draw_own_bbox(np.array(img), pred['xmin'], pred['ymin'], pred['xmax'], pred['ymax'], pred['name'])

            # Map the prediction to an ID
            name_to_id = {
                "NA": 'NA',
                "Bullseye": 0,
                "one": 11,
                "two": 12,
                "three": 13,
                "four": 14,
                "five": 15,
                "six": 16,
                "seven": 17,
                "eight": 18,
                "nine": 19,
                "A": 20,
                "B": 21,
                "C": 22,
                "D": 23,
                "E": 24,
                "F": 25,
                "G": 26,
                "H": 27,
                "S": 28,
                "T": 29,
                "U": 30,
                "V": 31,
                "W": 32,
                "X": 33,
                "Y": 34,
                "Z": 35,
                "up": 36,
                "down": 37,
                "right": 38,
                "left": 39,
                "circle": 40
            }
            
            # name_to_id = {
            #     "NA": 'NA',
            #     "Bullseye-id10": 0,
            #     "one_id11": 11,
            #     "two_id12": 12,
            #     "three_id13": 13,
            #     "four_id14": 14,
            #     "five_id15": 15,
            #     "six_id16": 16,
            #     "seven_id17": 17,
            #     "eight_id18": 18,
            #     "nine_id19": 19,
            #     "A_id20": 20,
            #     "B_id21": 21,
            #     "C_id22": 22,
            #     "D_id23": 23,
            #     "E_id24": 24,
            #     "F_id25": 25,
            #     "G_id26": 26,
            #     "H_id27": 27,
            #     "S_id28": 28,
            #     "T_id29": 29,
            #     "U_id30": 30,
            #     "V_id31": 31,
            #     "W_id32": 32,
            #     "X_id33": 33,
            #     "Y_id34": 34,
            #     "Z_id35": 35,
            #     "up_id36": 36,
            #     "down_id37": 37,
            #     "right_id38": 38,
            #     "left_id39": 39,
            #     "stop-id40": 40
            # }
                # name_to_id = {
                #     "NA": 'NA',
                #     "0": 0,
                #     "11": 11,
                #     "12": 12,
                #     "13": 13,
                #     "14": 14,
                #     "15": 15,
                #     "16": 16,
                #     "17": 17,
                #     "18": 18,
                #     "19": 19,
                #     "20": 20,
                #     "21": 21,
                #     "22": 22,
                #     "23": 23,
                #     "24": 24,
                #     "25": 25,
                #     "26": 26,
                #     "27": 27,
                #     "28": 28,
                #     "29": 29,
                #     "30": 30,
                #     "31": 31,
                #     "32": 32,
                #     "33": 33,
                #     "34": 34,
                #     "35": 35,
                #     "36": 36,
                #     "37": 37,
                #     "38": 38,
                #     "39": 39,
                #     "40": 40,
                #     "41": 41,
                # }
            if not isinstance(pred, str):
                image_id = str(name_to_id[pred['name']])
            else:
                image_id = 'NA'
            print(f"Final result: {image_id}")
            return image_id

        else:
            print("No detections found.")
            return 'NA'

    except Exception as e:
        print(f"Error during prediction: {e}")
        return 'NA'
      

def predict_image_week_9(image, model):
    # Load the image
    img = Image.open(os.path.join('images', image))
    # Run inference
    results = model(img)
    # Save the results
    results.save('runs')
    # Convert the results to a dataframe
    first_result = results[0]
    first_result.save('runs')
    df_results = first_result.pandas().xyxy[0]

    #df_results = results.pandas().xyxy[0]
    # Calculate the height and width of the bounding box and the area of the bounding box
    df_results['bboxHt'] = df_results['ymax'] - df_results['ymin']
    df_results['bboxWt'] = df_results['xmax'] - df_results['xmin']
    df_results['bboxArea'] = df_results['bboxHt'] * df_results['bboxWt']

    # Label with largest bbox height will be last
    df_results = df_results.sort_values('bboxArea', ascending=False)
    pred_list = df_results 
    pred = 'NA'
    # If prediction list is not empty
    if pred_list.size != 0:
        # Go through the predictions, and choose the first one with confidence > 0.5
        for _, row in pred_list.iterrows():
            if row['name'] != 'Bullseye' and row['confidence'] > 0.5:
                pred = row    
                break

        # Draw the bounding box on the image 
        if not isinstance(pred,str):
            draw_own_bbox(np.array(img), pred['xmin'], pred['ymin'], pred['xmax'], pred['ymax'], pred['name'])
        
    # Dictionary is shorter as only two symbols, left and right are needed
    name_to_id = {
        "NA": 'NA',
        "Bullseye": 10,
        "Right": 38,
        "Left": 39,
        "Right Arrow": 38,
        "Left Arrow": 39,
    }
    # Return the image id
    if not isinstance(pred,str):
        image_id = str(name_to_id[pred['name']])
    else:
        image_id = 'NA'
    return image_id


def stitch_image():
    """
    Stitches the images in the 'runs/' folder and saves the final stitched image inside 'runs/'.
    """
    imgFolder = 'runs'  # ✅ Looks in 'runs/' instead of 'runs/detect/'
    stitchedPath = os.path.join(imgFolder, f'stitched-{int(time.time())}.jpeg')

    # ✅ Search directly inside 'runs/' for images
    imgPaths = glob.glob(os.path.join(imgFolder, "*.jpg"))

    # ✅ Prevent crashing if no images are found
    if not imgPaths:
        print("⚠️ No images found in 'runs/' to stitch.")
        return None

    # Load images using PIL
    images = [Image.open(x) for x in imgPaths]

    # Get total width and max height for stitched image
    width, height = zip(*(i.size for i in images))
    total_width = sum(width)
    max_height = max(height)

    # Create blank stitched image
    stitchedImg = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        stitchedImg.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    # ✅ Save stitched image inside 'runs/'
    stitchedImg.save(stitchedPath)

    print(f"✅ Stitched image saved at: {stitchedPath}")

    # ✅ Move original images to "runs/originals/" after stitching
    originals_folder = os.path.join(imgFolder, "originals")
    if not os.path.exists(originals_folder):
        os.makedirs(originals_folder)

    for img in imgPaths:
        shutil.move(img, os.path.join(originals_folder, os.path.basename(img)))

    return stitchedImg

def stitch_image_own():
    """
    Stitches the images in the folder together and saves it into own_results folder

    Basically similar to stitch_image() but with different folder names and slightly different drawing of bounding boxes and text
    """
    imgFolder = 'own_results'
    stitchedPath = os.path.join(imgFolder, f'stitched-{int(time.time())}.jpeg')

    imgPaths = glob.glob(os.path.join(imgFolder+"/annotated_image_*.jpg"))
    imgTimestamps = [imgPath.split("_")[-1][:-4] for imgPath in imgPaths]
    
    sortedByTimeStampImages = sorted(zip(imgPaths, imgTimestamps), key=lambda x: x[1])

    images = [Image.open(x[0]) for x in sortedByTimeStampImages]
    width, height = zip(*(i.size for i in images))
    total_width = sum(width)
    max_height = max(height)
    stitchedImg = Image.new('RGB', (total_width, max_height))
    x_offset = 0

    for im in images:
        stitchedImg.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    stitchedImg.save(stitchedPath)

    return stitchedImg

