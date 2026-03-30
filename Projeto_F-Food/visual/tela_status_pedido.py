import customtkinter as ctk
from database import supabase

class TelaStatusPedido(ctk.CTkFrame):
    def __init__(self, parent, rm_usuario, voltar):
        super().__init__(parent, fg_color="#0F0C13")
        self.rm_usuario = rm_usuario
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=20)
        ctk.CTkButton(header, text="←", width=35, command=voltar).pack(side="left")
        ctk.CTkLabel(header, text="STATUS DO PEDIDO", font=("sans-serif", 18, "bold"), text_color="#D81B60").pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=350, height=450)
        self.scroll.pack(fill="both", expand=True)

        self.listar_pedidos()

    def listar_pedidos(self):
        try:
            # Busca pedidos que NÃO estão aguardando pagamento
            res = supabase.table("vendas").select("*").eq("rm", self.rm_usuario).neq("status", "Aguardando Pagamento").execute()
            
            if not res.data:
                ctk.CTkLabel(self.scroll, text="Nenhum pedido em andamento.", text_color="#666666").pack(pady=50)
                return

            for p in reversed(res.data):
                card = ctk.CTkFrame(self.scroll, fg_color="#1A1D26", corner_radius=12)
                card.pack(fill="x", pady=8, padx=15)

                # Tenta pegar o nome do item. Se não existir no banco, usa "Pedido"
                nome = p.get('item_nome', f"Pedido #{p['id_pedido']}")
                
                ctk.CTkLabel(card, text=nome, font=("sans-serif", 13, "bold")).pack(pady=(10,0))
                ctk.CTkLabel(card, text=f"Status: {p['status']}", text_color="#D81B60", font=("sans-serif", 11)).pack()
                
                # Código de Retirada em destaque
                code_box = ctk.CTkFrame(card, fg_color="#0F0C13", corner_radius=8)
                code_box.pack(pady=10, padx=20, fill="x")
                ctk.CTkLabel(code_box, text=p['codigo_retirada'], font=("mono", 18, "bold"), text_color="#4CAF50").pack(pady=5)
        except Exception as e:
            print(f"Erro ao listar status: {e}")