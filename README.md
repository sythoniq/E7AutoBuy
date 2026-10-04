# Tweaks And Steps to make it work for Waydroid on linux (Specifically Arch Linux... idk bout other stuff)

Fork changes so the script runs on Arch Linux against Waydroid instead of
Windows + an emulator. Only the Windows-specific parts were changed; the
coordinate math, OCR loop and buying logic are untouched.

## What changed in `autobuy.py`

- **Dialogs:** `ctypes.windll.user32.MessageBoxW` replaced with
  `tkinter.messagebox` (`showinfo`, `showerror`, `askyesno`).
- **ADB calls:** now go through one `adb()` helper that passes a list of
  arguments (no shell string quoting) and always captures output.
  - Targets one device with `-s <adbDevice>`.
  - Auto-reconnect: if a call fails or the error mentions
    not found / offline / unauthorized / no devices / closed, it runs
    `adb connect` and retries up to 4 times.
- **Screenshots:** `screen()` looks for the PNG signature in the output and
  ignores anything before it. Waydroid prints a warning line
  ("Failed to create //.cache for shader cache") to stdout before the image,
  which otherwise breaks Pillow. If no PNG is found, the error includes the
  first 200 bytes of output.
- **`killadb()`:** `taskkill /IM adb.exe` replaced with `adb kill-server`.
- **Config:** no more `tesseract.exe` / `adb.exe` pickers; both tools are
  found on `PATH`. `config.ini` is now:
```
  [Refresh]
  delay = 1.5
  adbDevice = 192.168.240.112:5555
```
  Delete any old Windows `config.ini` so it regenerates.
- **Resolution check:** `abs(w/h - 16/9) > 0.01` instead of exact float
  equality.
- Added the missing `import sys` (and `import shutil`); removed `ctypes`
  and `filedialog`.

## Setup on Arch

```bash
sudo pacman -S android-tools tesseract tesseract-data-eng python-pillow tk
python -m venv venv && source venv/bin/activate
pip install pytesseract pillow
```

`tesseract-data-eng` is required or OCR fails. `tk` provides tkinter.

## Waydroid setup

1. Start the session, then get the container IP: `waydroid status`
   (look for `IP address`). ADB port is 5555, so the address is
   `<ip>:5555`. Enter it when `config.ini` is first created.
2. The script runs `adb connect` itself. If Android shows an
   authorization prompt, accept it and tick "Always allow".
3. Screen must be **16:9**. The script scales every coordinate from the
   screen width (`width / 1280`) and rejects anything else. Check with
   `adb -s <ip>:5555 shell wm size`. To pin a size (examples: 1920x1080,
   or 1824x1026 to fit under 1900x1030):
```bash
   waydroid prop set persist.waydroid.width 1920
   waydroid prop set persist.waydroid.height 1080
   waydroid session stop && waydroid session start
```
   (Property names are from memory; `waydroid prop list` shows what your
   version supports.) Larger sizes work but make screenshots and OCR slower.
4. The game needs an ARM translation layer in Waydroid (libhoudini or
   libndk) to run at all.

## Known issues / not done

- If ADB drops and the IP changes after a session restart, update
  `adbDevice` in `config.ini`.
- No loading-screen detection; the script only uses fixed sleeps scaled
  by `delay`. Raise `delay` if the game is laggy.
- After clicking Yes on the "Ready to start?" dialog, the dialog may stay
  frozen on screen while the script runs (Tk gets no event loop). Possible
  fix: keep a `root = Tk()` reference and call `root.update()` after the
  dialog. Not applied.
- Untested: whether minimizing the Waydroid window pauses rendering and
  breaks `screencap`. Keep the window visible when testing.

## Debugging tips

- Test capture by hand:
  `adb -s <ip>:5555 exec-out screencap -p > /tmp/test.png; file /tmp/test.png`
- `crash.log` has the traceback and, for screenshot failures, the raw
  output that came back.
- If `adb()` is called with `capture=...` anywhere, you have an old helper;
  the current one is `def adb(*args):`.

# E7AutoBuy

Auto refreshes secret shop and buy all Covenant Bookmarks and Mystic Medals  
   
# 2.5  
- Added delay set up when creating config.ini
- Delay works with float values (ex: 1.7)
- Added Estimated time info
- Support to stop the script anytime, currently logs will be saved with no problem (Press Ctrl C in the console)
     
### 2.1.1  
- Show on console each interaction
  
# v2.1
- Now you can use your PC while AutoBuy is running  
- Your monitor resolution doesn't matter anymore  
- GUI to select paths and set the number of refreshes  
- Better crash handling
- Log improvement
  
