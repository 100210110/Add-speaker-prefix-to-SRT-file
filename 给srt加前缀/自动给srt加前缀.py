from pynput import keyboard
from pynput.keyboard import Key, Controller
from time import sleep as s
from pyperclip import copy




def ct_v():
    s(0.1)
    keyboard_controller.press(Key.ctrl_l)
    keyboard_controller.press('v')
    keyboard_controller.release('v')
    keyboard_controller.release(Key.ctrl_l)
    s(0.05)

def cv_names():
        ct_v()
        for i in range(4):
            keyboard_controller.press(Key.down)
            keyboard_controller.release(Key.down)

def on_press(key):
    if key in CV_NAMES:
        print(f"开始执行 {times} 次")
        for i in range(times):
            cv_names()

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass



if __name__ == "__main__":
    current = set()
    keyboard_controller = Controller()
    CV_NAMES = {keyboard.Key.f8}
    
    name = input("输入字幕前缀名, 默认Re: ") or "Re"
    copy(f"{name}：")
    times = int(input("输入执行次数, 默认1: ") or 1)
    print("切换到srt文件指定位置, 按下 F8 键开始执行...")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
