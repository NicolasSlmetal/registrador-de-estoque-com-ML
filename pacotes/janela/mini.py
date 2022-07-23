from tkinter import *
from pacotes.janela.default import Janela
import datetime


def str2int(n):
    if n[0] == "0":
        return int(n[1])
    else:
        return int(n)


def formatador_mask(data):
    mask = "a-%m-d% %h:%MM%"
    indexes2 = {"Ano": 'a', "Mês": '%m', "Dia": 'd%', "Hora": '%h', "Minutos": '%MM'}
    string = mask
    for k, v in data.items():
        string = string.replace(indexes2[k], v)
    for i in indexes2.values():
        string = string.replace(i, "%")
    string = string.strip()
    string.strip()
    string.replace(" ", "")
    return string

# Classe que cria janela para pesquisa de datas


class Mini(Janela):

    def __init__(self, geo, nome, main):
        super().__init__(geo, nome)
        self.var5 = None
        self.var4 = None
        self.cb5 = None
        self.cb4 = None
        self.cb3 = None
        self.cb2 = None
        self.cb1 = None
        self.main = main
        self.lbl5 = None
        self.lbl3 = None
        self.lbl4 = None
        self.lbl2 = None
        self.lbl6 = None
        self.mbox = None
        self.dbox = None
        self.ybox = None
        self.hbox = None
        self.mmbox = None
        self.win = None
        self.FEV = 28

    def iniciar(self):
        self.win = Tk()
        self.win.geometry(self.geometry)
        self.win.title(self.nome)
        self.var = BooleanVar()
        self.var2 = BooleanVar()
        self.var3 = BooleanVar()
        self.var4 = BooleanVar()
        self.var5 = BooleanVar()
        # Definindo valores dos spinboxes
        mm = [str(x) for x in range(0, 60)]
        h = [str(x) for x in range(0, 24)]
        d = [str(x) for x in range(1, 32)]
        m = [str(x) for x in range(1, 13)]
        y = [str(x) for x in range(2010, datetime.datetime.now().year + 1)]
        for x in range(0, 9):
            d[x] = f"0{d[x]}"
            m[x] = f"0{m[x]}"
        for x in range(0, 10):
            h[x] = f"0{h[x]}"
            mm[x] = f"0{mm[x]}"
        self.dbox = Spinbox(self.win, command=self.atualizar_horas, values=d)
        self.mbox = Spinbox(self.win, command=self.atualizar_dias, values=m)
        self.ybox = Spinbox(self.win, command=self.atualizar, values=y)
        self.hbox = Spinbox(self.win, command=self.atualizar_minutos, values=h)
        self.mmbox = Spinbox(self.win, values=mm)
        self.lbl1 = Label(self.win, text="Ano")
        self.lbl2 = Label(self.win, text="Mês")
        self.lbl3 = Label(self.win, text="Dia")
        self.lbl4 = Label(self.win, text="Hora")
        self.lbl5 = Label(self.win, text="Minutos")
        # Checkbuttons para verificar parâmetros de pesquisa
        self.cb1 = Checkbutton(self.win, text="Considerar", onvalue=True, offvalue=False, variable=self.var,
                               command=lambda: self._atualizar_var(0))
        self.cb2 = Checkbutton(self.win, text="Considerar", onvalue=True, offvalue=False, variable=self.var2,
                               command=lambda: self._atualizar_var(1))
        self.cb3 = Checkbutton(self.win, text="Considerar", onvalue=True, offvalue=False, variable=self.var3,
                               command=lambda: self._atualizar_var(2))
        self.cb4 = Checkbutton(self.win, text="Considerar", onvalue=True, offvalue=False, variable=self.var4,
                               command=lambda: self._atualizar_var(3))
        self.cb5 = Checkbutton(self.win, text="Considerar", onvalue=True, offvalue=False, variable=self.var5,
                               command=lambda: self._atualizar_var(4))
        self.lbl1.grid(row=0, column=0)
        self.ybox.grid(row=0, column=1)
        self.cb1.grid(row=0, column=2)
        self.lbl2.grid(row=1, column=0)
        self.mbox.grid(row=1, column=1)
        self.cb2.grid(row=1, column=2)
        self.lbl3.grid(row=2, column=0)
        self.dbox.grid(row=2, column=1)
        self.cb3.grid(row=2, column=2)
        self.lbl4.grid(row=3, column=0)
        self.hbox.grid(row=3, column=1)
        self.cb4.grid(row=3, column=2)
        self.lbl5.grid(row=4, column=0)
        self.mmbox.grid(row=4, column=1)
        self.cb5.grid(row=4, column=2)
        self.btnpesquisa = Button(self.win, text="Pesquisar", command=self.pesquisa)
        self.btnpesquisa.grid(row=6, column=1)
        self.win.protocol("WM_DELETE_WINDOW", self.encerrar)
        self.win.resizable(False, False)
        self.win.mainloop()

