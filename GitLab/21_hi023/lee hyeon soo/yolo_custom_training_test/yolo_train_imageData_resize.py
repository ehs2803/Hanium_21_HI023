import os
import glob
from PIL import Image

files = glob.glob('./aloe/*.jpg')

for f in files:
    img = Image.open(f)
    img_resize = img.resize((500,500))
    title, ext = os.path.splitext(f)
    img_resize.save(title + ext)
