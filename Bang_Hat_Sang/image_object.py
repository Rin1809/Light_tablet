from PIL import Image, ImageTk, ImageOps

class ImageObject:
    def __init__(self, image_path):
        self.image_path = image_path
        self.original_image = Image.open(image_path)
        if self.original_image.mode != 'RGBA':
            self.original_image = self.original_image.convert('RGBA')
        self.photo = self.original_image.copy()
        self.scale_factor = 1.0
        self.angle = 0
        self.x = 0
        self.y = 0
        self.canvas_image_id = None
        self.is_selected = False
        self.cached_image = None
        self.cached_size = None
        self.cached_angle = None
        self.is_visible = True 

    def get_transformed_image(self, window_width, window_height):
        img_width, img_height = self.photo.size
        ratio = min(window_width / img_width, window_height / img_height) * self.scale_factor
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        new_size = (new_width, new_height)

        if (self.cached_image is not None and
            self.cached_size == new_size and
            self.cached_angle == self.angle):
            return self.cached_image

        resized_image = self.photo.resize(new_size, Image.NEAREST)
        rotated_image = resized_image.rotate(-self.angle, expand=True)

        transparent_background = Image.new('RGBA', (rotated_image.width, rotated_image.height), (0, 0, 0, 0))
        final_image = Image.alpha_composite(transparent_background, rotated_image)

        self.cached_image = final_image
        self.cached_size = new_size
        self.cached_angle = self.angle
        return final_image