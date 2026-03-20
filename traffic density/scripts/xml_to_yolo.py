import os
from utils.file_paths import *
from utils.class_map import CLASS_MAP
import xml.etree.ElementTree as ET
from utils.box_utils import convert_box
import cv2

def xml_to_yolo():
    xml_files_list = [f for f in os.listdir(RAW_ANNOTATIONS_XML_DIR) if f.endswith(".xml")]
    total_xml_files = len(xml_files_list)

    for i, xml_file in enumerate(xml_files_list):
        if not xml_file.endswith(".xml"):
            print(f"Skipping non-XML file: {xml_file}")
            continue

        seq_name = xml_file.replace(".xml", "")
        xml_path = os.path.join(RAW_ANNOTATIONS_XML_DIR, xml_file)
        img_dir = os.path.join(RAW_IMAGES_DIR, seq_name)

        if not os.path.isdir(img_dir):
            print(f"Missing images for {seq_name}, skipping")
            continue

        tree = ET.parse(xml_path)
        root = tree.getroot()

        for frame in root.iter("frame"):
            frame_num = int(frame.attrib["num"])
            img_name = f"img{frame_num:05d}.jpg"
            img_path = os.path.join(img_dir, img_name)

            if not os.path.exists(img_path):
                print(f"Missing image: {img_path}")
                continue

            img = cv2.imread(img_path)
            if img is None:
                print(f"Error reading image: {img_path}")
                continue

            img_h, img_w = img.shape[:2]
            yolo_lines = []

            for target in frame.iter("target"):
                box = target.find("box")
                attr = target.find("attribute")

                if box is None or attr is None:
                    continue

                vehicle_type = attr.attrib.get("vehicle_type", "").lower()
                if vehicle_type not in CLASS_MAP:
                    continue

                class_id = CLASS_MAP[vehicle_type]
                x, y, w, h = convert_box(box, img_w, img_h)

                yolo_lines.append(
                    f"{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"
                )

            # Modify label file name to include sequence name
            label_file = f"{seq_name}_{img_name.replace('.jpg', '.txt')}"
            label_path = os.path.join(OUTPUT_ALL_LABELS, label_file)

            with open(label_path, "w") as f:
                f.write("\n".join(yolo_lines))

        progress = (i + 1) / total_xml_files * 100
        print(f"Processing XML files: {progress:.2f}% complete")

def check_yolo_file():
    print(f"Checking generated YOLO label files in: {OUTPUT_ALL_LABELS}")

    label_files = [f for f in os.listdir(OUTPUT_ALL_LABELS) if f.endswith('.txt')]

    if label_files:
        print(f"\nFirst 5 generated label files: {label_files[:5]}")

        # Display content of a sample label file
        sample_label_file = label_files[0]
        sample_label_path = os.path.join(OUTPUT_ALL_LABELS, sample_label_file)
        print(f"\nContent of sample label file '{sample_label_file}':")
        with open(sample_label_path, 'r') as f:
            print(f.read())

        total_generated_labels = len(label_files)
        print(f"Total number of generated label files: {total_generated_labels}")
    else:
        print("No label files found in the output directory. Please check the conversion process.")

def xml_to_yolo_test():
    xml_files_list = [f for f in os.listdir(RAW_ANNOTATIONS_XML_DIR_TEST) if f.endswith(".xml")]
    total_xml_files = len(xml_files_list)

    for i, xml_file in enumerate(xml_files_list):
        if not xml_file.endswith(".xml"):
            print(f"Skipping non-XML file: {xml_file}")
            continue

        seq_name = xml_file.replace(".xml", "")
        xml_path = os.path.join(RAW_ANNOTATIONS_XML_DIR_TEST, xml_file)
        img_dir = os.path.join(RAW_IMAGES_DIR, seq_name)

        if not os.path.isdir(img_dir):
            print(f"Missing images for {seq_name}, skipping")
            continue

        tree = ET.parse(xml_path)
        root = tree.getroot()

        for frame in root.iter("frame"):
            frame_num = int(frame.attrib["num"])
            img_name = f"img{frame_num:05d}.jpg"
            img_path = os.path.join(img_dir, img_name)

            if not os.path.exists(img_path):
                print(f"Missing image: {img_path}")
                continue

            img = cv2.imread(img_path)
            if img is None:
                print(f"Error reading image: {img_path}")
                continue

            img_h, img_w = img.shape[:2]
            yolo_lines = []

            for target in frame.iter("target"):
                box = target.find("box")
                attr = target.find("attribute")

                if box is None or attr is None:
                    continue

                vehicle_type = attr.attrib.get("vehicle_type", "").lower()
                if vehicle_type not in CLASS_MAP:
                    continue

                class_id = CLASS_MAP[vehicle_type]
                x, y, w, h = convert_box(box, img_w, img_h)

                yolo_lines.append(
                    f"{class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"
                )

            # Modify label file name to include sequence name
            label_file = f"{seq_name}_{img_name.replace('.jpg', '.txt')}"
            label_path = os.path.join(TEST_DIR, 'labels', label_file)

            with open(label_path, "w") as f:
                f.write("\n".join(yolo_lines))

        progress = (i + 1) / total_xml_files * 100
        print(f"Processing Test XML files: {progress:.2f}% complete")

