# Bar Shwatrz 313162265
# Alexndr Savitsky 316611409
import os
import tkinter.messagebox
import customtkinter
from tkinter import filedialog as fd, messagebox
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
import PickleHandler
import Pipeline

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = None
pre_dic = {}
data_dic = {}
algo_dic = {'my_tree': {'switch': False}, 'tree': {'switch': False}, 'my_nb': {'switch': False},
            'nb': {'switch': False}, 'knn': {'switch': False}, 'k_means': {'switch': False}}
modelz = {}


def numerizing(num, lst):
    if num == 1:
        for i in range(0, len(lst)):
            if is_numeric_dtype(App.df1[lst[i]]):
                lst[i] += " *"
    elif num == 0:
        for i in range(0, len(lst)):
            if ' *' in lst[i]:
                lst[i] = lst[i][:-2]


class App(customtkinter.CTk):
    WIDTH = 520
    HEIGHT = 280

    filename = ''
    file_loaded_flag = False
    df1 = None

    def __init__(self):
        super().__init__()
        self.title("Alex & Bar's Data Science Project")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create frame ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_top = customtkinter.CTkFrame(master=self, height=240)
        self.frame_top.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        # ============ frame_top ============

        self.label_1 = customtkinter.CTkLabel(master=self.frame_top,
                                              text="Data Project X",
                                              text_font=("Terminal", -38))  # font name and size in px
        self.label_1.place(relx=0.5, rely=0.17, anchor=tkinter.CENTER)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_top,
                                                   text="Please enter a CSV file\n" +
                                                        "Click the '...' button to load it from your computer.",
                                                   height=60,
                                                   width=370,
                                                   text_font=("System", -15),
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.CENTER)
        self.label_info_1.place(relx=0.5, rely=0.44, anchor=tkinter.CENTER)

        self.loadfileBTN = customtkinter.CTkButton(master=self.frame_top,
                                                   text="...",
                                                   height=30,
                                                   width=30,
                                                   text_font=("System", -16),
                                                   command=self.Load_CSV)
        self.loadfileBTN.place(relx=0.945, rely=0.69, anchor=tkinter.CENTER)

        self.entry = customtkinter.CTkEntry(master=self.frame_top,
                                            width=395,
                                            state=tkinter.DISABLED)
        self.entry.place(relx=0.475, rely=0.69, anchor=tkinter.CENTER)

        self.okBTN = customtkinter.CTkButton(master=self.frame_top,
                                             text="Let's go",
                                             height=30,
                                             width=130,
                                             text_font=("System", -16),
                                             command=self.Lets_GO)
        self.okBTN.place(relx=0.7, rely=0.88, anchor=tkinter.CENTER)

        self.cancelBTN = customtkinter.CTkButton(master=self.frame_top,
                                                 text="Cancel",
                                                 height=30,
                                                 width=130,
                                                 text_font=("System", -16),
                                                 command=self.on_closing)
        self.cancelBTN.place(relx=0.3, rely=0.88, anchor=tkinter.CENTER)

    # funcs
    def on_closing(self, event=0):
        self.destroy()

    def Load_CSV(self):
        App.filename = fd.askopenfilename()
        if App.filename[-3:] != 'csv' and App.filename != '':
            self.entry = customtkinter.CTkEntry(master=self.frame_top,
                                                width=395,
                                                state=tkinter.DISABLED)
            self.entry.place(relx=0.475, rely=0.69, anchor=tkinter.CENTER)

            App.file_loaded_flag = False
            messagebox.showerror('File Type Error', 'Please load only CSV files.')
            return

        if App.filename != '':
            App.df1 = pd.read_csv(App.filename)
            if len(App.df1) > 1:
                App.file_loaded_flag = True
                self.entry = customtkinter.CTkEntry(master=self.frame_top,
                                                    width=395,
                                                    state=tkinter.NORMAL)
                self.entry.place(relx=0.475, rely=0.69, anchor=tkinter.CENTER)
                self.entry.insert(tkinter.END, App.filename)
            else:
                self.entry = customtkinter.CTkEntry(master=self.frame_top,
                                                    width=395,
                                                    state=tkinter.DISABLED)
                self.entry.place(relx=0.475, rely=0.69, anchor=tkinter.CENTER)

                App.file_loaded_flag = False
                messagebox.showerror('CSV File Error', 'Please load a CSV file with 2 or more columns.')
                return


    def Lets_GO(self):
        if App.file_loaded_flag:
            main(self, 2)
        else:
            self.entry.configure(border_color='red')


