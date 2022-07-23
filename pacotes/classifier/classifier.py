import numpy as np
import keras
import os
from pacotes.utils import logger
import cv2


# 0 - Roupa; 1 - Calçado; 2 - Headset
# Classe que utiliza Machine Learning para classificar produtos

class Classifier:

    def __init__(self):
        self.dir = os.path.dirname(__file__) + "\\"
        # Modelo baseado em classificação de imagens
        self.models_dir = {"v3": self.dir + "modelV3", "v4": self.dir + "modelV4"}
        self.dim = (200, 200)
        self.cor_canal = 3
        self.cor_tam = 255
        self.img_form = self.dim + (self.cor_canal,)
        self.class_nomes = ["Roupa", "Calçado", "Headset"]
        self.models = {"v3": keras.models.load_model(self.models_dir["v3"]),
                       "v4": keras.models.load_model(self.models_dir["v4"])}

    # Classifica, retornando categoria

    def classificar(self, img):
        try:
            img = cv2.imread(img, cv2.IMREAD_COLOR)
            img = cv2.resize(img, self.dim)
            img = np.reshape(img, [1, self.dim[0], self.dim[1], 3])
            predict1 = list(self.models["v3"].predict(img))[0]
            predict2 = list(self.models["v4"].predict(img))[0]
            media = []
            for i in range(3):
                media.append((predict1[i] + predict2[i]) / 2)
            return self.class_nomes[media.index(max(media))]
        except Exception as exception:
            logger.salvar_log("classifier.py", exception)
