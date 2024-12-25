import os
import sys
import cv2
import numpy as np
from adbutils import adb
from tqdm import tqdm


d = adb.device(transport_id=24) # transport_id can be found in: adb devices -l


stream = d.shell("getevent -lt /dev/input/event4", stream=True)
f = stream.conn.makefile()

for _ in tqdm(range(10**12)):
    pilimg = d.screenshot()
    img = np.array(pilimg)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

