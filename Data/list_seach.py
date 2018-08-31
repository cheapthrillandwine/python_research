import os

path = r"C:\Users\NSW00_906882\Desktop\paper0201-0809"

files = os.listdir(path)
files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]

print(files_file)
