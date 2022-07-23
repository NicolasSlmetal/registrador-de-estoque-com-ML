import os.path
from urllib import request


dir = os.path.dirname(__file__) + "\\image\\"


def download(img_url):
    global dir
    try:
        request.urlretrieve(img_url, f"{dir}img.jpg")
    except Exception as error:
        if str(error).__contains__("403"):
            return "403"
        elif str(error).__contains__("401"):
            return "401"
        else:
            return "ERROR"
    else:
        return f"{dir}img.jpg"
