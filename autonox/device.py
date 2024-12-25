import cv2
import numpy as np
from adbutils import adb
from autonox.utils import get_position_with_image, retry_decorator, get_timestamp


class Device:
    def __enter__(self):
        self.d = adb.device(transport_id=24)
        self.stream = self.d.shell("getevent -lt /dev/input/event4", stream=True)
        self.f = self.stream.conn.makefile()
        return self

    def screenshot(self):
        pilimg = self.d.screenshot()
        img = np.array(pilimg)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def save_screenshot(self, path):
        img = self.screenshot()
        cv2.imwrite(path, img)

    @retry_decorator(retry_num=10, sleep_sec=1)
    def tap_with_template(self, template_path):
        img = self.screenshot()
        template = cv2.imread(template_path)  # テンプレート画像
        x, y = get_position_with_image(img, template)
        self.d.click(x, y)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        self.stream.close()

if __name__ == '__main__':
    with Device() as device:
        device.save_screenshot(f"autonox/assets/arknights/img_{get_timestamp()}.png")
