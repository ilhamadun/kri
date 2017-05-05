from PIL import Image, ImageDraw, ImageFont


class AutoFill:
    WIDTH, HEIGHT = (1000, 1000)

    def __init__(self, base_image):
        self.img = Image.open(base_image)
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        self.draw = ImageDraw.Draw(self.img)

    def add_text_center(self, text, y_pos):
        width, _ = self.draw.textsize(text, font=self.font)
        self.draw.text(((self.WIDTH - width) / 2, y_pos), text, '#FFA726', font=self.font)

    def show(self):
        """Display image"""
        self.img.show()

    def save(self, output_path):
        """Save image"""
        self.img.save(output_path)

class IDCardAutoFill(AutoFill):
    WIDTH, HEIGHT = (638, 1011)

    def add_photo(self, image_path):
        """Add photo to canvas"""
        photo = Image.open(image_path)
        width, height = photo.size

        ratio = height / width
        if ratio > 1.33:
            thumbnail_size = (170, height)
        else:
            thumbnail_size = (width, 228)

        photo.thumbnail(thumbnail_size)
        width, height = photo.size

        new_width = 170
        new_height = 228

        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        cropped = photo.crop((left, top, right, bottom))
        self.img.paste(cropped, (230, 159))

    def add_name(self, name):
        """Add participant name to canvas"""
        self.add_text_center(name.title(), 460)

    def add_team(self, name, category):
        """Add team name and category to canvas"""
        name = name.title()
        team = name + ' (' + category + ')'
        self.add_text_center(team, 560)

    def add_university(self, name):
        """Add university name to canvas"""
        name = name.title()
        self.add_text_center(name.title(), 658)