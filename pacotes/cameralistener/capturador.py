import PIL.Image
import cv2
from PIL import Image, ImageTk
from pacotes.cameralistener.scanner import Scannerqr
from pacotes.utils import logger


# Classe que mantém a câmera em loop

class Capturador:
    def __init__(self, lbl):
        self.lbl = lbl
        self.video = cv2.VideoCapture(0)
        self.qrdecoder = Scannerqr()
        self.imgpath = None

    def obtercamera(self):
        try:
            cvimg = cv2.cvtColor(self.video.read()[1], cv2.COLOR_BGR2RGB)
            cvimg = cv2.resize(cvimg, (500, 500))
            # Verifica se imagem tem QR code
            img = Image.fromarray(self.qrdecoder.analisarimg(cvimg, self.imgpath))
            imgTk = PIL.ImageTk.PhotoImage(img)
            self.lbl.imgtk = imgTk
            self.lbl.configure(image=imgTk)
            self.lbl.after_cancel(self.lbl.destroy)
            self.lbl.after(20, self.obtercamera)
        except Exception as exeption:
            logger.salvar_log("capturador.py", exeption)

