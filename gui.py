import numpy as np
from tkinter import *
from PIL import Image, ImageGrab, ImageOps
from win32gui import GetWindowRect
import tensorflow as tf

cnn = tf.keras.models.load_model('mnist.h5py')

intro_text = 'Please write\na digit on\nthe canvas'

def predicted_text(digit, accuracy):
    return 'Digit: {}\nAccuracy: {}%'.format(digit, str(int(accuracy*100)))

def predict(img):
    img = img.resize((28, 28))
    img = np.array(img.convert('L'))
    img.reshape(28, 28)
    img = img.reshape(1, 28, 28, 1)/255
    pred = cnn.predict(img)[0]
    return np.argmax(pred), max(pred)

def classify():
    hwnd = cv.winfo_id()
    cv_rect = GetWindowRect(hwnd)
    img = ImageGrab.grab(cv_rect)
    img = ImageOps.invert(img)

    digit, accuracy = predict(img)
    label.configure(text=predicted_text(digit, accuracy))
        
def clear():
    cv.delete('all')
    label.configure(text=intro_text)
    
def draw(event):
    x = event.x
    y = event.y
    r = 8
    cv.create_oval(x-r, y-r, x+r, y+r, fill='black')

root = Tk()

padding = 10

cv = Canvas(width=400, height=400, bg='white', cursor='cross')
cv.grid(row=0, column=0, padx=padding, sticky=W)

label = Label(text=intro_text, font=('Helvetica', 32))
label.grid(row=0, column=1, padx=(0, padding))

clear_button = Button(text='Clear', command=clear)
clear_button.grid(row=1, column=0)

recognize_button = Button(text='Recognize', command=classify)
recognize_button.grid(row=1, column=1)
        
cv.bind("<B1-Motion>", draw)

mainloop()
