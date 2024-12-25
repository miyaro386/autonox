from datetime import datetime


def init_device():
    from adbutils import adb
    d = adb.device(transport_id=24)
    return d


def get_position_with_image(img, target, view_result=False):
    import cv2
    # テンプレートマッチングを実行
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)

    # 最も一致する位置を取得
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 一致した位置に矩形を描画
    top_left = max_loc  # 一致した位置の左上の座標
    h, w = target.shape[:2]  # テンプレート画像の高さと幅
    bottom_right = (top_left[0] + w, top_left[1] + h)

    if view_result:
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.imshow('Matched Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    x = top_left[0] + w // 2
    y = top_left[1] + h // 2
    return x, y

from functools import wraps
import time


def retry_decorator(retry_num: int, sleep_sec: int):
    """
    リトライするデコレータを返す
    :param retry_num: リトライ回数
    :param sleep_sec: リトライするまでにsleepする秒数
    :return: デコレータ
    """

    def _retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for retry_count in range(1, retry_num + 1):
                try:
                    ret = func(*args, **kwargs)
                    return ret
                except Exception as exp:  # pylint: disable=broad-except
                    if retry_count == retry_num:
                        print(f"Retry_count over ({retry_count}/{retry_num})")
                        raise Exception from exp
                    else:
                        print(f"Retry after {sleep_sec} sec ({retry_count}/{retry_num}). Error = {exp}")
                        time.sleep(sleep_sec)

        return wrapper

    return _retry


if __name__ == '__main__':
    import cv2
    import numpy as np
    # 画像を読み込む
    image = cv2.imread('src_img.png')  # 対象画像
    template = cv2.imread('notification.png')  # テンプレート画像
    get_position_with_image(image, template, view_result=True)


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H-%f")
