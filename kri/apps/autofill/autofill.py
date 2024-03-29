import os
from PIL import Image, ImageDraw, ImageFont


class AutoFill:
    WIDTH, HEIGHT = (1000, 1000)

    def __init__(self, base_image):
        self.img = Image.open(base_image)
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        self.draw = ImageDraw.Draw(self.img)

    def set_font(self, font, size):
        self.font = ImageFont.truetype(font, size)

    def add_text_center(self, text, y_pos, color='#FFA726'):
        width, _ = self.draw.textsize(text, font=self.font)
        self.draw.text(((self.WIDTH - width) / 2, y_pos), text, color, font=self.font)

    def show(self):
        """Display image"""
        self.img.show()

    def save(self, output_path):
        """Save image"""
        self.img.save(output_path)


class TeamIDCard(AutoFill):
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

    def add_team(self, name, category, role):
        """Add team name and category to canvas"""
        name = name.title()
        team = name + ' (' + category + ')'
        self.add_text_center(team, 560)
        self.add_text_center(role, 590)

    def add_university(self, name):
        """Add university name to canvas"""
        name = name.title()
        self.add_text_center(name.title(), 682)

    @staticmethod
    def fill(base_image, persons, output_path):
        """Fill team members ID card"""
        for p in persons:
            card = TeamIDCard(base_image)
            card.add_photo(p.photo.path)
            card.add_name(p.name)
            card.add_team(p.team.name, p.team.get_division_display(), p.get_type_display())
            card.add_university(p.team.university.name)
            out = os.path.join(output_path, p.team.university.abbreviation + '-' +
                               p.team.division + '-' + str(p.id) + '.png')
            card.save(out)


class PersIDCard(AutoFill):
    WIDTH, HEIGHT = (638, 1011)

    def __init__(self, base_image):
        super(PersIDCard, self).__init__(base_image)
        self.set_font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)

    def add_agency(self, name):
        """Add agency name to canvas"""
        self.add_text_center(name, 485, '#222222')

    @staticmethod
    def fill(base_image, persons, output_path):
        """Fill pers ID card"""
        for p in persons:
            card = PersIDCard(base_image)
            card.add_agency(p.team.university.abbreviation)
            out = os.path.join(output_path, 'PERS-' + p.team.university.abbreviation + '.png')
            card.save(out)
