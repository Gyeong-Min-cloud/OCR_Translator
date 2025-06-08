# OCR_Translator
This is a real-time translation program using OCR

<br/>

## Contents

1. [what is this program](#what-is-this-program)
2. [how to use the program](#how-to-use-the-program)
    1. image
    2. video
3. [limitations of the program](#limitations-of-the-program)
4. [Reference](#Reference)
5. [License](#License)

<br/>

## what is this program

- This is the program that recognizes texts through the OCR function and translates them into Korean 
- If you want to use this program, you need to download the package below.

<br/>

```bash
pip install pytesseract deep-translator tkinterdnd2 opencv-python pillow
```
<br/>  

- In addition to the package, you need to download the Tesseract OCR. This program can't operate with the pip command alone, so a separate download is required.

![사진1](https://github.com/user-attachments/assets/a2f6d78c-ab98-40a0-95a3-5fae9c056ab3)

- Here's a link to download the Tesseract OCR

<br/>

https://github.com/UB-Mannheim/tesseract/wiki

<br/>

## how to use the program



### image



https://github.com/user-attachments/assets/17163097-7b90-4c53-9b4c-272ec7171427

- When you start the program, a Drag-and-Drop Window occurs. When you drop the desired image file into the window, the image will fit according to the size of the window. After that, draw a box so that the desired word can be entered, and press the Enter key to see the words translated into Korean below. Pressing the esc key ends the window.

<br/>
<br/>

### video



https://github.com/user-attachments/assets/fd0f83b6-97b8-41e2-81c5-9cb14d98344d

- When you start the program, a Drag-and-Drop Window occurs. When you drop a video file you want in the window, the video goes in according to the size of the window. The video plays automatically. When you press the space bar in the frame where the word you want comes out, the video stops. After that, draw a box so that the desired word can be entered, and press the Enter key to see the words translated into Korean below. If you press the space bar again, the video plays again. Pressing the esc key ends the window.

<br/>
<br/>

## limitations of the program

<br/>

- The quality of an image or video determines the performance of the program
- Since the translation function of the program relies on deep-translator, errors may occur in the translation itself
- To recognize words, you might need to draw boxes multiple times


<br/>
<br/>

## Reference
- [ChatGPT](https://chatgpt.com/)
- [tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)

<br/>
<br/>

## License

<br/>

- MIT License
