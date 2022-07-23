import datetime
import os.path
import sys
from tkinter import *
import tkinter.ttk
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox
from pacotes.SQLgerenciador.CRUD import CRUDexec
from pacotes.cameralistener.capturador import Capturador
import ctypes
import cv2

# Classe que cria janela principal


class Janela:

    def __init__(self, geo, nom):
        self.scaleqtd = None
        self.btndel = None
        self.entrycod = None
        self.lblfrdel = None
        self.btnlimpar_pesquisa = None
        self.var = None
        self.var2 = None
        self.var3 = None
        self.btnimg = None
        self.entryimg = None
        self.btnpesquisa = None
        self.entry_sch = None
        self.cbox = None
        self.lblfr = None
        self.btn = None
        self.tv = None
        self.win = None
        self.camera = None
        self.fr2 = None
        self.lbl1 = None
        self.fr1 = None
        self.notebook = None
        self.geometry = geo
        self.nome = nom
        self.db = CRUDexec()
        self.values = ["Nome", "Distribuidor", "Categoria", "Preço", "Código",  "Data de entrada", "Data de fabricação",
                       "Quantidade"]
        self.parse_vl = {"Nome": "nome", "Distribuidor": "distribuidor", "Categoria": "categoria", "Preço": "preco",
                         "Código": "codigo", "Data de entrada": "data_entrada", "Data de fabricação": "data_fab",
                         "Quantidade": "qtd"}
        self.icon = os.path.dirname(__file__).replace("janela", "utils\\icons\\icon.ico")
        self.win = None
        self.mini = None

# Inicialização de janela

    def iniciar(self):
        self.win = Tk()
        self.var2 = StringVar()
        self.var3 = StringVar()
        self.win.geometry(self.geometry)
        self.win.title(self.nome)
        self.win.configure(background="#fff")
        self.notebook = tkinter.ttk.Notebook(self.win)
        # Frame onde fica a câmera
        self.fr1 = Frame(self.notebook, relief="sunken", bg="#fff")
        # Label que armazenará a imagem da câmera
        self.lbl1 = Label(self.fr1)
        self.var2.set("Caminho da imagem")
        # Entry que exibe caminho da imagem do produto
        self.entryimg = Entry(self.fr1, bg="#fff", textvariable=self.var2, state="disabled")
        self.entryimg.place(x=220, y=100, width=300, height=30, anchor=CENTER)
        # Botão que seleciona arquivo
        self.btnimg = Button(self.fr1, command=self.anexar_img, text="Anexar")
        self.btnimg.place(x=400, y=85, width=150, height=30)
        self.lbl1.place(x=300, y=300, width=280, height=280, anchor=CENTER)
        # Frame que exibe os produtos registrados
        self.fr2 = Frame(self.notebook, relief="sunken", bg="#fff")
        # Treeview que apresenta os produtos
        self.tv = Treeview(self.fr2, columns=("Nome", "Distribuidor", "Categoria", "Preço", "Código", "Data de entrada",
                                              "Data de fabricação", 'Quantidade'), show="headings")
        self.tv.column("Nome", minwidth=0, width=100)
        self.tv.column("Distribuidor", minwidth=0, width=100)
        self.tv.column("Categoria", minwidth=0, width=100)
        self.tv.column("Preço", minwidth=0, width=100)
        self.tv.column("Código", minwidth=0, width=100)
        self.tv.column("Data de entrada", minwidth=0, width=160)
        self.tv.column("Data de fabricação", minwidth=0, width=160)
        self.tv.column("Quantidade", minwidth=0, width=100)
        self.tv.heading("Nome", text="Nome")
        self.tv.heading("Distribuidor", text="Distribuidor")
        self.tv.heading("Categoria", text="Categoria")
        self.tv.heading("Preço", text="Preço")
        self.tv.heading("Código", text="Código")
        self.tv.heading("Data de entrada", text="Data de entrada")
        self.tv.heading("Data de fabricação", text="Data de fabricação")
        self.tv.heading("Quantidade", text="Quantidade")
        # Movimentação horizontal de TV
        scrollx = tkinter.ttk.Scrollbar(self.fr2, orient=HORIZONTAL, command=self.tv.xview)
        self.tv.configure(xscrollcommand=scrollx.set)
        scrollx.place(x=290, y=230, width=593, height=10, anchor=CENTER)
        # Movimentação vertical de TV
        scrolly = tkinter.ttk.Scrollbar(self.fr2, orient=VERTICAL, command=self.tv.yview)
        self.tv.configure(yscrollcommand=scrolly.set)
        scrolly.place(x=587, y=0, width=10, height=235)
        self.tv.place(x=0, y=0, width=590, height=230)
        self.notebook.add(self.fr1, text="Escanear")
        self.notebook.add(self.fr2, text="Registro")
        self.notebook.place(x=0, y=0, width=700, height=700)
        self.camera = Capturador(self.lbl1)
        self.camera.obtercamera()
        # Botão que atualiza valores de TV
        self.btn = Button(self.fr2, command=self.obterprodutos, text="Atualizar", font=("Times New Roman", 20))
        self.btn.place(x=270, y=260, width=800, height=50, anchor=CENTER)
        # LabelFrame de pesquisa
        self.lblfr = LabelFrame(self.fr2, text="Pesquisa", font=("Times New Roman", 20))
        # LabelFrame de remoção
        self.lblfrdel = LabelFrame(self.fr2, text="Remover", font=("Times New Roman", 20))
        # Botão que remove quantidades informadas no scaleqtd
        self.btndel = Button(self.lblfrdel, text="Remover", command=self.remover)
        # Scale que determina quantidade de produto a ser removida
        self.scaleqtd = Scale(self.lblfrdel, orient="horizontal", sliderrelief="sunken")
        self.lblfrdel.place(x=280, y=320, width=200, height=210)
        self.btndel.place(x=10, y=80, height=30, width=150)
        self.scaleqtd.place(x=10, y=10, width=150, height=40)
        self.lblfr.place(x=40, y=320, width=200, height=210)
        # Combobox com as categorias
        self.cbox = Combobox(self.lblfr, values=self.values, postcommand=self.show_window_date)
        self.cbox.pack()
        # Entry para pesquisa
        self.entry_sch = Entry(self.lblfr, textvariable=self.var3)
        self.entry_sch.place(x=10, y=50, width=180, height=20)
        # Botão para pesquisa
        self.btnpesquisa = Button(self.lblfr, command=self.pesquisa, text="Pesquisar")
        self.btnpesquisa.place(x=10, y=90, width=70, height=50)
        # Botão para limpar pesquisa
        self.btnlimpar_pesquisa = Button(self.lblfr, command=self.limpar, text="Limpar")
        self.btnlimpar_pesquisa.place(x=110, y=90, width=70, height=50)
        self.obterprodutos()
        # Manter dimensionamento padrão
        self.win.resizable(False, False)
        # Ícone do aplicativo
        img = BitmapImage(self.icon)
        self.win.iconbitmap(False, img)
        self.win.protocol("WM_DELETE_WINDOW", self.encerrar)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("etec.registrador.estoque.1.0")
        self.win.mainloop()

