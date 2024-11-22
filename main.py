import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# Conexão com o banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Substitua pelo seu usuário MySQL
    password="0141",  # Substitua pela sua senha MySQL
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
        janela_adicionar_estoque.geometry("400x300")

        tk.Label(janela_adicionar_estoque, text="ID do Produto:", font=("Arial", 12)).pack(pady=5)
        entry_produto_id = tk.Entry(janela_adicionar_estoque, font=("Arial", 12))
        entry_produto_id.pack(pady=5)

        tk.Label(janela_adicionar_estoque, text="Local do Estoque:", font=("Arial", 12)).pack(pady=5)
        entry_estoque_local = tk.Entry(janela_adicionar_estoque, font=("Arial", 12))
        entry_estoque_local.pack(pady=5)

        tk.Label(janela_adicionar_estoque, text="Quantidade:", font=("Arial", 12)).pack(pady=5)
        entry_quantidade = tk.Entry(janela_adicionar_estoque, font=("Arial", 12))
        entry_quantidade.pack(pady=5)

        tk.Button(janela_adicionar_estoque, text="Salvar", command=salvar_novo_estoque, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

    janela_estoque = tk.Toplevel()
    janela_estoque.title("Gerenciamento de Estoque")
    janela_estoque.geometry("800x500")
    janela_estoque.config(bg="#F0F0F0")

    # Frame de entrada de dados
    frame_top = tk.Frame(janela_estoque, bg="#F0F0F0")
    frame_top.pack(pady=20, padx=20, fill="x")

    tk.Label(frame_top, text="Nome:", font=("Arial", 12), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_nome = tk.Entry(frame_top, font=("Arial", 12))
    entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(frame_top, text="Descrição:", font=("Arial", 12), anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_descricao = tk.Entry(frame_top, font=("Arial", 12))
    entry_descricao.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(frame_top, text="Preço de Custo:", font=("Arial", 12), anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_preco_custo = tk.Entry(frame_top, font=("Arial", 12))
    entry_preco_custo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(frame_top, text="Preço de Venda:", font=("Arial", 12), anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_preco_venda = tk.Entry(frame_top, font=("Arial", 12))
    entry_preco_venda.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    tk.Button(frame_top, text="Adicionar Produto", command=adicionar_produto, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=4, column=0, columnspan=2, pady=20)
    tk.Button(frame_top, text="Adicionar Produto ao Estoque", command=adicionar_novo_estoque, font=("Arial", 12), bg="#2196F3", fg="white").grid(row=5, column=0, columnspan=2, pady=20)
    
    frame_table = tk.Frame(janela_estoque)
    frame_table.pack(pady=20)
    
    tree = ttk.Treeview(frame_table, columns=("ID", "Nome", "Descrição", "Custo", "Venda"), show="headings", height=8)
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Custo", text="Custo")
    tree.heading("Venda", text="Venda")
    tree.pack(pady=10)

    tk.Button(janela_estoque, text="Remover Produto", command=remover_produto, font=("Arial", 12), bg="#F44336", fg="white").pack(pady=10)
    
    listar_produtos()

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
    janela_venda.geometry("400x300")

    tk.Label(janela_venda, text="ID do Produto:", font=("Arial", 12)).pack(pady=5)
    entry_produto_id = tk.Entry(janela_venda, font=("Arial", 12))
    entry_produto_id.pack(pady=5)

    tk.Label(janela_venda, text="Quantidade:", font=("Arial", 12)).pack(pady=5)
    entry_quantidade = tk.Entry(janela_venda, font=("Arial", 12))
    entry_quantidade.pack(pady=5)

    tk.Button(janela_venda, text="Vender", command=vender_produto, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

# Criar a interface principal
root = tk.Tk()
root.title("Sistema de Gestão de Produtos Naturais")
root.geometry("400x250")

# Botões principais
tk.Button(root, text="Gerenciar Estoque", command=gerenciar_estoque, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=20)
tk.Button(root, text="Realizar Venda", command=realizar_venda, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

root.mainloop()
