import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import csv
from Db import Db

class Gui(customtkinter.CTk):
    def __init__(self, dataBase=Db('ToDoListDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('To do list at home')
        self.geometry('1202x710')
        self.config(bg='#a9c7c7')
        self.resizable(False, False)

        self.font1 = ('Arial', 26, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        self.headinglabel = self.newLabel('To Do List', bg_color='#a9c7c7', font_size=50)
        self.headinglabel.place(x=30, y=20)

        self.divider = self.newLabel('========================================', 
                                        bg_color='#a9c7c7', font_size=36)
        self.divider.place(x=1, y=480)

        self.enter = self.newLabel('Enter Fields:', bg_color='#5EC7E2', font_size=32)
        self.enter.place(x=66, y=482)

        self.task_label = self.newLabel('Task no.:', bg_color='#a9c7c7', font_size=30)
        self.task_label.place(x=72, y=550)
        self.task_entry = self.newEntry()
        self.task_entry.place(x=235, y=550)

        self.name_label = self.newLabel('Name:', bg_color='#a9c7c7', font_size=30)
        self.name_label.place(x=118, y=600)
        self.name_entry = self.newEntry()
        self.name_entry.place(x=235, y=600)

        self.description_label = self.newLabel('Description:', bg_color='#a9c7c7', font_size=30)
        self.description_label.place(x=20, y=650)
        self.description_entry = self.newEntry()
        self.description_entry.place(x=235, y=650)

        self.deadline_label = self.newLabel('Deadline:', bg_color='#a9c7c7', font_size=30)
        self.deadline_label.place(x=579, y=550)
        self.deadline_entry = self.newEntry()
        self.deadline_entry.place(x=750, y=550)

        self.priority_label = self.newLabel('Priority:', bg_color='#a9c7c7', font_size=30)
        self.priority_label.place(x=599, y=600)
        self.priority_cboxVar = StringVar()
        self.priority_cboxOptions = ['Low Priority', 'Medium Priority', 'High Priority']
        self.priority_cbox = self.newComboBox(options=self.priority_cboxOptions, 
                                    entryVariable=self.priority_cboxVar)
        self.priority_cbox.place(x=750, y=600)

        self.progress_label = self.newLabel('Progress:', bg_color='#a9c7c7', font_size=30)
        self.progress_label.place(x=575, y=650)
        self.progress_cboxVar = StringVar()
        self.progress_cboxOptions = ['Done', 'In progress', 'Not yet started']
        self.progress_cbox = self.newComboBox(options=self.progress_cboxOptions, 
                                    entryVariable=self.progress_cboxVar)
        self.progress_cbox.place(x=750, y=650)


        self.add_button = self.newButton(text='Add +',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312',
                                bgColor='#a9c7c7')
        self.add_button.place(x=380,y=485)

        self.update_button = self.newButton(text='Update',
                                    onClickHandler=self.update_entry,bgColor='#a9c7c7',fgColor='#a39e0f', borderColor='#a39e0f')
        self.update_button.place(x=500,y=485)

        self.delete_button = self.newButton(text='Delete',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404',
                                    bgColor='#a9c7c7')
        self.delete_button.place(x=635,y=485)

        self.export_button = self.newButton(text='Export',
                                    onClickHandler=self.export_to_csv,
                                    bgColor='#a9c7c7',fgColor='#066578', borderColor='#066578')
        self.export_button.place(x=763,y=485)

        self.import_button = self.newButton(text='Import',onClickHandler=self.import_csv, bgColor='#a9c7c7',fgColor='#066578', borderColor='#066578')
        self.import_button.place(x=890,y=485)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#000',
                        background='#CCC',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('taskno', 'name', 'description', 'deadline', 'priority', 'progress')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('taskno', anchor=tk.CENTER, width=10)
        self.tree.column('name', anchor=tk.CENTER, width=150)
        self.tree.column('description', anchor=tk.CENTER, width=150)
        self.tree.column('deadline', anchor=tk.CENTER, width=150)
        self.tree.column('priority', anchor=tk.CENTER, width=150)
        self.tree.column('progress', anchor=tk.CENTER, width=150)

        self.tree.heading('taskno', text='Task no.')
        self.tree.heading('name', text='Name')
        self.tree.heading('description', text='Description')
        self.tree.heading('deadline', text='Deadline')
        self.tree.heading('priority', text='Priority')
        self.tree.heading('progress', text='Progress')

        self.tree.place(x=2, y=100, width=1200, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newLabel(self, text = 'Label', bg_color='#5f6e6e', font_size=20):
        widget_Font=('Arial', font_size, 'bold')
        widget_TextColor='#202626'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=bg_color)
        return widget

    # new Entry Widget
    def newEntry(self, text = 'Entry'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_width)
        return widget

    # new Combo Box Widget
    def newComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newButton(self, text = 'Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704', font_size=24):
        widget_Font=('Arial', font_size, 'bold')
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=100
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        data = self.db.fetch_data()
        self.tree.delete(*self.tree.get_children())
        for i in data:
            print(i)
            self.tree.insert('', END, values=i)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.task_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.deadline_entry.delete(0, END)
        self.priority_cboxVar.set('Medium Priority')
        self.progress_cboxVar.set('Not yet started')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.task_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.description_entry.insert(0, row[2])
            self.deadline_entry.insert(0, row[3])
            self.priority_cboxVar.set(row[4])
            self.progress_cboxVar.set(row[5])
        else:
            pass

    def add_entry(self):
        taskno=self.task_entry.get()
        name=self.name_entry.get()
        description=self.description_entry.get()
        deadline=self.deadline_entry.get()
        priority=self.priority_cboxVar.get()
        progress=self.progress_cboxVar.get()

        if not (taskno and name and description and deadline and priority and progress):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(taskno):
            messagebox.showerror('Error', 'task already exists')
        else:
            self.db.insert_data(taskno, name, description, deadline, priority, progress)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an Task to delete')
        else:
            taskno = self.task_entry.get()
            self.db.delete_data(taskno)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an task to update')
        else:
            taskno=self.task_entry.get()
            name=self.name_entry.get()
            description=self.description_entry.get()
            deadline=self.deadline_entry.get()
            priority=self.priority_cboxVar.get()
            progress=self.progress_cboxVar.get()
            self.db.update_data(name, description, deadline, priority, progress, taskno)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def import_csv(self):
        file = filedialog.askopenfile(filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file.name, "r") as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    taskno, name, description, deadline, priority, progress = row
                    if not self.db.id_exists(taskno):
                        self.db.insert_data(taskno, name, description, deadline, priority, progress)
            self.add_to_treeview()
            messagebox.showinfo('Success', 'Data imported from CSV file.')