# Função para pesquisa, atribuída ao btnpesquisa

    def pesquisa(self):
        from tkinter import messagebox as mb
        if len(self.cbox.get()) > 0:
            dataformat = f"%d/%m/%Y - %H:%M"
            if self.cbox.get() in self.values:
                self.tv.delete(*self.tv.get_children())
                pesquisa = self.db.read_where(self.parse_vl[self.cbox.get()], self.entry_sch.get())
                for (n, d, c, p, c2, de, df, qtd) in pesquisa:
                    dataent = datetime.datetime.fromisoformat(de).strftime(dataformat)
                    datafab = datetime.datetime.fromisoformat(df).strftime(dataformat)
                    self.tv.insert("", "end", values=(n, d, c, p, c2, dataent, datafab, qtd))
            else:
                mb.showwarning("Aviso", "Digite opções válidas na caixa de seleção")
                self.cbox.set("")
                self.entry_sch.delete(0, END)

        else:
            mb.showwarning("Aviso", message="Selecione uma opção de pesquisa")
            self.cbox.set("")
            self.entry_sch.delete(0, END)

# Função para atualizar o TV, atribuída ao btnatualizar

    def obterprodutos(self):
        self.tv.delete(*self.tv.get_children())
        dataformat = f"%d/%m/%Y - %H:%M"
        for (n, d, c, p, c2, de, df, qtd) in self.db.read():
            dataent = datetime.datetime.fromisoformat(de).strftime(dataformat)
            datafab = datetime.datetime.fromisoformat(df).strftime(dataformat)
            self.tv.insert("", "end", values=(n, d, c, p, c2, dataent, datafab, qtd))
        qtds = []
        for dados in self.db.read():
            qtds.append(dados[len(dados) - 1])
        if len(qtds) > 0:
            self.scaleqtd.configure(from_=1, to=max(qtds))
        else:
            self.scaleqtd.configure(from_=1, to=10)

# Função para anexar imagem, atribuída ao btnimg

    def anexar_img(self):
        from tkinter.filedialog import askopenfilename
        from tkinter import messagebox as mb
        Tk().withdraw()
        file = askopenfilename()
        extval = False
        for ext in ("jpg", "png"):
            if file.endswith(ext):
                extval = True
                break
        if extval:
            self.var2.set(file)
            self.camera.imgpath = file
            self.entryimg.update()
        else:
            mb.showwarning(title="Aviso", message="Selecione um arquivo com extensão válida")

# Função que remove produtos de acordo com quantidade, atribuída ao btndel

    def remover(self):
        import tkinter.messagebox as mb
        valor = self.tv.selection()
        if len(valor) > 0:
            valor = self.tv.item(valor[0], option="values")
            # Se valor maior que scaleqtd.get(), apenas atualiza a quantidade
            if self.scaleqtd.get() < int(valor[len(valor) - 1]):
                self.db.update_qtd(int(valor[len(valor) - 1]) - self.scaleqtd.get(), valor[4])
            elif self.scaleqtd.get() > int(valor[len(valor) - 1]):
                mb.showwarning("Aviso", message="O valor excede a quantidade desse produto")
                self.scaleqtd.set(1)
            # Se valor == scale.get(), remove o produto do estoque
            else:
                self.db.deletar(valor[4])
            self.obterprodutos()
        else:
            mb.showwarning(title="Aviso", message="Selecione um produto na tabela")

# Função de limpeza de pesquisa, atribuída ao btnlimpar

    def limpar(self):
        self.cbox.set("")
        self.var3.set("")
        self.obterprodutos()

# Função associada ao cbox, ativa uma janela para pesquisa de datas

    def show_window_date(self):
        from pacotes.janela.mini import Mini
        if self.mini is None:
            self.mini = Mini("300x200", "Data", self)
        if self.cbox.get() == "Data de entrada" or self.cbox.get() == "Data de fabricação":
            if self.mini.win is None:
                self.entry_sch.configure(state="disabled")
                self.mini.iniciar()
        else:
            self.entry_sch.configure(state="normal")
            if self.mini.win is not None:
                self.mini.encerrar()

    def encerrar(self):
        self.lbl1.destroy()
        self.win.destroy()
        cv2.destroyAllWindows()
        sys.exit()
