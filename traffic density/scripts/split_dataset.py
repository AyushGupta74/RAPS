import os, random, shutil
from utils.file_paths import IMAGE_ROOT, OUTPUT_ALL_LABELS as LBL_ALL

def split_dataset(seeder=42, split_ration=0.8):

    random.seed(seeder)

    sequences = sorted(os.listdir(IMAGE_ROOT)) 
    # data == IMAGE_ROOT
    random.shuffle(sequences)

    split = int(split_ration * len(sequences))
    train_seq = sequences[:split]
    val_seq   = sequences[split:]

    return train_seq, val_seq

def copy(seq_list, split_name):
    OUT_IMG = "./data/processed/images"
    OUT_LBL = "./data/processed/labels"
    
    for seq in seq_list:
        for img in os.listdir(os.path.join(IMAGE_ROOT, seq)):
            if img.endswith(".jpg"):
                src_img = os.path.join(IMAGE_ROOT, seq, img)
                lbl = f"{seq}_{img.replace('.jpg','.txt')}"
                src_lbl = os.path.join(LBL_ALL, lbl)

                if not os.path.exists(src_lbl):
                    continue

                new_name = f"{seq}_{img}"
                shutil.copy(src_img, os.path.join(OUT_IMG, split_name, new_name))
                shutil.copy(src_lbl, os.path.join(OUT_LBL, split_name, new_name.replace(".jpg",".txt")))

# if __name__ == "__main__":
#     train_seq, val_seq = split_dataset(seeder=42, split_ration=0.8)
#     copy(train_seq, "train")
#     copy(val_seq, "val")

#     print("Train/Val split done.")
#     # return train_seq, val_seq

