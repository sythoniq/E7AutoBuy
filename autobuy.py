from tkinter import simpledialog, messagebox
from tkinter import *
import pytesseract as ocr
import subprocess
import PIL
from PIL import Image
from io import BytesIO
import sys
import shutil
import time
import configparser
import datetime
import logging

PNG_SIG = b"\x89PNG\r\n\x1a\n"
ADB = shutil.which("adb")
adb_device = None

def connect():
    subprocess.run([ADB, "connect", adb_device], capture_output=True)


def adb(*args):
    cmd = [ADB]
    if adb_device:
        cmd += ["-s", adb_device]
    cmd += [str(a) for a in args]
    result = None
    for attempt in range(4):
        result = subprocess.run(cmd, capture_output=True)
        err = result.stderr.decode(errors="ignore").lower()
        dropped = any(s in err for s in ("not found", "offline", "unauthorized", "no devices", "closed"))
        if result.returncode == 0 and not dropped:
            return result
        if adb_device:
            connect()
        time.sleep(1)
    return result

def click(x, y):
    adb("shell", "input", "tap", x, y)


def screen():
    result = adb("exec-out", "screencap", "-p")
    img_bytes = result.stdout
    # Waydroid can print warning text to stdout before the PNG data
    start = img_bytes.find(PNG_SIG)
    if start == -1:
        raise PIL.UnidentifiedImageError(f"screencap returned no PNG. stdout={img_bytes[:200]!r} stderr={result.stderr[:200]!r}")
    screenshot = Image.open(BytesIO(img_bytes[start:]))
    return screenshot

def swipe(x1, y1, x2, y2):
    adb("shell", "input", "touchscreen", "swipe", x1, y1, x2, y2)


def reroll():
    time.sleep(1*delay)
    click(rbx, rby)
    time.sleep(1*delay)
    click(rbx, rby)
    time.sleep(1*delay)
    click(rbcx, rbcy)
    time.sleep(1*delay)
    click(rbcx, rbcy)
    time.sleep(2*delay)


def buy(slot):
    time.sleep(1 * delay)
    if slot == 5:
        y = slot5
    elif slot == 4:
        y = slot4
    else:
        swipe(swipex, swipey2, swipex, swipey1)
        time.sleep(2 * delay)
        if slot == 3:
            y = slot3
        elif slot == 2:
            y = slot2
        elif slot == 1:
            y = slot1
        elif slot == 0:
            y = slot0

    time.sleep(2 * delay)
    click(slotb, y)
    time.sleep(1 * delay)
    click(slotb, y)
    time.sleep(1 * delay)
    click(slotcx, slotcy)
    time.sleep(1 * delay)
    click(slotcx, slotcy)

    time.sleep(2 * delay)
    swipe(swipex, swipey1, swipex, swipey2)
    time.sleep(4 * delay)


def killadb():
    adb("kill-server")


def config():
    delayset = simpledialog.askfloat(" ", "Delay value (Default is 1.5)\nIf your emulator has bad performance set a higher value\nOpen config.ini if want to change it later")
    if delayset is None:
        delayset = 1.5
    device = simpledialog.askstring(" ", "Waydroid ADB address (IP is shown by 'waydroid status')\nExample: 192.168.240.112:5555")
    if not device:
        device = "192.168.240.112:5555"
    configFile = open('config.ini', 'w')
    configFile.write(f'[Refresh]\ndelay = {delayset}\nadbDevice = {device}')
    configFile.close()


def crashhandler(handled=""):
    logging.basicConfig(filename='crash.log')
    logging.exception(f'\n{datetime.datetime.now()}{handled}\n')
    killadb()
    messagebox.showerror("Crash Handler", "Something went wrong, check crash.log file")
    sys.exit()


Tk().withdraw()
try:
    open('config.ini', 'x')
    config()
except FileExistsError:
    pass

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    adb_device = config.get('Refresh', 'adbDevice')
    delay = config.getfloat('Refresh', 'delay')
except:
    crashhandler("\nCheck your config.ini file")

rolls = simpledialog.askinteger(" ", "Number of refreshes\nSkystones spent will be 3 times this value")
if rolls is None:
    sys.exit()