# Função associada aos checkbuttons. Atualiza suas vars

    def _atualizar_var(self, pos):
        assert type(pos) == int
        b_vars = [self.var, self.var2, self.var3, self.var4, self.var5]
        b_vars[pos].set(not b_vars[pos].get())

# Função que atualiza valores máximos com a seleção de um ano

    def atualizar(self):
        if self.ybox.get() != "":
            ano = int(self.ybox.get())
            if ano % 400 == 0 or (ano % 4 == 0 and ano % 100 != 0):
                self.FEV = 29
            else:
                self.FEV = 28
            if self.mbox.get() != "":
                self.atualizar_dias()
            if ano == datetime.datetime.now().year:
                m = [str(x) for x in range(1, datetime.datetime.now().month + 1)]
                for x in range(0, len(m)):
                    if len(m[x]) == 1:
                        m[x] = f"0{m[x]}"
            else:
                m = [str(x) for x in range(1, 13)]
                for x in range(0, len(m)):
                    if len(m[x]) == 1:
                        m[x] = f"0{m[x]}"
            self.mbox.configure(values=m)
            self.atualizar_dias()

# Ao atualizar o mês

    def atualizar_dias(self):
        mes = self.mbox.get()
        if mes != "":
            ano = self.ybox.get()
            if ano != "":
                ano = int(ano)
                if ano == datetime.datetime.now().year and str2int(mes) == datetime.datetime.now().month:
                    d = [str(x) for x in range(1, datetime.datetime.now().day + 1)]
                    for x in range(0, len(d)):
                        if len(d[x]) == 1:
                            d[x] = f"0{d[x]}"
                    self.dbox.configure(values=d)
                else:
                    meses = [["01", "03", "05", "07", "08", "10", "12"], ["04", "06", "09", "11"], ["02"]]
                    dias = [31, 30, self.FEV]
                    for i, ms in enumerate(meses):
                        if ms.count(mes) != 0:
                            d = [str(x) for x in range(1, dias[i] + 1)]
                            for x in range(0, len(d)):
                                if len(d[x]) == 1:
                                    d[x] = f"0{d[x]}"
                            self.dbox.configure(values=d)
                            break
                self.atualizar_horas()

# Ao atualizar o dia

    def atualizar_horas(self):
        if self.ybox.get() != "" and self.mbox.get() != "" and self.dbox.get() != "":
            ano = int(self.ybox.get())
            mes = str2int(self.mbox.get())
            dia = str2int(self.dbox.get())
            ano_atual = datetime.datetime.now().year
            mes_atual = datetime.datetime.now().month
            dia_atual = datetime.datetime.now().day
            if ano == ano_atual and mes == mes_atual and dia == dia_atual:
                h = [str(x) for x in range(0, datetime.datetime.now().hour + 1)]
                for x in range(0, len(h)):
                    if len(h[x]) == 1:
                        h[x] = f"0{h[x]}"
            else:
                h = [str(x) for x in range(0, 24)]
                for x in range(0, len(h)):
                    if len(h[x]) == 1:
                        h[x] = f"0{h[x]}"
            self.hbox.configure(values=h)
            self.atualizar_minutos()

