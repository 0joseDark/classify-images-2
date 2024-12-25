import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageChops

# Função para selecionar o ficheiro ou pasta de origem
def selecionar_origem():
    caminho = filedialog.askopenfilename(filetypes=[("Ficheiros de media", "*.mp4 *.avi")])
    if caminho:
        campo_origem.delete(0, tk.END)
        campo_origem.insert(0, caminho)

# Função para selecionar a pasta de destino
def selecionar_destino():
    caminho = filedialog.askdirectory()
    if caminho:
        campo_destino.delete(0, tk.END)
        campo_destino.insert(0, caminho)

# Função para criar pastas e renomear imagens numericamente
def criar_pastas_e_renomear():
    origem = campo_origem.get()
    destino = campo_destino.get()
    if not origem or not destino:
        messagebox.showerror("Erro", "Selecione os caminhos de origem e destino.")
        return

    try:
        # Criar a pasta de destino, se não existir
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Simular criação de imagens renomeadas para demonstração
        for i in range(10):  # Exemplo: Criar 10 imagens
            img_path = os.path.join(destino, f"imagem_{i+1}.jpg")
            img = Image.new("RGB", (100, 100), (i*25, i*25, i*25))  # Criar imagens fictícias
            img.save(img_path)

        messagebox.showinfo("Sucesso", "As imagens foram criadas e renomeadas.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar pastas ou renomear imagens: {e}")

# Função para comparar imagens em duas pastas
def comparar_imagens():
    origem = filedialog.askdirectory(title="Selecione a primeira pasta")
    destino = filedialog.askdirectory(title="Selecione a segunda pasta")
    if not origem or not destino:
        messagebox.showerror("Erro", "Selecione as duas pastas para comparação.")
        return

    try:
        imagens_originais = sorted(os.listdir(origem))
        imagens_destino = sorted(os.listdir(destino))

        diferencas = []
        for img1, img2 in zip(imagens_originais, imagens_destino):
            path1 = os.path.join(origem, img1)
            path2 = os.path.join(destino, img2)

            if not os.path.isfile(path1) or not os.path.isfile(path2):
                continue

            # Comparar imagens
            with Image.open(path1) as im1, Image.open(path2) as im2:
                diff = ImageChops.difference(im1, im2)
                if diff.getbbox():
                    diferencas.append((img1, img2))

        if diferencas:
            messagebox.showinfo("Diferenças", f"Imagens diferentes encontradas: {len(diferencas)}")
        else:
            messagebox.showinfo("Sucesso", "Não há diferenças entre as imagens.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao comparar imagens: {e}")

# Função para sair do programa
def sair():
    janela.destroy()

# Criar a interface gráfica
janela = tk.Tk()
janela.title("Gerenciador de Imagens e Comparação")
janela.geometry("600x400")

# Campo para caminho do ficheiro ou pasta de origem
tk.Label(janela, text="Origem:").pack(pady=5)
campo_origem = tk.Entry(janela, width=50)
campo_origem.pack(pady=5)
tk.Button(janela, text="Selecionar Origem", command=selecionar_origem).pack(pady=5)

# Campo para caminho da pasta de destino
tk.Label(janela, text="Destino:").pack(pady=5)
campo_destino = tk.Entry(janela, width=50)
campo_destino.pack(pady=5)
tk.Button(janela, text="Selecionar Destino", command=selecionar_destino).pack(pady=5)

# Botões de ação
tk.Button(janela, text="Criar Pastas e Renomear", command=criar_pastas_e_renomear).pack(pady=5)
tk.Button(janela, text="Comparar Imagens", command=comparar_imagens).pack(pady=5)
tk.Button(janela, text="Sair", command=sair).pack(pady=5)

# Barra de progresso
tk.Label(janela, text="Progresso:").pack(pady=5)
barra_progresso = Progressbar(janela, orient="horizontal", length=400, mode="determinate")
barra_progresso.pack(pady=5)

# Menu
menu = tk.Menu(janela)
janela.config(menu=menu)
menu.add_command(label="Sair", command=sair)

# Iniciar a aplicação
janela.mainloop()