cBM = 0
MM = 0
try:
    subprocess.run([ADB, "connect", adb_device])
    adb("devices")
    print("TO STOP ANYTIME PRESS CTRL+C IN THE CONSOLE")
    time.sleep(5)
    resolution = screen()
except PIL.UnidentifiedImageError:
    crashhandler("\nADB isn't working")

if abs(resolution.size[0]/resolution.size[1] - 16/9) > 0.01:
    messagebox.showerror("Error", f"Resolution {resolution.size[0]}x{resolution.size[1]} not supported, use 16:9 aspect ratio")
    killadb()
    sys.exit()
ET = str(datetime.timedelta(seconds=(rolls*11.5*delay)))[:8]
result = messagebox.askyesno("Setup", f"Skystones = {3*rolls}\nRefreshes = {rolls}\nDelay = {delay}x\nEstimated time = {ET}\nTO STOP ANYTIME PRESS CTRL+C IN THE CONSOLE\nReady to start ?")
if not result:
    killadb()
    sys.exit()

ratio = resolution.size[0]/1280

rbx = int(230*ratio)
rby = int(660*ratio)
rbcx = int(740*ratio)
rbcy = int(440*ratio)
slotb = int(1150*ratio)
slot0 = int(160*ratio)
slot1 = int(300*ratio)
slot2 = int(450*ratio)
slot3 = int(595*ratio)
slot4 = int(530*ratio)
slot5 = int(670*ratio)
slotcx = int(750*ratio)
slotcy = int(510*ratio)
cropulx = int(680*ratio)
cropul0 = int(90*ratio)
cropul1 = int(232*ratio)
cropul2 = int(375*ratio)
cropul3 = int(525*ratio)
cropul4 = int(460*ratio)
cropul5 = int(605*ratio)
cropbrx = int(1000*ratio)
cropbr0 = int(180*ratio)
cropbr1 = int(332*ratio)
cropbr2 = int(475*ratio)
cropbr3 = int(625*ratio)
cropbr4 = int(550*ratio)
cropbr5 = int(695*ratio)
swipex = int(1000*ratio)
swipey1 = int(575*ratio)
swipey2 = int(250*ratio)
start = datetime.datetime.now()

try:
    for x in range(rolls + 1):
        print(f'{x}/{rolls}')
        images = []
        ss = screen()

        images.append(ss.crop((cropulx, cropul0, cropbrx, cropbr0)))
        images.append(ss.crop((cropulx, cropul1, cropbrx, cropbr1)))
        images.append(ss.crop((cropulx, cropul2, cropbrx, cropbr2)))
        images.append(ss.crop((cropulx, cropul3, cropbrx, cropbr3)))

        time.sleep(1 * delay)
        swipe(swipex, swipey1, swipex, swipey2)
        time.sleep(2 * delay)
        ss = screen()
        images.append(ss.crop((cropulx, cropul4, cropbrx, cropbr4)))
        images.append(ss.crop((cropulx, cropul5, cropbrx, cropbr5)))

        ocrimage = []
        for im in images:
            ocrimage.append(ocr.image_to_string(im))

        count = 0
        slots = []
        for text in ocrimage:
            if "Covenant Bookmarks" in text:
                slots.append(count)
                cBM += 1
            elif "Mystic Medals" in text:
                slots.append(count)
                MM += 1
            count += 1

        if slots:
            for slot in slots:
                buy(slot)

        if x == rolls:
            break
        reroll()
except KeyboardInterrupt:
    pass
except:
    crashhandler()
end = datetime.datetime.now()
goldSpent = ((184*cBM) + (280*MM))*1000
rerollResults = f'Covenant Bookmark = {5*cBM}\nMystic Medals = {50*MM}\nGold Spent = {goldSpent}\n'
log = open("logs.txt", "a")
log.write(f'Started at {start}\nEnded at {end}\nTime elapsed: {end-start}\nRefreshes = {x}\nSkystones spent = {3*x}\n{rerollResults}\n')
log.close()
killadb()
messagebox.showinfo("Results", rerollResults)
