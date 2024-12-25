import cv2

from autonox.device import Device

with Device() as device:
    device.tap_with_template("notification.png")
    device.tap_with_template("autonox/assets/arknights/templates/receive.png")
    device.tap_with_template("autonox/assets/arknights/templates/deliver.png")
    device.tap_with_template("autonox/assets/arknights/templates/trust.png")
    device.tap_with_template("autonox/assets/arknights/templates/assignment.png")
