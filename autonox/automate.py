from yomitoku.data import load_image
from autonox.device import Device
from autonox.text_analyzer import TextAnalyzer

def try_click_with_text(device, text_analyzer, text):
    img = device.screenshot()
    position = text_analyzer.get_text_position(img, text)
    if position is None:
        print(f"{text} not found")
        return
    device.d.click(*position)

def main():
    text_analyzer = TextAnalyzer()
    with Device() as device:

        if device.check_template_exists("autonox/assets/arknights/templates/notification.png"):
            device.tap_with_template("autonox/assets/arknights/templates/notification.png")
            try_click_with_text(device, text_analyzer, "受取可")
            try_click_with_text(device, text_analyzer, "納品可")
            try_click_with_text(device, text_analyzer, "信頼獲得")


    # device.tap_with_template("notification.png")
    # device.tap_with_template("autonox/assets/arknights/templates/receive.png")
    # device.tap_with_template("autonox/assets/arknights/templates/deliver.png")
    # device.tap_with_template("autonox/assets/arknights/templates/trust.png")
    # device.tap_with_template("autonox/assets/arknights/templates/assignment.png")

    # device.d.swipe(800, 800, 800, 600, 0.5)

if __name__ == '__main__':
    main()