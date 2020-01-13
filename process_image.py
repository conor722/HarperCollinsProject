from PIL import Image
from tempfile import NamedTemporaryFile
from io import BytesIO
import requests

def apply_harper_collins_logo(url):
    response = requests.get(url)
    background = Image.open(BytesIO(response.content))
    foreground = Image.open('images/harper_collins_logo.png')
    foreground.thumbnail((background.width // 4, background.width // 4), Image.ANTIALIAS)
    y_coord = background.height - foreground.height
    background.paste(foreground, (0, y_coord), foreground.convert('RGBA'))

    temp_file=NamedTemporaryFile()
    background.save(temp_file, format='png')
    return temp_file
