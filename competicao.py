import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import time

"""
Programa: Gerenciador de Pesagens de Temperos
Versão: 1.0
Autor: Diego Mattos

Descrição:
Este programa foi desenvolvido para gerenciar as pesagens de diferentes tipos de temperos por funcionários. 
Ele permite o cadastro de funcionários e temperos, a realização de registros diários de pesagens, 
e a geração de rankings mensais com base na quantidade total pesada, ajustada pela dificuldade de cada tempero.
Também oferece funcionalidades para exportação de dados para Excel, filtragem dinâmica de cadastros, 
e uma interface gráfica interativa e amigável.

Funcionalidades Principais:
- Cadastro de funcionários e temperos.
- Registro de pesagens diárias.
- Geração e exibição de rankings mensais.
- Exportação de dados para Excel.
- Filtragem dinâmica de funcionários e temperos cadastrados.
- Animação na interface principal para melhor experiência do usuário.

Este software foi desenvolvido para proporcionar um controle eficiente e fácil de usar, 
com uma interface gráfica que torna o processo de registro e análise de pesagens intuitivo e acessível.
"""


# Usuário e senha fixos para o login administrativo
ADMIN_USER = "diego"
ADMIN_PASS = "diego"

def init_db():
    conn = sqlite3.connect('pesagens.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Temperos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        dificuldade FLOAT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pesagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcionario_id INTEGER,
        tempero_id INTEGER,
        quantidade INTEGER,
        data TEXT,
        horario TEXT,
        FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id),
        FOREIGN KEY (tempero_id) REFERENCES Temperos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ciclo (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        ativo INTEGER NOT NULL,
        inicio_disputa TEXT
    )
    ''')

    cursor.execute("INSERT OR IGNORE INTO Ciclo (id, ativo) VALUES (1, 0)")

    conn.commit()
    conn.close()
    
# Splashscreen function
def show_splashscreen():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)
    #splash_root.geometry("700x500")
    
    # Define a largura e altura do splashscreen
    splash_width = 700
    splash_height = 500

    # Obtém a largura e altura da tela
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()

    # Calcula a posição x, y para centralizar a janela
    x = (screen_width // 2) - (splash_width // 2)
    y = (screen_height // 2) - (splash_height // 2)

    splash_root.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

    # Adicione sua imagem de splash
    splash_image = Image.open("splash_image.png")
    splash_photo = ImageTk.PhotoImage(splash_image)
    splash_label = tk.Label(splash_root, image=splash_photo)
    splash_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Texto de descrição
    """
    description_text = '''
    Iniciando Gerenciador de Pesagens de Temperos...

    Projeto desenvolvido para facilitar o controle das pesagens de temperos por funcionários.
    Utilizando as seguintes tecnologias:
    - Tkinter para a interface gráfica
    - Pandas para manipulação e exportação de dados
    - SQLite3 para armazenamento de dados
    - PIL para manipulação de imagens
    - Datetime para controle de datas e horas
    '''
    Carregando, por favor aguarde...
    
    description_label = tk.Label(splash_root, text=description_text, justify=tk.LEFT, font=("Helvetica", 10), bg="white")
    description_label.place(x=20, y=20, width=splash_width // 2 - 40)
    """
    # Barra de progresso
    progress = ttk.Progressbar(splash_root, orient="horizontal", mode="determinate", length=splash_width - 40)
    progress.place(x=20, y=splash_height - 30)

    # Customizar a barra de progresso para ser branca e fininha
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TProgressbar", troughcolor='white', background='orange', thickness=5)


    # Animação de fade-in
    alpha = 0
    while alpha < 1:
        splash_root.attributes("-alpha", alpha)
        splash_root.update()
        time.sleep(0.01)
        alpha += 0.01
        
    # Atualização da barra de progresso
    for i in range(100):
        progress['value'] = i + 1
        splash_root.update()
        time.sleep(0.02)

    time.sleep(3)  # Mantém o splashscreen por 1 segundo após completar a barra de progresso

    # Animação de fade-out
    while alpha > 0:
        splash_root.attributes("-alpha", alpha)
        splash_root.update()
        time.sleep(0.01)
        alpha -= 0.01

    splash_root.destroy()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Pesagens")
        
        # Define a largura e altura da janela principal
        app_width = 800
        app_height = 600

        # Obtém a largura e altura da tela
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calcula a posição x, y para centralizar a janela
        x = (screen_width // 2) - (app_width // 2)
        y = (screen_height // 2) - (app_height // 2)

        root.geometry(f"{app_width}x{app_height}+{x}+{y}")

        # Adicionando imagem de fundo
        self.background_image = Image.open("background.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)
        
        bold_font = ("Helvetica", 10, "bold")

        # Container principal
        self.container = tk.Frame(root, bg='white')
        self.container.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Adicionar título "Controle de Produção" no topo
        title_label = tk.Label(self.container, text="Controle de Produção", font=("Helvetica", 24, "bold"), fg="black")
        title_label.pack(side=tk.TOP, pady=20)
        
        # Área de botões especiais - Certifique-se de que este frame é criado corretamente
        self.frame_botoes_especiais = tk.Frame(self.container, bg='#ffffff')
        self.frame_botoes_especiais.pack(pady=10, fill=tk.X)


        # Adicionar/remover funcionários
        self.frame_funcionarios = tk.Frame(self.container, bg='white')
        self.frame_funcionarios.pack(pady=10)

        tk.Label(self.frame_funcionarios, text="Nome do Funcionário:", bg='white',font=bold_font).grid(row=0, column=0)
        self.nome_funcionario = tk.Entry(self.frame_funcionarios)
        self.nome_funcionario.grid(row=0, column=1)
        tk.Button(self.frame_funcionarios, text="Cadastrar Funcionário", font=bold_font, command=self.login_admin_funcionario).grid(row=0, column=2)
        tk.Button(self.frame_funcionarios, text="Remover Funcionário",font=bold_font, command=self.login_admin_remove_funcionario).grid(row=0, column=3)

        # Adicionar/remover temperos
        self.frame_temperos = tk.Frame(self.container, bg='white')
        self.frame_temperos.pack(pady=10)

        tk.Label(self.frame_temperos, text="Nome do Tempero:", bg='white', font=bold_font).grid(row=0, column=0)
        self.nome_tempero = tk.Entry(self.frame_temperos)
        self.nome_tempero.grid(row=0, column=1)
        tk.Label(self.frame_temperos, text="Dificuldade:", bg='white', font=bold_font).grid(row=1, column=0)
        self.dificuldade_tempero = tk.Entry(self.frame_temperos)
        self.dificuldade_tempero.grid(row=1, column=1)
        tk.Button(self.frame_temperos, text="Cadastrar Tempero",font=bold_font, command=self.login_admin_tempero).grid(row=0, column=2)
        tk.Button(self.frame_temperos, text="Remover Tempero", font=bold_font, command=self.login_admin_remove_tempero).grid(row=0, column=3)

        # Registrar pesagens
        self.frame_pesagens = tk.Frame(self.container, bg='white')
        self.frame_pesagens.pack(pady=10)

        tk.Label(self.frame_pesagens, text="Funcionário:", bg='white', font=bold_font).grid(row=0, column=0)
        self.funcionario_pesagem = ttk.Combobox(self.frame_pesagens, values=self.get_funcionarios())
        self.funcionario_pesagem.grid(row=0, column=1)

        tk.Label(self.frame_pesagens, text="Tempero:", bg='white', font=bold_font).grid(row=1, column=0)
        self.tempero_pesagem = ttk.Combobox(self.frame_pesagens, values=self.get_temperos())
        self.tempero_pesagem.grid(row=1, column=1)

        tk.Label(self.frame_pesagens, text="Quantidade (UN):", bg='white', font=bold_font).grid(row=2, column=0)
        self.quantidade_pesagem = tk.Entry(self.frame_pesagens)
        self.quantidade_pesagem.grid(row=2, column=1)

        tk.Label(self.frame_pesagens, text="Data (DIA/MES/ANO):", bg='white', font=bold_font).grid(row=3, column=0)
        self.data_pesagem = tk.Entry(self.frame_pesagens)
        self.data_pesagem.grid(row=3, column=1)
        self.data_pesagem.insert(0, datetime.now().strftime("%d/%m/%Y"))

        self.btn_registrar = tk.Button(self.frame_pesagens, text="Registrar Pesagem", font=bold_font, command=self.registrar_pesagem)
        self.btn_registrar.grid(row=4, column=0, columnspan=2)

        #self.check_ciclo()

        # Calcular campeão mensal
        self.frame_campeao = tk.Frame(self.container, bg='white')
        self.frame_campeao.pack(pady=10)

        ano_mes_atual = datetime.now().strftime("%Y-%m")
        tk.Label(self.frame_campeao, text=f"Mês (padrão: {ano_mes_atual}):", bg='white').grid(row=0, column=0)
        self.mes_campeao = tk.Entry(self.frame_campeao)
        self.mes_campeao.insert(0, ano_mes_atual)
        self.mes_campeao.grid(row=0, column=1)
        tk.Button(self.frame_campeao, text="Mostrar Ranking", bg="white",  font=bold_font, command=self.calcular_ranking).grid(row=0, column=2)
        reset_button = tk.Button(self.frame_campeao, text="Resetar Banco de Dados", font=bold_font, command=self.login_admin_reset_bd, bg="red", fg="white")
        reset_button.grid(row=0, column=3)
        
        #Exportar dados para planilha
        tk.Button(self.frame_pesagens, text="Exportar para Excel", bg="green",  font=bold_font, command=self.exportar_para_excel).grid(row=6, column=0, columnspan=3)

        # Remover pesagens
        self.frame_remover = tk.Frame(self.container, bg='white')
        self.frame_remover.pack(pady=10)

        tk.Button(self.frame_remover, text="Remover Registro de Pesagem", bg="orange", font=bold_font, command=self.remover_pesagem).pack()

        # Adicionar o botão na interface principal para mostrar cadastros
        cadastro_button = tk.Button(self.frame_botoes_especiais, text="Mostrar Cadastros", command=self.mostrar_cadastros, 
                                        bg="blue", fg="white", width=20, height=2)
        cadastro_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Rodapé
        tk.Label(root, text="Aplicativo desenvolvido por Diego Matos", bg='white').pack(side=tk.BOTTOM, pady=10)

    def get_funcionarios(self):
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM Funcionarios")
        funcionarios = cursor.fetchall()
        conn.close()
        return [funcionario[0].capitalize() for funcionario in funcionarios]

    def get_temperos(self):
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM Temperos")
        temperos = cursor.fetchall()
        conn.close()
        return [tempero[0].capitalize() for tempero in temperos]

    def check_login(self, username, password):
        return username == ADMIN_USER and password == ADMIN_PASS

    def login_admin_funcionario(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login Administrativo")

        tk.Label(self.login_window, text="Usuário:").grid(row=0, column=0)
        self.login_usuario = tk.Entry(self.login_window)
        self.login_usuario.grid(row=0, column=1)

        tk.Label(self.login_window, text="Senha:").grid(row=1, column=0)
        self.login_senha = tk.Entry(self.login_window, show="*")
        self.login_senha.grid(row=1, column=1)

        tk.Button(self.login_window, text="Login", command=self.check_login_funcionario).grid(row=2, column=0, columnspan=2)

    def check_login_funcionario(self):
        if self.check_login(self.login_usuario.get(), self.login_senha.get()):
            self.login_window.destroy()
            self.confirm_add_funcionario()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def login_admin_remove_funcionario(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login Administrativo")

        tk.Label(self.login_window, text="Usuário:").grid(row=0, column=0)
        self.login_usuario = tk.Entry(self.login_window)
        self.login_usuario.grid(row=0, column=1)

        tk.Label(self.login_window, text="Senha:").grid(row=1, column=0)
        self.login_senha = tk.Entry(self.login_window, show="*")
        self.login_senha.grid(row=1, column=1)

        tk.Button(self.login_window, text="Login", command=self.check_login_remove_funcionario).grid(row=2, column=0, columnspan=2)

    def check_login_remove_funcionario(self):
        if self.check_login(self.login_usuario.get(), self.login_senha.get()):
            self.login_window.destroy()
            self.remove_funcionario()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def login_admin_tempero(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login Administrativo")

        tk.Label(self.login_window, text="Usuário:").grid(row=0, column=0)
        self.login_usuario = tk.Entry(self.login_window)
        self.login_usuario.grid(row=0, column=1)

        tk.Label(self.login_window, text="Senha:").grid(row=1, column=0)
        self.login_senha = tk.Entry(self.login_window, show="*")
        self.login_senha.grid(row=1, column=1)

        tk.Button(self.login_window, text="Login", command=self.check_login_tempero).grid(row=2, column=0, columnspan=2)

    def check_login_tempero(self):
        if self.check_login(self.login_usuario.get(), self.login_senha.get()):
            self.login_window.destroy()
            self.confirm_add_tempero()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def login_admin_remove_tempero(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login Administrativo")

        tk.Label(self.login_window, text="Usuário:").grid(row=0, column=0)
        self.login_usuario = tk.Entry(self.login_window)
        self.login_usuario.grid(row=0, column=1)

        tk.Label(self.login_window, text="Senha:").grid(row=1, column=0)
        self.login_senha = tk.Entry(self.login_window, show="*")
        self.login_senha.grid(row=1, column=1)

        tk.Button(self.login_window, text="Login", command=self.check_login_remove_tempero).grid(row=2, column=0, columnspan=2)

    def check_login_remove_tempero(self):
        if self.check_login(self.login_usuario.get(), self.login_senha.get()):
            self.login_window.destroy()
            self.remove_tempero()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def login_admin_reset_bd(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login Administrativo")

        tk.Label(self.login_window, text="Usuário:").grid(row=0, column=0)
        self.login_usuario = tk.Entry(self.login_window)
        self.login_usuario.grid(row=0, column=1)

        tk.Label(self.login_window, text="Senha:").grid(row=1, column=0)
        self.login_senha = tk.Entry(self.login_window, show="*")
        self.login_senha.grid(row=1, column=1)

        tk.Button(self.login_window, text="Login", command=self.check_login_reset_bd).grid(row=2, column=0, columnspan=2)

    def check_login_reset_bd(self):
        if self.check_login(self.login_usuario.get(), self.login_senha.get()):
            self.login_window.destroy()
            self.resetar_bd()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def confirm_add_funcionario(self):
        nome = self.nome_funcionario.get().strip().capitalize()
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira o nome do funcionário.")
            return
        if nome in [f.capitalize() for f in self.get_funcionarios()]:
            messagebox.showerror("Erro", "Funcionário já cadastrado.")
            return
        confirm = messagebox.askyesno("Confirmação", f"Você deseja cadastrar o funcionário {nome}?")
        if confirm:
            self.add_funcionario(nome)

    def add_funcionario(self, nome):
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Funcionarios (nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()
        self.funcionario_pesagem['values'] = self.get_funcionarios()
        self.nome_funcionario.delete(0, tk.END)  # Limpa o campo de input
        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso")

    def remove_funcionario(self):
        nome = self.nome_funcionario.get().strip().capitalize()
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira o nome do funcionário.")
            return
        if nome not in [f.capitalize() for f in self.get_funcionarios()]:
            messagebox.showerror("Erro", "Funcionário não encontrado.")
            return
        confirm = messagebox.askyesno("Confirmação", f"Você deseja remover o funcionário {nome}?")
        if confirm:
            conn = sqlite3.connect('pesagens.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Funcionarios WHERE nome = ?", (nome,))
            conn.commit()
            conn.close()
            self.funcionario_pesagem['values'] = self.get_funcionarios()
            self.nome_funcionario.delete(0, tk.END) # Limpa o campo input
            messagebox.showinfo("Sucesso", "Funcionário removido com sucesso")

    def confirm_add_tempero(self):
        nome = self.nome_tempero.get().strip().capitalize()
        dificuldade = self.dificuldade_tempero.get()
        if not nome or not dificuldade:
            messagebox.showerror("Erro", "Por favor, insira o nome e a dificuldade do tempero.")
            return
        if nome in [t.capitalize() for t in self.get_temperos()]:
            messagebox.showerror("Erro", "Tempero já cadastrado.")
            return
        confirm = messagebox.askyesno("Confirmação", f"Você deseja cadastrar o tempero {nome} com dificuldade {dificuldade}?")
        if confirm:
            self.add_tempero(nome, dificuldade)

    def add_tempero(self, nome, dificuldade):
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Temperos (nome, dificuldade) VALUES (?, ?)", (nome, dificuldade))
        conn.commit()
        conn.close()
        self.tempero_pesagem['values'] = self.get_temperos()
        self.nome_tempero.delete(0, tk.END)  # Limpa o campo de input
        self.dificuldade_tempero.delete(0, tk.END)  # Limpa o campo de input
        messagebox.showinfo("Sucesso", "Tempero cadastrado com sucesso")

    def remove_tempero(self):
        nome = self.nome_tempero.get().strip().capitalize()
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira o nome do tempero.")
            return
        if nome not in [f.capitalize() for f in self.get_temperos()]:
            messagebox.showerror("Erro", "Tempero não encontrado")
            return
        confirm = messagebox.askyesno("Confirmação", f"Você deseja remover o tempero {nome}?")
        if confirm:
            conn = sqlite3.connect('pesagens.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Temperos WHERE nome = ?", (nome,))
            conn.commit()
            conn.close()
            self.tempero_pesagem['values'] = self.get_temperos()
            self.nome_tempero.delete(0, tk.END) # Limpar campo do input
            messagebox.showinfo("Sucesso", "Tempero removido com sucesso")

    def registrar_pesagem(self):
        """
        ciclo_ativo = self.verificar_ciclo()
        if not ciclo_ativo:
            messagebox.showerror("Erro", "O ciclo de pesagem está fechado. Resete o banco de dados para iniciar um novo ciclo.")
            return
        """

        funcionario = self.funcionario_pesagem.get().strip().capitalize()
        tempero = self.tempero_pesagem.get().strip().capitalize()
        quantidade = self.quantidade_pesagem.get()
        data = self.data_pesagem.get()
        horario = datetime.now().strftime("%H:%M:%S")

        if not funcionario or not tempero or not quantidade or not data:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        if funcionario not in [f.capitalize() for f in self.get_funcionarios()]:
            messagebox.showerror("Erro", "Funcionário não encontrado")
            return
        if tempero not in [f.capitalize() for f in self.get_temperos()]:
            messagebox.showerror("Erro", "Tempero não encontrado")
            return

        try:
            quantidade = int(quantidade)  # Mantendo como unidades
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
            return

        try:
            data_formatada = pd.to_datetime(data, format="%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira uma data válida no formato DD/MM/YYYY.")
            return

        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, dificuldade FROM Temperos WHERE nome = ?", (tempero,))
        tempero_id, dificuldade = cursor.fetchone()

        cursor.execute("SELECT id FROM Funcionarios WHERE nome = ?", (funcionario,))
        funcionario_id = cursor.fetchone()[0]

        if funcionario_id and tempero_id:
            cursor.execute("INSERT INTO Pesagens (funcionario_id, tempero_id, quantidade, data, horario) VALUES (?, ?, ?, ?, ?)",
            (funcionario_id, tempero_id, quantidade, data_formatada, horario))
            
            conn.commit()
            
            total_peso = quantidade * dificuldade
            messagebox.showinfo("Sucesso", f"Pesagem registrada com sucesso. Peso total: {total_peso:.2f} unidades")
            self.funcionario_pesagem.set('')  # Limpa o campo de input
            self.tempero_pesagem.set('')      # Limpa o campo de input
            self.quantidade_pesagem.delete(0, tk.END)  # Limpa o campo de input
            self.data_pesagem.delete(0, tk.END)        # Limpa o campo de input
            self.data_pesagem.insert(0, datetime.now().strftime("%d/%m/%Y"))  # Reseta a data para a atual
        else:
            messagebox.showerror("Erro", "Funcionário ou tempero não encontrado")

        conn.close()

    def calcular_ranking(self):
        mes = self.mes_campeao.get()
        inicio_mes = f"{mes}-01"
        fim_mes = f"{mes}-{pd.Period(mes).days_in_month}"

        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()

        query = '''
        SELECT Funcionarios.nome, Temperos.nome, Pesagens.data, Pesagens.horario, Pesagens.quantidade, Temperos.dificuldade
        FROM Pesagens
        JOIN Funcionarios ON Pesagens.funcionario_id = Funcionarios.id
        JOIN Temperos ON Pesagens.tempero_id = Temperos.id
        WHERE Pesagens.data BETWEEN ? AND ?
        '''
        
        cursor.execute(query, (inicio_mes, fim_mes))
        pesagens = cursor.fetchall()

        df = pd.DataFrame(pesagens, columns=['Funcionário', 'Tempero', 'Data', 'Horário', 'Quantidade', 'Dificuldade'])
        df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d/%m/%Y')
        df['Quantidade Final'] = df['Quantidade'] * df['Dificuldade']
        ranking = df.groupby('Funcionário')['Quantidade Final'].sum().sort_values(ascending=False).astype(int)

        if not ranking.empty:
            self.mostrar_ranking(ranking, df)
            #self.mostrar_grafico(ranking)
        else:
            messagebox.showinfo("Ranking do Mês", "Nenhum registro encontrado para o mês especificado.")

        conn.close()
    
    def mostrar_ranking(self, ranking, df):
        ranking_window = tk.Toplevel(self.root)
        ranking_window.title("Ranking do Mês")

        tree = ttk.Treeview(ranking_window, columns=("posicao", "nome", "quantidade"), show='headings')
        tree.heading("posicao", text="Posição")
        tree.heading("nome", text="Nome")
        tree.heading("quantidade", text="Quantidade Final (unidades)")
        
        for idx, (nome, quantidade) in enumerate(ranking.items(), start=1):
            tree.insert("", "end", values=(idx, nome, quantidade))

        tree.pack(pady=10)

        detalhes_frame = tk.Frame(ranking_window)
        detalhes_frame.pack(pady=10)

        label_detalhes = tk.Label(detalhes_frame, text="Detalhes de Pesagens", font=('Arial', 14, 'bold'))
        label_detalhes.pack()

        top_tree = ttk.Treeview(detalhes_frame, columns=("nome", "data", "horario", "tempero", "quantidade", "dificuldade", "quantidade_final"), show='headings')
        top_tree.heading("nome", text="Nome")
        top_tree.heading("data", text="Data")
        top_tree.heading("horario", text="Horário")
        top_tree.heading("tempero", text="Tempero")
        top_tree.heading("quantidade", text="Quantidade")
        top_tree.heading("dificuldade", text="Dificuldade")
        top_tree.heading("quantidade_final", text="Quantidade Final")

        for idx, row in df.iterrows():
            top_tree.insert("", "end", values=(row['Funcionário'], row['Data'], row['Horário'], row['Tempero'], row['Quantidade'], row['Dificuldade'], row['Quantidade Final']))

        top_tree.pack(pady=10)

    
    def resetar_bd(self):
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Pesagens")
        count = cursor.fetchone()[0]
        
        if count == 0:
            messagebox.showinfo("Informaçao", "Não há nenhum registro de pesagens no banco de dados")
            conn.close()
            return
        
        cursor.execute("DELETE FROM Pesagens")
        cursor.execute("UPDATE Ciclo SET ativo = 1 WHERE id = 1")
        conn.commit()
        conn.close()
        #self.check_ciclo()
        messagebox.showinfo("Sucesso", "Banco de dados resetado com sucesso")

    def remover_pesagem(self):
        remover_window = tk.Toplevel(self.root)
        remover_window.title("Remover Registro de Pesagem")

        tree = ttk.Treeview(remover_window, columns=("id", "funcionario", "tempero", "data", "horario", "quantidade"), show='headings')
        tree.heading("id", text="ID")
        tree.heading("funcionario", text="Funcionário")
        tree.heading("tempero", text="Tempero")
        tree.heading("data", text="Data")
        tree.heading("horario", text="Horário")
        tree.heading("quantidade", text="Quantidade")

        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT Pesagens.id, Funcionarios.nome, Temperos.nome, Pesagens.data, Pesagens.horario, Pesagens.quantidade
        FROM Pesagens
        JOIN Funcionarios ON Pesagens.funcionario_id = Funcionarios.id
        JOIN Temperos ON Pesagens.tempero_id = Temperos.id
        ''')
        registros = cursor.fetchall()
        conn.close()

        for registro in registros:
            tree.insert("", "end", values=(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]))

        tree.pack(pady=10)

        def deletar_registro():
            selecionado = tree.selection()
            if not selecionado:
                messagebox.showerror("Erro", "Por favor, selecione um registro para remover.")
                return
            registro_id = tree.item(selecionado)['values'][0]
            confirm = messagebox.askyesno("Confirmação", f"Você deseja remover o registro com ID {registro_id}?")
            if confirm:
                conn = sqlite3.connect('pesagens.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Pesagens WHERE id = ?", (registro_id,))
                conn.commit()
                conn.close()
                tree.delete(selecionado)
                messagebox.showinfo("Sucesso", "Registro removido com sucesso")

        tk.Button(remover_window, text="Remover Registro", command=deletar_registro, bg="orange", fg="black").pack(pady=10)
    
    
    def exportar_para_excel(self):
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT Funcionarios.nome, Temperos.nome, Pesagens.data, Pesagens.horario, Pesagens.quantidade, Temperos.dificuldade
        FROM Pesagens
        JOIN Funcionarios ON Pesagens.funcionario_id = Funcionarios.id
        JOIN Temperos ON Pesagens.tempero_id = Temperos.id
        ''')
        registros = cursor.fetchall()
        conn.close()

        if not registros:
            messagebox.showinfo("Informação", "Não há registros de pesagens para exportar.")
            return
        
        # Criação do DataFrame incluindo a quantidade final
        df = pd.DataFrame(registros, columns=['Funcionário', 'Tempero', 'Data', 'Horário', 'Quantidade', 'Dificuldade'])
        df['Total'] = df['Quantidade'] * df['Dificuldade']
        
        # Seleção das colunas a serem exportadas
        df_export = df[['Funcionário', 'Tempero', 'Data', 'Horário', 'Total']]

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if file_path:
            df_export.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", "Os dados foram exportados para o Excel com sucesso!")
            
    def mostrar_cadastros(self):
        # Criar a janela de cadastros
        cadastro_window = tk.Toplevel(self.root)
        cadastro_window.title("Funcionários e Temperos Cadastrados")

        # Frame para funcionários
        frame_funcionarios = tk.Frame(cadastro_window)
        frame_funcionarios.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Título para a seção de funcionários
        tk.Label(frame_funcionarios, text="Funcionários Cadastrados", font=("Helvetica", 12, "bold")).pack(pady=5)

        # Listar os funcionários
        funcionarios_list = tk.Listbox(frame_funcionarios)
        funcionarios_list.pack(fill=tk.BOTH, expand=True)

        # Obter os funcionários do banco de dados
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM Funcionarios")
        funcionarios = cursor.fetchall()
        conn.close()

        # Adicionar os funcionários à Listbox
        for funcionario in funcionarios:
            funcionarios_list.insert(tk.END, funcionario[0])

        # Frame para temperos
        frame_temperos = tk.Frame(cadastro_window)
        frame_temperos.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Título para a seção de temperos
        tk.Label(frame_temperos, text="Temperos Cadastrados com Dificuldades", font=("Helvetica", 12, "bold")).pack(pady=5)

        # Listar os temperos e suas dificuldades
        temperos_list = tk.Listbox(frame_temperos)
        temperos_list.pack(fill=tk.BOTH, expand=True)

        # Obter os temperos e dificuldades do banco de dados
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, dificuldade FROM Temperos")
        temperos = cursor.fetchall()
        conn.close()

        # Adicionar os temperos e dificuldades à Listbox
        for tempero, dificuldade in temperos:
            temperos_list.insert(tk.END, f"{tempero} (Dificuldade: {dificuldade})")
            
class RankingScreen(tk.Toplevel):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Ranking dos Funcionários")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Adiciona um label de título
        self.label_title = tk.Label(self, text="Ranking dos Funcionários", font=("Arial", 16))
        self.label_title.pack(pady=10)

        # Listbox para mostrar o ranking
        self.listbox_ranking = tk.Listbox(self, font=("Arial", 12), width=50)
        self.listbox_ranking.pack(pady=20)

        # Botão para voltar
        self.button_back = tk.Button(self, text="Voltar", command=self.destroy)
        self.button_back.pack(pady=10)

        # Atualiza o ranking ao abrir a janela
        self.update_ranking()

    def get_month_start_end(self):
        today = datetime.now()
        if today.day < 28:
            start_date = datetime(today.year, today.month - 1, 28)
        else:
            start_date = datetime(today.year, today.month, 28)

        # Finaliza um mês após o início
        end_date = start_date + timedelta(days=32)
        end_date = end_date.replace(day=29)

        return start_date, end_date

    def update_ranking(self):
        # Limpa a listbox antes de atualizar
        self.listbox_ranking.delete(0, tk.END)

        # Obter as datas de início e fim para o filtro
        start_date, end_date = self.get_month_start_end()

        # Conecta ao banco de dados
        conn = sqlite3.connect('pesagens.db')
        cursor = conn.cursor()

        # Consulta o ranking filtrando por data de início e fim
        cursor.execute('''
        SELECT Funcionarios.nome, SUM(Pesagens.quantidade * Pesagens.dificuldade) as total 
        FROM Pesagens
        JOIN Funcionarios ON Pesagens.funcionario_id = Funcionarios.id
        WHERE Pesagens.data BETWEEN ? AND ?
        GROUP BY Funcionarios.nome
        ORDER BY total DESC
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))

        ranking = cursor.fetchall()
        conn.close()

        # Exibe os resultados na listbox
        for idx, item in enumerate(ranking):
            self.listbox_ranking.insert(tk.END, f"{idx+1}. {item[0].capitalize()} - {item[1]:.2f} pontos")
            
if __name__ == "__main__":
    show_splashscreen()
    init_db()
    root = tk.Tk()
    app = App(root)
    RankingScreen()
    root.mainloop()