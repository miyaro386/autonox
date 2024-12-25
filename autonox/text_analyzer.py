from yomitoku import DocumentAnalyzer
import numpy as np


class TextAnalyzer:
    def __init__(self):
        self.analyzer = DocumentAnalyzer(configs={}, device="cuda")

    def get_text_position(self, img, text):
        results = self.get_results(img)
        for word in results.words:
            if text in word.content:
                points = np.array(word.points)
                x, y = np.mean(points, axis=0).astype(int).tolist()
                return x, y
        return None

    def get_results(self, img):
        resutls, *_ = self.analyzer(img)
        return resutls

    def get_positions_in_results(self, results, text):
        positions = []
        for word in results.words:
            if text in word.content:
                points = np.array(word.points)
                x, y = np.mean(points, axis=0).astype(int).tolist()
                positions.append((x, y))
        return positions





