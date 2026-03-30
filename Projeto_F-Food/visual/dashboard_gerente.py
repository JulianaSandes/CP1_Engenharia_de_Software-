import customtkinter as ctk
from database import supabase

class DashboardGerente(ctk.CTkFrame):
    def __init__(self, parent, logout):
        super().__init__(parent, fg_color="#0F0C13")
        self.logout = logout
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        for widget in self.winfo_children(): widget.destroy()
        
        ctk.CTkLabel(self, text="MENU GERENTE", font=("sans-serif", 28, "bold"), text_color="#D81B60").pack(pady=(50, 5))
        ctk.CTkLabel(self, text="Administração de Cardápio", font=("sans-serif", 13), text_color="#B0B0B0").pack(pady=(0, 30))

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both")

        self.add_btn(container, "VISUALIZAR ESTOQUE", "#1A1D26", self.visualizar_estoque)
        self.add_btn(container, "CADASTRAR ITEM", "#1A1D26", self.cadastrar_item)
        self.add_btn(container, "EXCLUIR ITEM", "#1A1D26", self.excluir_item)
        self.add_btn(container, "ALTERAR PREÇO", "#1A1D26", self.alterar_preco)
        self.add_btn(container, "ALTERAR ESTOQUE", "#D81B60", self.alterar_estoque)

        ctk.CTkButton(self, text="SAIR (LOGOUT)", fg_color="transparent", text_color="#666666", 
                      font=("sans-serif", 12), command=self.logout).pack(side="bottom", pady=30)

    def add_btn(self, master, txt, cor, cmd):
        btn = ctk.CTkButton(master, text=txt, font=("sans-serif", 14, "bold"), fg_color=cor, 
                            width=320, height=60, corner_radius=12, command=cmd)
        btn.pack(pady=8)

    # --- 1. VISUALIZAR ESTOQUE (MATRIZ / TABELA SEM ID) ---
    def visualizar_estoque(self):
        for widget in self.winfo_children(): widget.destroy()
        
        header_main = ctk.CTkFrame(self, fg_color="transparent")
        header_main.pack(fill="x", padx=15, pady=15)
        ctk.CTkButton(header_main, text="←", width=35, command=self.mostrar_menu_principal).pack(side="left")
        ctk.CTkLabel(header_main, text="ESTOQUE", font=("sans-serif", 18, "bold"), text_color="#D81B60").pack(side="right")

        # Cabeçalho da Matriz
        tabela_head = ctk.CTkFrame(self, fg_color="#1A1D26", height=40)
        tabela_head.pack(fill="x", padx=10)
        ctk.CTkLabel(tabela_head, text="ITEM", font=("sans-serif", 12, "bold"), width=150, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(tabela_head, text="PREÇO", font=("sans-serif", 12, "bold"), width=80).pack(side="left")
        ctk.CTkLabel(tabela_head, text="QTD", font=("sans-serif", 12, "bold"), width=60).pack(side="left")

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=340, height=400)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        res = supabase.table("cardapio").select("*").execute()
        for item in res.data:
            linha = ctk.CTkFrame(scroll, fg_color="transparent")
            linha.pack(fill="x", pady=2)
            
            ctk.CTkLabel(linha, text=item['nome'], width=150, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(linha, text=f"R${item['preco']:.2f}", width=80, text_color="#D81B60").pack(side="left")
            ctk.CTkLabel(linha, text=str(item['estoque']), width=60).pack(side="left")
            
            ctk.CTkFrame(scroll, fg_color="#333333", height=1).pack(fill="x", padx=10) # Linha divisória

    # --- 2. CADASTRAR ITEM (CORRIGIDO PARA NÃO SUMIR) ---
    def cadastrar_item(self):
        for widget in self.winfo_children(): widget.destroy()
        
        # Header sem scroll para não bugar
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(header, text="←", width=35, command=self.mostrar_menu_principal).pack(side="left")
        ctk.CTkLabel(header, text="CADASTRAR ITEM", font=("sans-serif", 18, "bold"), text_color="#D81B60").pack(side="right")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True)

        e_nome = ctk.CTkEntry(container, placeholder_text="Nome do Produto", width=300, height=50)
        e_nome.pack(pady=10)
        e_preco = ctk.CTkEntry(container, placeholder_text="Preço (Ex: 10.50)", width=300, height=50)
        e_preco.pack(pady=10)
        e_estoque = ctk.CTkEntry(container, placeholder_text="Quantidade em Estoque", width=300, height=50)
        e_estoque.pack(pady=10)

        def salvar():
            supabase.table("cardapio").insert({
                "nome": e_nome.get(),
                "preco": float(e_preco.get().replace(',', '.')),
                "estoque": int(e_estoque.get())
            }).execute()
            self.mostrar_menu_principal()

        ctk.CTkButton(self, text="CADASTRAR AGORA", fg_color="#D81B60", height=60, width=300, 
                      font=("sans-serif", 14, "bold"), command=salvar).pack(pady=40)

    # --- 3, 4, 5 MANTIDOS CONFORME APROVADO ---
    def excluir_item(self):
        self.montar_lista_com_acao("EXCLUIR ITEM", "🗑️", "#922B21", self.confirmar_delete)

    def alterar_preco(self):
        self.montar_lista_com_acao("ALTERAR PREÇO", "✏️", "#1A1D26", lambda i: self.popup_edit(i, "preco"))

    def alterar_estoque(self):
        self.montar_lista_com_acao("ALTERAR ESTOQUE", "📦", "#1A1D26", lambda i: self.popup_edit(i, "estoque"))

    def montar_lista_com_acao(self, titulo, icone, cor_btn, comando_btn):
        for widget in self.winfo_children(): widget.destroy()
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=15)
        ctk.CTkButton(header, text="←", width=35, command=self.mostrar_menu_principal).pack(side="left")
        ctk.CTkLabel(header, text=titulo, font=("sans-serif", 18, "bold"), text_color="#D81B60").pack(side="right")

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=340, height=450)
        scroll.pack(fill="both", expand=True, padx=10)
        
        res = supabase.table("cardapio").select("*").execute()
        for item in res.data:
            card = ctk.CTkFrame(scroll, fg_color="#1A1D26", corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(card, text=f"ID: {item['id']} | {item['nome']}", font=("sans-serif", 12)).pack(side="left", padx=15, pady=10)
            ctk.CTkButton(card, text=icone, width=45, fg_color=cor_btn, command=lambda i=item: comando_btn(i)).pack(side="right", padx=10)

    def confirmar_delete(self, item):
        supabase.table("cardapio").delete().eq("id", item['id']).execute()
        self.excluir_item()

    def popup_edit(self, item, col):
        pop = ctk.CTkToplevel(self)
        pop.geometry("300x250")
        pop.attributes("-topmost", True)
        ctk.CTkLabel(pop, text=f"Novo valor para:\n{item['nome']}", font=("sans-serif", 13, "bold")).pack(pady=20)
        entry = ctk.CTkEntry(pop, placeholder_text=f"Atual: {item[col]}", width=200)
        entry.pack(pady=10)
        def salvar():
            val = float(entry.get().replace(',', '.')) if col == "preco" else int(entry.get())
            supabase.table("cardapio").update({col: val}).eq("id", item['id']).execute()
            pop.destroy()
            self.alterar_preco() if col == "preco" else self.alterar_estoque()
        ctk.CTkButton(pop, text="CONFIRMAR", fg_color="#4CAF50", command=salvar).pack(pady=20)