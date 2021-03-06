from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import tkinter as tk
import json


file_path = "settings.json"
themes = ["adapta", "aquativo", "arc", "black", "blue", "breeze", "clearlooks", "elegance", "equilux", "itft1", "keramik", "kroc", "plastik", "radiance", "scidblue", "scidgreen", "smog", "vista", "winxpblue", "yaru"]

class SettingsPage:
    def __init__(self, SETTINGS, main_window):
        self.SETTINGS = SETTINGS
        self.setting_variables = {}
        self.main_window = main_window

        self.window = tk.Tk()
        self.window.title(f'{self.SETTINGS["pdf_title"]} | Settings')
        self.window.geometry("900x750")
        self.window.resizable(True, True)

        style = ThemedStyle(self.window)
        style.set_theme(self.SETTINGS["theme"])

        self.window.iconbitmap('favicon.ico')

        ttk.Label(self.window, text = "SETTINGS", font = ("Arial", 14, "bold")).pack(padx = 10, pady = 10)

        self.header_frame = ttk.Frame(self.window, borderwidth=2, relief="groove")
        self.header_frame.pack(padx = 10, pady = 10)

        self.btn_save = ttk.Button(self.header_frame, text = "Save & Exit", command = self.save_and_exit)
        self.btn_save.pack(side = tk.LEFT, padx = 20, pady = 10)

        self.btn_cancel = ttk.Button(self.header_frame, text = "Cancel", command = self.back_to_home)
        self.btn_cancel.pack(side = tk.RIGHT, padx = 20, pady = 10)

        self.base_frame = ttk.Frame(self.window, borderwidth=2, relief="groove")
        self.base_frame.pack(padx=20, pady=10)
    
        self.canvas = tk.Canvas(self.base_frame, width=700, height=500)
        self.scrollbar_y = ttk.Scrollbar(self.base_frame, #canvas, maybe
            orient = "vertical", command = self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side="left", fill="both")
        self.scrollbar_y.pack(side="right", fill = "y")


        for setting in self.SETTINGS:
            self.setting_variables[setting] = tk.StringVar(self.window, value = self.SETTINGS[setting])
            f = ttk.Frame(self.frame, borderwidth=2, relief=tk.GROOVE)
            ttk.Label(f, text = setting.replace("_", " ").upper(), font = ("Arial", 10, "bold")).pack(side = tk.LEFT, padx = 10, pady = 30)                
            if setting == "theme":
                x = ttk.OptionMenu(f, self.setting_variables[setting], self.setting_variables[setting].get(), *themes)
                x.pack(padx = 20, pady = 10)
                f.pack(padx = 10, pady = 5)
            else:
                entry = ttk.Entry(f, textvariable = self.setting_variables[setting],  width = 60)
                entry.pack(side = tk.RIGHT, expand = True, padx = 30, pady = 10)
                f.pack(anchor = "e", padx = 10, pady = 5)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.window.mainloop()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", master=self.window):
            try:
                self.main_window.destroy()
            except:
                pass
            self.window.destroy()

    def save_settings(self):
        for setting in self.SETTINGS:
            if setting == "default_save_folder":
                self.setting_variables[setting].set(self.setting_variables[setting].get().replace("\\", "/"))
            self.SETTINGS[setting] = self.setting_variables[setting].get()
        try:
            with open(file_path, 'w') as json_file:
                json.dump(self.SETTINGS, json_file)
            return True
        except Exception as e:
            print(e)
            return False


    def save_and_exit(self):
        print("Saving settings...")
        if self.save_settings():
            print("Saved.")
            messagebox.showinfo("Success", "Settings saved.", master=self.window)
            self.back_to_home()
        else:
            print("Could not save.")
            messagebox.showinfo("Error", "Settings not saved.", master=self.window)


    def back_to_home(self):
        style = ThemedStyle(self.main_window)
        style.set_theme(self.SETTINGS["theme"])
  
        self.window.destroy()


def save_setting(setting, value):
    try:
        with open(file_path, 'rw') as json_file:
            x = json.load(json_file)
            x[setting] = value
            json.dump(x, json_file)
        return True
    except Exception as e:
        print(e)
        return False
    
    