import tkinter as tk
import utils as cg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import ttk
import numpy as np
import tkinter.messagebox as msg

bg_img = None
menu_img = None
menu_r_img = None
reload_img = None
current_frame = None

class Head(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(width=700, height=100, bg="#1D1C1D")
        self.place(x=0,y=0)
        self.label = tk.Label(self)
        self.label.configure(text="Métodos Numéricos", font=("Corinthia", 60), fg="white", bg="#1D1C1D")
        self.label.place(relx=0.5, rely=0.5, anchor="center")

class BaseFrame(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(width=700, height=400, bg="white")
        bg_img = cg.convert_image("ProyectoP3\\img\\logo.png", (303, 274))
        self.img = bg_img
        self.background = tk.Label(self, image=self.img, bg="white")
        self.background.place(relx=0.5, rely=0.5, anchor="center")
        self.label = tk.Label(self)
        self.label.configure(text="Seleccione una opción", font=("Poppins", 16, "bold"), fg="black", bg="white", state="normal")
        self.label.place(relx=0.5, rely=0.05, anchor="center")
        reload_img = cg.convert_image_ico("ProyectoP3\\img\\reload.png", (30, 30), "#FFFFFF")
        self.img = reload_img
        self.btn_reload = tk.Button(self, image=self.img, bd=0)
        self.btn_reload.place(x=660, y=10, width=30, height=30)

class DerivadaFrame(BaseFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.label.configure(text="Derivación numérica")
        self.label.place(relx=0.5, rely=0.05, anchor="center")
        cg.Labels(self, "text1", "Tipo de fórmula:", (38,84))
        #Control combobox
        def combo_control(event):
            orden = combo_derivada.current()
            tipo = combo_tipo.current()
            exct = combo_exactitud.current()
            formula = ""
            if orden != -1 and tipo != -1 and exct != -1:
                formula = cg.formulas_derivada[orden][tipo][exct]
            eq = cg.EquationImage(formula, (330,40), master=self)
            eq.place(x=15, y=185)
        combo_tipo = ttk.Combobox(self, values=cg.type_options, state="readonly")
        combo_tipo.configure(font=cg.font_text, foreground="black", background="white")
        combo_tipo.place(x=200, y=84-5, width=130, height=30)
        combo_tipo.bind("<<ComboboxSelected>>", combo_control)
        cg.Labels(self, "text1", "Orden derivada", (38,121))
        combo_derivada = ttk.Combobox(self, values=cg.orden_options, state="readonly")
        combo_derivada.configure(font=cg.font_text, foreground="black", background="white")
        combo_derivada.place(x=200, y=121-5, width=130, height=30)
        combo_derivada.bind("<<ComboboxSelected>>", combo_control)
        cg.Labels(self, "text1", "Exactitud", (38,158))
        combo_exactitud = ttk.Combobox(self, values=cg.exact_options, state="readonly")
        combo_exactitud.configure(font=cg.font_text, foreground="black", background="white")
        combo_exactitud.place(x=200, y=158-5, width=130, height=30)
        combo_exactitud.bind("<<ComboboxSelected>>", combo_control)
        cg.Labels(self, "text1", "Gráfica", (487, 42))
        grafica_frame = tk.Frame(self, width=300, height=300)
        grafica_frame.place(x=366, y=63)
        fig = Figure()
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=grafica_frame)
        canvas.get_tk_widget().place(x=0, y=0, width=300, height=270)
        toolbar = NavigationToolbar2Tk(canvas, grafica_frame)
        toolbar.update()
        toolbar.place(relx=0.5, rely=0.95, relwidth=1, relheight=0.1, anchor='center')
        cg.Labels(self, "text", "x:", (56, 239))
        txt_x0 = cg.Entries(self, (81, 234), (30,25))
        txt_x1 = cg.Entries(self, (120, 234), (30,25))
        txt_x2 = cg.Entries(self, (159, 234), (30,25))
        txt_x3 = cg.Entries(self, (198, 234), (30,25))
        txt_x4 = cg.Entries(self, (237, 234), (30,25))
        txt_x5 = cg.Entries(self, (276, 234), (30,25))
        cg.Labels(self, "text", "f(x):", (50, 274))
        txt_fx0 = cg.Entries(self, (81, 269), (30,25))
        txt_fx1 = cg.Entries(self, (120, 269), (30,25))
        txt_fx2 = cg.Entries(self, (159, 269), (30,25))
        txt_fx3 = cg.Entries(self, (198, 269), (30,25))
        txt_fx4 = cg.Entries(self, (237, 269), (30,25))
        txt_fx5 = cg.Entries(self, (276, 269), (30,25))
        cg.Labels(self, "text", "Evaluar en:", (160, 312))
        txt_eval = cg.Entries(self, (237,309), (30,20))
        cg.Labels(self, "text", "Resultado:", (421, 373))
        resultado = tk.StringVar()
        lbl_resultado = cg.Labels(self, "text", "", (500, 373))
        lbl_resultado.configure(textvariable=resultado.set(""), state="disabled")
        btn_calcular = cg.Buttons(self, (156, 350), (70,30))
        btn_calcular.configure(command=lambda: calcular(ax))

        def calcular(ax):
            try:
                orden = combo_derivada.current()
                tipo = combo_tipo.current()
                exct = combo_exactitud.current()
                x = [
                    float(txt_x0.get()),
                    float(txt_x1.get()),
                    float(txt_x2.get()),
                    float(txt_x3.get()),
                    float(txt_x4.get()),
                    float(txt_x5.get())
                ]
                y= [
                    float(txt_fx0.get()),
                    float(txt_fx1.get()),
                    float(txt_fx2.get()),
                    float(txt_fx3.get()),
                    float(txt_fx4.get()),
                    float(txt_fx5.get())
                ]
                if orden == 0 and tipo == 0 and exct == 1:
                    #Progresiva 1 Mayor
                    x_eval = float(txt_eval.get())
                    derivada, ax = cg.derivada_progresiva_1(x,y, x_eval, ax)
                    index = x.index(x_eval)
                    resultado.set(round(derivada[index],6))
                    lbl_resultado.configure(textvariable=resultado)
                    ax.plot([x[index], y[index]],[x[index],derivada[index]], linestyle='--', color='green')
                    canvas.draw()
                elif orden == 1 and tipo == 0 and exct == 1:
                    #Progresiva 2 Mayor
                    x_eval = float(txt_eval.get())
                    derivada, ax = cg.derivada_progresiva_2(x,y, x_eval, ax)
                    index = x.index(x_eval)
                    resultado.set(round(derivada[index],6))
                    lbl_resultado.configure(textvariable=resultado)
                    ax.plot([x[index], y[index]],[x[index],derivada[index]], linestyle='--', color='green')
                    canvas.draw()
                elif orden == 0 and tipo == 1 and exct == 0:
                    #Centrada 1 menor
                    x_eval = float(txt_eval.get())
                    derivada, ax = cg.derivada_centrada_1(x, y, x_eval, ax)
                    index = x.index(x_eval)
                    resultado.set(round(derivada[index],6))
                    lbl_resultado.configure(textvariable=resultado)
                    canvas.draw()
                elif orden == 1 and tipo == 1 and exct == 0:
                    #Centrada 2 menor
                    x_eval = float(txt_eval.get())
                    derivada, ax = cg.derivada_centrada_2(x, y, x_eval, ax)
                    index = x.index(x_eval)
                    resultado.set(round(derivada[index],6))
                    lbl_resultado.configure(textvariable=resultado)
                    canvas.draw()
                elif orden == 0 and tipo == 2 and exct == 0:
                    #Regresiva 1 menor
                    x_eval = float(txt_eval.get())
                    derivada, ax = cg.derivada_regresiva_1(x,y, x_eval, ax)
                    index = x.index(x_eval)
                    resultado.set(round(derivada[index],6))
                    lbl_resultado.configure(textvariable=resultado)
                    canvas.draw()
                elif orden == 1 and tipo == 2 and exct == 0:
                    #Regresiva 2 menor
                    x_eval = float(txt_eval.get())
                    derivada, ax = cg.derivada_regresiva_2(x,y, x_eval, ax)
                    index = x.index(x_eval)
                    resultado.set(round(derivada[index],6))
                    lbl_resultado.configure(textvariable=resultado)
                    canvas.draw()
                else:
                    msg.showerror("Error", f"Error: Método no implementado")
            except Exception as e:
                msg.showerror("Error", f"Error: {e.args[0]}")
                return

        self.btn_reload.configure(command=lambda: reload())
        def reload():
            self.destroy()
            derivada_frame = DerivadaFrame(master)
            derivada_frame.place(x=0, y=100)
            pass

class IntegracionFrame(BaseFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.label.configure(text="Integración numérica")
        #Control combobox
        def combo_control(event):
            tipo = combo_tipo.current()
            exct = combo_exactitud.current()
            formula = ""
            if tipo != -1 and exct != -1:
                formula = cg.formulas_integracion[tipo][exct]
            eq = cg.EquationImage(formula, (330,45), master=self)
            eq.place(x=15, y=170-20)
        cg.Labels(self, "text1", "Regla de Simpson:", (45,94))
        combo_tipo = ttk.Combobox(self, values=cg.type_options_int, state="readonly")
        combo_tipo.configure(font=cg.font_text, foreground="black", background="white")
        combo_tipo.place(x=200, y=94-5, width=130, height=30)
        combo_tipo.bind("<<ComboboxSelected>>", combo_control)
        cg.Labels(self, "text1", "Exactitud", (45,129))
        combo_exactitud = ttk.Combobox(self, values=cg.exact_options_int, state="readonly")
        combo_exactitud.configure(font=cg.font_text, foreground="black", background="white")
        combo_exactitud.place(x=200, y=129-5, width=130, height=30)
        combo_exactitud.bind("<<ComboboxSelected>>", combo_control)
        cg.Labels(self, "text1", "Gráfica", (487, 42-20))
        grafica_frame = tk.Frame(self, width=300, height=300)
        grafica_frame.place(x=366, y=63)
        fig = Figure()
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=grafica_frame)
        canvas.get_tk_widget().place(x=0, y=0, width=300, height=270)
        toolbar = NavigationToolbar2Tk(canvas, grafica_frame)
        toolbar.update()
        toolbar.place(relx=0.5, rely=0.95, relwidth=1, relheight=0.1, anchor='center')
        cg.Labels(self, "text", "x:", (56, 215))
        txt_x0 = cg.Entries(self, (81, 210), (30,25))
        txt_x1 = cg.Entries(self, (120, 210), (30,25))
        txt_x2 = cg.Entries(self, (159, 210), (30,25))
        txt_x3 = cg.Entries(self, (198, 210), (30,25))
        txt_x4 = cg.Entries(self, (237, 210), (30,25))
        txt_x5 = cg.Entries(self, (276, 210), (30,25))
        cg.Labels(self, "text", "f(x):", (50-5, 250))
        txt_fx0 = cg.Entries(self, (81, 245), (30,25))
        txt_fx1 = cg.Entries(self, (120, 245), (30,25))
        txt_fx2 = cg.Entries(self, (159, 245), (30,25))
        txt_fx3 = cg.Entries(self, (198, 245), (30,25))
        txt_fx4 = cg.Entries(self, (237, 245), (30,25))
        txt_fx5 = cg.Entries(self, (276, 245), (30,25))
        cg.Labels(self, "text", "Limite inferior:", (67-35, 288))
        txt_a = cg.Entries(self, (137,284), (30,20))
        cg.Labels(self, "text", "Limite superior:", (189-10, 288))
        txt_b = cg.Entries(self, (262+30,284), (30,20))
        cg.Labels(self, "text", "Resultado:", (421, 373))
        resultado = tk.StringVar()
        lbl_resultado = cg.Labels(self, "text", "", (500, 373))
        lbl_resultado.configure(textvariable=resultado.set(""), state="disabled")
        btn_calcular = cg.Buttons(self, (150, 338), (70,30))
        btn_calcular.configure(command=lambda: calcular(ax))
        def calcular(ax):
            try:
                tipo = combo_tipo.current()
                exct = combo_exactitud.current()
                x = [
                    float(txt_x0.get()),
                    float(txt_x1.get()),
                    float(txt_x2.get()),
                    float(txt_x3.get()),
                    float(txt_x4.get()),
                    float(txt_x5.get())
                ]
                y= [
                    float(txt_fx0.get()),
                    float(txt_fx1.get()),
                    float(txt_fx2.get()),
                    float(txt_fx3.get()),
                    float(txt_fx4.get()),
                    float(txt_fx5.get())
                ]
                a = float(txt_a.get())
                b = float(txt_b.get())
                if tipo == 0 and exct == 0:
                    #1/3 SIMPLE
                    integral, ax = cg.integral_13s(x,y,a,b,ax)
                    resultado.set(round(integral,6))
                    lbl_resultado.configure(textvariable=resultado)
                    canvas.draw()
                elif tipo == 0 and exct == 1:
                    #1/3 COMPUESTA
                    integral, ax = cg.integral_13c(x,y,a,b,ax)
                    resultado.set(round(integral,6))
                    lbl_resultado.configure(textvariable=resultado)
                    canvas.draw()
                elif tipo == 1 and exct == 0:
                    #3/8 SIMPLE
                    integral, ax = cg.integral_38s(x,y,a,b,ax)
                    resultado.set(round(integral,6))
                    lbl_resultado.configure(textvariable=resultado)
                    canvas.draw()
                else:
                    msg.showerror("Error", f"Error: Método no implementado")
            except Exception as e:
                msg.showerror("Error", f"Error: {e.args[0]}")
                return
    
        self.btn_reload.configure(command=lambda: reload())
        def reload():
            self.destroy()
            integracion_frame = IntegracionFrame(master)
            integracion_frame.place(x=0, y=100)
            pass

class EDOFrame(BaseFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.label.configure(text="Ecuaciones Diferenciales Ordinarias")
        self.btn_reload.configure(command=lambda: reload())
        
        msg.showerror("Error", f"Error: Método no implementado")
        self.destroy()

        self.base = BaseFrame(master).place(x=0, y=100)

        def reload():
            self.destroy()
            op3_frame = EDOFrame(master)
            op3_frame.place(x=0, y=100)
            pass

def generate_graphics():
    global current_frame
    window = tk.Tk()
    window = cg.start(window)

    head_frame = Head(window)
    head_frame.place(x=0, y=0)

    body_frame = BaseFrame(window)
    body_frame.place(x=0, y=100)
    current_frame = body_frame

    menu_img = cg.convert_image_ico("ProyectoP3\\img\\menu.png", (20,20), "#a30f09")
    menu_r_img = cg.convert_image_ico("ProyectoP3\\img\\menu_r.png", (20,20), "#292828")

    menu_frame = tk.Frame(window)
    menu_frame.configure(width=150, height=25, bg="#a30f09")
    menu_frame.place(x=0, y=75)
    bgn = menu_frame.cget("bg")
    pressed = False

    menu_button = tk.Button(menu_frame, image=menu_img, compound="right", anchor="center", padx=20, activeforeground="white", activebackground=bgn, command=lambda: on_press() if not pressed else on_release())
    menu_button.configure(text="Menu", font=("Poppins", 12), fg="white", bg="#a30f09", bd=0)
    menu_button.place(x=0, y=0, width=150, height=25)

    menu_derivada = tk.Button(menu_frame, activeforeground="white", activebackground="#1D1C1D", command=lambda:derivacion_option())
    menu_derivada.configure(text="Derivación", font=("Poppins", 12), anchor="w", padx=5, fg="white", bg="#292828", bd=0)
    menu_derivada.place(x=0, y=25, width=150, height=25)

    menu_integracion = tk.Button(menu_frame, activeforeground="white", activebackground="#1D1C1D", command=lambda:integracion_option())
    menu_integracion.configure(text="Integración", font=("Poppins", 12), anchor="w", padx=5, fg="white", bg="#292828", bd=0)
    menu_integracion.place(x=0, y=51, width=150, height=25)

    menu_op3 = tk.Button(menu_frame, activeforeground="white", activebackground="#1D1C1D", command=lambda:op3_option())
    menu_op3.configure(text="EDO", font=("Poppins", 12), anchor="w", padx=5, fg="white", bg="#292828", bd=0)
    menu_op3.place(x=0, y=77, width=150, height=25)

    def on_press():
        nonlocal pressed
        pressed = True
        menu_button.configure(image=menu_r_img, fg="white", bg="#292828")
        menu_frame.configure(width=150, height=100)
        menu_frame.tkraise()
    
    def on_release():
        nonlocal pressed
        pressed = False
        menu_button.configure(image=menu_img, fg="white", bg="#a30f09")
        menu_frame.configure(width=150, height=25)

    def derivacion_option():
        global current_frame
        on_release()
        if current_frame:
            current_frame.destroy()
        derivada_frame = DerivadaFrame(window)
        derivada_frame.place(x=0, y=100)
        current_frame = derivada_frame

    def integracion_option():
        global current_frame
        on_release()
        if current_frame:
            current_frame.destroy()
        integral_frame = IntegracionFrame(window)
        integral_frame.place(x=0, y=100)
        current_frame = integral_frame

    def op3_option():
        global current_frame
        on_release()
        if current_frame:
            current_frame.destroy()
        EDO_frame = EDOFrame(window)
        EDO_frame.place(x=0, y=100)
        current_frame = EDO_frame
    
    window.mainloop()

generate_graphics()