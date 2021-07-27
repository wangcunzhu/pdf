# ! /usr/bin/env python
# coding=utf-8
import os.path

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import *
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz

old_pdf = "old_pdf"
old_img = "old_img"
new_pdf = "new_pdf"


def run(path):
    pdf = PdfFileReader(open(path, 'rb'))
    page_1 = pdf.getPage(0)
    return page_1['/MediaBox'][2], page_1['/MediaBox'][3]


def convert_to_pdf1(filename):
    filename_jpg = os.path.join(old_img, "".join([filename, ".jpg"]))
    im = Image.open(filename_jpg)
    im_w, im_h = im.size
    x_h, x_w = run(os.path.join(old_pdf, "".join([filename, ".pdf"])))
    print(x_h, x_w)
    y_h = im_h * x_h / im_w
    newname = filename_jpg[:filename_jpg.rindex('.')] + '.pdf'
    c = canvas.Canvas(newname, pagesize=(x_h, x_w))
    c.drawImage(filename_jpg, 0, int((x_w - y_h) / 2), int(x_h), int(y_h))
    c.save()
    c.showPage()
    print("convert finish")


def merge_pdfs(filename):
    convert_to_pdf1(filename)
    pdf_writer = PdfFileWriter()
    pdf_list = [
        os.path.join(old_img, "".join([filename, ".pdf"])),
        os.path.join(old_pdf, "".join([filename, ".pdf"]))
    ]
    for path in pdf_list:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # 将每页添加到writer对象
            pdf_writer.addPage(pdf_reader.getPage(page))

    # 写入合并的pdf
    with open(os.path.join(new_pdf, "".join([filename, ".pdf"])), 'wb') as out:
        pdf_writer.write(out)


import sys, fitz
import os
import datetime
import glob

def pyMuPDF_fitz(pdfname):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    imagePath = os.path.join(new_pdf, pdfname)
    pdfPath = os.path.join(new_pdf, pdfname) + ".pdf"
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.writePNG(imagePath + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds)


# 图片转PDF
def pic2pdf2(pdfname):
    imagePath = os.path.join(new_pdf, pdfname)
    doc = fitz.open()
    for root, dirs, files in os.walk(imagePath):
        for img in files:
            imgdoc = fitz.open(os.path.join(root, img))
            imgpdf = imgdoc.convertToPDF()
            imgPDF = fitz.open("pdf", imgpdf)
            doc.insertPDF(imgPDF)
    doc.save("Image.pdf")
    doc.close()
    p2 = "\n操作完成，文件以保存在:\n"  + "Image.pdf"
    return p2


if __name__ == '__main__':
    pdfPath = 'new_pdf/110224112《新时代 新国防——大学生国防教育与军事训练》.pdf'
    imagePath = 'temp_file'
    # pyMuPDF_fitz(pdfPath, imagePath)

    pic2pdf2(imagePath)

    # for root, dirs, files in os.walk(old_pdf):
    #     for name in files:
    #         filename = os.path.splitext(name)[0]
    #         merge_pdfs(filename)

# if __name__ == '__main__':
#     pass
