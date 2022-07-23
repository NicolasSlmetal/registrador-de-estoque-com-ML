from pyzbar import pyzbar
from pacotes.SQLgerenciador.CRUD import CRUDexec
from pygame import mixer
from pacotes.utils import dictparser
import cv2
from pacotes.classifier.classifier import Classifier
import os


def verificacao(data):
    try:
        dictparser.str2dict(data)
    except ValueError:
        return False
    else:
        return True


# Classe que escaneia QR codes


class Scannerqr:

    def __init__(self):
        self.msg = ""
        self.dict = ["Nome", "Data de fabricacao", "Distribuidor", "Preco", "Quantidade"]
        self.db = CRUDexec()
        self.clf = Classifier()
        self.som = os.path.dirname(__file__).replace("cameralistener", "utils\\sons\\Sucesso.mp3")

# Verifica se existe no DB

    def alreadyadd(self, data, produto_img):
        from pacotes.utils import currency
        salvos = self.db.read()
        copia = data.copy()
        copia["Data de fabricacao"] = str(copia["Data de fabricacao"])
        copia["Preco"] = f"{currency.formatar(float(copia['Preco']))}"
        copia["Categoria"] = self.clf.classificar(produto_img)
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

    def analisarimg(self, img, produto_img):
        codigos = pyzbar.decode(img)
        for codigo in codigos:
            (x, y, w, h) = codigo.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            data = codigo.data.decode()
            if produto_img is not None:
                if verificacao(data):
                    data = dictparser.str2dict(data)
                    self.analisardados_add(data, produto_img)
                else:
                    self.msg = "QR code inadequado"
            else:
                self.msg = "Anexe uma imagem primeiro"
            cv2.putText(img, self.msg, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return img

# Verificação final e se envio ao CRUD

    def analisardados_add(self, data, produto_img):
        from pacotes.utils import codegenerator
        import datetime
        if not self.alreadyadd(data, produto_img):
            if produto_img is not None:
                self.msg = "QR code detectado"
                data["Codigo"] = codegenerator.gerarcod()
                while len(self.db.code_read(f"SELECT * FROM 'produtos' WHERE codigo='{data['Codigo']}'")) > 0:
                    data["Codigo"] = codegenerator.gerarcod()
                data["Categoria"] = self.clf.classificar(produto_img)
                data["Data de entrada"] = f"{datetime.datetime.now()}"
                self.db.adicionar(data)
                # Feedback de adição ao DB
                mixer.init()
                mixer.music.load(self.som)
                mixer.music.play()
