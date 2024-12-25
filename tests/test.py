import unittest

import cv2
from yomitoku.data import load_image

from autonox.device import Device
from autonox.text_analyzer import TextAnalyzer
from autonox.utils import get_timestamp


class TestCase(unittest.TestCase):
    def test_save_screenshot(self):
        with Device() as device:
            device.save_screenshot(f"../autonox/assets/arknights/img_{get_timestamp()}.png")

    def test_check_template_exists(self):
        from autonox.utils import check_template_exists

        template = cv2.imread("../autonox/assets/arknights/templates/notification.png")

        img = cv2.imread("../autonox/assets/arknights/img_2024-12-25-19-413571.png")
        print(check_template_exists(img, template))

        img2 = cv2.imread("../autonox/assets/arknights/img_2024-12-25-17-807901.png")
        print(check_template_exists(img2, template))

    def test_yomitoku(self):
        from yomitoku import DocumentAnalyzer
        img = load_image("../autonox/assets/arknights/img_2024-12-25-17-807901.png")
        analyzer = DocumentAnalyzer(configs={}, visualize=True, device="cuda")
        results, ocr_vis, layout_vis = analyzer(img)

        results.to_json("output.json")
        # 可視化画像を保存
        cv2.imwrite("output_ocr.jpg", ocr_vis)
        cv2.imwrite("output_layout.jpg", layout_vis)

    def test_yomitoku_with_adb(self):
        from yomitoku import DocumentAnalyzer
        with Device() as device:
            img = device.screenshot()
            analyzer = DocumentAnalyzer(configs={}, visualize=True, device="cuda")
            results, ocr_vis, layout_vis = analyzer(img)

            results.to_json("output.json")
            # 可視化画像を保存
            cv2.imwrite("output_ocr.jpg", ocr_vis)
            cv2.imwrite("output_layout.jpg", layout_vis)

    def test_get_text_position(self):
        img = load_image("../autonox/assets/arknights/img_2024-12-25-17-584374.png")
        text_analyzer = TextAnalyzer()
        position = text_analyzer.get_text_position(img, "受取可")
        print(position)




if __name__ == '__main__':
    unittest.main()
