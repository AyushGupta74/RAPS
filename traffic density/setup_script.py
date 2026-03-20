# NOTE: Run this script FROM 'trasffic_density_project' DIRECTORY
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from utils.file_paths import *

PATHS = [
    RAW_DIR,
    RAW_IMAGES_DIR,
    RAW_ANNOTATIONS_XML_DIR,
    RAW_ANNOTATIONS_XML_DIR_TEST,
    TRAIN_IMG_DIR,
    VAL_IMG_DIR,
    TRAIN_LABELS_DIR,
    VAL_LABELS_DIR,
    OUTPUT_ALL_LABELS,
    TEST_DIR
]

if __name__ == "__main__":
    while True:
        user_input = input("First time setup? (y/n): ").strip().lower()
        if user_input == 'y':
            # from scripts.download_dataset import download
            # download()
            from scripts.setup_folders import *
            setup_folders(PATHS)
            copy_files_to_directories(
                IMAGE_ROOT,
                RAW_IMAGES_DIR, 
                XML_ROOT, 
                RAW_ANNOTATIONS_XML_DIR, 
                RAW_ANNOTATIONS_XML_DIR_TEST, 
                XML_ROOT_TEST
            )
            break
        elif user_input == 'n':
            print("Setup skipped.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue
    
    while True:
        user_input = input("Convert XML to YOLO format labels? (y/n): ").strip().lower()
        if user_input == 'y':
            from scripts.xml_to_yolo import *
            xml_to_yolo()
            break
        elif user_input == 'n':
            print("XML to YOLO conversion skipped.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue
    while True:
        input_user = input("Split dataset into Train and Val sets? (y/n): ").strip().lower()
        if input_user == 'y':
            from scripts.split_dataset import *
            train_seq, val_seq = split_dataset(seeder=42, split_ration=0.8)
            copy(train_seq, "train")
            copy(val_seq, "val")
            print("Train/Val split done.")
            break
        elif input_user == 'n':
            print("Dataset splitting skipped.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue
    while True:
        input_user = input("Generate yaml config file? (y/n): ").strip().lower()
        if input_user == 'y':
            from scripts.generate_yaml import *
            generate_yaml()
            break
        elif input_user == 'n':
            print("YAML generation skipped.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
            continue