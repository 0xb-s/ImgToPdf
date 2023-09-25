from pathlib import Path
from fpdf import FPDF
from PIL import Image

def get_path():
    return Path('.')

def get_files(dir_path):
    files = []
    for file_path in dir_path.iterdir():
        if file_path.is_file():
            file_str = str(file_path).lower()
            if "png" in file_str or "jpg" in file_str:
                ctime = file_path.stat().st_ctime
                files.append((ctime, file_path))
    return files

def create_pdf_file(images, pdf_name):
    pdf = FPDF()
    for image in images:
        pdf.add_page()

        with Image.open(image) as img:
            img_width, img_height = img.size

        img_width_mm = (img_width / 72) * 25.4
        img_height_mm = (img_height / 72) * 25.4

        aspect_ratio = img_width_mm / img_height_mm
        pdf_width, pdf_height = 210, 297  
        new_width = pdf_width
        new_height = pdf_width / aspect_ratio
        if new_height > pdf_height:
            new_height = pdf_height
            new_width = pdf_height * aspect_ratio

        x = (pdf_width - new_width) / 2
        y = (pdf_height - new_height) / 2

        pdf.image(str(image), x = x, y = y, w = new_width, h = new_height)

    pdf.output(pdf_name)

def main():
    dir_path = get_path()
    files = get_files(dir_path)
    files.sort()
    images = [file_path for ctime, file_path in files]
    create_pdf_file(images, "test.pdf")

main()
