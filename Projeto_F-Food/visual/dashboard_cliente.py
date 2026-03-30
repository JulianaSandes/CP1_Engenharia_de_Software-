import customtkinter as ctk

class DashboardCliente(ctk.CTkFrame):
    def __init__(self, parent, rm_usuario, ir_cardapio, ir_pagamento, ir_status, logout):
        super().__init__(parent, fg_color="#0F0C13")
        
        # Header mais compacto
        ctk.CTkLabel(self, text="F-FOOD", font=("sans-serif", 28, "bold"), text_color="#D81B60").pack(pady=(30, 5))
        ctk.CTkLabel(self, text=f"RM: {rm_usuario}", font=("sans-serif", 13), text_color="#B0B0B0").pack(pady=(0, 30))

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True)

        # Botões com altura reduzida (60 em vez de 70)
        self.add_btn(container, "CARDÁPIO", "#D81B60", ir_cardapio)
        self.add_btn(container, "PAGAMENTOS PENDENTES", "#1A1D26", ir_pagamento)
        self.add_btn(container, "STATUS DO PEDIDO", "#1A1D26", ir_status)

        # Logout
        ctk.CTkButton(self, text="SAIR DA CONTA", fg_color="transparent", text_color="#666666", 
                      font=("sans-serif", 12), command=logout).pack(side="bottom", pady=20)

    def add_btn(self, master, txt, cor, cmd):
        ctk.CTkButton(master, text=txt, font=("sans-serif", 14, "bold"), fg_color=cor, 
                      width=300, height=60, corner_radius=12, command=cmd).pack(pady=8)