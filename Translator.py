import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import cv2
import numpy as np
from deep_translator import GoogleTranslator
import pytesseract
import threading

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

translator = GoogleTranslator(source='en', target='ko')

img = None
tk_img = None
rect_start = None
rect_id = None
rect_coords = None
translated_text = ''
video_path = None
video_cap = None
video_running = False
current_frame = None

def translate_roi(roi):
    global translated_text
    text = pytesseract.image_to_string(roi, lang='eng')
    print(f"Detected Text: {text.strip()}")
    if text.strip():
        try:
            translated_text = translator.translate(text.strip())
            print(f"Translated Text: {translated_text}")
        except Exception as e:
            translated_text = f"Translation error: {e}"
    else:
        translated_text = 'No text detected'
    translated_label.config(text=translated_text)

def resize_image(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def load_image(path):
    global img, tk_img, rect_id, rect_coords, translated_text, video_cap, video_running

    if video_cap:
        video_cap.release()
        video_cap = None
        video_running = False

    img_bgr = cv2.imread(path)
    if img_bgr is None:
        print("Failed to load image.")
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_rgb = resize_image(img_rgb, canvas.winfo_width(), canvas.winfo_height())
    img = img_rgb

    show_image(img)

def show_image(image):
    global tk_img
    img_pil = Image.fromarray(image)
    tk_img = ImageTk.PhotoImage(img_pil)
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_img)

def on_button_press(event):
    global rect_start, rect_id
    rect_start = (event.x, event.y)
    if rect_id:
        canvas.delete(rect_id)
    rect_id = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='green', width=2)

def on_mouse_move(event):
    if rect_start and rect_id:
        canvas.coords(rect_id, rect_start[0], rect_start[1], event.x, event.y)

def on_button_release(event):
    global rect_coords
    if rect_id:
        rect_coords = canvas.coords(rect_id)
        print("Selected rect coords:", rect_coords)

def perform_ocr():
    global rect_coords, img
    if rect_coords and img is not None:
        x1, y1, x2, y2 = map(int, rect_coords)
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        h, w, _ = img.shape
        x1 = max(0, min(x1, w - 1))
        x2 = max(0, min(x2, w - 1))
        y1 = max(0, min(y1, h - 1))
        y2 = max(0, min(y2, h - 1))

        if x2 - x1 > 0 and y2 - y1 > 0:
            roi = img[y1:y2, x1:x2]
            threading.Thread(target=translate_roi, args=(roi,), daemon=True).start()
        else:
            print("Invalid ROI selected.")

def on_key_press(event):
    global video_running

    if event.keysym == 'Return':
        perform_ocr()
    elif event.keysym == 'Escape':
        root.destroy()
    elif event.keysym == 'space':
        video_running = not video_running

def drop(event):
    global video_path, video_cap, video_running
    filepath = event.data.strip('{}')
    print(f"Loading file: {filepath}")
    if filepath.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        video_path = filepath
        video_cap = cv2.VideoCapture(video_path)
        video_running = True
        play_video()
    else:
        load_image(filepath)

def play_video():
    global video_cap, video_running, img, current_frame, rect_coords, rect_id

    if not video_cap:
        return

    if video_running:
        ret, frame = video_cap.read()
        if not ret:
            
            video_running = False
            video_cap.release()
            video_cap = None
            canvas.delete("all")
            canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill="black")
            translated_label.config(text='')
            rect_coords = None
            if rect_id:
                canvas.delete(rect_id)
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = resize_image(frame_rgb, canvas.winfo_width(), canvas.winfo_height())
        img = frame_rgb
        current_frame = frame_rgb
        show_image(frame_rgb)

    root.after(30, play_video)


root = TkinterDnD.Tk()
root.title('Drag & Drop Video/Image OCR Translator')
root.geometry('800x600')

canvas = tk.Canvas(root, width=800, height=480, bg='black')
canvas.pack()

translated_label = tk.Label(root, text="", font=("Arial", 16), bg="white", height=4, anchor='nw', justify='left', wraplength=780)
translated_label.pack(fill="x")

canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<Drop>>', drop)

canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_mouse_move)
canvas.bind("<ButtonRelease-1>", on_button_release)
root.bind("<Key>", on_key_press)

root.mainloop()
