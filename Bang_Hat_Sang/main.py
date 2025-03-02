import customtkinter as ctk
from light_table import LightTableApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = LightTableApp(root)
    root.mainloop()