import customtkinter as ctk
import random
from database import supabase

# ESTA LINHA ABAIXO PRECISA TER ESSE NOME EXATO:
class MenuClienteGUI(ctk.CTkFrame):
    def __init__(self, parent, rm_usuario, voltar, ir_pagamento):
        super().__init__(parent, fg_color="#0F0C13")
        self.rm_usuario = rm_usuario
        self.voltar = voltar
        self.ir_pagamento = ir_pagamento
        self.itens_no_carrinho = 0
        
        # ... restante do código que te mandei antes ...
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(header, text="←", width=35, fg_color="#1A1D26", command=voltar).pack(side="left")
        ctk.CTkLabel(header, text="CARDÁPIO", font=("sans-serif", 18, "bold"), text_color="#D81B60").pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=350, height=480)
        self.scroll.pack(fill="both", expand=True, padx=5)

        self.btn_carrinho = ctk.CTkButton(
            self, text="CARRINHO VAZIO", fg_color="#333333", state="disabled",
            height=60, font=("sans-serif", 15, "bold"), corner_radius=0, command=self.ir_pagamento
        )
        self.btn_carrinho.pack(fill="x", side="bottom")
        self.carregar_itens()

    def carregar_itens(self):
        res = supabase.table("cardapio").select("*").execute()
        for item in res.data:
            card = ctk.CTkFrame(self.scroll, fg_color="#1A1D26", corner_radius=10)
            card.pack(fill="x", pady=5, padx=8)
            ctk.CTkLabel(card, text=item['nome'], font=("sans-serif", 13, "bold")).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(card, text=f"R$ {item['preco']:.2f}", text_color="#D81B60").pack(side="left", padx=5)
            ctk.CTkButton(card, text="+", width=35, fg_color="#D81B60", 
                          command=lambda p=item: self.registrar_pedido(p)).pack(side="right", padx=10)

    def registrar_pedido(self, item):
        try:
            cod_retirada = f"FF-{random.randint(100, 999)}"
            # IMPORTANTE: Se você não criou a coluna 'item_nome' no Supabase, tire a linha abaixo!
            supabase.table("vendas").insert({
                "rm": self.rm_usuario, 
                "valor": item['preco'],
                "status": "Aguardando Pagamento", 
                "codigo_retirada": cod_retirada
            }).execute()
            
            self.itens_no_carrinho += 1
            self.btn_carrinho.configure(text=f"REVISAR E PAGAR ({self.itens_no_carrinho})", fg_color="#D81B60", state="normal")
        except Exception as e:
            print(f"❌ Erro ao registrar: {e}")