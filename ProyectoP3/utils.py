import pyautogui as screen
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
import numpy as np
from scipy.integrate import quad

font_tittle = ("Poppins", 12, "bold")
font_text1 = ("Poppins", 10, "bold")
font_text = ("Cambria Math", 10, "bold")
font_entry = ("Cambria Math", 8)
font_btn = ("Poppins", 8, "bold")

orden_options = [1, 2]
type_options = ["Progresiva", "Centrada", "Regresiva"]
exact_options = ["Menor exactitud", "Mayor exactitud"]

type_options_int = ["Regla de Simpson 1/3", "Regla de Simpson 3/8"]
exact_options_int = ["Simple", "Compuesta"]
formulas_derivada = [
    ##Primera derivada
    [
    #Progresiva [menor, mayor]
    [r"${f(x_{i})}'=\frac{{f(x_{i+1})-f(x_{i})}}{h}$", r"${f(x_{i})}'= \frac{-{f(x_{i+2})}+4f(x_{i+1})-3f(x_{i})}{2h}$"],
    #Centrada [menor, mayor]
    [r"${f(x_{i})}'= \frac{f(x_{i+1})-f(x_{i-1}))}{2h}$", r"${f(x_{i})}'= \frac{-f(x_{i+2})+8f(x_{i+1})-8f(x_{i-1})+f(x_{i-2})}{12h}$"],
    #Reresiva [menor, mayor]
    [r"${f(x_{i})}'= \frac{f(x_{i})-f(x_{i-1})}{h}$", r"${f(x_{i})}'= \frac{3f(x_{i})-4f(x_{i-1})+f(x_{i-2})}{2h}$"]],
    ##Segunda derivada
    [
    #Progresiva [menor, mayor]
    [r"${f(x_{i})}''= \frac{f(x_{i+2})-2f(x_{i+1})+f(x_{i})}{h^{2}}$", r"${f(x_{i})}''= \frac{-f(x_{i+3})+4f(x_{i+2})-5f(x_{i+1})+2f(x_{i})}{h^{2}}$"], 
    #Centrada [menor, mayor]
    [r"${f(x_{i})}''= \frac{f(x_{i+1})-2f(x_{i})+f(x_{i-1})}{h^{2}}$", r"${f(x_{i})}''= \frac{-f(x_{i+2})+16f(x_{i+1})-30f(x_{i})+16f(x_{i-1})-f(x_{i-2})}{12h^{2}}$"],
    #Reresiva [menor, mayor]
    [r"${f(x_{i})}''= \frac{f(x_{i})-2f(x_{i-1})+f(x_{i-2})}{h^{2}}$", r"${f(x_{i})}''= \frac{2f(x_{i})-5f(x_{i-1})+4f(x_{i-2})-f(x_{i-3})}{h^{2}}$"]]
]
type_int_options = ["1/3", "3/8"]
exct_int_options = ["Simple", "Compuesta"]
formulas_integracion =[
    #1/3 [simple, compuesta]
    [r"$I = \int_{a}^{b}{f(x) dx} = h*\left [\frac{{f(x_{0})+ 4f(x_{1})+f(x_{2})}}{3}\right ]$", r"$I = \frac{h}{3} [f(x_0) + 2\sum_{j=1}^{(n/2)-1}f(x_{2j}) + 4\sum_{j=1}^{n/2}f(x_{2j-1}) + f(x_n)]$"],
    #3/8 [simple, compuesta]
    [r"$I = \frac{3h}{8}\left \{ f(a) + 3f(\frac{2a+b}{3}) + 3f(\frac{a+2b}{3}) + f(b)\right\}$", r"$I = \frac{3h}{8} [ (y_0 + y_n) + 3 \sum_{j=1}^{n-1} y_j + 2 \sum_{j=1}^{n/3-1} y_{3j} ]$"]
]

def start(frame):
    frame.title("Proyecto de unidad - Universidad de las Fuerzas Armadas ESPE")
    frame.resizable(False, False)
    frame.config(bg="black")
    window_width = 700
    window_height = 500
    width_screen, height_screen = screen.size()
    window_pos_width = (width_screen/2) - (window_width/2)
    window_pos_heigth = (height_screen/2) - (window_height/2)
    geometry = str(int(window_width)) + "x" + str(int(window_height))+"+"+str(int(window_pos_width)) + "+" + str(int(window_pos_heigth))
    frame.geometry(geometry)
    return frame

def convert_image(img_path, size) -> ImageTk.PhotoImage:
    img = Image.open(img_path)
    alpha = Image.new('L', img.size, 128)
    img.putalpha(alpha)
    img = img.resize((size[0],size[1]))
    return ImageTk.PhotoImage(img)

def convert_image_ico(img_path, size, bg_color=None)-> ImageTk.PhotoImage:
    img = Image.open(img_path)
    if bg_color:
        bg = Image.new('RGB', img.size, bg_color)
        bg.paste(img, mask=img.split()[-1])
        img = bg
    img = img.resize((size[0],size[1]))
    return ImageTk.PhotoImage(img)

