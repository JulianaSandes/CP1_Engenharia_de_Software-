import customtkinter as ctk
from database import supabase

class TelaPagamento(ctk.CTkFrame):
    def __init__(self, parent, rm_usuario, voltar, confirmar_pagamento):
        super().__init__(parent, fg_color="#0F0C13")
        self.rm_usuario = rm_usuario
        self.voltar = voltar
        self.confirmar_pagamento = confirmar_pagamento

        ctk.CTkLabel(self, text="MEU CARRINHO", font=("sans-serif", 20, "bold"), text_color="#D81B60").pack(pady=20)

        # Container do Carrinho
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#1A1D26", width=330, height=400)
        self.scroll.pack(pady=10, padx=15, fill="both", expand=True)

        self.label_total = ctk.CTkLabel(self, text="Total: R$ 0.00", font=("sans-serif", 20, "bold"))
        self.label_total.pack(pady=15)

        self.carregar_carrinho()

        # Botão de Confirmar
        ctk.CTkButton(self, text="PAGAR AGORA", fg_color="#D81B60", height=60, 
                      font=("sans-serif", 16, "bold"), command=self.processar_pagamento).pack(pady=5, padx=20, fill="x")
        
        ctk.CTkButton(self, text="ADICIONAR MAIS", fg_color="transparent", text_color="#B0B0B0", 
                      command=voltar).pack(pady=10)

    def carregar_carrinho(self):
        # 1. Busca os pedidos pendentes
        res_vendas = supabase.table("vendas").select("*").eq("rm", self.rm_usuario).eq("status", "Aguardando Pagamento").execute()
        vendas = res_vendas.data
        
        # 2. Busca o cardápio para cruzar os nomes (para não mostrar Item #23)
        res_cardapio = supabase.table("cardapio").select("nome, preco").execute()
        # Cria um "dicionário" de preços para achar o nome pelo valor (ajuste técnico rápido)
        nomes_produtos = {p['preco']: p['nome'] for p in res_cardapio.data}

        total = 0
        for p in vendas:
            total += p['valor']
            
            # Tenta encontrar o nome do produto baseado no valor (ou você pode ajustar sua tabela vendas para salvar o nome)
            # Por enquanto, vamos usar o valor para identificar o nome:
            nome_display = nomes_produtos.get(p['valor'], "Produto")

            f = ctk.CTkFrame(self.scroll, fg_color="transparent")
            f.pack(fill="x", pady=5)
            
            # Mostra o NOME em vez do ID
            ctk.CTkLabel(f, text=nome_display, font=("sans-serif", 13, "bold")).pack(side="left", padx=10)
            ctk.CTkLabel(f, text=f"R$ {p['valor']:.2f}", text_color="#D81B60").pack(side="right", padx=10)
            
        self.label_total.configure(text=f"Total: R$ {total:.2f}")

    def processar_pagamento(self):
        try:
            supabase.table("vendas").update({"status": "Pago - Preparando"}).eq("rm", self.rm_usuario).eq("status", "Aguardando Pagamento").execute()
            self.confirmar_pagamento()
        except Exception as e:
            print(f"Erro no pagamento: {e}")