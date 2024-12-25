#%%
from glob import glob

paths = glob("dataset/**/*.png", recursive=True)

#%%
import cv2
import pickle
import os
import random

random.shuffle(paths)

for i, path in enumerate(paths):
    img = cv2.imread(path)
    pkl_path = path.replace(".png", ".pkl").replace("img", "tap")
    with open(pkl_path, "rb") as f:
        taps = pickle.load(f)
    print(taps)
    
    for tap in taps:
        x = tap["x"]
        y = tap["y"]
        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)
    
    cv2.imshow('image', img)  
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    