class App2(customtkinter.CTk):
    WIDTH = 750
    HEIGHT = 580
    # Pipeline.model

    def __init__(self):
        super().__init__()
        self.title("Alex & Bar's Data Science Project")
        self.geometry(f"{App2.WIDTH}x{App2.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, height=540, width=270)
        self.frame_left.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self, height=540, width=390)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.radio_var = tkinter.IntVar(0)
        self.radio_var2 = tkinter.IntVar(0)
        self.radio_var3 = tkinter.IntVar(0)
        self.radio_var4 = tkinter.IntVar(0)

        self.discrete_cols_lst = App.df1.columns.tolist()

        print("Before numerizing - " + str(self.discrete_cols_lst))

        # return: "name_of_column *" is a numerized column
        numerizing(1, self.discrete_cols_lst)

        print("After numerizing - " + str(self.discrete_cols_lst))

        self.continuous_cols_lst = []
        self.normalize_lst = []

        # ============ frame_left ============

        # ------ first choice

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Missing Data Completion",
                                              text_font=("Arial", -15))  # font name and size in px
        self.label_1.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                           text="By Classification Column",
                                                           text_font=("Arial", -12),
                                                           variable=self.radio_var,
                                                           value=0)
        self.radio_button_1.place(relx=0.03, rely=0.12, anchor=tkinter.W)

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                           text="By Column",
                                                           text_font=("Arial", -12),
                                                           variable=self.radio_var,
                                                           value=1)
        self.radio_button_2.place(relx=0.97, rely=0.12, anchor=tkinter.E)

        self.progressbar_1 = customtkinter.CTkProgressBar(master=self.frame_left, width=270)
        self.progressbar_1.place(relx=1, rely=0.19, anchor=tkinter.E)
        self.progressbar_1.set(1)

        # ------ second choice

        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Normalize Values",
                                              text_font=("Arial", -15))  # font name and size in px
        self.label_2.place(relx=0.55, rely=0.26, anchor=tkinter.CENTER)

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_left,
                                                command=self.switched_normalize,
                                                text="")
        self.switch_1.place(relx=0.2, rely=0.26, anchor=tkinter.CENTER)

        self.progressbar_2 = customtkinter.CTkProgressBar(master=self.frame_left,
                                                          width=270)
        self.progressbar_2.place(relx=1, rely=0.43, anchor=tkinter.E)
        self.progressbar_2.set(1)

        # ------ third choice

        self.label_3 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Discretize Data",
                                              text_font=("Arial", -15))  # font name and size in px
        self.label_3.place(relx=0.53, rely=0.5, anchor=tkinter.CENTER)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                command=self.switched_disc,
                                                state=tkinter.ACTIVE,
                                                cursor="hand2",
                                                text="")
        self.switch_2.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)

        self.progressbar_3 = customtkinter.CTkProgressBar(master=self.frame_left,
                                                          width=270)
        self.progressbar_3.place(relx=1, rely=0.76, anchor=tkinter.E)
        self.progressbar_3.set(1)

        # ------ fourth choice

        self.label_4 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Train / Test",
                                              text_font=("Arial", -15))  # font name and size in px
        self.label_4.place(relx=0.5, rely=0.83, anchor=tkinter.CENTER)

        self.label_train = customtkinter.CTkLabel(master=self.frame_left,
                                                  text='Train',
                                                  width=40,
                                                  text_font=("Arial", -13))  # font name and size in px
        self.label_train.place(relx=0.15, rely=0.86, anchor=tkinter.CENTER)

        self.label_test = customtkinter.CTkLabel(master=self.frame_left,
                                                 width=40,
                                                 text="Test",
                                                 text_font=("Arial", -13))  # font name and size in px
        self.label_test.place(relx=0.85, rely=0.86, anchor=tkinter.CENTER)

        self.label_train_percent = customtkinter.CTkLabel(master=self.frame_left,
                                                          text='70%',
                                                          width=40,
                                                          text_font=("Arial", -13))  # font name and size in px
        self.label_train_percent.place(relx=0.15, rely=0.9, anchor=tkinter.CENTER)

        self.label_test_percent = customtkinter.CTkLabel(master=self.frame_left,
                                                         width=40,
                                                         text='30%',
                                                         text_font=("Arial", -13))  # font name and size in px
        self.label_test_percent.place(relx=0.85, rely=0.9, anchor=tkinter.CENTER)

        self.slider_1 = customtkinter.CTkSlider(master=self.frame_left,
                                                width=270,
                                                command=self.slider_changed,
                                                from_=0,
                                                to=100,
                                                number_of_steps=100)
        self.slider_1.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

        # ============ frame_right ============

        # ------ first choice

        self.label_5 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Your Discrete Columns:",
                                              text_font=("Arial", -15))  # font name and size in px
        self.label_5.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)

        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    width=320,
                                                    height=40,
                                                    command=self.label_switch1,
                                                    values=self.discrete_cols_lst)
        self.combobox_1.place(relx=0.5, rely=0.12, anchor=tkinter.CENTER)

        self.label_discrete = customtkinter.CTkLabel(master=self.frame_right,
                                                     text=self.combobox_1.get(),
                                                     width=120,
                                                     text_font=("Arial", -15))  # font name and size in px
        self.label_discrete.place(relx=0, rely=0.2, anchor=tkinter.W)

        # if empty disc list when loaded
        if len(self.discrete_cols_lst) == 0:
            self.combobox_1.configure(state=tkinter.NORMAL, values=[''])
            self.combobox_1.set('')
            self.label_discrete.configure(text='')

        self.radio_button_6 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           text="Make Continuous",
                                                           text_font=("Arial", -12),
                                                           variable=self.radio_var3,
                                                           state=tkinter.NORMAL,
                                                           value=0)
        self.radio_button_6.place(relx=0.55, rely=0.2, anchor=tkinter.CENTER)

        self.radio_button_7 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           text="Delete",
                                                           text_font=("Arial", -12),
                                                           variable=self.radio_var3,
                                                           state=tkinter.NORMAL,
                                                           value=1)
        self.radio_button_7.place(relx=0.85, rely=0.2, anchor=tkinter.CENTER)

        # ------ second choice

        self.confirmBTN1 = customtkinter.CTkButton(master=self.frame_right,
                                                   text="Confirm",
                                                   border_color='black',
                                                   height=20,
                                                   width=60,
                                                   text_font=("System", -14),
                                                   command=self.confirm_handler1)
        self.confirmBTN1.place(relx=0.5, rely=0.255, anchor=tkinter.CENTER)

        self.progressbar_3 = customtkinter.CTkProgressBar(master=self.frame_right,
                                                          progress_color='gray',
                                                          width=400)
        self.progressbar_3.place(relx=1, rely=0.3, anchor=tkinter.E)
        self.progressbar_3.set(1)

        self.label_5 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Your Continuous Columns:",
                                              text_font=("Arial", -15))  # font name and size in px
        self.label_5.place(relx=0.5, rely=0.36, anchor=tkinter.CENTER)

        self.combobox_2 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    width=320,
                                                    height=40,
                                                    command=self.label_switch2)
        self.combobox_2.place(relx=0.5, rely=0.43, anchor=tkinter.CENTER)

        self.label_continuous = customtkinter.CTkLabel(master=self.frame_right,
                                                       text=self.combobox_2.get(),
                                                       width=120,
                                                       text_font=("Arial", -15))  # font name and size in px
        self.label_continuous.place(relx=0, rely=0.51, anchor=tkinter.W)

        # if empty list when loaded
        if len(self.continuous_cols_lst) == 0:
            self.combobox_2.configure(state=tkinter.NORMAL, values=[''])
            self.combobox_2.set('')
            self.label_continuous.configure(text='')

        self.radio_button_8 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           text="Make Discrete",
                                                           text_font=("Arial", -12),
                                                           variable=self.radio_var4,
                                                           state=tkinter.NORMAL,
                                                           value=0)
        self.radio_button_8.place(relx=0.55, rely=0.51, anchor=tkinter.CENTER)

        self.radio_button_9 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           text="Delete",
                                                           text_font=("Arial", -12),
                                                           variable=self.radio_var4,
                                                           state=tkinter.NORMAL,
                                                           value=1)
        self.radio_button_9.place(relx=0.85, rely=0.51, anchor=tkinter.CENTER)

        self.confirmBTN2 = customtkinter.CTkButton(master=self.frame_right,
                                                   text="Confirm",
                                                   border_color='black',
                                                   height=20,
                                                   width=60,
                                                   command=self.confirm_handler2,
                                                   text_font=("System", -14))
        self.confirmBTN2.place(relx=0.5, rely=0.565, anchor=tkinter.CENTER)

        self.progressbar_4 = customtkinter.CTkProgressBar(master=self.frame_right,
                                                          progress_color='gray',
                                                          width=400)
        self.progressbar_4.place(relx=1, rely=0.61, anchor=tkinter.E)
        self.progressbar_4.set(1)

        self.cls_entry = customtkinter.CTkComboBox(master=self.frame_right,
                                                 width=140,
                                                 values=self.discrete_cols_lst)
        self.cls_entry.place(relx=0.95, rely=0.95, anchor=tkinter.E)

        self.label_6 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Choose a \nclassifier column:",
                                              width=90,
                                              text_font=("Arial", -12))  # font name and size in px
        self.label_6.place(relx=0.43, rely=0.95, anchor=tkinter.CENTER)

        # ------ third choice

        self.label_6 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Choose an Algorithm For The Model:",
                                              text_font=("Arial", -16))  # font name and size in px
        self.label_6.place(relx=0.5, rely=0.67, anchor=tkinter.CENTER)

        self.combobox_3 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    width=320,
                                                    height=40,
                                                    command=self.algo_combobox,
                                                    values=["Decision Tree by us",
                                                            "Decision Tree by sklearn",
                                                            "Naïve Bayes by us",
                                                            "Naïve Bayes by sklearn",
                                                            "KNN by sklearn",
                                                            "K-MEANS by sklearn"])
        self.combobox_3.place(relx=0.5, rely=0.74, anchor=tkinter.CENTER)

        self.executeBTN = customtkinter.CTkButton(master=self.frame_right,
                                                 text="Execute",
                                                 height=30,
                                                 width=90,
                                                 text_font=("System", -16),
                                                 command=self.activate_model)
        self.executeBTN.place(relx=0.15, rely=0.95, anchor=tkinter.CENTER)

        # set default values
        self.radio_button_1.select()
        self.radio_button_6.select()
        self.radio_button_8.select()
        self.switch_1.select()
        self.switch_2.select()
        self.radio_button_3.select()
        self.slider_1.set(70)
        self.combobox_3.set('Decision Tree by us')

    local_list = []
    algo_list = [['False'], ['False'], ['False'], ['False'], ['False'], ['False']]
    save_model_num = 7
    # funcs

    def on_closing(self, event=0):
        exit(0)
        # self.destroy()

    def radiobutton_event(self):
        print("radio1 value:", self.radio_var.get())
        print("switch1 value:", self.switch_1.get())
        print("radio2 value:", self.radio_var2.get())

    def slider_changed(self, value):
        a = str(int(value)) + "%"
        b = str(int(100 - value)) + "%"
        self.label_train_percent = customtkinter.CTkLabel(master=self.frame_left,
                                                          text=a,
                                                          width=40,
                                                          text_font=("Arial", -13))  # font name and size in px
        self.label_train_percent.place(relx=0.15, rely=0.9, anchor=tkinter.CENTER)

        self.label_test_percent = customtkinter.CTkLabel(master=self.frame_left,
                                                         width=40,
                                                         text=b,
                                                         text_font=("Arial", -13))  # font name and size in px
        self.label_test_percent.place(relx=0.85, rely=0.9, anchor=tkinter.CENTER)

    def switched_disc(self):
        if self.switch_2.get() == 0:
            for item in self.disc_lst:
                item.destroy()
        elif self.switch_2.get() == 1:
            self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                               text="Equal Frequency",
                                                               text_font=("Arial", -12),
                                                               variable=self.radio_var2,
                                                               state=tkinter.NORMAL,
                                                               value=0)
            self.radio_button_3.place(relx=0.05, rely=0.57, anchor=tkinter.W)

            self.radio_button_4 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                               text="Equal Width",
                                                               text_font=("Arial", -12),
                                                               variable=self.radio_var2,
                                                               state=tkinter.NORMAL,
                                                               value=1)
            self.radio_button_4.place(relx=0.05, rely=0.63, anchor=tkinter.W)

            self.radio_button_5 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                               text="Entropy Based",
                                                               text_font=("Arial", -12),
                                                               variable=self.radio_var2,
                                                               state=tkinter.NORMAL,
                                                               value=2)
            self.radio_button_5.place(relx=0.05, rely=0.69, anchor=tkinter.W)

            self.bins_entry = customtkinter.CTkEntry(master=self.frame_left,
                                                     width=120,
                                                     placeholder_text="Number of bins")
            self.bins_entry.place(relx=0.95, rely=0.69, anchor=tkinter.E)

            self.disc_lst = []
            self.disc_lst.append(self.radio_button_3)
            self.disc_lst.append(self.radio_button_4)
            self.disc_lst.append(self.radio_button_5)
            self.disc_lst.append(self.bins_entry)

    def label_switch1(self, val):
        self.label_discrete.configure(text=self.combobox_1.get())

    def label_switch2(self, val):
        self.label_continuous.configure(text=self.combobox_2.get())

    def confirm_handler1(self):
        if self.radio_var3.get() == 1:
            self.delete_col1()
        elif self.radio_var3.get() == 0:
            self.move_to_continuous()

    def confirm_handler2(self):
        if self.radio_var4.get() == 1:
            self.delete_col2()
        elif self.radio_var4.get() == 0:
            self.move_to_discrete()

    def delete_col1(self):
        if len(self.discrete_cols_lst) > 1:
            self.discrete_cols_lst.remove(self.combobox_1.get())
            self.combobox_1.configure(values=self.discrete_cols_lst)
            self.combobox_1.set(self.discrete_cols_lst[0])
            self.label_discrete.configure(text=self.discrete_cols_lst[0])
            self.cls_entry.configure(values=self.discrete_cols_lst)
            self.cls_entry.set(self.discrete_cols_lst[0])
        else:
            if len(self.discrete_cols_lst) > 0:
                self.discrete_cols_lst.remove(self.combobox_1.get())
                self.combobox_1.configure(state=tkinter.NORMAL, values=[''])
                self.combobox_1.set('')
                self.label_discrete.configure(text='')
                self.cls_entry.configure(values=[''])
                self.cls_entry.set('')

    def delete_col2(self):
        if len(self.continuous_cols_lst) > 1:
            self.continuous_cols_lst.remove(self.combobox_2.get())
            self.combobox_2.configure(values=self.continuous_cols_lst)
            self.combobox_2.set(self.continuous_cols_lst[0])
            self.label_continuous.configure(text=self.continuous_cols_lst[0])

            if self.switch_1.get() == 1:
                self.combobox_normalize.configure(values=self.continuous_cols_lst)
                self.combobox_normalize.set(self.continuous_cols_lst[0])
                print("To be normalized: " + str(self.normalize_lst))

        else:
            if len(self.continuous_cols_lst) > 0:
                self.continuous_cols_lst.remove(self.combobox_2.get())
                self.combobox_2.configure(state=tkinter.NORMAL, values=[''])
                self.combobox_2.set('')
                if self.switch_1.get() == 1:
                    self.combobox_normalize.configure(state=tkinter.NORMAL, values=[''])
                    self.combobox_normalize.set('')
                self.label_continuous.configure(text='')

    def move_to_continuous(self):
        if (self.combobox_1.get() in self.discrete_cols_lst) and (self.combobox_1.get() != '') \
                and ('*' in self.combobox_1.get()):
            self.continuous_cols_lst.append(self.combobox_1.get())
            self.label_continuous.configure(text=self.combobox_1.get())
            self.combobox_2.set(self.combobox_1.get())

            temp_set = set(self.continuous_cols_lst)
            self.continuous_cols_lst = list(temp_set)

            self.combobox_2.configure(values=self.continuous_cols_lst)
            self.delete_col1()
            print("Continuous cols list: " + str(self.continuous_cols_lst))

    def move_to_discrete(self):
        if (self.combobox_2.get() in self.continuous_cols_lst) and self.combobox_2.get() != '':
            self.discrete_cols_lst.append(self.combobox_2.get())
            if self.combobox_2.get() in self.normalize_lst:
                self.normalize_lst.remove(self.combobox_2.get())
                if len(self.normalize_lst) == 0: self.combobox_normalize.set('')
            self.label_discrete.configure(text=self.combobox_2.get())
            self.combobox_1.set(self.combobox_2.get())

            temp_set = set(self.discrete_cols_lst)
            self.discrete_cols_lst = list(temp_set)

            self.combobox_1.configure(values=self.discrete_cols_lst)
            self.delete_col2()
            print("Discrete cols list: " + str(self.discrete_cols_lst))

    def all_normalizers(self):
        if self.switch_1.get() == 1:
            if len(self.continuous_cols_lst) > 0:
                self.normalize_lst = self.continuous_cols_lst.copy()
                self.combobox_normalize.configure(values=self.normalize_lst)
                self.combobox_normalize.set(self.continuous_cols_lst[0])
                print("To be normalized: " + str(self.normalize_lst))
            else:
                self.combobox_normalize.configure(state=tkinter.NORMAL, values=[''])
                self.combobox_normalize.set('')

    def remove_normalizer(self):
        if self.switch_1.get() == 1:
            if self.combobox_normalize.get() in self.normalize_lst and (len(self.normalize_lst) > 1):
                self.normalize_lst.remove(self.combobox_normalize.get())
                self.combobox_normalize.configure(values=self.normalize_lst)
                self.combobox_normalize.set(self.normalize_lst[0])
                print("To be normalized: " + str(self.normalize_lst))
            else:
                if len(self.normalize_lst) == 1:
                    self.normalize_lst.remove(self.combobox_normalize.get())
                self.combobox_normalize.configure(state=tkinter.NORMAL, values=[''])
                self.combobox_normalize.set('')
                print("To be normalized: " + str(self.normalize_lst))

    def switched_normalize(self):
        if self.switch_1.get() == 0:
            for item in self.temp_lst:
                item.destroy()
        elif self.switch_1.get() == 1:
            self.normalize_lst = []
            self.combobox_normalize = customtkinter.CTkComboBox(master=self.frame_left,
                                                                width=250,
                                                                height=30,
                                                                values=self.normalize_lst)
            self.combobox_normalize.place(relx=0.5, rely=0.32, anchor=tkinter.CENTER)

            if len(self.normalize_lst) == 0:
                self.combobox_normalize.set('')
                # self.combobox_normalize.configure(state=tkinter.NORMAL, values=[''])

            print("To be normalized: " + str(self.normalize_lst))

            self.remove_normalizeBTN = customtkinter.CTkButton(master=self.frame_left,
                                                               text="Remove",
                                                               border_color='black',
                                                               height=20,
                                                               width=60,
                                                               command=self.remove_normalizer,
                                                               cursor='hand2',
                                                               text_font=("System", -14))
            self.remove_normalizeBTN.place(relx=0.3, rely=0.385, anchor=tkinter.CENTER)

            self.all_normalizeBTN = customtkinter.CTkButton(master=self.frame_left,
                                                            text="All",
                                                            border_color='black',
                                                            height=20,
                                                            width=60,
                                                            cursor='hand2',
                                                            text_font=("System", -14),
                                                            command=self.all_normalizers)
            self.all_normalizeBTN.place(relx=0.7, rely=0.385, anchor=tkinter.CENTER)

            self.temp_lst = []
            self.temp_lst.append(self.combobox_normalize)
            self.temp_lst.append(self.remove_normalizeBTN)
            self.temp_lst.append(self.all_normalizeBTN)

    def algo_combobox(self, value):
        if self.combobox_3.get() == 'Decision Tree by us':
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
            self.algo_temp_lst = []
            self.switch_algo = customtkinter.CTkSwitch(master=self.frame_right,
                                                       command=self.switched_algo1,
                                                       text="Off/On")
            self.switch_algo.place(relx=0.88, rely=0.82, anchor=tkinter.CENTER)
            self.switch_algo.deselect()

        elif self.combobox_3.get() == 'Decision Tree by sklearn':
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
            self.algo_temp_lst = []
            self.switch_algo = customtkinter.CTkSwitch(master=self.frame_right,
                                                       command=self.switched_algo2,
                                                       text="Off/On")
            self.switch_algo.place(relx=0.88, rely=0.82, anchor=tkinter.CENTER)
            self.switch_algo.deselect()

        elif self.combobox_3.get() == 'Naïve Bayes by us':
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
            self.algo_temp_lst = []
            self.switch_algo = customtkinter.CTkSwitch(master=self.frame_right,
                                                       command=self.switched_algo3,
                                                       text="Off/On")
            self.switch_algo.place(relx=0.88, rely=0.82, anchor=tkinter.CENTER)
            self.switch_algo.deselect()

        elif self.combobox_3.get() == 'Naïve Bayes by sklearn':
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
            self.algo_temp_lst = []
            self.switch_algo = customtkinter.CTkSwitch(master=self.frame_right,
                                                       command=self.switched_algo4,
                                                       text="Off/On")
            self.switch_algo.place(relx=0.88, rely=0.82, anchor=tkinter.CENTER)
            self.switch_algo.deselect()

        elif self.combobox_3.get() == 'KNN by sklearn':
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
            self.algo_temp_lst = []
            self.switch_algo = customtkinter.CTkSwitch(master=self.frame_right,
                                                       command=self.switched_algo5,
                                                       text="Off/On")
            self.switch_algo.place(relx=0.88, rely=0.82, anchor=tkinter.CENTER)
            self.switch_algo.deselect()

        elif self.combobox_3.get() == 'K-MEANS by sklearn':
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
            self.algo_temp_lst = []
            self.switch_algo = customtkinter.CTkSwitch(master=self.frame_right,
                                                       command=self.switched_algo6,
                                                       text="Off/On")
            self.switch_algo.place(relx=0.88, rely=0.82, anchor=tkinter.CENTER)
            self.switch_algo.deselect()

    def switched_algo1(self):
        if self.switch_algo.get() == 0:
            App2.algo_list[0] = ['False']
            algo_dic['my_tree'] = {'switch': False}
            print(App2.algo_list)
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
        elif self.switch_algo.get() == 1:
            self.radio_algo_var = tkinter.IntVar(0)

            self.radio_button_algoA = customtkinter.CTkRadioButton(master=self.frame_right,
                                                               text="Info Gain",
                                                               text_font=("Arial", -12),
                                                               variable=self.radio_algo_var,
                                                               value=0)
            self.radio_button_algoA.place(relx=0.65, rely=0.82, anchor=tkinter.CENTER)

            self.radio_button_algoB = customtkinter.CTkRadioButton(master=self.frame_right,
                                                                   text="Min Sample Leaf",
                                                                   text_font=("Arial", -12),
                                                                   variable=self.radio_algo_var,
                                                                   value=1)
            self.radio_button_algoB.place(relx=0.38, rely=0.82, anchor=tkinter.CENTER)

            self.entry_algo = customtkinter.CTkEntry(master=self.frame_right,
                                                     width=70,
                                                     placeholder_text="Value",
                                                     state=tkinter.NORMAL)
            self.entry_algo.place(relx=0.11, rely=0.82, anchor=tkinter.CENTER)

            self.radio_button_algoC = customtkinter.CTkRadioButton(master=self.frame_right,
                                                                   text="None",
                                                                   text_font=("Arial", -12),
                                                                   variable=self.radio_algo_var,
                                                                   value=2)
            self.radio_button_algoC.place(relx=0.87, rely=0.87, anchor=tkinter.CENTER)
            self.radio_button_algoC.select()

            self.confirm_algoBTN = customtkinter.CTkButton(master=self.frame_right,
                                                           text="Confirm",
                                                           border_color='black',
                                                           height=20,
                                                           width=60,
                                                           text_font=("System", -14),
                                                           command=self.add_to_algo_list1)
            self.confirm_algoBTN.place(relx=0.5, rely=0.87, anchor=tkinter.CENTER)

            App2.local_list.append(self.radio_button_algoA)
            App2.local_list.append(self.radio_button_algoB)
            App2.local_list.append(self.radio_button_algoC)
            App2.local_list.append(self.entry_algo)
            App2.local_list.append(self.confirm_algoBTN)

    def switched_algo2(self):
        if self.switch_algo.get() == 0:
            App2.algo_list[1] = ['False']
            algo_dic['tree'] = {'switch': False}
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
        elif self.switch_algo.get() == 1:
            self.radio_algo_var2 = tkinter.IntVar(0)

            self.radio_button_algoA = customtkinter.CTkRadioButton(master=self.frame_right,
                                                               text="Info Gain",
                                                               text_font=("Arial", -12),
                                                               variable=self.radio_algo_var2,
                                                               value=0)
            self.radio_button_algoA.place(relx=0.65, rely=0.82, anchor=tkinter.CENTER)

            self.radio_button_algoB = customtkinter.CTkRadioButton(master=self.frame_right,
                                                                   text="Min Sample Leaf",
                                                                   text_font=("Arial", -12),
                                                                   variable=self.radio_algo_var2,
                                                                   value=1)
            self.radio_button_algoB.place(relx=0.38, rely=0.82, anchor=tkinter.CENTER)

            self.radio_button_algoC = customtkinter.CTkRadioButton(master=self.frame_right,
                                                                   text="None",
                                                                   text_font=("Arial", -12),
                                                                   variable=self.radio_algo_var2,
                                                                   value=2)
            self.radio_button_algoC.place(relx=0.87, rely=0.87, anchor=tkinter.CENTER)
            self.radio_button_algoC.select()

            self.entry_algo = customtkinter.CTkEntry(master=self.frame_right,
                                                width=70,
                                                placeholder_text="Value",
                                                state=tkinter.NORMAL)
            self.entry_algo.place(relx=0.11, rely=0.82, anchor=tkinter.CENTER)

            self.confirm_algoBTN = customtkinter.CTkButton(master=self.frame_right,
                                                           text="Confirm",
                                                           border_color='black',
                                                           height=20,
                                                           width=60,
                                                           text_font=("System", -14),
                                                           command=self.add_to_algo_list2)
            self.confirm_algoBTN.place(relx=0.5, rely=0.87, anchor=tkinter.CENTER)

            App2.local_list.append(self.radio_button_algoA)
            App2.local_list.append(self.radio_button_algoB)
            App2.local_list.append(self.radio_button_algoC)
            App2.local_list.append(self.entry_algo)
            App2.local_list.append(self.confirm_algoBTN)

    def switched_algo3(self):
        if self.switch_algo.get() == 0:
            App2.algo_list[2] = ['False']
            algo_dic['my_nb'] = {'switch': False}
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
        elif self.switch_algo.get() == 1:
            App2.algo_list[2] = ['True']
            algo_dic['my_nb'] = {'switch': True}

    def switched_algo4(self):
        if self.switch_algo.get() == 0:
            App2.algo_list[3] = ['False']
            algo_dic['nb'] = {'switch': False}
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
        elif self.switch_algo.get() == 1:
            App2.algo_list[3] = ['True']
            algo_dic['nb'] = {'switch': True}

    def switched_algo5(self):
        if self.switch_algo.get() == 0:
            App2.algo_list[4] = ['False']
            algo_dic['knn'] = {'switch': False}
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
        elif self.switch_algo.get() == 1:
            self.entry_algo = customtkinter.CTkEntry(master=self.frame_right,
                                                     width=100,
                                                     placeholder_text="Value",
                                                     state=tkinter.NORMAL)
            self.entry_algo.place(relx=0.5, rely=0.815, anchor=tkinter.CENTER)
            App2.local_list.append(self.entry_algo)

            self.confirm_algoBTN = customtkinter.CTkButton(master=self.frame_right,
                                                           text="Confirm",
                                                           border_color='black',
                                                           height=20,
                                                           width=60,
                                                           text_font=("System", -14),
                                                           command=self.add_to_algo_list5)
            self.confirm_algoBTN.place(relx=0.5, rely=0.87, anchor=tkinter.CENTER)
            App2.local_list.append(self.confirm_algoBTN)

    def switched_algo6(self):
        if self.switch_algo.get() == 0:
            App2.algo_list[5] = ['False']
            algo_dic['k_means'] = {'switch': False}
            if len(App2.local_list) > 0:
                for item in App2.local_list: item.destroy()
                App2.local_list = []
        elif self.switch_algo.get() == 1:
            self.entry_algo = customtkinter.CTkEntry(master=self.frame_right,
                                                     width=100,
                                                     placeholder_text="Value",
                                                     state=tkinter.NORMAL)
            self.entry_algo.place(relx=0.5, rely=0.815, anchor=tkinter.CENTER)
            App2.local_list.append(self.entry_algo)

            self.confirm_algoBTN = customtkinter.CTkButton(master=self.frame_right,
                                                           text="Confirm",
                                                           border_color='black',
                                                           height=20,
                                                           width=60,
                                                           text_font=("System", -14),
                                                           command=self.add_to_algo_list6)
            self.confirm_algoBTN.place(relx=0.5, rely=0.87, anchor=tkinter.CENTER)
            App2.local_list.append(self.confirm_algoBTN)

    def add_to_algo_list1(self):
        if self.switch_algo.get() == 1:
            if self.radio_algo_var.get() == 0:
                try:
                    float(self.entry_algo.get())
                except ValueError:
                    messagebox.showerror('Value Type Error', 'Please type a value between 0-1.')
                    return
                if 0 > float(self.entry_algo.get()) or float(self.entry_algo.get()) > 1:
                    messagebox.showerror('Value Type Error', 'Please type a value between 0-1.')
                    return
                App2.algo_list[0] = ['True', 'ig', self.entry_algo.get()]
                algo_dic['my_tree'] = {'switch': True, 'ig_limit': App2.algo_list[0][1],
                                       'num': float(App2.algo_list[0][2])}
            elif self.radio_algo_var.get() == 1:
                try:
                    int(self.entry_algo.get())
                except ValueError:
                    messagebox.showerror('Value Type Error', 'Please type int type in the value entry.')
                    return
                App2.algo_list[0] = ['True', 'min samples leaf', self.entry_algo.get()]
                algo_dic['my_tree'] = {'switch': True,
                                    'ig_limit': App2.algo_list[0][1],
                                    'num': int(App2.algo_list[0][2])}
                print(algo_dic)

            else:
                algo_dic['my_tree'] = {'switch': True, 'ig_limit': False,
                                       'num': False}

        print(App2.algo_list)

    def add_to_algo_list2(self):
        if self.switch_algo.get() == 1:
            if self.radio_algo_var2.get() == 0:
                try:
                    float(self.entry_algo.get())
                except ValueError:
                    messagebox.showerror('Value Type Error', 'Please type a value between 0-1.')
                    return
                if 0 > float(self.entry_algo.get()) or float(self.entry_algo.get()) > 1:
                    messagebox.showerror('Value Type Error', 'Please type a value between 0-1.')
                    return
                App2.algo_list[1] = ['True', 'ig', self.entry_algo.get()]
                algo_dic['tree'] = {'switch': True,
                                    'ig_limit or min samples leaf': App2.algo_list[1][1],
                                    'num': float(App2.algo_list[1][2])}
            elif self.radio_algo_var2.get() == 1:
                try:
                    int(self.entry_algo.get())
                except ValueError:
                    messagebox.showerror('Value Type Error', 'Please type int type in the value entry.')
                    return
                App2.algo_list[1] = ['True', 'min samples leaf', self.entry_algo.get()]
                algo_dic['tree'] = {'switch': True,
                                    'ig_limit or min samples leaf': App2.algo_list[1][1],
                                    'num': int(App2.algo_list[1][2])}
            else:
                algo_dic['tree'] = {'switch': True,
                                    'ig_limit or min samples leaf': False,
                                    'num': False}
        print(App2.algo_list)

    def add_to_algo_list5(self):
        if self.switch_algo.get() == 1:
            try:
                int(self.entry_algo.get())
            except ValueError:
                messagebox.showerror('Value Type Error', 'Please type int type in the value entry.')
                return
            App2.algo_list[4] = ['True', self.entry_algo.get()]
            algo_dic['knn'] = {'switch': True, 'n_neighbors': int(App2.algo_list[4][1])}
        print(App2.algo_list)

    def add_to_algo_list6(self):
        if self.switch_algo.get() == 1:
            try:
                int(self.entry_algo.get())
            except ValueError:
                messagebox.showerror('Value Type Error', 'Please type int type in the value entry.')
                return
            App2.algo_list[5] = ['True', self.entry_algo.get()]
            algo_dic['k_means'] = {'switch': True, 'n_clusters': int(App2.algo_list[5][1])}
        print(App2.algo_list)

    def activate_model(self):
        App2.save_model_num += 1
        save_model_num = App2.save_model_num
        #if bins entry is not int or empty
        if self.switch_2.get() == 1:
            try:
                int(self.bins_entry.get())
            except ValueError:
                messagebox.showerror('Value Type Error', 'Please type int type in the bins amount.')
                return

        #Preprocess model
        if self.radio_var.get() == 0: pre_dic['features_cleaner'] = 'class'
        elif self.radio_var.get() == 1: pre_dic['features_cleaner'] = 'column'

        if len(self.normalize_lst) > 0:
            numerizing(0, self.normalize_lst)
            pre_dic['normalize'] = self.normalize_lst
        else:
            pre_dic['normalize'] = False

        if self.switch_2.get() == 1:
            if self.radio_var2.get() == 0: pre_dic['discretization'] = 'equal freq'
            elif self.radio_var2.get() == 1: pre_dic['discretization'] = 'equal width'
            elif self.radio_var2.get() == 2: pre_dic['discretization'] = 'entropy'

            if self.bins_entry.get() != '':
                pre_dic['bins'] = int(self.bins_entry.get())
        else:
            pre_dic['discretization'] = False
            pre_dic['bins'] = False

        pre_dic['train_size'] = int(self.label_train_percent.text[:-1]) / 100

        #Dataframe model
        data_dic['name'] = os.path.basename(App.filename)[:-4]

        if self.cls_entry.get() != '':
            data_dic['class_column'] = self.cls_entry.get()
            self.discrete_cols_lst.remove(self.cls_entry.get())

        numerizing(0, self.discrete_cols_lst)
        numerizing(0, self.continuous_cols_lst)

        data_dic['discrete_columns'] = self.discrete_cols_lst
        data_dic['continuous_columns'] = self.continuous_cols_lst

        model = {}
        model['dataframe'] = data_dic
        model['preprocess'] = pre_dic
        model['algorithm'] = algo_dic
        print(model)
        os.chdir(f'{os.getcwd()}\models')
        Pipeline.save(model,save_model_num)
        clean_df = Pipeline.clean_df_return_and_save(App.df1,model,save_model_num)
        model = Pipeline.excute_algorithems(clean_df,model,save_model_num)


        modelz = model
        print(modelz)

        main(self, 3)


