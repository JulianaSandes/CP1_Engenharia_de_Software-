import customtkinter as ctk
from database import supabase

class DashboardRestaurante(ctk.CTkFrame):
    def __init__(self, parent, logout):
        super().__init__(parent, fg_color="#0F0C13")
        self.logout = logout

        # Header - MENU COZINHA
        ctk.CTkLabel(self, text="MENU COZINHA", font=("sans-serif", 28, "bold"), text_color="#D81B60").pack(pady=(50, 5))
        ctk.CTkLabel(self, text="Gerenciamento Interno", font=("sans-serif", 13), text_color="#B0B0B0").pack(pady=(0, 40))

        # Container para os botões
        self.container_menu = ctk.CTkFrame(self, fg_color="transparent")
        self.container_menu.pack(expand=True, fill="both")

        # Botão 1 - PEDIDOS PENDENTES
        self.add_menu_button("PEDIDOS PENDENTES", "#1A1D26", self.abrir_lista)
        
        # Botão 2 - STATUS
        self.add_menu_button("STATUS", "#D81B60", self.abrir_lista)

        # Botão 3 - SAIR
        ctk.CTkButton(self, text="SAIR (LOGOUT)", fg_color="transparent", text_color="#666666", 
                      font=("sans-serif", 12), command=logout).pack(side="bottom", pady=40)

    def add_menu_button(self, texto, cor, comando):
        btn = ctk.CTkButton(self.container_menu, text=texto, font=("sans-serif", 15, "bold"),
                            fg_color=cor, hover_color="#2D2A32" if cor == "#1A1D26" else "#AD1457",
                            width=320, height=75, corner_radius=15, command=comando)
        btn.pack(pady=15)

    def abrir_lista(self):
        # Esconde o menu e mostra a lista de pedidos
        self.container_menu.pack_forget()
        
        self.lista_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True)

        header_lista = ctk.CTkFrame(self.lista_frame, fg_color="transparent")
        header_lista.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(header_lista, text="←", width=40, fg_color="#1A1D26", 
                      command=self.voltar).pack(side="left")
        
        ctk.CTkLabel(header_lista, text="FILA DE PRODUÇÃO", font=("sans-serif", 16, "bold")).pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.lista_frame, fg_color="transparent", width=350, height=450)
        scroll.pack(fill="both", expand=True, padx=10)

        try:
            res = supabase.table("vendas").select("*").eq("status", "Pago - Preparando").execute()
            if not res.data:
                ctk.CTkLabel(scroll, text="Sem pedidos pendentes.", text_color="#666666").pack(pady=50)
            else:
                for p in res.data:
                    card = ctk.CTkFrame(scroll, fg_color="#1A1D26", corner_radius=12)
                    card.pack(fill="x", pady=8, padx=10)
                    
                    info = f"ID: #{p['id_pedido']}\n{p.get('item_nome', 'Lanche')}"
                    ctk.CTkLabel(card, text=info, font=("sans-serif", 12, "bold"), justify="left").pack(side="left", padx=15, pady=10)

                    ctk.CTkButton(card, text="PRONTO", width=70, fg_color="#4CAF50",
                                  command=lambda id_p=p['id_pedido']: self.marcar_pronto(id_p)).pack(side="right", padx=10)
        except: pass

    def marcar_pronto(self, id_pedido):
        try:
            supabase.table("vendas").update({"status": "Pronto para Retirada"}).eq("id_pedido", id_pedido).execute()
            self.voltar()
            self.abrir_lista()
        except: pass

    def voltar(self):
        self.lista_frame.destroy()
        self.container_menu.pack(expand=True, fill="both")