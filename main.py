from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import datetime

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import load_data as ld
import visualization as v
import processing as p


DATA_FILE = 'Object 01.csv'
APP_TITLE = 'МТК БО ДГА Дата хэндлер'


class Application():

    def __init__(self):
        self.root = Tk()
        self.root.title(APP_TITLE)
        self.root.geometry('600x400')

        self.menubar = Menu(self.root)

        self.menu_data = Menu(self.menubar, tearoff=0)
        self.menu_data.add_command(label='Загрузить xlsx', command=self.command_load_xlsx_data)

        self.menu_processing = Menu(self.menubar, tearoff=0)
        self.menu_processing.add_command(label='Проверить равномерность', command=self.command_check_sparsity)

        self.menubar.add_cascade(label='Данные', menu=self.menu_data)
        self.menubar.add_cascade(label='Обработка', menu=self.menu_processing)

        self.root.config(menu=self.menubar)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=4)
        self.root.rowconfigure(1, weight=1)

        self.frame_notifications = Frame(self.root, relief=RAISED, bg='blue')
        self.status_field = Text(self.frame_notifications, height=0, width=0, wrap=WORD)
        self.scrollbar1 = Scrollbar(self.frame_notifications)
        self.scrollbar1.configure(command=self.status_field.yview)
        self.status_field.pack(side=LEFT, expand=1, fill=BOTH)
        self.scrollbar1.pack(side=LEFT, fill=Y)

        self.tabbed = ttk.Notebook(self.root)
        self.frame_data = Frame(self.tabbed, relief=RAISED, bg='green')
        self.frame_table = Frame(self.tabbed, relief=RAISED, bg='yellow')
        self.frame_viz = Frame(self.tabbed, relief=RAISED)
        self.tabbed.add(self.frame_data, text='Данные')
        self.tabbed.add(self.frame_table, text='Таблица данных')
        self.tabbed.add(self.frame_viz, text='Визуализация')

        self.label_data_source = Label(self.frame_data, text='Источник данных: данные не загружены')
        self.label_data_summary = Label(self.frame_data, text='Анализ данных: данные не загружены')

        self.label_data_summary.grid(row=0, column=0, sticky='w')

        self.tree = ttk.Treeview(self.frame_table, columns=('h2', 'co', 'co2', 'ch4', 'c2h2', 'c2h6', 'c2h4'))
        self.tree.heading('#0', text='date')
        self.tree.heading('h2', text='h2')
        self.tree.heading('ch4', text='ch4')
        self.tree.heading('co', text='co')
        self.tree.heading('co2', text='co2')
        self.tree.heading('c2h6', text='c2h6')
        self.tree.heading('c2h4', text='c2h4')
        self.tree.heading('c2h2', text='c2h2')
        self.tree.column('#0', width=20, stretch=TRUE)
        self.tree.column('h2', width=20, stretch=TRUE)
        self.tree.column('ch4', width=20, stretch=TRUE)
        self.tree.column('co', width=20, stretch=TRUE)
        self.tree.column('co2', width=20, stretch=TRUE)
        self.tree.column('c2h6', width=20, stretch=TRUE)
        self.tree.column('c2h4', width=20, stretch=TRUE)
        self.tree.column('c2h2', width=20, stretch=TRUE)

        self.scrollbar2 = Scrollbar(self.frame_table)
        self.scrollbar2.configure(command=self.tree.yview)

        self.tree.pack(fill=BOTH, expand=1, side=LEFT)
        self.scrollbar2.pack(fill=Y, side=LEFT)

        self.gas_label = StringVar()
        self.gas_label.set('h2')

        self.frame_viz_graph = Frame(self.frame_viz)
        self.frame_gas_labels = Frame(self.frame_viz)
        self.radiobtn_h2 = Radiobutton(self.frame_gas_labels, text='H2', variable=self.gas_label, value='h2')
        self.radiobtn_ch4 = Radiobutton(self.frame_gas_labels, text='CH4', variable=self.gas_label, value='сh4')
        self.radiobtn_co = Radiobutton(self.frame_gas_labels, text='CO', variable=self.gas_label, value='co')
        self.radiobtn_co2 = Radiobutton(self.frame_gas_labels, text='CO2', variable=self.gas_label, value='co2')
        self.radiobtn_c2h6 = Radiobutton(self.frame_gas_labels, text='C2H6', variable=self.gas_label, value='c2h6')
        self.radiobtn_c2h2 = Radiobutton(self.frame_gas_labels, text='C2H2', variable=self.gas_label, value='c2h2')
        self.radiobtn_c2h4 = Radiobutton(self.frame_gas_labels, text='C2H4', variable=self.gas_label, value='c2h4')

        self.frame_viz.rowconfigure(0, weight=1)
        self.frame_viz.rowconfigure(1, weight=0)
        self.frame_viz.columnconfigure(0, weight=1)

        self.frame_viz_graph.grid(row=0, column=0, sticky='snew')
        self.frame_gas_labels.grid(row=1, column=0, sticky='ew')
        self.radiobtn_h2.pack(side=LEFT)
        self.radiobtn_ch4.pack(side=LEFT)
        self.radiobtn_co.pack(side=LEFT)
        self.radiobtn_co2.pack(side=LEFT)
        self.radiobtn_c2h6.pack(side=LEFT)
        self.radiobtn_c2h2.pack(side=LEFT)
        self.radiobtn_c2h4.pack(side=LEFT)

        self.tabbed.grid(row=0, column=0, sticky='snew')
        self.frame_notifications.grid(row=1, column=0, sticky='snew')

        self.data = pd.DataFrame()

        self.root.mainloop()

    def show_status(self, s):
        self.status_field.insert(END, f'\n{datetime.datetime.now()} >> {s}\n')

    def show_data_summary_message(self, s):
        self.label_data_summary.configure(text=s)

    def show_text_data_table(self, s):
        ln = range(len(s))
        for i in ln:
            self.tree.insert('', 'end', '', text=s['date'][i],
                 values=(s['H2'][i], s['CH4'][i], s['CO'][i], s['CO2'][i], s['C2H6'][i], s['C2H4'][i], s['C2H2'][i]))

    def show_plot(self, s, s_gas):
        f = Figure(figsize=(1, 1), dpi=100)
        a = f.add_subplot(111)
        a.plot(s['date'], s[s_gas])

        c = FigureCanvasTkAgg(f, self.frame_viz_graph)
        c.draw()
        c.get_tk_widget().pack(fill=BOTH, expand=TRUE)

        f.delaxes([0][0])

    def command_load_xlsx_data(self):
        xlsx_file_path = filedialog.askopenfilename()
        self.data = ld.load_data_from_xlsx(xlsx_file_path)
        self.show_status(f'Данные загружены из {xlsx_file_path}')
        self.show_data_summary_message(p.get_data_summary(self.data))
        self.show_text_data_table(self.data)
        self.show_plot(self.data, 'H2')

    def command_check_sparsity(self):
        try:
            s = p.check_sparsity(self.data['date'])
            self.show_status(s)
        except Exception as e:
            self.show_status(f'Произошла ошибка: {e}')


if __name__ == "__main__": Application()
