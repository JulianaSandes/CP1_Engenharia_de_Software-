import customtkinter as ctk
from database import supabase

class TelaMetodoPagamento(ctk.CTkFrame):
    def __init__(self, parent, rm_usuario, finalizar):
        super().__init__(parent, fg_color="#0F0C13")
        self.rm_usuario = rm_usuario
        self.finalizar = finalizar

        ctk.CTkLabel(self, text="FORMA DE PAGAMENTO", font=("sans-serif", 20, "bold"), text_color="#D81B60").pack(pady=40)

        # Opções que chamam a confirmação
        self.add_opcao("PIX", "Pagamento Instantâneo")
        self.add_opcao("CARTÃO DE CRÉDITO", "Crédito Online")
        self.add_opcao("CARTÃO DE DÉBITO", "Débito Online")

        ctk.CTkButton(self, text="CANCELAR", fg_color="transparent", text_color="#666666", 
                      command=self.finalizar).pack(side="bottom", pady=20)

    def add_opcao(self, titulo, subtitulo):
        btn = ctk.CTkButton(
            self, text=f"{titulo}\n{subtitulo}", font=("sans-serif", 14, "bold"),
            fg_color="#1A1D26", hover_color="#2D2A32", height=80, width=300,
            command=self.confirmar_pagamento
        )
        btn.pack(pady=10)

    def confirmar_pagamento(self):
        try:
            # 1. Atualiza o status para "Pago" no banco
            # Nota: Ele vai atualizar todos os itens que estavam "Aguardando Pagamento" deste RM
            supabase.table("vendas").update({"status": "Pago - Preparando"}).eq("rm", self.rm_usuario).eq("status", "Aguardando Pagamento").execute()
            
            print(f"✅ Pagamento confirmado para RM {self.rm_usuario}!")
            
            # 2. Direciona para a tela de Status
            self.finalizar()
        except Exception as e:
            print(f"❌ ERRO AO PROCESSAR PAGAMENTO: {e}")