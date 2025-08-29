import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

ARQUIVO = "tarefas.txt"
tarefas = []  # Lista global

# ---------- Funções ----------
def carregar_tarefas():
    """Carrega as tarefas do arquivo"""
    global tarefas
    tarefas = []
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            tarefas = [linha.strip() for linha in f if linha.strip()]
    atualizar_lista()  # Atualiza o Listbox após carregar

def salvar_tarefas():
    """Salva todas as tarefas no arquivo"""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for tarefa in tarefas:
            f.write(tarefa + "\n")
    atualizar_contador()

def atualizar_lista(filtro="Todas", pesquisa=""):
    """Atualiza o Listbox conforme filtro/pesquisa"""
    lista_tarefas.delete(0, tk.END)
    pesquisa = pesquisa.lower()
    for tarefa in tarefas:
        if filtro == "Pendentes" and tarefa.startswith("✔️ "):
            continue
        if filtro == "Concluídas" and not tarefa.startswith("✔️ "):
            continue
        if pesquisa and pesquisa not in tarefa.lower():
            continue
        lista_tarefas.insert(tk.END, tarefa)
    atualizar_contador()

def adicionar_tarefa(event=None):
    global tarefas
    tarefa = entrada.get()
    if tarefa.strip() != "":
        tarefas.append(tarefa)
        entrada.delete(0, tk.END)
        salvar_tarefas()
        atualizar_lista(var_filtro.get(), entrada_pesquisa.get())
    else:
        messagebox.showwarning("Aviso", "Digite uma tarefa antes de adicionar!")

def remover_tarefa(event=None):
    global tarefas
    try:
        selecionada = lista_tarefas.curselection()[0]
        tarefa = lista_tarefas.get(selecionada)
        tarefas.remove(tarefa)
        salvar_tarefas()
        atualizar_lista(var_filtro.get(), entrada_pesquisa.get())
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")

def concluir_tarefa(event=None):
    global tarefas
    try:
        selecionada = lista_tarefas.curselection()[0]
        tarefa = lista_tarefas.get(selecionada)
        if tarefa.startswith("✔️ "):
            messagebox.showinfo("Info", "Essa tarefa já está concluída!")
            return
        index = tarefas.index(tarefa)
        tarefas[index] = "✔️ " + tarefa
        salvar_tarefas()
        atualizar_lista(var_filtro.get(), entrada_pesquisa.get())
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para concluir!")

def editar_tarefa(event=None):
    global tarefas
    try:
        selecionada = lista_tarefas.curselection()[0]
        tarefa_antiga = lista_tarefas.get(selecionada)
        nova_tarefa = simpledialog.askstring(
            "Editar tarefa", "Digite a nova descrição:", initialvalue=tarefa_antiga
        )
        if nova_tarefa and nova_tarefa.strip() != "":
            index = tarefas.index(tarefa_antiga)
            tarefas[index] = nova_tarefa.strip()
            salvar_tarefas()
            atualizar_lista(var_filtro.get(), entrada_pesquisa.get())
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para editar!")

def mudar_filtro(*args):
    atualizar_lista(var_filtro.get(), entrada_pesquisa.get())

def pesquisar(*args):
    atualizar_lista(var_filtro.get(), entrada_pesquisa.get())

# ---------- Exportações ----------
def exportar_txt(event=None):
    with open("tarefas_exportadas.txt", "w", encoding="utf-8") as f:
        f.write("📌 Lista de Tarefas\n\n")
        f.write("Pendentes:\n")
        for t in tarefas:
            if not t.startswith("✔️ "):
                f.write(" - " + t + "\n")
        f.write("\nConcluídas:\n")
        for t in tarefas:
            if t.startswith("✔️ "):
                f.write(" - " + t + "\n")
    messagebox.showinfo("Exportação", "Tarefas exportadas para 'tarefas_exportadas.txt'")

