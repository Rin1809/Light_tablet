import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import os
class LightTableUI:
    def __init__(self, app):
        self.app = app  # Reference to the main application instance
        self.root = app.root
        self.create_widgets()

    def create_widgets(self):
        switch_on_color = "#FF4081"
        switch_off_color = "#555555"
        try:
            # Load icons with relative paths
            assets_path = os.path.join(os.path.dirname(__file__), "assets")
            self.icon_flip_h = ctk.CTkImage(Image.open(os.path.join(assets_path, "flip_horizontal.png")), size=(48, 48))
            self.icon_select_image = ctk.CTkImage(Image.open(os.path.join(assets_path, "select_image.png")), size=(48, 48))
            self.icon_open_light_table = ctk.CTkImage(Image.open(os.path.join(assets_path, "open_light_table.png")), size=(48, 48))
            self.icon_reset = ctk.CTkImage(Image.open(os.path.join(assets_path, "reset.png")), size=(48, 48))
            self.icon_delete_image = ctk.CTkImage(Image.open(os.path.join(assets_path, "delete_image.png")), size=(48, 48))

        except Exception as e:
            print(f"Error loading icons: {e}")
            # Provide fallback if icons fail to load.
            self.icon_flip_h, self.icon_select_image, self.icon_open_light_table, self.icon_reset, self.icon_delete_image = None, None, None, None, None

        top_button_frame = ctk.CTkFrame(self.root)
        top_button_frame.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")

        control_frame = ctk.CTkFrame(self.root)
        control_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")


        self.btn_select_in_options = ctk.CTkButton(top_button_frame, text="",
                                                  image=self.icon_select_image,
                                                  command=self.app.select_images,
                                                  fg_color="transparent", hover_color="gray",
                                                  width=48, height=48)

        self.btn_open_light_table = ctk.CTkButton(top_button_frame, text="",
                                                  image=self.icon_open_light_table,
                                                  command=self.app.toggle_light_table,
                                                  fg_color="transparent", hover_color="gray",
                                                  width=48, height=48)

        self.btn_flip_horizontal = ctk.CTkButton(top_button_frame, text="",
                                                image=self.icon_flip_h,
                                                command=self.app.flip_horizontal,
                                                fg_color="transparent", hover_color="gray",
                                                width=48, height=48)

        self.btn_delete_image = ctk.CTkButton(top_button_frame, text="",
                                              image=self.icon_delete_image,
                                              command=self.app.delete_selected_image,
                                              fg_color="transparent", hover_color="gray",
                                              width=48, height=48)

        self.btn_reset = ctk.CTkButton(top_button_frame, text="",
                                        image=self.icon_reset,
                                        command=self.app.reset_selected_image,  # Keep original command
                                        fg_color="transparent", hover_color="gray",
                                        width=48, height=48)

        self.btn_save_state = ctk.CTkButton(top_button_frame, text="Lưu",
                                            command=self.app.save_state_to_file,
                                            fg_color="transparent", hover_color="gray",
                                            width=48, height=48)

        self.btn_load_state = ctk.CTkButton(top_button_frame, text="Tải lại",
                                            command=self.app.load_state_from_file,
                                            fg_color="transparent", hover_color="gray",
                                            width=48, height=48)

        self.btn_select_in_options.grid(row=0, column=0, padx=5)
        self.btn_open_light_table.grid(row=0, column=1, padx=5)
        self.btn_flip_horizontal.grid(row=0, column=2, padx=5)
        self.btn_delete_image.grid(row=0, column=3, padx=5)
        self.btn_reset.grid(row=0, column=4, padx=5)
        self.btn_save_state.grid(row=0, column=5, padx=5)
        self.btn_load_state.grid(row=0, column=6, padx=5)

        self.switch_ontop = ctk.CTkSwitch(control_frame, text="Ghim",
                                          command=self.app.toggle_always_on_top,
                                          onvalue=True, offvalue=False,
                                          switch_width=50, switch_height=25,
                                          fg_color=switch_off_color, progress_color=switch_on_color)
        self.switch_ontop.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        self.switch_clickthrough = ctk.CTkSwitch(control_frame, text="Click-through",
                                                command=self.app.toggle_clickthrough,
                                                onvalue=True, offvalue=False,
                                                switch_width=50, switch_height=25,
                                                fg_color=switch_off_color, progress_color=switch_on_color)
        self.switch_clickthrough.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        self.opacity_label = ctk.CTkLabel(control_frame, text="Độ mờ:")
        self.opacity_label.grid(row=1, column=0, pady=(5,0), padx=5, sticky="w")
        self.scale_opacity = ctk.CTkSlider(control_frame, from_=0.1, to=1.0, command=self.app.update_opacity)
        self.scale_opacity.set(0.7)
        self.scale_opacity.grid(row=2, column=0, columnspan=2, pady=(0,5), padx=10, sticky="ew")

        self.rotation_label = ctk.CTkLabel(control_frame, text="Xoay:")
        self.rotation_label.grid(row=3, column=0, pady=(5,0), padx=10, sticky="w")
        self.scale_rotation = ctk.CTkSlider(control_frame, from_=0, to=360, number_of_steps=360, command=self.app.rotate_image)
        self.scale_rotation.set(0)
        self.scale_rotation.grid(row=4, column=0, columnspan=2, pady=(0,5), padx=10, sticky="ew")

        # --- Treeview Style Customization ---
        style = ttk.Style(self.root)
        style.theme_use('default')  # Start with a base theme

        # Configure the general Treeview style
        style.configure("Treeview",
                        background="#2D303D",
                        foreground="white",
                        borderwidth=0,
                        font=('Arial', 10))
        style.map('Treeview',
                  background=[('selected', '#4A4D5A')],
                  foreground=[('selected', 'white')])

        # Configure the Treeview.Treearea (the area where the items are displayed)
        style.configure("Treeview.Treearea", background="#2D303D")

        # Configure the Treeview.Heading (column headers)
        style.configure("Treeview.Heading",
                        background="#40424F",
                        foreground="white",
                        borderwidth=0,
                        font=('Arial', 10, 'bold'))
        style.map('Treeview.Heading',
                  background=[('active', '#505261')])  # Hover color


        self.image_list = ttk.Treeview(self.root, columns=("thumb", "name"), show="headings", height=10, style="Treeview")
        self.image_list.heading("thumb", text="STT")
        self.image_list.column("thumb", width=64, anchor="center")
        self.image_list.heading("name", text="Danh sách ảnh")
        self.image_list.column("name", width=150)
        self.image_list.grid(row=2, column=0, pady=5, padx=10, sticky="nsew")
        self.image_list.bind("<ButtonPress-1>", self.app.on_drag_start_list)
        self.image_list.bind("<B1-Motion>", self.app.on_drag_motion_list)
        self.image_list.bind("<ButtonRelease-1>", self.app.on_drag_release_list)


        self.image_info_label = ctk.CTkLabel(self.root, text="", font=("Arial", 10))
        self.image_info_label.grid(row=5, column=0, sticky='w', padx=5, pady=5)

        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)

        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)