import os
import sys
import shutil

# RUN THIS CODE ONCE TO SORT YOUR IMAGES!
# Cats and dogs - https://www.kaggle.com/competitions/dogs-vs-cats/data?select=train.zip
# Other - https://www.kaggle.com/datasets/puneet6060/intel-image-classification?select=seg_train
def move_to_val(source, validation, num):
    try:
        for filename in os.listdir(source):
            file_path = os.path.join(source, filename)
            try:
                file_name = os.path.splitext(filename)[0]
                file_number = file_name.split('.')[1]
                if int(file_number) > num:
                    shutil.move(file_path, validation)
            except (IndexError, ValueError):
                continue
    except Exception as e:
        print(f"An error occurred: {e}")

def move_other_to_val(source, validation, num):
    try:
        for filename in os.listdir(source):
            file_path = os.path.join(source, filename)
            try:
                file_number = os.path.splitext(filename)[0]
                if int(file_number) > num:
                    shutil.move(file_path, validation)
            except (IndexError, ValueError):
                continue
    except Exception as e:
        print(f"An error occurred: {e}")

SOURCE = r"C:\Users\admin\Downloads\train\train"
SOURCE_OTHER = r"C:\Users\admin\Downloads\seg_train\seg_train"
CATS_T = r"C:\Users\admin\Desktop\VSCProjects\CatDog\train\cats"
DOGS_T = r"C:\Users\admin\Desktop\VSCProjects\CatDog\train\dogs"
OTHER_T = r"C:\Users\admin\Desktop\VSCProjects\CatDog\train\other"
CATS_V = r"C:\Users\admin\Desktop\VSCProjects\CatDog\validate\cats"
DOGS_V = r"C:\Users\admin\Desktop\VSCProjects\CatDog\validate\dogs"
OTHER_V = r"C:\Users\admin\Desktop\VSCProjects\CatDog\validate\other"

os.makedirs(CATS_T, exist_ok=True)
os.makedirs(DOGS_T, exist_ok=True)
os.makedirs(CATS_V, exist_ok=True)
os.makedirs(DOGS_V, exist_ok=True)
os.makedirs(OTHER_T, exist_ok=True)
os.makedirs(OTHER_V, exist_ok=True)

try:
    if not os.path.isdir(SOURCE):
        print(f"{SOURCE} does not exist")
        sys.exit()
    for filename in os.listdir(SOURCE):
        file_path = os.path.join(SOURCE, filename)
        if os.path.isfile(file_path):
            if filename.startswith("cat"):
                shutil.move(file_path, CATS_T)
            elif filename.startswith("dog"):
                shutil.move(file_path, DOGS_T)
except Exception as e:
    print(f"An error occurred: {e}")

try:
    if not os.path.isdir(SOURCE_OTHER):
        print(f"{SOURCE_OTHER} does not exist")
        sys.exit()
    for dirname in os.listdir(SOURCE_OTHER):
        dir_path = os.path.join(SOURCE_OTHER, dirname)
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                shutil.move(file_path, OTHER_T)
except Exception as e:
    print(f"An error occurred: {e}")

print("Sorting finished")


move_to_val(CATS_T, CATS_V, 10000)
move_to_val(DOGS_T, DOGS_V, 10000)
move_other_to_val(OTHER_T, OTHER_V, 16000)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^