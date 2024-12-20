import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import csv
from tkinter import ttk

# Conexão com o banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="",  # Substitua pelo seu usuário MySQL
    password="",  # Substitua pela sua senha MySQL
    database="pro_natural"  # Nome do banco de dados
)
cursor = db.cursor()



# Função para gerenciar o estoque
def gerenciar_estoque():
    def adicionar_produto():
        nome = entry_nome.get()
        descricao = entry_descricao.get()
        preco_custo = entry_preco_custo.get()
        preco_venda = entry_preco_venda.get()
        
        if not nome or not preco_custo or not preco_venda:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            cursor.execute(
                "INSERT INTO produtos (nome, descricao, preco_custo, preco_venda) VALUES (%s, %s, %s, %s)",
                (nome, descricao, preco_custo, preco_venda)
            )
            db.commit()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            listar_produtos()
            janela_estoque.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar produto: {e}")
    
    def remover_produto():
        try:
            selecionado = tree.selection()[0]
            produto_id = tree.item(selecionado)['values'][0]
            cursor.execute("DELETE FROM estoque WHERE produto_id = %s", (produto_id,))
            cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (produto_id,))
            db.commit()
            listar_produtos()
            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
        except IndexError:
            messagebox.showerror("Erro", "Selecione um produto para remover.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover produto: {e}")
    
    def listar_produtos():
        for i in tree.get_children():
            tree.delete(i)
        cursor.execute("SELECT id_produto, nome, descricao, preco_custo, preco_venda FROM produtos")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    def adicionar_novo_estoque():
        def salvar_novo_estoque():
            estoque_local = entry_estoque_local.get()
            produto_id = entry_produto_id.get()
            quantidade = entry_quantidade.get()

            if not estoque_local or not produto_id or not quantidade:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            try:
                cursor.execute(
                    "SELECT * FROM estoque WHERE produto_id = %s AND estoque_local_id = %s",
                    (produto_id, estoque_local)
                )
                resultado = cursor.fetchone()

                if resultado:
                    cursor.execute(
                        "UPDATE estoque SET quantidade = quantidade + %s WHERE produto_id = %s AND estoque_local_id = %s",
                        (quantidade, produto_id, estoque_local)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO estoque (produto_id, estoque_local_id, quantidade) VALUES (%s, %s, %s)",
                        (produto_id, estoque_local, quantidade)
                    )
                
                db.commit()
                messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
                janela_adicionar_estoque.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar ao estoque: {e}")
        
        janela_adicionar_estoque = tk.Toplevel()
        janela_adicionar_estoque.title("Adicionar Produto ao Estoque")
        janela_adicionar_estoque.geometry("1024x600")
        
        try:
            janela_adicionar_estoque.iconphoto(False, tk.PhotoImage(file="favicon-32x32.png"))  # Substitua "icone.png" pelo nome do arquivo
        except:
            print("Ícone não encontrado, continuando sem ícone.")

        
        tk.Label(janela_adicionar_estoque, text="ID do Produto:", font=("Arial", 12)).pack(pady=5)
        entry_produto_id = tk.Entry(janela_adicionar_estoque, font=("Arial", 12))
        entry_produto_id.pack(pady=5)

        tk.Label(janela_adicionar_estoque, text="Local do Estoque:", font=("Arial", 12)).pack(pady=5)
        entry_estoque_local = tk.Entry(janela_adicionar_estoque, font=("Arial", 12))
        entry_estoque_local.pack(pady=5)

        tk.Label(janela_adicionar_estoque, text="Quantidade:", font=("Arial", 12)).pack(pady=5)
        entry_quantidade = tk.Entry(janela_adicionar_estoque, font=("Arial", 12))
        entry_quantidade.pack(pady=5)

        botao_salvar = ttk.Button(janela_adicionar_estoque, text="Salvar", command=salvar_novo_estoque)
        botao_salvar.pack(pady=10, fill="x")

    janela_estoque = tk.Toplevel()
    janela_estoque.title("Gerenciamento de Estoque")
    janela_estoque.geometry("1024x700")
    janela_estoque.config(bg="#F0F0F0")
    
    try:
        janela_estoque.iconphoto(False, tk.PhotoImage(file="favicon-32x32.png"))  # Substitua "icone.png" pelo nome do arquivo
    except:
        print("Ícone não encontrado, continuando sem ícone.")


    # Frame superior com campos de entrada
    frame_top = ttk.Frame(janela_estoque, padding="20")
    frame_top.pack(fill="x", pady=20, padx=20)

    # Labels e Entradas com ttk
    ttk.Label(frame_top, text="Nome:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_nome = ttk.Entry(frame_top, font=("Arial", 12))
    entry_nome.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_top, text="Descrição:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_descricao = ttk.Entry(frame_top, font=("Arial", 12))
    entry_descricao.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_top, text="Preço de Custo:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_preco_custo = ttk.Entry(frame_top, font=("Arial", 12))
    entry_preco_custo.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

    ttk.Label(frame_top, text="Preço de Venda:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_preco_venda = ttk.Entry(frame_top, font=("Arial", 12))
    entry_preco_venda.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

    # Botões com ttk
    ttk.Button(frame_top, text="Adicionar Produto", command=adicionar_produto, style="TButton").grid(row=4, column=0, columnspan=2, pady=20)
    ttk.Button(frame_top, text="Adicionar Produto ao Estoque", command=adicionar_novo_estoque, style="TButton").grid(row=5, column=0, columnspan=2, pady=20)

    # Frame para a tabela (Treeview)
    frame_table = ttk.Frame(janela_estoque, padding="20")
    frame_table.pack(fill="x", pady=20)

    # Treeview (Tabela) para exibir os produtos
    tree = ttk.Treeview(frame_table, columns=("ID", "Nome", "Descrição", "Custo", "Venda"), show="headings", height=8)
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Custo", text="Custo")
    tree.heading("Venda", text="Venda")

    # Ajustando a largura das colunas
    tree.column("ID", width=50, anchor="center")
    tree.column("Nome", width=150, anchor="w")
    tree.column("Descrição", width=200, anchor="w")
    tree.column("Custo", width=100, anchor="w")
    tree.column("Venda", width=100, anchor="w")

    tree.pack(pady=10, fill="x")

    # Botão de Remover Produto
    ttk.Button(janela_estoque, text="Remover Produto", command=remover_produto, style="TButton").pack(pady=10)

    # Chamada para listar os produtos
    listar_produtos()

    # Iniciar a janela principal
    janela_estoque.mainloop()

# Função para realizar a venda
def realizar_venda():
    def vender_produto():
        produto_id = entry_produto_id.get()
        quantidade = entry_quantidade.get()

        if not produto_id or not quantidade:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        try:
            cursor.execute("SELECT preco_venda FROM produtos WHERE id_produto = %s", (produto_id,))
            produto = cursor.fetchone()

            if produto:
                preco_venda = produto[0]
                total = preco_venda * int(quantidade)
                data_venda = datetime.now()

                # Registra a venda no histórico
                cursor.execute(
                    "INSERT INTO historico_vendas (produto_id, quantidade, data_venda, preco_venda, total) VALUES (%s, %s, %s, %s, %s)",
                    (produto_id, quantidade, data_venda, preco_venda, total)
                )
                db.commit()

                # Atualiza o estoque após a venda
                cursor.execute(
                    "UPDATE estoque SET quantidade = quantidade - %s WHERE produto_id = %s",
                    (quantidade, produto_id)
                )
                db.commit()

                messagebox.showinfo("Sucesso", f"Venda realizada com sucesso! Total: R${total:.2f}")
                janela_venda.destroy()
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar a venda: {e}")
    
    janela_venda = tk.Toplevel()
    janela_venda.title("Realizar Venda")
    janela_venda.geometry("1024x600")
    
    try:
        janela_venda.iconphoto(False, tk.PhotoImage(file="favicon-32x32.png"))  # Substitua "icone.png" pelo nome do arquivo
    except:
        print("Ícone não encontrado, continuando sem ícone.")
    

    tk.Label(janela_venda, text="ID do Produto:", font=("Arial", 12)).pack(pady=5)
    entry_produto_id = tk.Entry(janela_venda, font=("Arial", 12))
    entry_produto_id.pack(pady=5)

    tk.Label(janela_venda, text="Quantidade:", font=("Arial", 12)).pack(pady=5)
    entry_quantidade = tk.Entry(janela_venda, font=("Arial", 12))
    entry_quantidade.pack(pady=5)

    botao_vender = ttk.Button(janela_venda, text="Vender", command=vender_produto)
    botao_vender.pack(pady=10)
    
def gerar_relatorio_vendas():
    def exibir_relatorio():
        periodo = combo_periodo.get()
        query = ""
        if periodo == "Diário":
            query = "SELECT produto_id, quantidade, data_venda, total FROM historico_vendas WHERE DATE(data_venda) = CURDATE()"
        elif periodo == "Mensal":
            query = "SELECT produto_id, quantidade, data_venda, total FROM historico_vendas WHERE MONTH(data_venda) = MONTH(CURDATE()) AND YEAR(data_venda) = YEAR(CURDATE())"
        elif periodo == "Anual":
            query = "SELECT produto_id, quantidade, data_venda, total FROM historico_vendas WHERE YEAR(data_venda) = YEAR(CURDATE())"

        # Limpa a tabela antes de exibir os novos resultados
        for item in tree.get_children():
            tree.delete(item)

        # Preenche a tabela com os resultados da consulta
        try:
            cursor.execute(query)
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

    # Janela de Relatório de Vendas
    janela_relatorio = tk.Toplevel()
    janela_relatorio.title("Relatório de Vendas")
    janela_relatorio.geometry("1024x600")
    try:
        janela_relatorio.iconphoto(False, tk.PhotoImage(file="favicon-32x32.png"))  # Substitua "icone.png" pelo nome do arquivo
    except:
        print("Ícone não encontrado, continuando sem ícone.")

    tk.Label(janela_relatorio, text="Selecione o Período:", font=("Arial", 12)).pack(pady=10)
    
    # Combobox para selecionar o período
    combo_periodo = ttk.Combobox(janela_relatorio, values=["Diário", "Mensal", "Anual"], font=("Arial", 12))
    combo_periodo.pack(pady=5, fill="x")
    combo_periodo.current(0)  # Define o valor padrão como "Diário"

    botao_gerar = ttk.Button(janela_relatorio, text="Gerar Relatório", command=exibir_relatorio)
    botao_gerar.pack(pady=10, fill="x") 

    # Frame para a tabela
    frame_table = tk.Frame(janela_relatorio)
    frame_table.pack(pady=10)

    # Configuração da tabela
    tree = ttk.Treeview(frame_table, columns=("Produto ID", "Quantidade", "Data Venda", "Total"), show="headings")
    tree.heading("Produto ID", text="Produto ID")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Data Venda", text="Data Venda")
    tree.heading("Total", text="Total")
    tree.pack(pady=10)

def exportar_relatorio():
    with open("relatorio_vendas.csv", "w", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Produto ID", "Quantidade", "Data Venda", "Total"])
        cursor.execute("SELECT produto_id, quantidade, data_venda, total FROM historico_vendas")
        for row in cursor.fetchall():
            escritor.writerow(row)
    messagebox.showinfo("Sucesso", "Relatório exportado para relatorio_vendas.csv!")

#nova função cópia da de cima
def exportar_relatorio_estoque():
    with open("relatorio_estoque.csv", "w", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Produto ID", "Nome", "Quantidade"])
        cursor.execute("SELECT e.produto_id, p.nome, e.quantidade FROM estoque e JOIN produtos p ON p.id_produto = e.produto_id")
        for row in cursor.fetchall():
            escritor.writerow(row)
    messagebox.showinfo("Sucesso", "Relatório exportado para relatorio_estoque.csv!")

def verificar_estoque_baixo():
    try:
        cursor.execute("""
            SELECT e.produto_id, p.nome, e.quantidade, e.nivel_minimo
            FROM estoque e
            JOIN produtos p ON e.produto_id = p.id_produto
            WHERE e.quantidade < e.nivel_minimo
        """)
        resultados = cursor.fetchall()

        if resultados:
            alerta_texto = "Produtos com estoque baixo:\n"
            for produto_id, nome, quantidade, nivel_minimo in resultados:
                alerta_texto += f"ID: {produto_id}, Nome: {nome}, Estoque: {quantidade}, Nível Mínimo: {nivel_minimo}\n"
            messagebox.showwarning("Alerta de Estoque Baixo", alerta_texto)
        else:
            messagebox.showinfo("Estoque OK", "Todos os produtos estão acima do nível mínimo.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao verificar estoque baixo: {e}")


root = tk.Tk()

# Configurações gerais
root.title("Sistema de Gestão de Produtos Naturais")  # Título da janela
root.geometry("1024x600")  # Tamanho da janela (ajustado para boa visualização)
root.minsize(800, 500)  # Tamanho mínimo para redimensionamento
root.config(bg="#EAEDED")  # Cor de fundo neutra e agradável

# Ícone personalizado (adicione um arquivo de ícone na pasta do projeto)
try:
    root.iconphoto(False, tk.PhotoImage(file="favicon-32x32.png"))  # Substitua "icone.png" pelo nome do arquivo
except:
    print("Ícone não encontrado, continuando sem ícone.")

# Adicionar espaçamento e margens gerais usando frames
frame_header = tk.Frame(root, bg="#4c692d", height=80)
frame_header.pack(fill="x")

titulo = tk.Label(
    frame_header,
    text="Sistema de Gestão de Produtos Naturais",
    font=("Arial", 20, "bold"),
    bg="#4c692d",
    fg="#ECF0F1"
)
titulo.pack(pady=20)

# Criar a interface principal
frame_principal = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20)
frame_principal.pack(expand=True, fill="both")

titulo = tk.Label(frame_principal, text="Sistema de Gestão", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#333333")
titulo.pack(pady=10)

botao_estoque = ttk.Button(frame_principal, text="Gerenciar Estoque", command=gerenciar_estoque)
botao_estoque.pack(pady=10, fill="x")

botao_venda = ttk.Button(frame_principal, text="Realizar Venda", command=realizar_venda)
botao_venda.pack(pady=10, fill="x")

botao_relatorio = ttk.Button(frame_principal, text="Relatórios de Vendas", command=gerar_relatorio_vendas)
botao_relatorio.pack(pady=10, fill="x")

botao_alerta = ttk.Button(frame_principal, text="Verificar Estoque Baixo", command=verificar_estoque_baixo)
botao_alerta.pack(pady=10, fill="x")

botao_exporta_venda = ttk.Button(frame_principal, text="Exportar Relatório de Vendas CSV", command=exportar_relatorio)
botao_exporta_venda.pack(pady=10, fill="x")

botao_exporta_estoque = ttk.Button(frame_principal, text="Exportar Relatório do Estoque CSV", command=exportar_relatorio_estoque)
botao_exporta_estoque.pack(pady=10, fill="x")


root.mainloop()
