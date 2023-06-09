import zipfile
import os
from deep_translator import GoogleTranslator
import json
import shutil
import tkinter as tk
from tkinter import filedialog
# ask user to select mods folder

folder_selected = filedialog.askdirectory(title="Select input folder")
if not folder_selected:
    exit()
output_folder = filedialog.askdirectory(title="Select output folder")
if not output_folder:
    output_folder = folder_selected
print(folder_selected,output_folder)
# get all files in mods folder
mods = os.listdir(folder_selected)
for mod in mods:
    print(mod)
    if not mod.endswith(".jar"):
        continue
    mod_path = folder_selected+"/" + mod
    with zipfile.ZipFile(mod_path,"r") as zip_ref:
        zip_ref.extractall("temp")
    # check is assets folder in mod
    if not os.path.isdir("./temp/assets"):
        continue
    for creator in os.listdir("./temp/assets"):
        # check is lang folder in creators folder
        if not os.path.isdir("./temp/assets/" + creator + "/lang"):
            continue
        # parse file in lang folder and set input path if exists
        input_path = ""
        for file in os.listdir("./temp/assets/" + creator + "/lang"):
            if file.endswith(".json"):
                input_path = "./temp/assets/" + creator + "/lang/" + file
                break

        if input_path == "":
            continue
        output_path = "./temp/assets/" + creator + "/lang/uk_ua.json"
        with open(input_path) as f:
            file = json.load(f)
        res = {}
        for key,item in file.items():
            res[key] = GoogleTranslator(source='auto', target='uk').translate(item)
        print(res)
        with open(output_path, "w",encoding="utf-8") as f:
            encodedUnicode = json.dump(res,f, ensure_ascii=False,indent=4)
        # create zip if not exists
    zipObj = zipfile.ZipFile(file=output_folder+"/"+mod, mode='w')
    for folderName, subfolders, filenames in os.walk('./temp'):
        for filename in filenames:
            filePath = os.path.join(folderName, filename)
            zipObj.write(filePath, os.path.relpath(filePath, './temp'), compress_type=zipfile.ZIP_DEFLATED)
    zipObj.close()
    shutil.rmtree("./temp")