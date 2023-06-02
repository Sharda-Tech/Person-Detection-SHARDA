import os
import json
import shutil

# Path to COCO dataset
coco_images_dir = r"C:\Users\adith\fiftyone\coco-2017\validation\data"
coco_annotations_file = r"C:\Users\adith\fiftyone\coco-2017\train\labels.json"

# Output YOLO folders
yolo_output_images = r'cocodataset/images'
yolo_output_labels = r'C:\Users\adith\Documents\computer vision\cocodataset\train\labels'
os.makedirs(yolo_output_images, exist_ok=True)
os.makedirs(yolo_output_labels, exist_ok=True)

# Load COCO annotations
with open(coco_annotations_file, 'r') as f:
    coco_data = json.load(f)

# Filter annotations for 'person' category
person_category_id = 1
person_annotations = [ann for ann in coco_data['annotations'] if ann['category_id'] == person_category_id]

for ann in person_annotations:
    image_id = ann['image_id']
    image_info = next((img for img in coco_data['images'] if img['id'] == image_id), None)
    if image_info:
        image_path = os.path.join(coco_images_dir, image_info['file_name'])
        image_width = image_info['width']
        image_height = image_info['height']

        bbox = ann['bbox']
        x, y, width, height = bbox

        # Convert bbox to YOLO format
        x_center = x + width / 2
        y_center = y + height / 2
        x_center /= image_width
        y_center /= image_height
        width /= image_width
        height /= image_height

        # Copy image to yolo_output_images folder
        
        output_image_path = os.path.join(yolo_output_images, os.path.basename(image_path))
        shutil.copyfile(image_path, output_image_path)
        
        # Write YOLO annotation to file
        label_filename = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
        output_label_path = os.path.join(yolo_output_labels, label_filename)
        with open(output_label_path, 'a') as label_file:  # Use 'a' to append to the existing file
            line = f"{person_category_id} {x_center} {y_center} {width} {height}\n"
            label_file.write(line)
