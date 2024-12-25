import time
from autonox.device import Device
from autonox.text_analyzer import TextAnalyzer



class Automate:
    def __init__(self):
        self._text_analyzer = None
        self.device = None

    def try_click_with_text(self, text):
        img = self.device.screenshot()
        position = self.text_analyzer.get_text_position(img, text)
        if position is None:
            print(f"{text} not found")
            return
        self.device.click(*position)

    def get_positions(self, texts):
        img = self.device.screenshot()
        results = self.text_analyzer.get_results(img)
        positions = []
        for text in texts:
            positions += self.text_analyzer.get_positions_in_results(results, text)
        return positions


    def click_all_text(self, text):
        img = self.device.screenshot()
        results = self.text_analyzer.get_results(img)
        positions = self.text_analyzer.get_positions_in_results(results, text)
        positions = sorted(positions, key=lambda point: point[0])
        for position in positions:
            self.device.click(*position)

    def click_texts_if_all_exists(self, texts):
        img = self.device.screenshot()
        results = self.text_analyzer.get_results(img)
        positions = []
        for text in texts:
            positions += self.text_analyzer.get_positions_in_results(results, text)
        if len(texts) != len(positions):
            print(f"{texts} not found")
            return False
        for position in positions:
            self.device.click(*position)
        return True


    def run(self, ):
        with Device() as self.device:
            # positions = self.get_positions(["貿易所", "発電所", "製造所"])
            # for i, position in enumerate(positions):
            #     if i == 2:
            #         self.device.d.click(*position)
            #         break

            # self.try_click_with_text("配属情報")
            # self.try_click_with_text("クリア")
            # self.device.tap_with_template("autonox/assets/arknights/templates/ok.png")
            # self.device.tap_with_template("autonox/assets/arknights/templates/assign.png")

            # team = ["シャマレ", "カフカ", "バイビーク"]
            # team = ["グラベル", "スポット", "ブライオファイタ"]
            team = ["イフリータ"]
            result = self.click_texts_if_all_exists(team +["確定"])
            self.device.tap_with_template("autonox/assets/arknights/templates/back.png")


            # if device.check_template_exists("autonox/assets/arknights/templates/notification.png"):
            #     device.tap_with_template("autonox/assets/arknights/templates/notification.png")
            #     try_click_with_text(device, text_analyzer, "受取可")
            #     try_click_with_text(device, text_analyzer, "納品可")
            #     try_click_with_text(device, text_analyzer, "信頼獲得")

            # device.d.swipe(800, 800, 800, 400, 0.5)

            # try_click_with_text(device, text_analyzer, "配属一覧")
            # while text_analyzer.get_text_position(device.screenshot(), "宿舎") is None:
            #     device.d.swipe(800, 800, 800, 600, 0.5)

        # device.tap_with_template("notification.png")
        # device.tap_with_template("autonox/assets/arknights/templates/receive.png")
        # device.tap_with_template("autonox/assets/arknights/templates/deliver.png")
        # device.tap_with_template("autonox/assets/arknights/templates/trust.png")
        # device.tap_with_template("autonox/assets/arknights/templates/assignment.png")
        # device.d.swipe(800, 800, 800, 600, 0.5)

    @property
    def text_analyzer(self):
        if self._text_analyzer is None:
            self._text_analyzer = TextAnalyzer()
        return self._text_analyzer


if __name__ == '__main__':
    Automate().run()