class App3(customtkinter.CTk):
    WIDTH = 750
    HEIGHT = 580

    def __init__(self):

        super().__init__()

        self.title("Alex & Bar's Data Science Project")
        self.geometry(f"{App3.WIDTH}x{App3.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.counter = 0
        # ============ create frame ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_top = customtkinter.CTkFrame(master=self, height=540, width=700)
        self.frame_top.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        name = App2.save_model_num

        name = str(name)
        model = PickleHandler.load_model(name)
        print('\n\n')
        print(model)
        self.res_dict = model['res']
        self.res_list_label = self.res_dict.keys()
        self.res_list_label = list(self.res_list_label)
        print(self.res_dict)
        print(self.res_list_label)


        if self.res_list_label[self.counter] != 'majority' :
            self.card_for_algo(self.res_dict, self.res_list_label[self.counter], 0.45, 0.05)
        else:
            self.majority(self.res_dict['majority'], 0.45, 0.05)


        self.executeBTN = customtkinter.CTkButton(master=self.frame_top,
                                                  text="Next",
                                                  height=30,
                                                  width=90,
                                                  text_font=("System", -16),
                                                  command=self.activate_model)
        self.executeBTN.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

    def activate_model(self):
        self.counter += 1
        if self.res_list_label[self.counter] != 'majority':
            self.label_1.destroy()
            self.label_1a.destroy()
            self.label_1b.destroy()
            self.label_1c.destroy()
            self.label_1d.destroy()
            self.label_1e.destroy()
            self.label_1f.destroy()
            self.label_1g.destroy()
            self.label_1h.destroy()
            self.label_1i.destroy()
            self.label_1j.destroy()
            self.label_1k.destroy()
            self.label_1l.destroy()
            self.card_for_algo(self.res_dict, self.res_list_label[self.counter], 0.45, 0.05)
        else:
            self.majority(self.res_dict['majority'],0.45, 0.05)
            self.executeBTN.configure(text='Finish', command=self.on_closing)
            self.label_1.destroy()
            self.label_1a.destroy()
            self.label_1b.destroy()
            self.label_1c.destroy()
            self.label_1d.destroy()
            self.label_1e.destroy()
            self.label_1f.destroy()
            self.label_1g.destroy()
            self.label_1h.destroy()
            self.label_1i.destroy()
            self.label_1j.destroy()
            self.label_1k.destroy()
            self.label_1l.destroy()


    def majority(self,majority,relax , relay):
        self.label_2 = customtkinter.CTkLabel(master=self.frame_top,
                                              text=f"Majority Results: {majority}",
                                              width= 350,
                                              text_font=("Arial", -18))  # font name and size in px
        self.label_2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def card_for_algo(self,res_dict,algo,relax , relay):
            #0.4,0.3
            relax_sub_title1 =relax -0.2
            relax_sub_title2 = relax + 0.3
            relay_sub_title = relay +0.1
            font_size = -14
            txt = f"Confusion Matrix:\n {res_dict[algo]['train on train']['confusion matrix']}"
            txt2 = f"Confusion Matrix:\n {res_dict[algo]['train on test']['confusion matrix']}"
            txt = txt.replace('[', '')
            txt = txt.replace(']', '')
            txt2 = txt2.replace('[', '')
            txt2 = txt2.replace(']', '')

            self.label_1 = customtkinter.CTkLabel(master=self.frame_top,
                                                  text=f"{algo} results:",
                                                  width=240,
                                                  text_font=("Arial", font_size-10))  # font name and size in px
            self.label_1.place(relx=0.5, rely=relay, anchor=tkinter.CENTER)

            self.label_1a = customtkinter.CTkLabel(master=self.frame_top,
                                                   text="train on train",
                                                   text_font=("Terminal", font_size-5))  # font name and size in px
            self.label_1a.place(relx=relax_sub_title1, rely=relay_sub_title, anchor=tkinter.CENTER)

            self.label_1b = customtkinter.CTkLabel(master=self.frame_top,
                                                   text="train on test",
                                                   text_font=("Terminal", font_size-5))  # font name and size in px
            self.label_1b.place(relx=relax_sub_title2, rely=relay_sub_title, anchor=tkinter.CENTER)
            relay_sub_title +=0.1
            self.label_1c = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=f"Accuracy Score: {res_dict[algo]['train on train']['accuracy_score']}",
                                                   width=300,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1c.place(relx=relax_sub_title1, rely=relay_sub_title, anchor=tkinter.CENTER)

            self.label_1d = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=f"Accuracy Score: {res_dict[algo]['train on test']['accuracy_score']}",
                                                   width=300,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1d.place(relx=relax_sub_title2, rely=relay_sub_title, anchor=tkinter.CENTER)

            relay_sub_title += 0.1
            self.label_1e = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=f"Precision: {res_dict[algo]['train on train']['precision score']}",
                                                   width=300,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1e.place(relx=relax_sub_title1, rely=relay_sub_title, anchor=tkinter.CENTER)
            self.label_1f = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=f"Precision: {res_dict[algo]['train on test']['precision score']}",
                                                   width=300,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1f.place(relx=relax_sub_title2, rely=relay_sub_title, anchor=tkinter.CENTER)

            relay_sub_title += 0.1
            self.label_1g = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=f"Recall Score: {res_dict[algo]['train on train']['recall score']}",
                                                   width=300,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1g.place(relx=relax_sub_title1, rely=relay_sub_title, anchor=tkinter.CENTER)

            self.label_1h = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=f"Recall Score: {res_dict[algo]['train on test']['recall score']}",
                                                   width=300,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1h.place(relx=relax_sub_title2, rely=relay_sub_title, anchor=tkinter.CENTER)
            relay_sub_title += 0.1

            self.label_1i = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=f"F-Measure: {res_dict[algo]['train on train']['F-measure']}",
                                                   width=300,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1i.place(relx=relax_sub_title1, rely=relay_sub_title, anchor=tkinter.CENTER)

            self.label_1j = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=f"F-Measure: {res_dict[algo]['train on test']['F-measure']}",
                                                   width=300,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1j.place(relx=relax_sub_title2, rely=relay_sub_title, anchor=tkinter.CENTER)

            relay_sub_title += 0.1

            self.label_1k = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=txt,
                                                   width=300,
                                                   height=40,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1k.place(relx=relax_sub_title1, rely=relay_sub_title, anchor=tkinter.CENTER)

            self.label_1l = customtkinter.CTkLabel(master=self.frame_top,
                                                   text=txt2,
                                                   width=300,
                                                   height=40,
                                                   text_font=("Arial", font_size))  # font name and size in px
            self.label_1l.place(relx=relax_sub_title2, rely=relay_sub_title, anchor=tkinter.CENTER)

    def on_closing(self, event=0):
        exit(0)


def main(app, current_window):
    if current_window == 1:
        app = App()
        app.resizable(False, False)
        app.mainloop()
    if current_window == 2:
        app.withdraw()
        app = App2()
        app.resizable(False, False)
        app.mainloop()
    if current_window == 3:
        app.withdraw()
        app = App3()
        app.resizable(False, False)
        app.mainloop()

if __name__ == '__main__':
    main(app, 1)


