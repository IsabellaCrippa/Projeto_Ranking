import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
import logica_ranking  

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🏆 Ranking de Vendedores")
app.geometry("800x500")
app.grid_columnconfigure(0, weight=2)
app.grid_columnconfigure(1, weight=1)

painel_esquerdo = ctk.CTkFrame(app)
painel_esquerdo.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(painel_esquerdo, text="📋 Entrada de Dados", font=("Arial", 20)).pack(pady=10)

entrada_nome = ctk.CTkEntry(painel_esquerdo, placeholder_text="Nome do Vendedor")
entrada_nome.pack(pady=5)

entrada_vendas = ctk.CTkEntry(painel_esquerdo, placeholder_text="Valor de Vendas (R$)")
entrada_vendas.pack(pady=5)

def on_adicionar():
    nome = entrada_nome.get().strip()
    vendas = entrada_vendas.get().strip()

    if not nome or not vendas:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
        return

    ok, msg = logica_ranking.adicionar_vendedor(nome, vendas)
    if ok:
        entrada_nome.delete(0, ctk.END)
        entrada_vendas.delete(0, ctk.END)
        atualizar_ranking()
    else:
        messagebox.showerror("Erro", msg)

def atualizar_ranking():
    ranking_textbox.configure(state="normal")
    ranking_textbox.delete("1.0", ctk.END)
    ranking_textbox.insert(ctk.END, logica_ranking.get_ranking_text())
    ranking_textbox.configure(state="disabled")

ctk.CTkButton(painel_esquerdo, text="Adicionar Vendedor", command=on_adicionar).pack(pady=10)

ctk.CTkLabel(painel_esquerdo, text="📊 Ranking Atual", font=("Arial", 16)).pack(pady=(15, 5))
ranking_textbox = ctk.CTkTextbox(painel_esquerdo, height=200, width=400, state="disabled")
ranking_textbox.pack(pady=5)

painel_direito = ctk.CTkFrame(app)
painel_direito.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

ctk.CTkLabel(painel_direito, text="⚙️ Ações", font=("Arial", 20)).pack(pady=15)

def on_salvar():
    ok, msg = logica_ranking.salvar_em_txt()
    if ok:
        messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{msg}")
    else:
        messagebox.showerror("Erro", msg)

def on_limpar():
    if messagebox.askyesno("Confirmar", "Deseja realmente limpar todos os dados?"):
        logica_ranking.limpar_dados()
        atualizar_ranking()

def on_grafico():
    nomes, vendas = logica_ranking.get_dados_para_grafico()
    if not nomes:
        messagebox.showwarning("Sem dados", "Adicione vendedores primeiro.")
        return
    plt.figure(figsize=(10, 6))
    plt.bar(nomes, vendas, color='royalblue')
    plt.xlabel("Vendedores")
    plt.ylabel("Vendas (R$)")
    plt.title("Desempenho dos Vendedores")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

ctk.CTkButton(painel_direito, text="Salvar Relatório (.txt)", command=on_salvar).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(painel_direito, text="Exibir Gráfico", command=on_grafico).pack(pady=10, fill="x", padx=10)
ctk.CTkButton(painel_direito, text="Limpar Dados", command=on_limpar).pack(pady=10, fill="x", padx=10)

app.mainloop()