def Labels(frame, type, string, place=(0,0)):
    label = tk.Label(frame)
    color=frame.cget("bg")
    if type == "tittle":
        font = font_tittle
    elif type == "text":
        font = font_text
    elif type == "text1":
        font = font_text1
    label.configure(text=string, font=font, fg="black", bg=color)
    label.place(x=place[0], y=place[1], height= 16)
    return label

def Entries(frame, place=(0,0), dim=(0,0)):
    entry = tk.Entry(frame)
    entry.configure(font=font_entry, fg="black", bg="#E4ECF4")
    entry.place(x=place[0], y=place[1], width=dim[0], height=dim[1])
    return entry

def Buttons(frame, place=(0,0), dim=(0,0)):
    button = tk.Button(frame, text="Calcular", font=font_btn, fg="black", bg="#D9D3CF", anchor="center", compound="center", bd=0)
    button.place(x=place[0], y=place[1], width=dim[0], height=dim[1])
    return button

class EquationImage(tk.Frame):
    def __init__(self, latex_string, image_size, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.latex_string = latex_string
        self.image_size = image_size
        self.create_image()

    def create_image(self):
        fig = Figure(figsize=(self.image_size[0] / 100, self.image_size[1] / 100), dpi=100)
        ax = fig.add_subplot(111)
        if len(self.latex_string) > 80:
            ax.text(0.5, 0.5, self.latex_string, fontsize=10, ha='center', va='center')
        elif len(self.latex_string) > 100:
            ax.text(0.5, 0.5, self.latex_string, fontsize=8, ha='center', va='center')
        else:
            ax.text(0.5, 0.5, self.latex_string, fontsize=12, ha='center', va='center')
        ax.axis('off')
        buf = io.BytesIO()
        canvas = FigureCanvasAgg(fig)
        canvas.print_png(buf)
        buf.seek(0)
        img = tk.PhotoImage(data=buf.getvalue())
        self.image = img
        self.label = tk.Label(self, image=self.image)
        self.label.pack()

#IMPLEMENTACION DERIVADAS
##PRIMERA DERIVADA
#PROGRESIVA
def derivada_progresiva_1(x, y, value, ax):
    h=x[1]-x[0]
    def derivada_progresiva(x, y, h):
        n = len(x)
        f_derivada = []
        for i in range(n-2):
            f_d = (-3*y[i] + 4*y[i+1] - y[i+2]) / (2*h)
            f_derivada.append(f_d)
        return f_derivada

    ax.clear()
    f_d = derivada_progresiva(x, y, h)
    dim = len(f_d)
    ax.plot(x, y, label="Función original")
    ax.plot(value, y[x.index(value)], 'ro', label="Punto seleccionado")
    ax.plot(x[:dim], f_d[:dim], 'o-', label="Primera derivada")
    ax.legend()
    return f_d, ax

#CENTRADA
def derivada_centrada_1(x, y, value, ax) :
    h=x[1]-x[0]
    def derivada_centrada(xi, yi, h):
        n=np.size(xi)
        h=xi[1]-xi[0]
        deriv=np.zeros(n)
        deriv[0]=(yi[1]-yi[0])/h
        for i in range(1,n-1) :
            deriv[i]=(yi[i+1]-yi[i-1])/(2*h)
            deriv[n-1]=(yi[n-1]-yi[n-2])/h
        return deriv
    ax.clear()
    derivada = derivada_centrada(x, y, h)
    dim = len(derivada)
    ax.plot(x, y, label="Función original")
    ax.plot(value, y[x.index(value)], 'ro', label="Punto seleccionado")
    ax.plot(x[:dim], derivada[:dim], 'o-', label="Segunda derivada")
    ax.legend()
    return derivada, ax

#REGRESIVA
def derivada_regresiva_1(x,y,value,ax):
    h=x[1]-x[0]
    def derivada_regresiva(x ,y, h):
        N = len(x)
        dy = np.zeros(N)
        for k in range(1,N -1):
            dy[k] = (y[k] - y[k-1])/h
        return dy
    ax.clear()
    derivada = derivada_regresiva(x, y, h)
    dim = len(derivada)
    ax.plot(x, y, label="Función original")
    ax.plot(value, y[x.index(value)], 'ro', label="Punto seleccionado")
    ax.plot(x[:dim], derivada[:dim], 'o-', label="Segunda derivada")
    ax.legend()
    return derivada, ax

##SEGUNDA DERIVADA
#PROGRESIVA
def derivada_progresiva_2(x, y, x_eval, ax):
    h=x[1]-x[0]
    def derivada_progresiva(x, y, h):
        n = len(x)
        fpp = []
        for i in range(n-3):
            fp = (-y[i+3] + 4*y[i+2] - 5*y[i+1] + 2*y[i]) / (h**2)
            fpp.append(fp)
        return fpp
    ax.clear()
    derivada = derivada_progresiva(x, y, h)
    dim = len(derivada)
    ax.plot(x, y, label="Función original")
    ax.plot(x_eval, y[x.index(x_eval)], 'ro', label="Punto seleccionado")
    ax.plot(x[:dim], derivada[:dim], 'o-', label="Segunda derivada")
    ax.legend()
    return derivada, ax
    
#CENTRADA
def derivada_centrada_2(x, y, value, ax) :
    h=x[1]-x[0]
    def derivada_centrada(xi, yi, h):
        n=len(xi)
        deriv=np.zeros(n)
        deriv[0]=(yi[2]-2*yi[1]+yi[0])/(h**2)
        for i in range(1,n-1) :
            deriv[i]=(yi[i+1]-2*yi[i]+yi[i-1])/(h**2)
            deriv[n-1]=(yi[n-1]-2*yi[n-2]+yi[n-3])/(h**2)
        return deriv
    ax.clear()
    derivada = derivada_centrada(x, y, h)
    dim = len(derivada)
    ax.plot(x, y, label="Función original")
    ax.plot(value, y[x.index(value)], 'ro', label="Punto seleccionado")
    ax.plot(x[:dim], derivada[:dim], 'o-', label="Segunda derivada")
    ax.legend()
    return derivada, ax

#REGRESIVA
def derivada_regresiva_2(x,y,value,ax):
    h=x[1]-x[0]
    def derivada_regresiva(x ,y, h):
        N = len(x)
        dy = np.zeros(N)
        for k in range(1,N-1):
            dy[k] = (y[k] - 2*y[k-1]+y[k-2])/(h*h)
        return dy
    ax.clear()
    derivada = derivada_regresiva(x, y, h)
    dim = len(derivada)
    ax.plot(x, y, label="Función original")
    ax.plot(value, y[x.index(value)], 'ro', label="Punto seleccionado")
    ax.plot(x[:dim], derivada[:dim], 'o-', label="Segunda derivada")
    ax.legend()
    return derivada, ax

##INTEGRACION
#1/3
#SIMPLE
def integral_13s(x,y,a,b,ax):
    n = len(x) - 1
    def simpson(y,a,b):
        suma = 0
        for i in range(1,n):
            if i%2 == 0:
                suma = suma + 2*y[i]
            else:
                suma = suma + 4*y[i]
        suma = suma + y[0] + y[n]
        area = (b-a)*suma/(3*n)
        return area
    area = simpson(y,a,b)
    ax.clear()
    ax.plot(x, y, 'go-',label="Función original")
    indexA = x.index(a)
    indexB = x.index(b)
    X = [a,b]
    Y = [y[indexA],y[indexB]]
    ax.fill_between(X, [0,0], Y, color='orange')
    ax.legend()
    ax = Lagrange_interpolation(x, y, ax)
    return area, ax

#COMPUESTA
def integral_13c(x,y,a,b,ax):
    def simpson(x, y,a,b):
        if len(x) % 2 != 0:
            raise ValueError("La lista de puntos debe tener un número par de elementos.")
        h = (b - a) / (len(x) - 1)
        integral = y[0] + y[-1]
        for i in range(1, len(x) - 1):
            if i % 2 == 0:
                integral += 2 * y[i]
            else:
                integral += 4 * y[i]
        integral *= h / 3
        return integral
    area = simpson(x,y,a,b)
    ax.clear()
    ax.plot(x, y, 'go-',label="Función original")
    indexA = x.index(a)
    indexB = x.index(b)
    X = [a,b]
    Y = [y[indexA],y[indexB]]
    ax.fill_between(X, [0,0], Y, color='orange')
    ax.legend()
    ax = Lagrange_interpolation(x, y, ax)
    return area, ax

#3/8
#SIMPLE
def integral_38s(x,y,a,b,ax):
    n = len(x) - 1
    def simpson(y,a,b):
        suma = 0
        for i in range(1,n):
            if i%2 == 0:
                suma = suma + 2*y[i]
            else:
                suma = suma + 4*y[i]
        suma = suma + y[0] + y[n]
        area = (b-a)*suma/(3*n)
        return area
    area = simpson(y,a,b)
    ax.clear()
    ax.plot(x, y, 'go-',label="Función original")
    indexA = x.index(a)
    indexB = x.index(b)
    X = [a,b]
    Y = [y[indexA],y[indexB]]
    ax.fill_between(X, [0,0], Y, color='orange')
    ax.legend()
    ax = Lagrange_interpolation(x, y, ax)
    return area, ax

#Interpolacion
def Lagrange_interpolation(points, values, ax):
    def interpolar(points, values, x):
        n = len(points)
        Px = 0
        for i in range(n):
            Li = 1
            for j in range(n):
                if i != j:
                    Li *= (x - points[j])/(points[i] - points[j])
            Px += Li * values[i]
        return Px
    x_min = min(points)*0.8
    x_max = max(points)*1.01
    x = np.linspace(x_min, x_max, 100)
    y = []
    for i in x:
        y.append(interpolar(points, values, i))
    ax.plot(x, y)
    return ax
##EJEMPLOS
#x = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
#y = np.array([0.0, 0.1987, 0.3894, 0.5646, 0.7174, 0.8415])
#x = np.array([1, 1.01, 1.02, 1.03, 1.04])
#y = np.array([3.1, 3.12, 3.14, 3.18, 3.24])
