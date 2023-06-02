import fiftyone as fo
import pandas as pd
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
# Load the dataset

#This will stores the dataset at fiftyone folder in user name folder(if we use colab then the fiftyone folder in root folder
# else if we are using our own storage the fiftyone  folder will be along with the documents and downloads in C or D drive  )
dataset = fo.zoo.load_zoo_dataset(
    "coco-2017",
    split='train', 
    label_types=["detections"],
    classes=['person']
)



