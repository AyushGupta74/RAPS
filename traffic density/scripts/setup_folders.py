def setup_folders(folders: list):
    import os

    for f in folders:
        os.makedirs(f, exist_ok=True)

    print("Folder structure ready.")

def copy_files_to_directories(
        IMAGE_ROOT,
        RAW_IMAGES_DIR, 
        XML_ROOT, 
        RAW_ANNOTATIONS_XML_DIR, 
        RAW_ANNOTATIONS_XML_DIR_TEST, 
        XML_ROOT_TEST
):
    import os,shutil
    
    def copy_imgs():

        print("copying files to created directories...")

        source_image_root = IMAGE_ROOT
        destination_images_dir = RAW_IMAGES_DIR

        os.makedirs(destination_images_dir, exist_ok=True)

        for item_name in os.listdir(source_image_root):
            item_path = os.path.join(source_image_root, item_name)

            if os.path.isdir(item_path) and item_name.startswith('MVI_'):
                destination_path = os.path.join(destination_images_dir, item_name)
                try:
                    shutil.copytree(item_path, destination_path)
                    # print(f"Successfully copied: {item_name}")
                except FileExistsError:
                    print(f"Directory {item_name} already exists in destination, skipping.")
                except Exception as e:
                    print(f"Error copying {item_name}: {e}")

        print("Finished copying MVI_xxxxx folders.")
    
    # -----------------------------------------------------------------
    def copy_xml_train():

        print(f"Copying XML files from {XML_ROOT} to {RAW_ANNOTATIONS_XML_DIR}")

        # List all items in the XML_ROOT
        for item_name in os.listdir(XML_ROOT):
            if item_name.endswith('.xml'):
                source_path = os.path.join(XML_ROOT, item_name)
                destination_path = os.path.join(RAW_ANNOTATIONS_XML_DIR, item_name)
                try:
                    shutil.copy(source_path, destination_path)
                    # print(f"Successfully copied: {item_name}")
                except FileExistsError:
                    print(f"File {item_name} already exists in destination, skipping.")
                except Exception as e:
                    print(f"Error copying {item_name}: {e}")

        print("Finished copying train XML files.")

    # -----------------------------------------------------------------
    
    def copy_xml_test():
        os.makedirs(RAW_ANNOTATIONS_XML_DIR_TEST, exist_ok=True)
        print(f"Copying XML files from {XML_ROOT_TEST} to {RAW_ANNOTATIONS_XML_DIR_TEST}")

        # List all items in the XML_ROOT_TEST
        for item_name in os.listdir(XML_ROOT_TEST):
            if item_name.endswith('.xml'):
                source_path = os.path.join(XML_ROOT_TEST, item_name)
                destination_path = os.path.join(RAW_ANNOTATIONS_XML_DIR_TEST, item_name)
                try:
                    shutil.copy(source_path, destination_path)
                    # print(f"Successfully copied: {item_name}")
                except FileExistsError:
                    print(f"File {item_name} already exists in destination, skipping.")
                except Exception as e:
                    print(f"Error copying {item_name}: {e}")

    copy_imgs()
    copy_xml_train()
    copy_xml_test()