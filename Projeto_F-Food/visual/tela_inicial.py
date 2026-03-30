import customtkinter as ctk

def criar_tela_inicial(janela, ir_para_login, ir_para_cadastro):
    # Limpa a janela antes de desenhar
    for widget in janela.winfo_children():
        widget.destroy()

    # Frame principal (Fundo escuro)
    frame = ctk.CTkFrame(janela, fg_color="#0F0C13")
    frame.pack(fill="both", expand=True)

    # Título F-FOOD (Rosa)
    label_titulo = ctk.CTkLabel(
        frame, text="F-FOOD", 
        font=("sans-serif", 48, "bold"), 
        text_color="#D81B60"
    )
    label_titulo.pack(pady=(120, 10))

    # Subtítulo
    label_sub = ctk.CTkLabel(
        frame, text="Sistema de Gerenciamento", 
        font=("sans-serif", 16), 
        text_color="#B0B0B0"
    )
    label_sub.pack(pady=(0, 100))

    # Botão Login (Borda Rosa)
    btn_login = ctk.CTkButton(
        frame, text="Login", 
        fg_color="transparent", 
        border_width=2, 
        border_color="#D81B60",
        hover_color="#2D2A32",
        width=280, height=50,
        corner_radius=12,
        command=ir_para_login
    )
    btn_login.pack(pady=10)

    # Botão Cadastro (Rosa Preenchido)
    btn_cadastrar = ctk.CTkButton(
        frame, text="Cadastro", 
        fg_color="#D81B60", 
        hover_color="#AD1457",
        width=280, height=50,
        corner_radius=12,
        command=ir_para_cadastro
    )
    btn_cadastrar.pack(pady=10)

    # Rodapé v1.0.0
    label_footer = ctk.CTkLabel(
        frame, text="Sistema ERP de Restaurante\nv1.0.0", 
        font=("sans-serif", 10), 
        text_color="#444444"
    )
    label_footer.pack(side="bottom", pady=20)