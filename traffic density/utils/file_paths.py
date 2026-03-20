import os

DOANLOAD_PATH = 'UA-DETRAC' #DOANLOAD_PATH TO DOWNLOADED DATASET}
IMAGE_ROOT = os.path.join(DOANLOAD_PATH,"DETRAC-Images/DETRAC-Images")
XML_ROOT = os.path.join(DOANLOAD_PATH, "DETRAC-Train-Annotations-XML/DETRAC-Train-Annotations-XML")
XML_ROOT_TEST = os.path.join(DOANLOAD_PATH, "DETRAC-Test-Annotations-XML/DETRAC-Test-Annotations-XML")

DATASET_DIR = "data"

RAW_DIR = os.path.join(DATASET_DIR, "raw")
RAW_IMAGES_DIR = os.path.join(RAW_DIR, "images")
RAW_ANNOTATIONS_XML_DIR = os.path.join(RAW_DIR, "annotations_xml") 
RAW_ANNOTATIONS_XML_DIR_TEST = os.path.join(RAW_DIR, "test_annotations_xml") 

TRAIN_IMG_DIR = os.path.join(DATASET_DIR, "processed", "images", "train")
VAL_IMG_DIR = os.path.join(DATASET_DIR, "processed", "images", "val")
TRAIN_LABELS_DIR = os.path.join(DATASET_DIR, "processed", "labels", "train")
VAL_LABELS_DIR = os.path.join(DATASET_DIR, "processed", "labels", "val")

OUTPUT_ALL_LABELS = os.path.join(DATASET_DIR, "processed", "labels_all")

TEST_DIR = os.path.join(DATASET_DIR, "test")