# Ao atualizar a hora

    def atualizar_minutos(self):
        ano = self.ybox.get()
        mes = self.mbox.get()
        dia = self.dbox.get()
        hora = self.hbox.get()
        if ano != "" and mes != "" and dia != "" and hora != "":
            try:
                ano = int(ano)
                mes = str2int(mes)
                dia = str2int(dia)
                hora = str2int(hora)
            except TypeError:
                import tkinter.messagebox as mb
                mb.showwarning("Aviso", message="Não digite caracteres não númericos nas caixas de valores")
            ano_atual = datetime.datetime.now().year
            mes_atual = datetime.datetime.now().month
            dia_atual = datetime.datetime.now().day
            hora_atual = datetime.datetime.now().hour
            if ano == ano_atual and mes == mes_atual and dia == dia_atual and hora == hora_atual:
                mm = [str(x) for x in range(0, datetime.datetime.now().minute + 1)]
            else:
                mm = [str(x) for x in range(0, 60)]
            for x in range(0, len(mm)):
                if len(mm[x]) == 1:
                    mm[x] = f"0{mm[x]}"
            self.mmbox.configure(values=mm)

    def encerrar(self):
        self.win.destroy()
        self.win = None

    def pesquisa(self):
        import tkinter.messagebox as mb
        info = [self.ybox.get(), self.mbox.get(), self.dbox.get(), self.hbox.get(), self.mmbox.get()]
        verify = list(filter(lambda x: str(x).isnumeric() or str(x)[1:].isnumeric(), info))
        if len(verify) < 5:
            mb.showwarning("Aviso", message="Não digite valores não númericos")
            self.encerrar()
        else:
            checks = [self.var.get(), self.var2.get(), self.var3.get(), self.var4.get(), self.var5.get()]
            # Um dos checks deve ser True
            if checks.count(False) == 5:
                mb.showwarning("Aviso", message="Indique o valor de pelo menos um campo")
                self.encerrar()
            else:
                itens = ["Ano", "Mês", "Dia", "Hora", "Minutos"]
                data = {}
                for i, v in enumerate(checks):
                    # Se usuário deixou parâmetro como True
                    if v:
                        data[itens[i]] = info[i]
                # Selecionando as datas do DB
                datas = self.db.read_date(self.main.parse_vl[self.main.cbox.get()])
                split_data = []
                for data_ in datas:
                    # Até a hora
                    split = data_[0][0:19].split()
                    data_atual = []
                    # Organizando primeira parte[????-??-??]
                    for s in split[0].split("-"):
                        data_atual.append(s)
                    # Organizando segunda parte [??:??]
                    for s in split[1].split(":"):
                        data_atual.append(s)
                    data_atual.pop()
                    split_data.append(data_atual)
                indexes = {"Ano": 0, "Mês": 1, "Dia": 2, "Hora": 3, "Minutos": 4}
                founds = []
                for data_ in split_data:
                    count = 0
                    for k, v in data.items():
                        # Verifica se todos os valores são iguais
                        if data_[indexes[k]] == v:
                            count += 1
                        # Verifica se todos correspondem
                        if count == len(data.keys()):
                            founds.append(data_)
                where = self.main.parse_vl[self.main.cbox.get()]
                geral = []
                for item in founds:
                    for k, v in data.items():
                        if item[indexes[k]] == v:
                            # Adiciona valores comuns entre as datas
                            if geral.count(v) == 0:
                                geral.append(v)
                # Máscara de formatação
                string = formatador_mask(data)
                dataformat = f"%d/%m/%Y - %H:%M"
                self.main.tv.delete(*self.main.tv.get_children())
                for (n, d, c, p, c2, de, df, qtd) in self.db.read_where(where, "", string):
                    dataent = datetime.datetime.fromisoformat(de).strftime(dataformat)
                    datafab = datetime.datetime.fromisoformat(df).strftime(dataformat)
                    self.main.tv.insert("", "end", values=(n, d, c, p, c2, dataent, datafab, qtd))
                # Encerra a mini janela
                self.win.destroy()
                self.win = None




