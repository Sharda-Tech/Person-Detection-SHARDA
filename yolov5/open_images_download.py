import fiftyone as fo
import fiftyone.zoo as foz
# Loading Open Images person detection dataset
dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=["Person"]
)