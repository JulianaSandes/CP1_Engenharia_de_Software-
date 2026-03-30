import os
import sys
import customtkinter as ctk

# --- AJUSTE DE RESOLUÇÃO PARA WINDOWS ---
if sys.platform == "win32":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass 

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
if diretorio_atual not in sys.path:
    sys.path.append(diretorio_atual)

try:
    from backend.fazer_login import autenticar_usuario
    from visual.tela_inicial import criar_tela_inicial
    from visual.tela_login import criar_tela_login
    from visual.tela_cadastro import criar_tela_cadastro
    from visual.dashboard_cliente import DashboardCliente
    from visual.menu_cliente_gui import MenuClienteGUI
    from visual.tela_pagamento import TelaPagamento
    from visual.tela_metodo_pagamento import TelaMetodoPagamento
    from visual.tela_status_pedido import TelaStatusPedido
    from visual.dashboard_restaurante import DashboardRestaurante
    from visual.dashboard_gerente import DashboardGerente # NOVO IMPORT
except Exception as e:
    print(f"❌ ERRO DE IMPORTAÇÃO: {e}")
    sys.exit()

class SistemaFFood:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("F-FOOD")
        self.janela.geometry("360x600") 
        self.janela.resizable(False, False)
        self.mostrar_inicio()
        self.janela.mainloop()

    def limpar_janela(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpar_janela()
        criar_tela_inicial(self.janela, self.mostrar_login, self.mostrar_cadastro)

    def mostrar_login(self):
        self.limpar_janela()
        criar_tela_login(self.janela, self.mostrar_inicio, self.executar_login_backend, self.mostrar_cadastro)

    def mostrar_cadastro(self):
        self.limpar_janela()
        criar_tela_cadastro(self.janela, self.mostrar_inicio, lambda r,c,n,s: print("Cadastro..."))

    def executar_login_backend(self, rm, senha):
        sucesso, perfil, nome, erro = autenticar_usuario(rm, senha)
        if sucesso:
            print(f"✅ Login OK: {nome} ({perfil})")
            if perfil == "Cliente": self.abrir_dashboard_cliente(rm)
            elif perfil == "Restaurante": self.abrir_dashboard_cozinha()
            elif perfil == "Gerente": self.abrir_dashboard_gerente() # NOVA ROTA
        else:
            print(f"❌ {erro}")

    # --- ÁREA CLIENTE ---
    def abrir_dashboard_cliente(self, rm):
        self.limpar_janela()
        dash = DashboardCliente(self.janela, rm, 
                                lambda: self.abrir_vitrine_produtos(rm),
                                lambda: self.abrir_tela_pagamento(rm),
                                lambda: self.abrir_status_pedidos(rm),
                                self.mostrar_inicio)
        dash.pack(fill="both", expand=True)

    def abrir_vitrine_produtos(self, rm):
        self.limpar_janela()
        vitrine = MenuClienteGUI(self.janela, rm, lambda: self.abrir_dashboard_cliente(rm), lambda: self.abrir_tela_pagamento(rm))
        vitrine.pack(fill="both", expand=True)

    def abrir_tela_pagamento(self, rm):
        self.limpar_janela()
        pag = TelaPagamento(self.janela, rm, lambda: self.abrir_vitrine_produtos(rm), lambda: self.abrir_metodo_pagamento(rm))
        pag.pack(fill="both", expand=True)

    def abrir_metodo_pagamento(self, rm):
        self.limpar_janela()
        metodo = TelaMetodoPagamento(self.janela, rm, lambda: self.abrir_status_pedidos(rm))
        metodo.pack(fill="both", expand=True)

    def abrir_status_pedidos(self, rm):
        self.limpar_janela()
        status = TelaStatusPedido(self.janela, rm, lambda: self.abrir_dashboard_cliente(rm))
        status.pack(fill="both", expand=True)

    # --- ÁREA COZINHA ---
    def abrir_dashboard_cozinha(self):
        self.limpar_janela()
        dash = DashboardRestaurante(self.janela, self.mostrar_inicio)
        dash.pack(fill="both", expand=True)

    # --- ÁREA GERENTE ---
    def abrir_dashboard_gerente(self):
        self.limpar_janela()
        dash = DashboardGerente(self.janela, self.mostrar_inicio)
        dash.pack(fill="both", expand=True)

if __name__ == "__main__":
    SistemaFFood()