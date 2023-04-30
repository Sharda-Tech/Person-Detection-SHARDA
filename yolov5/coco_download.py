import fiftyone as fo
import fiftyone.zoo as foz

# Load COCO person detection dataset
coco = foz.load_zoo_dataset(
    "coco-2017",
    
    classes=["person"],
    
)

