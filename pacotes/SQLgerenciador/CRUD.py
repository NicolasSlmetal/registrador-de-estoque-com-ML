import os
import sqlite3
from sqlite3 import Error
from pacotes.utils import logger


# Classe que executa operações ao DB

class CRUDexec:
    def __init__(self):
        self.path = os.path.dirname(__file__) + "\\database\\database.db"
        self.sql = None

# Conexão ao DB

    def conectar(self):
        try:
            self.sql = sqlite3.connect(self.path)
            return True
        except Error as e:
            logger.salvar_log("CRUD.py" f"CONNECT - {e}")
            return False

# Adicionar produto

    def adicionar(self, produto):
        from pacotes.utils import currency
        if self.conectar():
            query = f"""INSERT INTO 'produtos' (nome, distribuidor, categoria, 
            preco, codigo, data_entrada, data_fab, qtd) VALUES(
                '{produto['Nome']}', '{produto['Distribuidor']}', 
                '{produto['Categoria']}', '{currency.formatar(float(produto['Preco']))}', 
                '{produto['Codigo']}', '{produto['Data de entrada']}',
                '{produto['Data de fabricacao']}', {produto['Quantidade']})"""
            try:
                cursor = self.sql.cursor()
                cursor.execute(query)
                self.sql.commit()
                cursor.close()
            except Error as e:
                logger.salvar_log("CRUD.py" f"ADD - {e}")
            finally:
                self.sql.close()

# Selecionar todos

    def read(self):
        if self.conectar():
            query = """SELECT * FROM 'produtos'"""
            try:
                cursor = self.sql.cursor()
                con = cursor.execute(query)
                produtos = con.fetchall()
                con.close()
                cursor.close()
                return produtos
            except Error as e:
                logger.salvar_log("CRUD.py" f"READ - {e}")
                return None
            finally:
                self.sql.close()

# Deletar de acordo com código

    def deletar(self, codigo):
        correspondente = list(self.code_read(f"""SELECT * FROM 'produtos' WHERE codigo='{codigo}'"""))
        if len(correspondente) == 0:
            raise NameError(f"Código inválido, nenhum produto registrado com \033[33m{codigo}\033[m")
        query = f"""DELETE FROM 'produtos' WHERE codigo='{codigo}'"""
        if self.conectar():
            try:
                cursor = self.sql.cursor()
                cursor.execute(query)
                self.sql.commit()
                cursor.close()
            except Error as e:
                logger.salvar_log("CRUD.py" f"DEL - {e}")
            finally:
                self.sql.close()

# Selecionar produto com código

    def code_read(self, query):
        if self.conectar():
            try:
                cursor = self.sql.cursor()
                con = cursor.execute(query)
                produtos = con.fetchall()
                con.close()
                cursor.close()
                return produtos
            except Error as e:
                logger.salvar_log("CRUD.py" f"READ CODE - {e}")
                return None
            finally:
                self.sql.close()

# Selecionar com parâmetro opcional

    def read_where(self, param, valor, mask=f"%a%"):
        if self.conectar():
            query = f"""SELECT * FROM 'produtos' WHERE {param} LIKE '{mask.replace('a', valor)}'"""
            try:
                cursor = self.sql.cursor()
                con = cursor.execute(query)
                produtos = con.fetchall()
                return produtos
            except Error as e:
                logger.salvar_log("CRUD.py" f"READ WHERE - {e}")
            finally:
                self.sql.close()

# Atualizar quantidades

    def update_qtd(self, valor, codigo):
        if self.conectar():
            query = f"""UPDATE 'produtos' SET qtd={valor} WHERE codigo='{codigo}'"""
            try:
                cursor = self.sql.cursor()
                con = cursor.execute(query)
                self.sql.commit()
            except Error as e:
                logger.salvar_log("CRUD.py" f"UPDATE - {e}")
            finally:
                self.sql.close()

# Selecionar data_fab ou data_entrada de todos os produtos

    def read_date(self, data):
        if self.conectar():
            try:
                query = f"""SELECT {data} FROM 'produtos'"""
                cursor = self.sql.cursor()
                con = cursor.execute(query)
                datas = con.fetchall()
                return datas
            except Error as e:
                logger.salvar_log("CRUD.py", f"READ DATA - {e}")
            finally:
                self.sql.close()