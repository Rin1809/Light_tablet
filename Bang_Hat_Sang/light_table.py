import customtkinter as ctk
from tkinter import filedialog, Canvas, ttk, messagebox
import ctypes
import platform
import os
import pickle
import keyboard
from image_object import ImageObject
from ui import LightTableUI
from PIL import ImageTk, Image, ImageOps 
import tkinter as tk 


class LightTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LightTable Control") 
        self.root.geometry("550x650")  # Đặt kích thước ban đầu cho cửa sổ chính
        self.root.resizable(True, True)  
        self.ui = LightTableUI(self)
        self.images = []
        self.always_on_top = False
        self.click_through = False
        self.light_table_window = None
        self.light_table_opened = False
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.dragged_image = None


        # Lưu trạng thái cửa sổ chính và bàn sáng
        self.saved_state = {
            'images_data': [], 
            'light_table_window_geom': "400x300+100+100",  # Kích thước và vị trí bàn sáng
            'main_window_geom': "550x650+50+50",         # Kích thước và vị trí cửa sổ chính
            'always_on_top': False,
            'click_through': False,
            'opacity': 0.7  # Lưu độ mờ cửa sổ bàn sáng
        }

        self.transparent_color = 'gray'
        self.canvas = None  

        self.setup_keyboard_shortcuts()


    def setup_keyboard_shortcuts(self):
        keyboard.add_hotkey('ctrl+q', self.toggle_clickthrough)
        keyboard.add_hotkey('ctrl+e', self.toggle_always_on_top)
        keyboard.add_hotkey('ctrl+o', self.toggle_light_table)
        keyboard.add_hotkey('ctrl+f', self.toggle_visibility)

    def toggle_visibility(self):
        """Ẩn/hiện ảnh đã chọn."""
        selected_images = self.get_selected_image_objects()
        if not selected_images:
            messagebox.showinfo("Thông báo", "Không có ảnh nào được chọn.")
            return
        for img_obj in selected_images:
            img_obj.is_visible = not img_obj.is_visible
            if self.canvas:
                if img_obj.is_visible:
                    self.canvas.itemconfig(img_obj.canvas_image_id, state='normal')
                else:
                    self.canvas.itemconfig(img_obj.canvas_image_id, state='hidden')

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

            # Áp dụng kích thước/vị trí đã lưu
            try:
                geom = self.saved_state.get('light_table_window_geom', "400x300+100+100")
                self.light_table_window.geometry(geom)
            except:
                self.light_table_window.geometry("400x300+100+100")


            self.always_on_top = self.saved_state.get('always_on_top', False)
            self.click_through = self.saved_state.get('click_through', False)
            opacity_value = self.saved_state.get('opacity', 0.7)

            self.ui.switch_ontop.select() if self.always_on_top else self.ui.switch_ontop.deselect()
            self.ui.switch_clickthrough.select() if self.click_through else self.ui.switch_clickthrough.deselect()

   
            self.ui.scale_opacity.set(opacity_value)
            self.ui.opacity_var.set(f"{opacity_value * 100:.1f}")
            self.apply_opacity(opacity_value) 

            self.apply_always_on_top()
            self.apply_clickthrough()

            self.canvas = Canvas(self.light_table_window, bg=self.transparent_color, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)

            self.light_table_window.bind("<Configure>", self.on_light_table_configure)  
            self.light_table_window.bind("<MouseWheel>", self.zoom_with_wheel)
            self.canvas.bind("<ButtonPress-1>", self.on_drag_start)  
            self.canvas.bind("<B1-Motion>", self.on_drag_motion)    
            self.canvas.bind("<ButtonRelease-1>", self.on_drag_release)
            self.light_table_opened = True
            self.redraw_all_images()  

    def close_light_table(self):
        if self.light_table_window:
            # Lưu vị trí/kích thước trước khi đóng
            self.saved_state['light_table_window_geom'] = self.light_table_window.geometry()
            self.light_table_window.destroy()
            self.light_table_window = None
            self.light_table_opened = False
            self.canvas = FileNotFoundError

    def on_light_table_configure(self, event=None):
        """Xử lý khi cửa sổ bàn sáng thay đổi kích thước/vị trí"""
        if self.light_table_opened and self.canvas:

            self.redraw_all_images()

    def select_images(self):
        # ảnh ok
        filetypes = [("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico;*.webp")]  
        image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
        if image_paths:
            newly_added = []
            for path in image_paths:
                # Kiểm tra trùng lặp
                if not any(img.image_path == path for img in self.images):
                    try:
                        image_obj = ImageObject(path)
                        self.images.append(image_obj)
                        newly_added.append(image_obj)
                    except Exception as e:
                        messagebox.showerror("Lỗi mở ảnh", f"Không thể mở file:\n{path}\n\nLỗi: {e}")
                else:
                    print(f"Ảnh đã tồn tại, bỏ qua: {path}")

            if newly_added:
                self.update_image_list()
                # Chọn ảnh mới thêm vào cuối cùng trong list
                if self.images:
                    last_added_index = len(self.images) - 1
                    item_id = self.ui.image_list.get_children()[last_added_index]
                    self.ui.image_list.selection_set(item_id) 
                    self.ui.image_list.focus(item_id)      
                    self.ui.image_list.see(item_id)      
      
                    self.on_image_selected_from_list()

                self.redraw_all_images()  

    def add_image(self, image_path):  
        if not any(img.image_path == image_path for img in self.images):
            try:
                image_obj = ImageObject(image_path)
                self.images.append(image_obj)
                self.update_image_list()  
                self.redraw_all_images()
            except Exception as e:
                messagebox.showerror("Lỗi mở ảnh", f"Không thể mở file:\n{image_path}\n\nLỗi: {e}")
        else:
            print(f"Ảnh đã tồn tại, bỏ qua: {image_path}")

    # --- Xử lý chọn ảnh từ Treeview ---
    def on_list_item_click(self, event):
        """Xử lý khi click vào một dòng trong Treeview"""
        item_id = self.ui.image_list.identify_row(event.y)
        if not item_id:
            # Click vào vùng trống, bỏ chọn tất cả
            self.ui.image_list.selection_remove(self.ui.image_list.selection())
            self.clear_selection_and_info()
            return

        # Nếu không giữ Ctrl, bỏ chọn các item khác
        if not (event.state & 0x0004):  
            current_selection = self.ui.image_list.selection()
            if item_id in current_selection and len(current_selection) == 1:
                # Click lại vào item đã chọn duy nhất -> không làm gì cả hoặc bỏ chọn? (Hiện tại không làm gì)
                pass
            else:
 
                self.ui.image_list.selection_set(item_id)
        else:

            if item_id in self.ui.image_list.selection():
                self.ui.image_list.selection_remove(item_id)
            else:
                self.ui.image_list.selection_add(item_id)


        self.on_image_selected_from_list()

    def on_image_selected_from_list(self, event=None):
        """Được gọi khi lựa chọn trong Treeview thay đổi (qua click hoặc sự kiện <<TreeviewSelect>>)"""
        selected_item_ids = self.ui.image_list.selection()
        selected_images = self.get_selected_image_objects()

        if not selected_images:
            self.clear_selection_and_info()
            return

        first_selected_img = selected_images[0]


        all_item_ids = self.ui.image_list.get_children()
        for i, item_id in enumerate(all_item_ids):
            if i < len(self.images): 
                self.images[i].is_selected = (item_id in selected_item_ids)


        self.update_image_info(selected_images)  
        self.ui.update_control_state(first_selected_img)  

    def get_selected_image_objects(self):
        """Lấy danh sách các đối tượng ImageObject đang được chọn trong Treeview"""
        selected_ids = self.ui.image_list.selection()
        selected_images = []
        id_to_index_map = {item_id: index for index, item_id in enumerate(self.ui.image_list.get_children())}

        for item_id in selected_ids:
            index = id_to_index_map.get(item_id)
            if index is not None and index < len(self.images):
                selected_images.append(self.images[index])
        return selected_images

    def clear_selection_and_info(self):
        """Bỏ chọn tất cả và xóa thông tin, cập nhật UI controls"""



        for img in self.images:
            img.is_selected = False

   
        self.update_image_info([])
        self.ui.update_control_state(None)  

    def update_image_list(self):
        """Cập nhật Treeview danh sách ảnh"""
        self.ui.image_list.delete(*self.ui.image_list.get_children()) 

        selected_ids_to_restore = []

 
        if not hasattr(self, '_thumb_cache'):
            self._thumb_cache = {}

        for i, img_obj in enumerate(self.images):
            file_name = os.path.basename(img_obj.image_path)


            if img_obj.image_path not in self._thumb_cache:
                try:
                    thumb = img_obj.original_image.copy()
                    thumb.thumbnail((48, 48))  
                    self._thumb_cache[img_obj.image_path] = ImageTk.PhotoImage(thumb)
                except Exception as e:
                    print(f"Lỗi tạo thumbnail cho {file_name}: {e}")

                    placeholder = Image.new('RGBA', (48, 48), (80, 80, 80, 255))
                    self._thumb_cache[img_obj.image_path] = ImageTk.PhotoImage(placeholder)

            thumb_tk = self._thumb_cache[img_obj.image_path]


            item_id = self.ui.image_list.insert("", "end", image=thumb_tk, values=("", file_name))
            
            self.ui.image_list.item(item_id, tags=(img_obj.image_path,)) 
            if img_obj.is_selected:
                selected_ids_to_restore.append(item_id)

        # Khôi phục lựa chọn
        if selected_ids_to_restore:
            self.ui.image_list.selection_set(selected_ids_to_restore)

    def delete_selected_image(self):
        """Xóa các ảnh đang được chọn trong Treeview"""
        selected_images = self.get_selected_image_objects()
        if not selected_images:
            messagebox.showinfo("Thông báo", "Không có ảnh nào được chọn.")
            return

        confirm = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa {len(selected_images)} ảnh đã chọn?")
        if not confirm:
            return

        indices_to_delete = []

        selected_paths = {img.image_path for img in selected_images}
        for i in range(len(self.images) - 1, -1, -1):
            if self.images[i].image_path in selected_paths:
                indices_to_delete.append(i)


        for index in sorted(indices_to_delete, reverse=True):  
            img_obj = self.images[index]
            if self.canvas and img_obj.canvas_image_id:
                try:
                    self.canvas.delete(img_obj.canvas_image_id)
                except tk.TclError:  
                    print(f"Cảnh báo: Không thể xóa canvas_id {img_obj.canvas_image_id}")
                    pass  
            del self.images[index]  

        self.update_image_list()
        self.clear_selection_and_info() 

    def redraw_all_images(self, event=None):
        """Vẽ lại tất cả các ảnh lên canvas (thường dùng khi mở/resize cửa sổ)"""
        if not self.light_table_opened or not self.canvas:
            return 

        window_width = self.light_table_window.winfo_width()
        window_height = self.light_table_window.winfo_height()

        for img_obj in self.images:
            if not hasattr(img_obj, 'photoimage'):  
                img_obj.photoimage = None
            if not hasattr(img_obj, 'canvas_image_id'):
                img_obj.canvas_image_id = None

            if img_obj.is_visible:
                try:
                    final_image = img_obj.get_transformed_image(window_width, window_height)
                    img_obj.photoimage = ImageTk.PhotoImage(image=final_image)

                    # Giả sử (0,0) của ảnh là tâm cửa sổ
                    canvas_x = img_obj.x + window_width / 2
                    canvas_y = img_obj.y + window_height / 2

                    if img_obj.canvas_image_id is None or not self.canvas.winfo_exists():
                    
                        img_obj.canvas_image_id = self.canvas.create_image(
                            canvas_x, canvas_y, anchor="center", image=img_obj.photoimage, tags=(img_obj.image_path, "image") 
                        )
               
                    else:
                     
                        try:
                            self.canvas.coords(img_obj.canvas_image_id, canvas_x, canvas_y)
                            self.canvas.itemconfig(img_obj.canvas_image_id, image=img_obj.photoimage)
                            self.canvas.itemconfig(img_obj.canvas_image_id, state='normal')  
                            
                        except ctk.TclError: 
                            print(f"TclError: invalid command name {img_obj.canvas_image_id}. Creating new image.")
                            img_obj.canvas_image_id = self.canvas.create_image(
                                canvas_x, canvas_y, anchor="center", image=img_obj.photoimage, tags=(img_obj.image_path, "image")
                            )


                except Exception as e:
                    print(f"Error drawing image {img_obj.image_path}: {e}")
                    if img_obj.canvas_image_id:  # Ẩn ảnh bị lỗi
                        try:
                            self.canvas.itemconfig(img_obj.canvas_image_id, state='hidden')
                        except ctk.TclError:
                            img_obj.canvas_image_id = None  # ID không hợp lệ
            else:
                # Ẩn ảnh nếu is_visible là False
                if img_obj.canvas_image_id:
                    try:
                        self.canvas.itemconfig(img_obj.canvas_image_id, state='hidden')

                    except ctk.TclError:
                        img_obj.canvas_image_id = None 

 
        for img_obj in self.images:
            if img_obj.canvas_image_id and img_obj.is_visible:
                try:
                    self.canvas.tag_raise(img_obj.canvas_image_id)
                except ctk.TclError:
                    pass  # Bỏ qua nếu ID không hợp lệ

    # --- Xử lý Opacity ---
    def update_opacity_from_slider(self, value):
        """Gọi khi slider độ mờ thay đổi"""
        opacity_value = float(value)
        self.ui.opacity_var.set(f"{opacity_value * 100:.1f}")
        self.apply_opacity(opacity_value)

    def update_opacity_from_entry(self, event=None):
        """Gọi khi nhấn Enter hoặc mất focus trên Entry độ mờ"""
        try:
            percent_str = self.ui.opacity_var.get().replace('%', '').strip()
            percent = float(percent_str)
            if 0 <= percent <= 100:
                opacity_value = percent / 100.0
                self.ui.scale_opacity.set(opacity_value)  
                self.apply_opacity(opacity_value)
            else:
                current_slider_val = self.ui.scale_opacity.get()
                self.ui.opacity_var.set(f"{current_slider_val * 100:.1f}")
                messagebox.showwarning("Giá trị không hợp lệ", "Độ mờ phải từ 0 đến 100%.")
        except ValueError:
            current_slider_val = self.ui.scale_opacity.get()
            self.ui.opacity_var.set(f"{current_slider_val * 100:.1f}")
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập một số cho độ mờ.")
        finally:

            self.root.focus()

    def apply_opacity(self, value):
        """Áp dụng độ mờ cho cửa sổ bàn sáng"""
        if self.light_table_window and self.light_table_window.winfo_exists():
            self.light_table_window.attributes('-alpha', value)
            self.saved_state['opacity'] = value  # Lưu trạng thái độ mờ

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
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            if self.click_through:
                style |= 0x00080000
                style |= 0x00000020
            else:
                style &= ~0x00000020
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)

    def toggle_clickthrough(self):
        self.click_through = not self.click_through
        self.saved_state['click_through'] = self.click_through
        self.apply_clickthrough()
        self.ui.switch_clickthrough.select() if self.click_through else self.ui.switch_clickthrough.deselect()

    # --- Xử lý Transform Ảnh ---
    def flip_horizontal(self):
        selected_images = self.get_selected_image_objects()
        if not selected_images: return
        for img_obj in selected_images:
            img_obj.photo = ImageOps.mirror(img_obj.photo)
            img_obj.cached_image = None 
        self.redraw_all_images()  

    def rotate_image(self, value):
        """Gọi khi slider xoay thay đổi"""
        selected_images = self.get_selected_image_objects()
        if not selected_images: return
        angle_val = int(float(value))
        for img_obj in selected_images:
            img_obj.angle = angle_val
            img_obj.cached_image = None  
        self.redraw_all_images() 

    # --- Xử lý Zoom ---
    def update_zoom_from_slider(self, value):
        """Gọi khi slider phóng to thay đổi"""
        selected_images = self.get_selected_image_objects()
        if not selected_images: return
        scale_factor = float(value)
        self.ui.zoom_var.set(f"{scale_factor * 100:.0f}") 
        self.apply_zoom(scale_factor, selected_images)

    def update_zoom_from_entry(self, event=None):
        """Gọi khi nhấn Enter hoặc mất focus trên Entry phóng to"""
        selected_images = self.get_selected_image_objects()
        if not selected_images:
            # Nếu không có ảnh nào được chọn, reset entry về 100%
            self.ui.zoom_var.set("100")
            self.root.focus()
            return
        try:
            percent_str = self.ui.zoom_var.get().replace('%', '').strip()
            percent = float(percent_str)
            # Giới hạn zoom hợp lý, ví dụ 1% đến 1000%
            min_zoom, max_zoom = 1, 1000
            if min_zoom <= percent <= max_zoom:
                scale_factor = percent / 100.0
                # Cập nhật Slider, giá trị nằm trong khoảng của slider (0.1 - 10.0)
                slider_val = max(0.1, min(10.0, scale_factor))
                self.ui.scale_zoom.set(slider_val)
                self.apply_zoom(scale_factor, selected_images)
            else:

                current_scale = selected_images[0].scale_factor
                self.ui.zoom_var.set(f"{current_scale * 100:.0f}")
                messagebox.showwarning("Giá trị không hợp lệ", f"Phóng to phải từ {min_zoom}% đến {max_zoom}%.")
        except ValueError:

            current_scale = selected_images[0].scale_factor
            self.ui.zoom_var.set(f"{current_scale * 100:.0f}")
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập một số cho mức phóng to.")
        finally:
            self.root.focus()

    def apply_zoom(self, scale_factor, images_to_zoom):
        """Áp dụng mức phóng to cho các ảnh được chỉ định"""
        if not images_to_zoom: return
        for img_obj in images_to_zoom:
            img_obj.scale_factor = scale_factor
            img_obj.cached_image = None  
        self.redraw_all_images()  

    def zoom_with_wheel(self, event):
        """Xử lý zoom bằng chuột lăn trên cửa sổ bàn sáng"""
        selected_images = self.get_selected_image_objects()
        if not selected_images or not self.light_table_opened: return

        factor = 1.1  # Giảm tốc độ zoom wheel
        new_scale_factors = {}

        for img_obj in selected_images:
            current_scale = img_obj.scale_factor
            if event.delta > 0:  # Lăn lên = zoom vào
                new_scale = current_scale * factor
            else:  # Lăn xuống = zoom ra
                new_scale = current_scale / factor

            # Giới hạn scale factor (ví dụ: 0.01 đến 20.0 - tương đương 1% đến 2000%)
            new_scale = max(0.01, min(20.0, new_scale))
            new_scale_factors[img_obj] = new_scale

        for img_obj, new_scale in new_scale_factors.items():
            img_obj.scale_factor = new_scale
            img_obj.cached_image = None

        if selected_images:
            first_img_scale = selected_images[0].scale_factor
            slider_val = max(0.1, min(10.0, first_img_scale))  
            self.ui.scale_zoom.set(slider_val)
            self.ui.zoom_var.set(f"{first_img_scale * 100:.0f}")

        self.redraw_all_images()

    # --- Xử lý kéo thả ảnh trên Canvas ---
    def on_drag_start(self, event):
        if not self.canvas: return
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)


        overlapping_items = self.canvas.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1)
        self.dragged_image = None
        top_image_obj = None

        # Duyệt ngược từ trên xuống dưới (theo thứ tự vẽ) để tìm ảnh trên cùng
        for img_obj in reversed(self.images):
            if img_obj.canvas_image_id in overlapping_items and img_obj.is_visible:
                top_image_obj = img_obj
                break

        if top_image_obj:
            self.dragging = True
            self.dragged_image = top_image_obj
            self.drag_start_x = canvas_x
            self.drag_start_y = canvas_y
            self.drag_image_start_x = self.dragged_image.x
            self.drag_image_start_y = self.dragged_image.y
            if self.dragged_image.canvas_image_id:
                try:
                    self.canvas.tag_raise(self.dragged_image.canvas_image_id)
                except ctk.TclError: pass
            target_item_id = None
            for item_id in self.ui.image_list.get_children():
                item_tags = self.ui.image_list.item(item_id, "tags")
                if item_tags and item_tags[0] == self.dragged_image.image_path:
                    target_item_id = item_id
                    break
            # Nếu tìm thấy và chưa được chọn (và không giữ Ctrl) thì chọn nó
            if target_item_id and target_item_id not in self.ui.image_list.selection() and not (event.state & 0x0004):
                self.ui.image_list.selection_set(target_item_id)
                self.on_image_selected_from_list() 

    def on_drag_motion(self, event):
        if not self.dragging or not self.dragged_image or not self.canvas:
            return

        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        delta_x = canvas_x - self.drag_start_x
        delta_y = canvas_y - self.drag_start_y

        self.dragged_image.x = self.drag_image_start_x + delta_x
        self.dragged_image.y = self.drag_image_start_y + delta_y

        if self.dragged_image.canvas_image_id:
            if self.light_table_window:
                window_width = self.light_table_window.winfo_width()
                window_height = self.light_table_window.winfo_height()
                new_canvas_x = self.dragged_image.x + window_width / 2
                new_canvas_y = self.dragged_image.y + window_height / 2
                try:
                    self.canvas.coords(self.dragged_image.canvas_image_id, new_canvas_x, new_canvas_y)
                except ctk.TclError: pass  
    def on_drag_release(self, event):
        self.dragging = False
        self.dragged_image = None
        # Không cần làm gì thêm ở đây vì vị trí đã được cập nhật trong on_drag_motion

    # --- Reset và Update Info ---
    def reset_selected_image_transform(self):
        """Reset vị trí, xoay, phóng to, lật của ảnh đã chọn về mặc định."""
        selected_images = self.get_selected_image_objects()
        if not selected_images:
            messagebox.showinfo("Thông báo", "Chọn ít nhất một ảnh để reset.")
            return

        confirm = messagebox.askyesno("Xác nhận Reset", f"Reset vị trí, xoay, phóng to và lật của {len(selected_images)} ảnh đã chọn?")
        if not confirm:
            return

        for img_obj in selected_images:
            # Reset thuộc tính hình học
            img_obj.x = 0
            img_obj.y = 0
            img_obj.angle = 0
            img_obj.scale_factor = 1.0

            # Reset trạng thái lật bằng cách tải lại ảnh gốc
            try:
                original_img = Image.open(img_obj.image_path)
                if original_img.mode != 'RGBA':
                    original_img = original_img.convert('RGBA')
                img_obj.photo = original_img  
            except Exception as e:
                print(f"Lỗi tải lại ảnh gốc cho {img_obj.image_path}: {e}")


            img_obj.cached_image = None 

        if selected_images:
            self.ui.update_control_state(selected_images[0])

        self.redraw_all_images()  # Vẽ lại tất cả ảnh

    def update_image_info(self, selected_images):
        """Cập nhật label thông tin ảnh"""
        if selected_images:
            img_obj = selected_images[0]  # Lấy thông tin của ảnh đầu tiên
            file_name = os.path.basename(img_obj.image_path)
            try:

                width, height = img_obj.original_image.size
                image_format = img_obj.original_image.format if img_obj.original_image.format else "N/A"
            except Exception as e:
                print(f"Lỗi lấy thông tin ảnh {file_name}: {e}")
                width, height, image_format = "N/A", "N/A", "N/A"

            info_text = f"Tên: {file_name}\nKích thước: {width} x {height} | Định dạng: {image_format}"
            if len(selected_images) > 1:
                info_text += f"\n(+ {len(selected_images) - 1} ảnh khác được chọn)"
            self.ui.image_info_label.configure(text=info_text)
        else:
            self.ui.image_info_label.configure(text="Chọn một ảnh để xem thông tin")

    # --- Lưu/Tải Trạng Thái ---
    def save_state_to_file(self):
        """Lưu trạng thái hiện tại vào file pickle"""
        filetypes = [("Light Table State", "*.lts")]
        filepath = filedialog.asksaveasfilename(title="Lưu Trạng Thái", filetypes=filetypes, defaultextension=".lts", initialdir=".")  # Thêm initialdir
        if not filepath: return

        try:
            # Cập nhật geometry trước khi lưu
            if self.light_table_window and self.light_table_window.winfo_exists():
                self.saved_state['light_table_window_geom'] = self.light_table_window.geometry()
            self.saved_state['main_window_geom'] = self.root.geometry()

            # Lưu các thuộc tính cửa sổ khác
            self.saved_state['always_on_top'] = self.always_on_top
            self.saved_state['click_through'] = self.click_through
            self.saved_state['opacity'] = self.ui.scale_opacity.get() 

            # Tạo danh sách ảnh sạch để lưu (chỉ lưu các thuộc tính cần thiết)
            cleaned_images_data = []
            for img_obj in self.images:
                img_data = {
                    'image_path': img_obj.image_path,
                    'scale_factor': img_obj.scale_factor,
                    'angle': img_obj.angle,
                    'x': img_obj.x,
                    'y': img_obj.y,
                    'is_selected': img_obj.is_selected,
                    'is_visible': img_obj.is_visible,
                }


                cleaned_images_data.append(img_data)

            self.saved_state['images_data'] = cleaned_images_data  

            with open(filepath, "wb") as f:
                pickle.dump(self.saved_state, f)
            print(f"Trạng thái đã lưu vào: {filepath}")
            messagebox.showinfo("Lưu thành công", f"Trạng thái đã được lưu vào:\n{filepath}")

        except Exception as e:
            print(f"Lỗi lưu trạng thái: {e}")
            messagebox.showerror("Lỗi", f"Không thể lưu trạng thái:\n{e}")

    def load_state_from_file(self):
        """Tải trạng thái từ file pickle"""
        filetypes = [("Light Table State", "*.lts")]
        filepath = filedialog.askopenfilename(title="Tải Trạng Thái", filetypes=filetypes, initialdir=".")
        if not filepath: return

        try:
            with open(filepath, "rb") as f:
                loaded_state = pickle.load(f)

            # Khôi phục trạng thái cửa sổ chính
            if 'main_window_geom' in loaded_state:
                try:
                    self.root.geometry(loaded_state['main_window_geom'])
                except: pass 


            self.images = []  
            if 'images_data' in loaded_state:  
                for img_data in loaded_state['images_data']:
                    try:
                        # Tạo lại đối tượng ImageObject
                        img_obj = ImageObject(img_data['image_path'])
                        img_obj.scale_factor = img_data.get('scale_factor', 1.0)
                        img_obj.angle = img_data.get('angle', 0)
                        img_obj.x = img_data.get('x', 0)
                        img_obj.y = img_data.get('y', 0)
                        img_obj.is_selected = img_data.get('is_selected', False)
                        img_obj.is_visible = img_data.get('is_visible', True)
                        self.images.append(img_obj)
                    except FileNotFoundError:
                        print(f"Cảnh báo: Không tìm thấy file ảnh '{img_data['image_path']}' khi tải trạng thái. Bỏ qua ảnh này.")
                    except Exception as e:
                        print(f"Lỗi khôi phục ảnh {img_data.get('image_path', 'N/A')}: {e}")


            self.update_image_list()

            # Khôi phục trạng thái bàn sáng (nếu đang mở hoặc sẽ mở)
            self.saved_state = loaded_state 

            if self.light_table_opened:
                self.close_light_table()  
                self.open_light_table()   
            elif self.images: 
                # Tự động mở nếu muốn, hoặc chỉ cập nhật trạng thái chờ
                self.open_light_table()  
                pass

            selected_images = self.get_selected_image_objects()
            if selected_images:
                self.ui.update_control_state(selected_images[0])
  
            else:
                self.clear_selection_and_info() 

            # Vẽ lại ảnh trên bàn sáng (nếu đã mở)
            self.redraw_all_images()

            print(f"Trạng thái đã tải từ: {filepath}")

        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy file trạng thái:\n{filepath}")
        except EOFError:
            print(f"Lỗi: File trạng thái ({filepath}) bị hỏng hoặc không hợp lệ.")
            messagebox.showerror("Lỗi", f"File trạng thái bị hỏng hoặc không hợp lệ:\n{filepath}")
        except Exception as e:
            print(f"Lỗi tải trạng thái: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải trạng thái:\n{e}")

    # --- Hàm tiện ích ---
    def _get_selected_image(self):
        """Trả về đối tượng ImageObject đầu tiên được chọn (nếu có)"""
        selected_items = self.ui.image_list.selection()
        if selected_items:
            # Lấy index từ item_id (cách này hơi chậm nếu list dài)
            try:
                index = self.ui.image_list.index(selected_items[0])
                if 0 <= index < len(self.images):
                    return self.images[index]
            except ValueError:  # Item không tồn tại
                return None
        return None

    def on_close(self):

        if self.light_table_opened:
            self.close_light_table()

        # Đảm bảo gỡ bỏ hotkey trước khi thoát
        try:
            keyboard.remove_all_hotkeys()
        except Exception as e:
            print(f"Lỗi gỡ bỏ hotkey: {e}")  # Có thể lỗi nếu keyboard listener không chạy

        self.root.destroy()  

if __name__ == "__main__":
    import tkinter as tk
    # Đặt DPI Awareness (quan trọng cho Windows để tỷ lệ đúng)
    try:
        if platform.system() == "Windows":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print(f"Không thể đặt DPI awareness: {e}")

    root = ctk.CTk()
    app = LightTableApp(root)
    # Gán hàm xử lý đóng cửa sổ
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()