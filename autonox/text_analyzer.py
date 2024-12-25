from yomitoku import DocumentAnalyzer
import numpy as np


class TextAnalyzer:
    def __init__(self):
        self.analyzer = DocumentAnalyzer(configs={}, device="cuda")

    def get_text_position(self, img, text):
        resutls, *_ = self.analyzer(img)
        for word in resutls.words:
            if text in word.content:
                points = np.array(word.points)
                x, y = np.mean(points, axis=0).astype(int).tolist()
                return x, y
        return None