def exportar_pdf(event=None):
    doc = SimpleDocTemplate("tarefas_exportadas.pdf")
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("📌 Lista de Tarefas", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Pendentes:", styles["Heading2"]))
    for t in tarefas:
        if not t.startswith("✔️ "):
            story.append(Paragraph("• " + t, styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Concluídas:", styles["Heading2"]))
    for t in tarefas:
        if t.startswith("✔️ "):
            story.append(Paragraph("• " + t, styles["Normal"]))
    doc.build(story)
    messagebox.showinfo("Exportação", "Tarefas exportadas para 'tarefas_exportadas.pdf'")

# ---------- Janela ----------
janela = tk.Tk()
janela.title("📝 Bloco de Notas - Lista de Tarefas")
janela.geometry("550x800")
janela.configure(bg="#1e1e1e")

# ---------- Estilos ----------
fonte_padrao = ("Segoe UI", 11)
cor_caixa = "#2d2d2d"
cor_texto = "#ffffff"
cor_botao = "#3a3a3a"
cor_botao_hover = "#505050"
cor_destaque = "#00ff88"

# ---------- Entrada ----------
entrada = tk.Entry(
    janela, width=35, font=fonte_padrao,
    bg=cor_caixa, fg=cor_texto, insertbackground="white",
    relief="flat"
)
entrada.pack(pady=15)

# ---------- Hover ----------
def on_enter(e): e.widget["bg"] = cor_botao_hover
def on_leave(e): e.widget["bg"] = cor_botao

# ---------- Botões ----------
botoes = [
    ("➕ Adicionar", adicionar_tarefa, cor_destaque),
    ("🗑️ Remover", remover_tarefa, "#ff5555"),
    ("✔️ Concluir", concluir_tarefa, "#55ff55"),
    ("✏️ Editar", editar_tarefa, "#ffaa00"),
    ("📄 Exportar TXT", exportar_txt, "#88c0ff"),
    ("📑 Exportar PDF", exportar_pdf, "#ffcc00"),
]

for texto, comando, cor in botoes:
    btn = tk.Button(janela, text=texto, font=fonte_padrao,
                    bg=cor_botao, fg=cor, relief="flat",
                    command=comando)
    btn.pack(pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ---------- Lista ----------
lista_tarefas = tk.Listbox(
    janela, width=50, height=15,
    bg=cor_caixa, fg=cor_texto, selectbackground=cor_destaque,
    font=fonte_padrao, relief="flat"
)
lista_tarefas.pack(pady=10)

# ---------- Filtro ----------
var_filtro = tk.StringVar(value="Todas")
opcoes_filtro = ["Todas", "Pendentes", "Concluídas"]
menu_filtro = tk.OptionMenu(janela, var_filtro, *opcoes_filtro, command=mudar_filtro)
menu_filtro.config(bg=cor_botao, fg=cor_destaque, font=fonte_padrao, relief="flat")
menu_filtro.pack(pady=10)

# ---------- Pesquisa ----------
entrada_pesquisa = tk.Entry(
    janela, width=30, font=fonte_padrao,
    bg=cor_caixa, fg=cor_texto, insertbackground="white",
    relief="flat"
)
entrada_pesquisa.pack(pady=10)
entrada_pesquisa.insert(0, "🔍 Pesquisar...")
entrada_pesquisa.bind("<KeyRelease>", pesquisar)

def limpar_placeholder(event):
    if entrada_pesquisa.get() == "🔍 Pesquisar...":
        entrada_pesquisa.delete(0, tk.END)

entrada_pesquisa.bind("<FocusIn>", limpar_placeholder)

# ---------- Contador ----------
label_contador = tk.Label(
    janela, text="Pendentes: 0 | Concluídas: 0",
    font=fonte_padrao, bg="#1e1e1e", fg=cor_destaque
)
label_contador.pack(pady=10)

def atualizar_contador():
    pendentes = sum(1 for t in tarefas if not t.startswith("✔️ "))
    concluidas = sum(1 for t in tarefas if t.startswith("✔️ "))
    label_contador.config(text=f"Pendentes: {pendentes} | Concluídas: {concluidas}")

# ---------- Carregar ao abrir ----------
carregar_tarefas()

# ---------- Atalhos ----------
janela.bind("<Return>", adicionar_tarefa)
janela.bind("<Delete>", remover_tarefa)
janela.bind("<Control-s>", lambda e: salvar_tarefas())
janela.bind("<Control-e>", editar_tarefa)
janela.bind("<Control-d>", concluir_tarefa)
janela.bind("<Control-t>", exportar_txt)
janela.bind("<Control-p>", exportar_pdf)

# ---------- Loop ----------
janela.mainloop()
