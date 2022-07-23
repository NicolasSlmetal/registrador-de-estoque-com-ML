import datetime


# Conversão de string para dictionary
# string deve seguir o padrão: {Nome: XXXX, Distribuidor: XXXX, Data de fabricacao: Objeto datetime
# , Preco: XX.XX (float), Quantidade: XXXX (int)}


def str2dict(string):
    string = str(string.replace("(", "").replace(")", "").replace("datetime.", "").replace("datetime", "")).replace("'", "")
    datastring = string[string.index("Data de fabricacao"):string.index("Preco")]
    string = string.replace(datastring, "")
    datasplit = datastring.split(":")
    datasplit.append(datasplit.pop().replace(" ", "").split(","))
    data = datetime.datetime.replace(datetime.datetime.now(), int(datasplit[1][0]), int(datasplit[1][1]),
                                     int(datasplit[1][2]), int(datasplit[1][3]), int(datasplit[1][4]),
                                     int(datasplit[1][5]), int(datasplit[1][6]))
    dict_ = {datasplit[0]: data}
    splitstring = string.replace("{", "").replace("}", "").split(",")
    for item in splitstring:
        item = item.split(":")
        dict_[item[0].strip()] = item[1].strip()
    return dict_
