import io
import os

from django.conf import settings
from fpdf import FPDF


INVALID_QUANTITY = 'Неправильно задано количество у ингредиента {name}.'
INGREDIENT_DOES_NOT_EXIST = 'Ингредиента {name} не существует.'
INGREDIENT_ADDED = 'Ингредиент {name} добавлен в рецепт больше одного раза.'


BOTTOM_MARGIN = 15
FONT_SIZE = 14
HEIGHT = 8
TOP_MARGIN = 15
LEFT_MARGIN = 15
fonts = os.path.join(settings.BASE_DIR, 'fonts')
FONT_FILE = os.path.join(fonts, 'DejaVuSansCondensed.ttf')
BOLD_FONT_FILE = os.path.join(fonts, 'DejaVuSansCondensed-Bold.ttf')


def get_shop_list_pdf_binary(ingredients):
    keys = sorted(ingredients.keys())
    pdf = FPDF()
    pdf.add_font('DejaVu', '', FONT_FILE, uni=True)
    pdf.add_font('DejaVu', 'B', BOLD_FONT_FILE, uni=True)
    pdf.set_top_margin(TOP_MARGIN)
    pdf.set_left_margin(LEFT_MARGIN)
    pdf.set_auto_page_break(True, BOTTOM_MARGIN)

    pdf.add_page()
    pdf.set_font('DejaVu', 'B', FONT_SIZE + 2)
    pdf.cell(180, HEIGHT, 'Список покупок', 0, 1, 'C', )
    pdf.cell(180, HEIGHT, '', 0, 1, 'C', )
    pdf.set_font('DejaVu', '', FONT_SIZE)

    for index, title in enumerate(keys):
        pdf.cell(10, HEIGHT, f'{index + 1}.', 1, 0, 'C', )
        pdf.cell(140, HEIGHT, title, 1, 0, 'L', )
        text = (f'{ingredients[title]["quantity"]} '
                f'{ingredients[title]["dimension"]}')
        pdf.cell(30, HEIGHT, text, 1, 1, 'C', )

    pdf.cell(180, HEIGHT, '', 0, 1, 'C', )
    pdf.set_font('DejaVu', '', FONT_SIZE - 2)
    pdf.cell(180, HEIGHT, 'Создано на сайте foodgram', 0, 1, 'R', )

    if pdf.state < 3:
        pdf.close()
    return io.BytesIO(pdf.buffer.encode('latin1'))
