from pyzbar import pyzbar
from pacotes.SQLgerenciador.CRUD import CRUDexec
from pygame import mixer
from pacotes.utils import dictparser
import cv2
from pacotes.classifier.classifier import Classifier
from pacotes.utils import imgdown
from tkinter import messagebox as mb
import os





# Classe que escaneia QR codes


class Scannerqr:

    def __init__(self):
        self.msg = ""
        self.dict = ["Nome", "Data de fabricacao", "Distribuidor", "Preco", "Quantidade", "Imagem"]
        self.db = CRUDexec()
        self.clf = Classifier()
        self.som = os.path.dirname(__file__).replace("cameralistener", "utils\\sons\\Sucesso.mp3")

    def verificacao(self, data):
        try:
            teste = dictparser.str2dict(data)
        except ValueError:
            return False
        else:
            keys = list(teste.keys())
            keys.sort()
            self.dict.sort()
            if keys == self.dict:
                return True
            else:
                return False

# Verifica se existe no DB

    def alreadyadd(self, data):
        from pacotes.utils import currency
        salvos = self.db.read()
        copia = data.copy()
        copia["Data de fabricacao"] = str(copia["Data de fabricacao"])
        copia["Preco"] = f"{currency.formatar(float(copia['Preco']))}"
        download = imgdown.download(copia["Imagem"])
        if download == "403" or download == "401":
            mb.showerror("Erro", message="Acesso a imagem foi negado")
            return False
        copia["Categoria"] = self.clf.classificar(download)
        del copia["Imagem"]
        lcopia = list(copia.values())
        lcopia.sort(reverse=True)
        presente = False
        for dados in salvos:
            atual = list(dados[:])
            del atual[4], atual[4]
            atual[len(atual) - 1] = str(atual[len(atual) - 1])
            atual.sort(reverse=True)
            if lcopia == atual:
                self.msg = "Produto existente"
                presente = True
                break
        return presente

# Analisa a imagem

    def analisarimg(self, img):
        codigos = pyzbar.decode(img)
        for codigo in codigos:
            (x, y, w, h) = codigo.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            data = codigo.data.decode()
            if self.verificacao(data):
                data = dictparser.str2dict(data)
                self.analisardados_add(data)
            else:
                self.msg = "QR code inadequado"
            cv2.putText(img, self.msg, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return img

# Verificação final e se envio ao CRUD

    def analisardados_add(self, data):
        from pacotes.utils import codegenerator
        import datetime
        if not self.alreadyadd(data):
            self.msg = "QR code detectado"
            data["Codigo"] = codegenerator.gerarcod()
            while len(self.db.code_read(f"SELECT * FROM 'produtos' WHERE codigo='{data['Codigo']}'")) > 0:
                data["Codigo"] = codegenerator.gerarcod()
            download = imgdown.download(data["Imagem"])
            if download != "401" and download != "403":
                data["Categoria"] = self.clf.classificar(download)
                data["Data de entrada"] = f"{datetime.datetime.now()}"
                self.db.adicionar(data)
                # Feedback de adição ao DB
                mixer.init()
                mixer.music.load(self.som)
                mixer.music.play()
            else:
                mb.showerror("Erro", message="Acesso a imagem foi negado")
