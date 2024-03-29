import os
import threading
from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
import pickle
from adbutils import adb
from pynput import keyboard

is_alive = True
d = adb.device()


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H-%f")


output = d.shell("wm size")
res = output.split()[-1]
res_x, res_y = res.split("x")
res_x, res_y = int(res_x), int(res_y)

output_dir = f"dataset/{get_timestamp()}"
os.makedirs(output_dir, exist_ok=True)


def key_press(key):
    global is_alive
    if key == keyboard.Key.esc:
        print("catch")
        is_alive = False


listener = keyboard.Listener(on_press=key_press)
listener.start()


@dataclass
class Event:
    timestamp: float
    key: str
    name: str
    value: str


def run_and_capture():
    global is_alive
    stream = d.shell("getevent -lt /dev/input/event4", stream=True)
    with stream:
        f = stream.conn.makefile()
        positions = None
        events = []
        while is_alive:
            line = f.readline()
            outputs = line.split()
            outputs = outputs[1:]
            outputs[0] = float(outputs[0].strip(']'))
            event = Event(*outputs)
            events.append(event)
            if event.key == "EV_KEY" and event.value == "DOWN":
                pilimg = d.screenshot()
                timestamp = get_timestamp()
                pilimg.save(f"{output_dir}/img_{timestamp}.png")
                positions = []
                position = {}
                start_time = event.timestamp

            if positions is not None and event.key == "EV_ABS":
                if event.name == 'ABS_MT_POSITION_X':
                    position["x"] = int(event.value, 16)
                if event.name == 'ABS_MT_POSITION_Y':
                    position["y"] = int(event.value, 16)

                if "x" in position and "y" in position:
                    elapsed_time = event.timestamp - start_time
                    position.update({"timestamp": event.timestamp, "elapsed_time": elapsed_time})
                    position["rel_x"] = position["x"] / res_x
                    position["rel_y"] = position["y"] / res_y
                    positions.append(position)
                    position = {}

            if event.key == "EV_KEY" and event.value == "UP":
                pprint(positions)
                filename = f"tap_{timestamp}.pkl"
                with open(f"{output_dir}/{filename}", "wb") as tapfile:
                    pickle.dump(positions, tapfile)
                positions = None

    print("break")


t = threading.Thread(target=run_and_capture)
t.start()
t.join()
listener.stop()
