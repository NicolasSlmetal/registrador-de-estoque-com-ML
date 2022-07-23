import os
import datetime


# Salva logs para verificação de erros

def salvar_log(class_nome, exception):
    file = open(os.path.dirname(__file__) + "\\logs\\logs.txt", "a")
    file.writelines(f"[{datetime.datetime.now()}] Exception in {class_nome} - {exception}\n")
    file.close()
