import threading
from pynput import mouse
from PIL import ImageGrab, ImageTk, Image
from tkinter import Tk, Canvas, Toplevel, Label
import keyboard
import time
from ctypes import windll
import httpx
import os
import json
import base64
import io

KEY = 'alt'

def get_access_token(force_update=False):
    data = json.load(open("translate_image_cache"+os.sep+"translateAPI.json", "r"))
    if not (force_update or data["expires_in"] < int(time.time())):
        return data["access_token"]
    url = "https://image-translate-api.xxtg666.top/token?uuid="+data["uuid"]
    response = httpx.post(url)
    odata = json.loads(response.text)
    access_token = odata['access_token']
    expires_in = odata['expires_in']
    data["access_token"] = str(access_token)
    data["expires_in"] = int(expires_in)
    json.dump(data, open("translate_image_cache"+os.sep+"translateAPI.json", "w"))
    return access_token

def get_translate(file_name):
    payload = {'from': 'en', 'to': 'zh', 'v': '3', 'paste': '1'}
    image = {'image': (os.path.basename(file_name), open(file_name, 'rb'), "multipart/form-data")}
    response = httpx.post("https://aip.baidubce.com/file/2.0/mt/pictrans/v1?access_token="+get_access_token(), params = payload, files = image)
    img_data = base64.b64decode(json.loads(response.text)['data']['pasteImg'])
    image = Image.open(io.BytesIO(img_data))
    filename = "translate_image_cache"+os.sep+f"temp_translate_{time.time()}.png"
    image.save(filename)
    os.system("python show_image.pyw "+filename) # 不用 import 是因为 DPI 适配有问题

class ScreenshotTool:
    def __init__(self):
        self.scale=windll.shcore.GetScaleFactorForDevice(0)/100
        self.root = Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.canvas = Canvas(self.root, cursor='cross')
        self.canvas.pack(fill='both', expand=True)
        self.root.withdraw()
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.drawing = False
        self.key_pressed = False
        self.rect = None
        self.window_showed = False

        self.listener_mouse = mouse.Listener(
            on_click=self.on_click,
            on_move=self.on_move,
        )
        self.listener_mouse.start()
        keyboard.on_press_key(KEY, self.on_key_press)
        keyboard.on_release_key(KEY, self.on_key_release)

    def show_window(self):
        self.window_showed = True
        self.window_image = ImageGrab.grab(all_screens=True)
        self.window_image = self.window_image.resize((int(self.window_image.width/self.scale), int(self.window_image.height/self.scale)))
        self.window_image = ImageTk.PhotoImage(self.window_image)
        self.canvas.create_image(0,0,anchor='nw',image=self.window_image)
        self.canvas.pack()
        self.root.deiconify()
        
    def hide_window(self):
        self.window_showed = False
        self.root.withdraw()

    def on_key_press(self, _):
        print(KEY+' key pressed')
        self.key_pressed = True
        self.show_window()

    def on_key_release(self, _):
        print(KEY+' key released')
        self.key_pressed = False
        if not self.drawing:
            self.hide_window()

    def on_click(self, x, y, button, pressed):
        if self.key_pressed and pressed:
            self.start_x = x
            self.start_y = y
            self.end_x = x
            self.end_y = y
            self.drawing = True
            if not self.window_showed:
                self.show_window()
            return
        if not pressed and self.drawing:
            self.drawing = False
            x1 = min(self.start_x, self.end_x)
            y1 = min(self.start_y, self.end_y)
            x2 = max(self.start_x, self.end_x)
            y2 = max(self.start_y, self.end_y)
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            try:
                self.canvas.delete(self.rect)
                filename = "translate_image_cache"+os.sep+f'temp_screenshot_{time.time()}.png'
                screenshot.save(filename)
                print('Screenshot saved: '+filename.split(os.sep)[-1])
            except:
                print('Failed to take screenshot')
            time.sleep(0.1)
            self.hide_window()
            threading.Thread(target=get_translate, args=(filename,)).start()

    def on_move(self, x, y):
        if self.drawing:
            self.end_x = x
            self.end_y = y
            if self.rect:
                self.canvas.delete(self.rect)
            self.rect = self.canvas.create_rectangle(self.start_x/self.scale, self.start_y/self.scale, x/self.scale, y/self.scale, outline='red', width=1)
            self.canvas.after(50, self.canvas.delete, self.rect)

if __name__ == '__main__':
    try:
        os.mkdir('translate_image_cache')
    except:
        pass
    screenshot_tool = ScreenshotTool()
    screenshot_tool.root.mainloop()