from models import Entity, GSTValues
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedStyle
import models


class AddEntityPage:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(background = "#f3f3f3")
        self.window.title("Add an Entity")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)

        
        style = ThemedStyle(self.window)
        style.set_theme("vista")

        self.data = {}
        self.titles = [column.key for column in Entity.__table__.columns]
        self.titles.remove('entity_id')

        ttk.Button(self.window, text = "Back",
            command = self.back_to_home).grid(row = 0, column = 0, padx = 30, pady = 10)

        ttk.Label(self.window, text="ADD ENTITY", font = ("Arial", 14, "bold")).grid(padx = 30, pady = 10, row = 0, column = 1)
        
        row = 1
        for field in self.titles:
            self.data[field] = tk.StringVar(self.window)
            ttk.Label(self.window, text=field.replace("_", " ").upper()).grid(padx = 30, pady = 10, row = row, column = 0)
        
            en = ttk.Entry(self.window, width = 30, textvariable = self.data[field])
            en.grid(padx = 30, row = row, column = 1, pady = 10)

            row += 1

        ttk.Button(self.window, text = "Add Entity",
            command = self.add_entity).grid(row = 9, column = 0, padx = 30, pady = 10)

        ttk.Label(self.window, text='CGST: ').grid(row = 10, column = 0, padx = 30, pady = 10)
        ttk.Label(self.window, text='SGST: ').grid(row = 11, column = 0, padx = 30, pady = 10)
        ttk.Label(self.window, text='IGST: ').grid(row = 12, column = 0, padx = 30, pady = 10)
        self.cgst = ttk.Entry(self.window)
        self.cgst.grid(row = 10, column = 1, padx = 30, pady = 10)
        self.sgst = ttk.Entry(self.window)
        self.sgst.grid(row = 11, column = 1, padx = 30, pady = 10)
        self.igst = ttk.Entry(self.window)
        self.igst.grid(row = 12, column = 1, padx = 30, pady = 10)
        ttk.Button(self.window, text = "Save GST values",
        command = self.save_gst).grid(row = 13, column = 0, padx = 30, pady = 10)

        self.window.mainloop()

    def save_gst(self):
        models.set_gst(cgst=int(self.cgst.get()), sgst=int(self.sgst.get()), igst=int(self.igst.get()))

    def add_entity(self):
        data = {}
        for field in self.data:
            x = self.data[field].get()
            if x == "":
                messagebox.showerror(
                    title = "Error",
                    message = "Invalid / empty fields"
                )
                return
            data[field] = x
        
        res = models.create_entity(
            data["name"],
            data["address"],
            data["gstin_uid"],
            data["state"],
            data["state_code"],
            data["bank_name"],
            data["a_c_no"],
            data["ifc_code"]
        )
        print(res)
        if res:
            messagebox.showinfo(
                title = "Success!",
                message = "Created entity"
            )
            self.back_to_home()
        else:
            messagebox.showerror(
                title = "Failed",
                message = "Unable to create entity."
            )

    def back_to_home(self):
        self.window.destroy()