## Get Started:  
1. Download AutoBuy latest version [Download](https://github.com/senkkou/E7AutoBuy/releases/download/2.5/AutoBuy.exe)  
2. Install Tesseract OCR [Download](https://github.com/UB-Mannheim/tesseract/wiki)  
3. Download and unzip platform-tools [Download](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)  
4. Make sure your game is in english  
5. Enable ADB on your emulator  
<details><summary>Enabling ADB</summary>  
  
Ldplayer  
![adb](https://user-images.githubusercontent.com/54269537/132781083-e40bd44b-e551-4b84-9da4-586aa519a937.png)  
  
Note: Some version of BlueStacks has ADB not working properly  
BlueStacks  
![adbbs](https://user-images.githubusercontent.com/54269537/132966725-813692ca-37f9-4cd6-8db5-c72796607455.png)  
  
  
</details>  
  
[Video tutorial](https://github.com/senkkou/E7AutoBuy#tutorial-and-demonstration)  
  
 ### How to use:  
1. Finish your dispatch mission or start long ones (So the window doesnt pop up during shop reroll).  
2. When starting for the first time AutoBuy will ask to select 2 .exe files
- tesserect.exe from Tesseract OCR
- adb.exe from platform-tools
3. Open secret shop screen before press the confirm button to start.
  
Now you can minimize your emulator and console window and freely use your PC while AutoBuy is running.  
When it finishes, a window will pop up and shows the results and a log file will be saved in AutoBuy directory.  
  
## Important  
***In config.ini there is a delay section, value is 1 by default, if you are using a PC with bad performance try to increase the delay to run it slowly.***  
  
  
### Tutorial and Demonstration  
  You can freely move my mouse and do other activities while AutoBuy is running, auto refreshing the shop and buying any covenant bookmarks and mystic medals that shows up there.  


https://user-images.githubusercontent.com/54269537/177623527-b84bbb64-0bb5-4ed0-8eca-9490e8fc050d.mp4

  
### Python and packages used to compile:  
- python 3.8.11  
- pytesseract 0.3.8  
- pillow 8.3.1  
  
  

<details><summary>v1.0 OLD</summary>  
  
## Get Started:  
1. Install Tesseract OCR https://github.com/UB-Mannheim/tesseract/wiki  
2. Open config.ini  
3. Make sure tesseractPath is the same you installed tesseract-ocr  
4. Make sure your game is in english  
  
### How to use:  
1. In config.ini set the number of refreshes you want AutoBuy to do, the number of skystones spent will be 3 times this value  
2. Delay = 1 is the default speed, if you are using a PC with bad performance try to increase the delay to run it slowly  
3. Use your emulator with maximized window (Like the images bellow) and it must be on your main monitor  
4. Finish your dispatch mission or start long ones. (So the window doesnt pop up during shop reroll)  
5. Change chat to a empty channel  
6. Start the program  
7. Open secret shop  
8. Confirm program window.  
  
Additional notes:  
It will only work if your screen resolution is in presets.ini, by default 1280x720, 1920x1080 and 2560x1080  
if you use any other resolution change to one of the three above or do your own configuration and write in the file.  
  
### Python and packages used to compile:  
- python 3.8.11  
- pytesseract 0.3.8  
- pillow 8.3.1  
- pyautogui 0.9.53  
  
 ### Setting Up your own resolution:  
 You can edit the presets.ini to add your own resolution, you just need to type for each variable the pixel's coordinates for you resolution.  
 Bellow are some images showing where you should be getting your cordinates from, for each variable.  
 
 Ps: cropubr in images were supose to be cropbr, but i'm too lazy to redo the screens.  
   
 <details><summary>Show Images</summary>  
  
Open up each image to see better the marked pixel  

![1](https://user-images.githubusercontent.com/54269537/131053834-5c2f2efb-09cc-44f0-8692-d1758e5252b7.png)  
  
![2](https://user-images.githubusercontent.com/54269537/131054917-0ba0246b-ad83-4f32-ad44-b41c0cd866a5.png)  
  
![3](https://user-images.githubusercontent.com/54269537/131054932-3c4f4c5e-1f61-4b22-80b9-d96fa14c02ad.png)  
   
![4](https://user-images.githubusercontent.com/54269537/131054955-8722a72b-cfa0-4246-92e9-0cc37cbd1db9.png)

</details>  
</details>  
  
## Warning  
For the first time, before you try it with a great number of rerolls, refresh it manually until a covenant or mystic shows up.  
Then set the number of reroll to something like 3 just to test if it is working fine.
