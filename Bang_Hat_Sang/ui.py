import customtkinter as ctk
from tkinter import ttk, StringVar 
from PIL import Image, ImageTk
import os

class LightTableUI:
    def __init__(self, app):
        self.app = app 
        self.root = app.root

        # --- Biến kiểm soát cho Entry ---
        self.opacity_var = StringVar(value="70.0") # Giá trị mặc định %
        self.zoom_var = StringVar(value="100")    # Giá trị mặc định %
        # --- ---

        self.create_widgets()
        self.update_control_state() 

    def create_widgets(self):
        switch_on_color = "#FF4081"
        switch_off_color = "#555555"
        entry_bg_color = "#333333" 
        entry_text_color = "white" 
        entry_border_color = "#555555"
        try:

            assets_path = os.path.join(os.path.dirname(__file__), "assets")
            self.icon_flip_h = ctk.CTkImage(Image.open(os.path.join(assets_path, "flip_horizontal.png")), size=(48, 48))
            self.icon_select_image = ctk.CTkImage(Image.open(os.path.join(assets_path, "select_image.png")), size=(48, 48))
            self.icon_open_light_table = ctk.CTkImage(Image.open(os.path.join(assets_path, "open_light_table.png")), size=(48, 48))
            self.icon_reset = ctk.CTkImage(Image.open(os.path.join(assets_path, "reset.png")), size=(48, 48))
            self.icon_delete_image = ctk.CTkImage(Image.open(os.path.join(assets_path, "delete_image.png")), size=(48, 48))

        except Exception as e:
            print(f"Error loading icons: {e}")
      
            self.icon_flip_h, self.icon_select_image, self.icon_open_light_table, self.icon_reset, self.icon_delete_image = None, None, None, None, None

        top_button_frame = ctk.CTkFrame(self.root)
        top_button_frame.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="ew")

        control_frame = ctk.CTkFrame(self.root)
        control_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        # --- Các nút trên cùng ---
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
                                        command=self.app.reset_selected_image_transform,
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

        # --- Điều khiển Ghim và Click-through ---
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
        self.switch_clickthrough.grid(row=0, column=1, pady=5, padx=(15, 5), sticky="w")

        # --- Điều khiển Độ mờ (Opacity) ---
        self.opacity_label = ctk.CTkLabel(control_frame, text="Độ mờ:")
        self.opacity_label.grid(row=1, column=0, columnspan=3, pady=(10,0), padx=5, sticky="w") 

        self.scale_opacity = ctk.CTkSlider(control_frame, from_=0.0, to=1.0, command=self.app.update_opacity_from_slider) 
        self.scale_opacity.set(0.7)
        self.scale_opacity.grid(row=2, column=0, columnspan=2, pady=(0,10), padx=10, sticky="ew") 

        self.entry_opacity = ctk.CTkEntry(control_frame, textvariable=self.opacity_var, width=55, 
                                          justify="right", fg_color=entry_bg_color, text_color=entry_text_color, border_color=entry_border_color)
        self.entry_opacity.grid(row=2, column=2, pady=(0,10), padx=(0, 5), sticky="w") 

        self.entry_opacity.bind("<Return>", self.app.update_opacity_from_entry)
        self.entry_opacity.bind("<FocusOut>", self.app.update_opacity_from_entry)

        self.opacity_percent_label = ctk.CTkLabel(control_frame, text="%")
        self.opacity_percent_label.grid(row=2, column=3, pady=(0,10), padx=(0, 10), sticky="w") 

        # --- Điều khiển Xoay (Rotation) ---
        self.rotation_label = ctk.CTkLabel(control_frame, text="Xoay:")
        self.rotation_label.grid(row=3, column=0, columnspan=3, pady=(5,0), padx=10, sticky="w") 
        self.scale_rotation = ctk.CTkSlider(control_frame, from_=0, to=360, number_of_steps=360, command=self.app.rotate_image)
        self.scale_rotation.set(0)
        self.scale_rotation.grid(row=4, column=0, columnspan=4, pady=(0,10), padx=10, sticky="ew")

        # --- Điều khiển Phóng to (Zoom) - MỚI ---
        self.zoom_label = ctk.CTkLabel(control_frame, text="Phóng to:")
        self.zoom_label.grid(row=5, column=0, columnspan=3, pady=(5,0), padx=5, sticky="w") 

        # Slider: giá trị từ 0.1 (10%) đến 10.0 (1000%)
        self.scale_zoom = ctk.CTkSlider(control_frame, from_=0.1, to=10.0, command=self.app.update_zoom_from_slider)
        self.scale_zoom.set(1.0) # Mặc định 100%
        self.scale_zoom.grid(row=6, column=0, columnspan=2, pady=(0,10), padx=10, sticky="ew")

        self.entry_zoom = ctk.CTkEntry(control_frame, textvariable=self.zoom_var, width=55, 
                                       justify="right", fg_color=entry_bg_color, text_color=entry_text_color, border_color=entry_border_color)
        self.entry_zoom.grid(row=6, column=2, pady=(0,10), padx=(0, 5), sticky="w")
        self.entry_zoom.bind("<Return>", self.app.update_zoom_from_entry)
        self.entry_zoom.bind("<FocusOut>", self.app.update_zoom_from_entry)

        self.zoom_percent_label = ctk.CTkLabel(control_frame, text="%")
        self.zoom_percent_label.grid(row=6, column=3, pady=(0,10), padx=(0, 10), sticky="w")


        # --- Treeview Style Customization (Giữ nguyên) ---
        style = ttk.Style(self.root)
        style.theme_use('default')
        style.configure("Treeview", background="#2D303D", foreground="white", borderwidth=0, font=('Arial', 10))
        style.map('Treeview', background=[('selected', '#4A4D5A')], foreground=[('selected', 'white')])
        style.configure("Treeview.Treearea", background="#2D303D")
        style.configure("Treeview.Heading", background="#40424F", foreground="white", borderwidth=0, font=('Arial', 10, 'bold'))
        style.map('Treeview.Heading', background=[('active', '#505261')])

        # --- Danh sách ảnh Treeview (Tăng row) ---
        self.image_list = ttk.Treeview(self.root, columns=("thumb", "name"), show="headings", height=10, style="Treeview")
        self.image_list.heading("thumb", text="Ảnh") 
        self.image_list.column("thumb", width=64, anchor="center")
        self.image_list.heading("name", text="Tên File") 
        self.image_list.column("name", width=300) # độ cao cột lít file  
        self.image_list.grid(row=2, column=0, pady=5, padx=10, sticky="nsew")
        self.image_list.bind("<ButtonPress-1>", self.app.on_list_item_click)
        self.image_list.bind("<<TreeviewSelect>>", self.app.on_image_selected_from_list) 

        # --- Thông tin ảnh (Tăng row) ---
        self.image_info_label = ctk.CTkLabel(self.root, text="Chọn một ảnh để xem thông tin", font=("Arial", 10), justify="left", anchor="w")
        self.image_info_label.grid(row=3, column=0, sticky='ew', padx=10, pady=(0, 5)) 

        # --- Cấu hình Grid Layout ---
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=0)
        control_frame.columnconfigure(3, weight=0) 

        self.root.rowconfigure(0, weight=0) 
        self.root.rowconfigure(1, weight=0) 
        self.root.rowconfigure(2, weight=1) 
        self.root.rowconfigure(3, weight=0)
        self.root.columnconfigure(0, weight=1)

    def update_control_state(self, selected_image=None):
        """ Bật/tắt các điều khiển dựa trên việc có ảnh được chọn hay không """
        has_selection = selected_image is not None
        state = "normal" if has_selection else "disabled"

        # Các nút/điều khiển cần có ảnh được chọn
        if self.icon_flip_h: self.btn_flip_horizontal.configure(state=state)
        if self.icon_delete_image: self.btn_delete_image.configure(state=state)
        if self.icon_reset: self.btn_reset.configure(state=state)
        self.scale_opacity.configure(state=state)
        self.entry_opacity.configure(state=state)
        self.scale_rotation.configure(state=state)
        self.scale_zoom.configure(state=state)
        self.entry_zoom.configure(state=state)

        # Cập nhật giá trị nếu có ảnh được chọn
        if selected_image:
            current_alpha = self.app.light_table_window.attributes('-alpha') if self.app.light_table_window else 0.7
            opacity_percent = current_alpha * 100
            self.opacity_var.set(f"{opacity_percent:.1f}")
            self.scale_opacity.set(current_alpha)

            # Rotation
            self.scale_rotation.set(selected_image.angle)

            # Zoom
            zoom_percent = selected_image.scale_factor * 100
            self.zoom_var.set(f"{zoom_percent:.0f}") # Hiển thị số nguyên %
            # Đảm bảo giá trị slider nằm trong khoảng hợp lệ
            slider_zoom_val = max(0.1, min(10.0, selected_image.scale_factor))
            self.scale_zoom.set(slider_zoom_val)
        else:
            # Reset giá trị khi không có ảnh nào được chọn (hoặc đặt giá trị mặc định)
            self.opacity_var.set("70.0")
            self.scale_opacity.set(0.7)
            self.scale_rotation.set(0)
            self.zoom_var.set("100")
            self.scale_zoom.set(1.0)