import os.path
import tkinter as tk
from tkinter.ttk import Label, Combobox

from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
# import glob
from model_predection import m1_pred # model 1
from model_2 import fun_main  # model 2
from model_3 import lstm_pre # model 3

import glob


class App:
    def __init__(self, window, window_title, file_name):
        self.window = window
        # self.window.attributes('-fullscreen', True)
        self.window.title(window_title)
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (self.width, self.height))
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.company_csv_path = f'csv'
        self.login_status = False
        self.dic = {}
        self.clear_fun()
        # lis = os.listdir('img')
        # for a in lis:
        #     a.re

        self.create_widgets()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()

    def submit_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "user" and password == "password":
            self.login_status = True
            self.clear_frame()
            self.create_widgets()
            return True

        else:
            print('false')
            self.password_entry = tk.Entry(self.window, show="*")
            self.password_entry.place(x=self.width * 0.4225, y=int(self.height * 0.4502))
            self.username_entry = tk.Entry(self.window)
            self.username_entry.place(x=self.width * 0.4225, y=int(self.height * 0.4002))

            password_label = tk.Label(self.window, text="User name and Password incorrect", height=2, fg='red')
            password_label.place(x=self.width * 0.3325, y=int(self.height * 0.2502))

            self.login_status = False

            return False

    def create_login_widgets(self):
        self.username_label = tk.Label(self.window, text="Username:")
        self.username_label.place(x=self.width * 0.3225, y=int(self.height * 0.4002))
        self.username_entry = tk.Entry(self.window)
        self.username_entry.place(x=self.width * 0.4225, y=int(self.height * 0.4002))

        self.password_label = tk.Label(self.window, text="Password:")
        self.password_label.place(x=self.width * 0.3225, y=int(self.height * 0.4502))

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.place(x=self.width * 0.4225, y=int(self.height * 0.4502))

        self.submit_button = tk.Button(self.window, text="Submit", command=self.submit_login)
        self.submit_button.place(x=self.width * 0.4225, y=int(self.height * 0.5002))

        btn4 = tk.Button(self.window, text='Exit',
                         command=self.window.destroy)
        btn4.place(x=self.width * 0.4825, y=int(self.height * 0.5002))

    def create_widgets(self):
        if self.login_status == False:
            self.create_login_widgets()
        else:
            pass

            # companies = glob.glob(f'{self.company_csv_path}/*.csv')
            companies = os.listdir(self.company_csv_path)
            # print(companies)

            options = [company.split('/')[-1].split('.')[0] for company in companies]
            self.company_names = options
            print(self.company_names)
            # print()

            options_model = [
                "FB-Prophet Linear Model",
                "LSTM",
                "FB-Prophet Logistic Model",
            ]

            options_int = ['10', '20', '30', '40', '50']
            # options_int = [f"{i+1}" for i in range(50)]

            self.btn2 = tk.Button(self.window, text='Choose Compnrs', font=("bold", 12), width=20, height=2,
                                  command=self.choose_fun)
            self.btn2.place(x=self.width * 0.4225, y=int(self.height * 0.1002))

            self.clear_history = tk.Button(self.window, text='Clear History', font=("bold", 12), width=15, height=3,
                                           command=self.clear_fun)
            self.clear_history.place(x=self.width * 0.0225, y=int(self.height * 0.79922))

            # btn3 = tk.Button(self.window, text='Chosse The Number', font=("bold", 12),  width=20, height=2,
            # command=self.choose_number) btn3.place(x=int(self.width * 0.4225), y=int(self.height * 0.2002))

            label_1 = Label(self.window, text="Select prediction period", width=30, font=("bold", 12))
            label_1.place(x=int(self.width * 0.0525), y=int(self.height * 0.1066))
            # self.inputtxt_1 = Entry(width=20)
            # self.inputtxt_1.place(x=int(self.width * 0.1575), y=int(self.height * 0.1056))
            # self.inputtxt_1.bind('<KeyPress>', self.keybind1)
            self.clicked = StringVar()

            self.clicked_int = StringVar()
            self.clicked_int.set('10')
            self.drop_int = OptionMenu(self.window, self.clicked_int, *options_int)
            self.drop_int.place(x=int(self.width * 0.1775), y=int(self.height * 0.1056))

            self.clicked.set(self.company_names[0] if len(self.company_names) > 0 else '')

            label_trad_select = Label(self.window, text="Select Company*", width=20, font=("bold", 10))
            label_trad_select.place(x=int(self.width * 0.7375), y=int(self.height * 0.0756))

            # self.drop = OptionMenu(self.window, self.clicked, *options)
            # self.drop.place(x=int(self.width * 0.7575), y=int(self.height * 0.1056))
            self.drop = Combobox(self.window, textvariable=self.clicked, values=options, state='readonly')
            self.drop.place(x=int(self.width * 0.7575), y=int(self.height * 0.1056))

            self.clicked_model = StringVar()

            self.clicked_model.set("FB-Prophet Linear Model")
            label_model_select = Label(self.window, text="Model Select*", width=20, font=("bold", 10))
            label_model_select.place(x=int(self.width * 0.5975), y=int(self.height * 0.0756))

            self.drop_model = OptionMenu(self.window, self.clicked_model, *options_model)
            self.drop_model.place(x=int(self.width * 0.6075), y=int(self.height * 0.1056))

            self.input_1 = Label(self.window, text='FB-Prophet Linear Model', font=("Arial", 18), width=30, height=2)
            self.input_1.place(x=int(self.width * 0.0855), y=int(self.height * 0.7302))

            # self.entry_m_2 = Entry(self.window, width=16, font=('Arial 18'))
            # self.entry_m_2.place(x=int(self.width * 0.4225), y=int(self.height * 0.7502))
            # self.entry_m_2.insert(0, 'Arima')
            # self.entry_m_2.bind("<Button-1>", self.click)
            self.input_2 = Label(self.window, text='LSTM Model', font=("Arial", 18), width=25, height=2)
            self.input_2.place(x=int(self.width * 0.3955), y=int(self.height * 0.7302))

            # self.entry_m_3 = Entry(self.window, width=16, font=('Arial 18'))
            # self.entry_m_3.place(x=int(self.width * 0.6225), y=int(self.height * 0.7502))
            # self.entry_m_3.insert(0, 'M3 prediction')
            # self.entry_m_3.bind("<Button-1>", self.click)

            self.input_3 = Label(self.window, text='FB-Prophet Logistic Model', font=("Arial", 18), width=30,
                                 height=2)
            self.input_3.place(x=int(self.width * 0.6555), y=int(self.height * 0.7302))

            btn4 = tk.Button(self.window, text='Quit ', width=15, height=3,
                             command=self.window.destroy)
            btn4.place(x=int(self.width * 0.8125), y=int(self.height * 0.79922))

            btn4 = tk.Button(self.window, text='Logout', width=15, height=3,
                             command=self.redircte_login_page)
            btn4.place(x=int(self.width * 0.7125), y=int(self.height * 0.79922))

        self.window.mainloop()

    def redircte_login_page(self):
        self.login_status = False
        self.clear_frame()
        self.create_widgets()

    def clear_fun(self):
        result = glob.glob('img/*')
        for f in result:
            os.remove(f)
        self.clear_frame()
        self.create_widgets()

    def clear_frame(self):
        for widgets in self.window.winfo_children():
            widgets.destroy()

    def choose_fun(self):

        try:
            self.btn2 = tk.Button(self.window, text='Choose Compnrs', font=("bold", 12), width=20, height=2,
                                  command=self.choose_fun)
            self.btn2.place(x=self.width * 0.4225, y=int(self.height * 0.1002))
            # text = self.inputtxt_1.get()
            text = self.clicked_int.get()
            if text == '':
                pass
                # label_1 = Label(self.window, text="Enter Integer Value", width=20, font=("bold", 10), background="black",
                #                 foreground="red")
                # label_1.place(x=int(self.width * 0.1575), y=int(self.height * 0.0556))
            else:
                self.prophet_output = self.clicked.get()
                self.prophet_output_model = self.clicked_model.get()

                try:
                    self.text_value = int(text)
                    # self.text_value = int(text)
                    self.clear_frame()

                    if not os.path.exists(
                            f'img/{self.prophet_output_model}_{self.prophet_output}_{self.text_value}.png'):
                        csv_file = f'{self.company_csv_path}/{self.prophet_output}.csv'

                        if self.prophet_output_model == 'FB-Prophet Linear Model':
                            img_path,mse = m1_pred(self.text_value, csv_file, self.prophet_output,
                                               self.prophet_output_model, False)
                            self.dic[img_path]=mse

                            label_1 = Label(self.window, text=f"Prediction Period: {self.text_value}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.0255), y=int(self.height * 0.2556))
                            label_1 = Label(self.window, text=f"MSE: {mse}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.1255), y=int(self.height * 0.2200))

                            label_1 = Label(self.window, text=f"Trade: {self.prophet_output}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.2155), y=int(self.height * 0.2556))

                            self.canvas_img = Canvas(self.window, width=int(self.width * 0.443),
                                                     height=int(self.height * 0.556))
                            self.canvas_img.place(x=int(self.width * 0.0455), y=int(self.height * 0.3002))
                            logo_picture_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
                            logo_picture_img = cv2.resize(logo_picture_img,
                                                          (int(self.width * 0.350), int(self.height * 0.400)))
                            self.photo_logo_img = ImageTk.PhotoImage(image=Image.fromarray(logo_picture_img))
                            self.canvas_img.create_image(0, 0, image=self.photo_logo_img, anchor=NW)

                        elif self.prophet_output_model == 'LSTM':
                            img_path ,mse= lstm_pre(self.text_value, csv_file, self.prophet_output,
                                                self.prophet_output_model)
                            self.dic[img_path] = mse

                            label_1 = Label(self.window, text=f"Prediction Period: {self.text_value}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.3025), y=int(self.height * 0.2556))
                            label_1 = Label(self.window, text=f"MSE: {mse}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.3777), y=int(self.height * 0.2200))

                            label_1 = Label(self.window, text=f"Trade: {self.prophet_output}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.4825), y=int(self.height * 0.2556))

                            self.canvas_img = Canvas(self.window, width=int(self.width * 0.443),
                                                     height=int(self.height * 0.556))
                            self.canvas_img.place(x=int(self.width * 0.3025), y=int(self.height * 0.3202))
                            logo_picture_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
                            logo_picture_img = cv2.resize(logo_picture_img,
                                                          (int(self.width * 0.350), int(self.height * 0.400)))
                            self.photo_logo_img = ImageTk.PhotoImage(image=Image.fromarray(logo_picture_img))
                            self.canvas_img.create_image(0, 0, image=self.photo_logo_img, anchor=NW)

                        # elif self.prophet_output_model == "Close":
                        #     self.input_2 = Label(self.window, text='This model is pending.....?', font=("Arial", 18), width=25,
                        #                          height=2)
                        #     self.input_2.place(x=int(self.width * 0.3955), y=int(self.height * 0.4302))

                        else:
                            img_path ,mse= m1_pred(self.text_value, csv_file, self.prophet_output,
                                               self.prophet_output_model, True)
                            self.dic[img_path] = mse
                            # img_path = fun_main(self.text_value, self.prophet_output, self.prophet_output_model)
                            label_1 = Label(self.window, text=f"MSE: {mse}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.6456), y=int(self.height * 0.2200))
                            label_1 = Label(self.window, text=f"Prediction Period: {self.text_value}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.5455), y=int(self.height * 0.2556))

                            label_1 = Label(self.window, text=f"Trade: {self.prophet_output}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.7255), y=int(self.height * 0.2556))

                            self.canvas_img = Canvas(self.window, width=int(self.width * 0.343),
                                                     height=int(self.height * 0.556))
                            self.canvas_img.place(x=int(self.width * 0.5755), y=int(self.height * 0.3202))
                            logo_picture_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
                            logo_picture_img = cv2.resize(logo_picture_img,
                                                          (int(self.width * 0.350), int(self.height * 0.400)))
                            self.photo_logo_img = ImageTk.PhotoImage(image=Image.fromarray(logo_picture_img))
                            self.canvas_img.create_image(0, 0, image=self.photo_logo_img, anchor=NW)



                    else:
                        img_path = f'img/{self.prophet_output_model}_{self.prophet_output}_{self.text_value}.png'
                        if self.prophet_output_model == 'FB-Prophet Linear Model':
                            mse = self.dic[img_path]
                            label_1 = Label(self.window, text=f"MSE: {mse}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.1255), y=int(self.height * 0.2200))

                            label_1 = Label(self.window, text=f"Prediction Period: {self.text_value}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.0255), y=int(self.height * 0.2556))

                            label_1 = Label(self.window, text=f"Trade: {self.prophet_output}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.2155), y=int(self.height * 0.2556))

                            self.canvas_img = Canvas(self.window, width=int(self.width * 0.343),
                                                     height=int(self.height * 0.556))
                            self.canvas_img.place(x=int(self.width * 0.0455), y=int(self.height * 0.3002))
                            logo_picture_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
                            logo_picture_img = cv2.resize(logo_picture_img,
                                                          (int(self.width * 0.350), int(self.height * 0.400)))
                            self.photo_logo_img = ImageTk.PhotoImage(image=Image.fromarray(logo_picture_img))
                            self.canvas_img.create_image(0, 0, image=self.photo_logo_img, anchor=NW)

                        elif self.prophet_output_model == 'LSTM':
                            mse = self.dic[img_path]
                            label_1 = Label(self.window, text=f"MSE: {mse}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.3777), y=int(self.height * 0.2200))

                            label_1 = Label(self.window, text=f"Prediction Period: {self.text_value}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.3025), y=int(self.height * 0.2556))

                            label_1 = Label(self.window, text=f"Trade: {self.prophet_output}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.4825), y=int(self.height * 0.2556))

                            self.canvas_img = Canvas(self.window, width=int(self.width * 0.343),
                                                     height=int(self.height * 0.556))
                            self.canvas_img.place(x=int(self.width * 0.3225), y=int(self.height * 0.3202))
                            logo_picture_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
                            logo_picture_img = cv2.resize(logo_picture_img,
                                                          (int(self.width * 0.350), int(self.height * 0.400)))
                            self.photo_logo_img = ImageTk.PhotoImage(image=Image.fromarray(logo_picture_img))
                            self.canvas_img.create_image(0, 0, image=self.photo_logo_img, anchor=NW)

                        # elif self.prophet_output_model == "Close":
                        #     self.input_2 = Label(self.window, text='This model is pending.....?', font=("Arial", 18), width=25,
                        #                          height=2)
                        #     self.input_2.place(x=int(self.width * 0.3955), y=int(self.height * 0.4302))
                        else:
                            mse = self.dic[img_path]
                            label_1 = Label(self.window, text=f"MSE: {mse}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.6456), y=int(self.height * 0.2200))
                            label_1 = Label(self.window, text=f"Prediction Period: {self.text_value}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.5455), y=int(self.height * 0.2556))

                            label_1 = Label(self.window, text=f"Trade: {self.prophet_output}", width=30,
                                            font=("bold", 18))
                            label_1.place(x=int(self.width * 0.7255), y=int(self.height * 0.2556))

                            self.canvas_img = Canvas(self.window, width=int(self.width * 0.343),
                                                     height=int(self.height * 0.556))
                            self.canvas_img.place(x=int(self.width * 0.5755), y=int(self.height * 0.3202))
                            logo_picture_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
                            logo_picture_img = cv2.resize(logo_picture_img,
                                                          (int(self.width * 0.350), int(self.height * 0.400)))
                            self.photo_logo_img = ImageTk.PhotoImage(image=Image.fromarray(logo_picture_img))
                            self.canvas_img.create_image(0, 0, image=self.photo_logo_img, anchor=NW)

                    self.create_widgets()
                except Exception as error:
                    print(error)
        except Exception as error:
            print(error)

    def click(self, *args):
        pass


if __name__ == '__main__':
    out_file = '0'
    App(tk.Tk(), 'Stock Prediction', out_file)
