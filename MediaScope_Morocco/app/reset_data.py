import glob
import os

for pattern in ["data/bronze/*.json", "data/silver/*.csv", "data/gold/*.csv", "data/gold/*.json"]:
    for path in glob.glob(pattern):
        os.remove(path)
        print(f"Deleted {path}")
print("Data folders cleaned.")
