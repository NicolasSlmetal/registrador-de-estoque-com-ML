import math


# Formatação de valores

def formatar(valor):
    decimal_ = valor - math.floor(valor)
    if decimal_ < 0.5:
        hundred = math.floor(decimal_ * 100)
    else:
        hundred = math.ceil(decimal_ * 100)
    print(hundred)
    if decimal_ == 0.0:
        return f"R${str(valor).replace('.', ',')}0"
    elif hundred % 10 == 0:
        return f"R${str(valor).replace('.', ',')}0"
    else:
        return f"R${str(valor).replace('.', ',')}"
