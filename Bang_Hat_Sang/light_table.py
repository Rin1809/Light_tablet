import customtkinter as ctk
from tkinter import filedialog, Canvas, ttk, messagebox
import ctypes
import platform
import os
import pickle
import keyboard
from image_object import ImageObject
from ui import LightTableUI  
from PIL import ImageTk, Image


class LightTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ライトボード")
        self.root.resizable(False, False)
        self.ui = LightTableUI(self)  # Tạo một instance của lớp UI
        self.images = []
        self.always_on_top = False
        self.click_through = False
        self.light_table_window = None
        self.light_table_opened = False
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.dragged_image = None
        self.dragged_image_index = None

        self.saved_state = {
            'images': [],
            'current_image_index': None,
            'window_size': (200, 100),
            'always_on_top': False,
            'click_through': False
        }

        self.transparent_color = 'gray'

        self.setup_keyboard_shortcuts()

        self.drag_index = None
        self.drag_item = None

    def setup_keyboard_shortcuts(self):
        keyboard.add_hotkey('ctrl+q', self.toggle_clickthrough)
        keyboard.add_hotkey('ctrl+e', self.toggle_always_on_top)
        keyboard.add_hotkey('ctrl+o', self.toggle_light_table)

    def toggle_light_table(self):
        if self.light_table_opened:
            self.close_light_table()
        else:
            self.open_light_table()

    def open_light_table(self):
        if not self.light_table_opened:
            self.light_table_window = ctk.CTkToplevel(self.root)
            self.light_table_window.title("Light Table")
            self.light_table_window.attributes("-transparentcolor", self.transparent_color)
            self.light_table_window.protocol("WM_DELETE_WINDOW", self.close_light_table)

            if self.saved_state and self.saved_state['window_size']:
                width, height = self.saved_state['window_size']
                self.light_table_window.geometry(f"{width}x{height}")

            if self.saved_state:
                self.always_on_top = self.saved_state.get('always_on_top', False)
                self.click_through = self.saved_state.get('click_through', False)
                self.ui.switch_ontop.select() if self.always_on_top else self.ui.switch_ontop.deselect()
                self.ui.switch_clickthrough.select() if self.click_through else self.ui.switch_clickthrough.deselect()
                self.apply_always_on_top()
                self.apply_clickthrough()

            self.canvas = Canvas(self.light_table_window, bg=self.transparent_color, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)

            self.light_table_window.bind("<Configure>", self.resize_image)
            self.light_table_window.bind("<MouseWheel>", self.zoom_with_wheel)
            self.light_table_window.bind("<ButtonPress-1>", self.on_drag_start)
            self.light_table_window.bind("<B1-Motion>", self.on_drag_motion)
            self.light_table_window.bind("<ButtonRelease-1>", self.on_drag_release)

            self.light_table_opened = True

    def close_light_table(self):
        if self.light_table_window:
            self.light_table_window.destroy()
            self.light_table_window = None
            self.light_table_opened = False
            self.canvas = None

    def select_images(self):
        filetypes = [("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico")]
        image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
        if image_paths:
            for path in image_paths:
                self.add_image(path)
            self.resize_image()
            self.update_image_info()
            if self.images:
                self.on_image_selected_from_card(0)
            self.update_image_list()

    def add_image(self, image_path):
        image_obj = ImageObject(image_path)
        self.images.append(image_obj)
        self.update_image_list()

    def on_drag_start_list(self, event):
        item = self.ui.image_list.identify_row(event.y)
        if item:
            self.drag_item = item
            for i, img_obj in enumerate(self.images):
              if os.path.basename(img_obj.image_path) == self.ui.image_list.item(item,"values")[1]:
                self.drag_index = i
                break

    def on_drag_motion_list(self, event):
        if not self.drag_item:
            return
        target_item = self.ui.image_list.identify_row(event.y)
        if target_item:
            self.ui.image_list.move(self.drag_item, '', self.ui.image_list.index(target_item))
            for i, img_obj in enumerate(self.images):
                if os.path.basename(img_obj.image_path) == self.ui.image_list.item(self.drag_item,"values")[1]:
                    self.drag_index = i
                    break

    def on_drag_release_list(self, event):
      if not self.drag_item:
        return
      new_images = []
      for item_id in self.ui.image_list.get_children():
          file_name = self.ui.image_list.item(item_id, "values")[1]
          for img_obj in self.images:
              if os.path.basename(img_obj.image_path) == file_name:
                  new_images.append(img_obj)
                  break
      self.images = new_images
      self.resize_image()
      self.drag_item = None

    def update_image_list(self):
        for item in self.ui.image_list.get_children():
            self.ui.image_list.delete(item)

        for i, img_obj in enumerate(self.images):
            file_name = os.path.basename(img_obj.image_path)

            thumb = img_obj.original_image.copy()
            thumb.thumbnail((64, 64))
            thumb_tk = ImageTk.PhotoImage(thumb)

            item_id = self.ui.image_list.insert("", "end", values=("", file_name))
            self.ui.image_list.item(item_id, image=thumb_tk, values=(thumb_tk, file_name))

            if img_obj.is_selected:
                self.ui.image_list.selection_add(item_id)
            else:
                self.ui.image_list.selection_remove(item_id)

    def on_image_selected_from_card(self, index, event=None):
        if event and event.state & 0x4:  # Check for Ctrl key
            self.images[index].is_selected = not self.images[index].is_selected
        else:
            for i, img_obj in enumerate(self.images):
                img_obj.is_selected = (i == index)

        for index, img_obj in enumerate(self.images):
            for item in self.ui.image_list.get_children():
                item_text = self.ui.image_list.item(item, "values")[1]
                if item_text == os.path.basename(img_obj.image_path):
                    if img_obj.is_selected:
                        self.ui.image_list.selection_add(item)
                    else:
                        self.ui.image_list.selection_remove(item)
                    break

        self.update_image_info()

    def delete_selected_image(self):
        images_to_delete = [img_obj for img_obj in self.images if img_obj.is_selected]
        if not images_to_delete:
            messagebox.showinfo("Notification","Không có ảnh nào được chọn.")
            return
        for img_obj in reversed(images_to_delete):
            if self.light_table_opened and self.canvas and img_obj.canvas_image_id:
                self.canvas.delete(img_obj.canvas_image_id)
            self.images.remove(img_obj)

        self.update_image_list()
        self.resize_image()
        self.update_image_info()

    def resize_image(self, event=None):
        if self.light_table_window and self.images:
            window_width = self.light_table_window.winfo_width()
            window_height = self.light_table_window.winfo_height()

            for img_obj in self.images:
                final_image = img_obj.get_transformed_image(window_width, window_height)
                img_obj.photoimage = ImageTk.PhotoImage(image=final_image)

                x = img_obj.x + window_width / 2
                y = img_obj.y + window_height / 2

                if img_obj.canvas_image_id is None:
                    img_obj.canvas_image_id = self.canvas.create_image(
                        x, y, anchor="center", image=img_obj.photoimage, tags="image"
                    )
                else:
                    self.canvas.coords(img_obj.canvas_image_id, x, y)
                    self.canvas.itemconfig(img_obj.canvas_image_id, image=img_obj.photoimage)

                self.canvas.tag_lower(img_obj.canvas_image_id)

    def update_opacity(self, value=None):
        if self.light_table_window and self.light_table_window.winfo_exists():
            if value is None:
                value = self.ui.scale_opacity.get()
            else:
                value = float(value)
            self.light_table_window.attributes('-alpha', value)


    def apply_always_on_top(self):
        if self.light_table_window and self.light_table_window.winfo_exists():
            self.light_table_window.attributes("-topmost", self.always_on_top)

    def toggle_always_on_top(self):
        self.always_on_top = not self.always_on_top
        self.saved_state['always_on_top'] = self.always_on_top
        self.apply_always_on_top()
        self.ui.switch_ontop.select() if self.always_on_top else self.ui.switch_ontop.deselect()

    def apply_clickthrough(self):
        if self.light_table_window and self.light_table_window.winfo_exists() and platform.system() == "Windows":
            hwnd = ctypes.windll.user32.GetParent(self.light_table_window.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE
            if self.click_through:
                style |= 0x00080000  # WS_EX_LAYERED
                style |= 0x00000020  # WS_EX_TRANSPARENT
            else:
                style &= ~0x00000020  # Remove WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)  # GWL_EXSTYLE

    def toggle_clickthrough(self):
        self.click_through = not self.click_through
        self.saved_state['click_through'] = self.click_through
        self.apply_clickthrough()
        self.ui.switch_clickthrough.select() if self.click_through else self.ui.switch_clickthrough.deselect()

    def flip_horizontal(self):
        for i, img_obj in enumerate(self.images):
            if img_obj.is_selected:
                img_obj.photo = ImageOps.mirror(img_obj.photo)
                img_obj.cached_image = None # Reset cached image
        self.resize_image()

    def rotate_image(self, value):
      for i, img_obj in enumerate(self.images):
            if img_obj.is_selected:
                img_obj.angle = int(float(value))
                img_obj.cached_image = None
      self.resize_image()

    def zoom_with_wheel(self, event):
      for i, img_obj in enumerate(self.images):
            if img_obj.is_selected:
                if event.delta > 0:
                    img_obj.scale_factor *= 1.2
                else:
                    img_obj.scale_factor /= 1.2
                img_obj.cached_image = None  # Invalidate cache
      self.resize_image()

    def on_drag_start(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        self.drag_start_x = canvas_x
        self.drag_start_y = canvas_y
        self.dragged_image = None
        self.dragged_image_index = None

        for i, img_obj in enumerate(self.images):
            if self.light_table_window:
                window_width = self.light_table_window.winfo_width()
                window_height = self.light_table_window.winfo_height()

                img_x = img_obj.x + window_width / 2
                img_y = img_obj.y + window_height / 2
                img_width, img_height = img_obj.photoimage.width(), img_obj.photoimage.height()
                left = img_x - img_width/2
                top = img_y - img_height/2
                right = img_x + img_width/2
                bottom = img_y + img_height/2

                if left <= canvas_x <= right and top <= canvas_y <= bottom:
                    self.dragged_image_index = i
                    self.dragging = True
                    self.dragged_image = img_obj
                    if self.dragged_image.canvas_image_id:
                        self.canvas.tag_raise(self.dragged_image.canvas_image_id)
                    break
            else:
                self.dragging = False

    def on_drag_motion(self, event):
        if not self.dragging or self.dragged_image is None:
            return

        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        delta_x = canvas_x - self.drag_start_x
        delta_y = canvas_y - self.drag_start_y

        self.dragged_image.x += delta_x
        self.dragged_image.y += delta_y

        self.drag_start_x = canvas_x
        self.drag_start_y = canvas_y

        if self.dragged_image.canvas_image_id:
            if self.light_table_window:
                window_width = self.light_table_window.winfo_width()
                window_height = self.light_table_window.winfo_height()
                x = self.dragged_image.x + window_width / 2
                y = self.dragged_image.y + window_height / 2
                self.canvas.coords(self.dragged_image.canvas_image_id, x, y)

    def on_drag_release(self, event):
        if self.dragging and self.dragged_image_index is not None:
            self.on_image_selected_from_card(self.dragged_image_index, event)  # Pass the event
        self.dragging = False
        self.dragged_image = None
        self.dragged_image_index = None

    def reset_selected_image(self):
        messagebox.showinfo("Thông báo", "Chức năng này đã bị xóa")
        pass

    def update_image_info(self):
        selected_images = [img_obj for img_obj in self.images if img_obj.is_selected]

        if selected_images:
            img_obj = selected_images[0]
            file_name = os.path.basename(img_obj.image_path)
            width, height = img_obj.photo.size
            image_format = img_obj.photo.format
            info_text = f"File Name: {file_name}\nSize: {width} x {height}\nFormat: {image_format}"
            if len(selected_images) > 1:
                info_text += f"\n (+ {len(selected_images) - 1} other selected images)"
            self.ui.image_info_label.configure(text=info_text)
        else:
            self.ui.image_info_label.configure(text="")

    def save_state_to_file(self):
        filetypes = [("Light Table State", "*.lts")]
        filepath = filedialog.asksaveasfilename(title="Save State", filetypes=filetypes, defaultextension=".lts")
        if filepath:
            try:
                if self.light_table_window:
                    self.saved_state['window_size'] = (self.light_table_window.winfo_width(), self.light_table_window.winfo_height())

                self.saved_state['always_on_top'] = self.always_on_top
                self.saved_state['click_through'] = self.click_through

                cleaned_images = []
                for img_obj in self.images:
                    # Only store necessary data, not the entire image object
                    cleaned_obj = ImageObject(img_obj.image_path)
                    cleaned_obj.scale_factor = img_obj.scale_factor
                    cleaned_obj.angle = img_obj.angle
                    cleaned_obj.x = img_obj.x
                    cleaned_obj.y = img_obj.y
                    cleaned_obj.is_selected = img_obj.is_selected  # Save selection state
                    cleaned_images.append(cleaned_obj)

                self.saved_state['images'] = cleaned_images

                with open(filepath, "wb") as f:
                    pickle.dump(self.saved_state, f)
                print(f"State saved to {filepath}")
            except Exception as e:
                print(f"Error saving state: {e}")
                messagebox.showerror("Error", f"Error saving state: {e}")

    def load_state_from_file(self):
        filetypes = [("Light Table State", "*.lts")]
        filepath = filedialog.askopenfilename(title="Load State", filetypes=filetypes)
        if filepath:
            try:
                with open(filepath, "rb") as f:
                    loaded_state = pickle.load(f)

                # Restore images and their properties
                self.images = loaded_state['images']

                for img_obj in self.images:
                    img_obj.original_image = Image.open(img_obj.image_path)
                    if img_obj.original_image.mode != 'RGBA':
                        img_obj.original_image = img_obj.original_image.convert('RGBA')
                    img_obj.photo = img_obj.original_image.copy()
                    img_obj.cached_image = None  # Clear cached images
                    img_obj.cached_size = None
                    img_obj.cached_angle = None

                self.update_image_list()  # Update the image list after loading

                # Restore other settings
                self.always_on_top = loaded_state.get('always_on_top', False)
                self.click_through = loaded_state.get('click_through', False)
                self.ui.switch_ontop.select() if self.always_on_top else self.ui.switch_ontop.deselect()
                self.ui.switch_clickthrough.select() if self.click_through else self.ui.switch_clickthrough.deselect()

                # Open light table if not already open
                if not self.light_table_opened:
                    self.open_light_table()

                if self.light_table_window:
                    width, height = loaded_state['window_size']
                    self.light_table_window.geometry(f"{width}x{height}")

                self.apply_always_on_top()
                self.apply_clickthrough()

                self.resize_image()
                self.update_opacity()
                print(f"State loaded from {filepath}")

            except EOFError:
                print(f"Error: State file ({filepath}) is corrupted or invalid.")
                messagebox.showerror("Error", f"Error: State file ({filepath}) is corrupted or invalid.")

            except Exception as e:
                print(f"Error loading state: {e}")
                messagebox.showerror("Error", f"Error loading state: {e}")
            finally:
                # Any cleanup can go here
                pass