from adbutils import adb

d = adb.device(transport_id=24)

d.swipe(800, 800, 800, 200, 0.5)