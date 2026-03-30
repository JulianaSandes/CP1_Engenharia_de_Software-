import customtkinter as ctk

def criar_tela_cadastro(janela, voltar_inicio, realizar_cadastro):
    # Limpa os widgets antigos da janela
    for widget in janela.winfo_children():
        widget.destroy()

    # Frame de fundo (Mesmo tom escuro do Figma)
    frame_bg = ctk.CTkFrame(janela, fg_color="#0F0C13")
    frame_bg.pack(fill="both", expand=True)

    # Botão Voltar (Seta rosa no canto superior esquerdo)
    btn_voltar = ctk.CTkButton(
        frame_bg, text="←", width=30, height=30,
        fg_color="transparent", text_color="#D81B60",
        hover_color="#1A1A1A", font=("sans-serif", 24, "bold"),
        command=voltar_inicio
    )
    btn_voltar.place(x=20, y=20)

    # Título do App no topo
    label_top = ctk.CTkLabel(
        frame_bg, text="F-FOOD", font=("sans-serif", 20, "bold"), text_color="#D81B60"
    )
    label_top.pack(pady=(20, 10))

    # --- CARD DE CADASTRO (Com Scroll para caber todos os campos) ---
    card = ctk.CTkScrollableFrame(
        frame_bg, fg_color="#1A1D26", corner_radius=20, 
        width=320, height=520, scrollbar_button_color="#D81B60"
    )
    card.place(relx=0.5, rely=0.55, anchor="center")

    # Título interno do Card
    ctk.CTkLabel(
        card, text="Cadastro", font=("sans-serif", 24, "bold"), text_color="#FFFFFF"
    ).pack(pady=(15, 10), padx=25, anchor="w")

    # Função interna para criar campos padronizados (Label + Input)
    def add_campo(txt_label, placeholder, senha=False):
        ctk.CTkLabel(card, text=txt_label, text_color="#B0B0B0", font=("sans-serif", 12)).pack(padx=25, anchor="w")
        entry = ctk.CTkEntry(
            card, placeholder_text=placeholder, show="*" if senha else "",
            fg_color="#000000", border_color="#2D2A32",
            width=270, height=40, corner_radius=10
        )
        entry.pack(pady=(2, 10))
        return entry

    # Criando os campos exatamente como no seu Figma
    ent_rm = add_campo("RM:", "Digite seu RM")
    ent_cpf = add_campo("CPF:", "Digite seu CPF")
    ent_nome = add_campo("Nome:", "Digite seu nome completo")
    
    # Texto de ajuda para conta ADMIN (conforme seu print)
    ctk.CTkLabel(
        card, text='Adicione "ADMIN" no final do nome para criar\numa conta de administrador',
        text_color="#666666", font=("sans-serif", 10), justify="left"
    ).pack(padx=25, anchor="w", pady=(0, 10))

    ent_senha = add_campo("Senha:", "Crie uma senha", senha=True)

    # Botão CADASTRAR (Rosa Preenchido)
    btn_cad = ctk.CTkButton(
        card, text="👤+ Cadastrar", fg_color="#D81B60", 
        hover_color="#AD1457", width=270, height=45,
        corner_radius=10, font=("sans-serif", 16, "bold"),
        command=lambda: realizar_cadastro(
            ent_rm.get(), ent_cpf.get(), ent_nome.get(), ent_senha.get()
        )
    )
    btn_cad.pack(pady=(15, 10))

    # Botão de retorno "Já tem conta? Faça login"
    btn_link = ctk.CTkButton(
        card, text="Já tem conta? Faça login", 
        fg_color="transparent", text_color="#B0B0B0",
        hover_color="#2D2A32", width=270,
        font=("sans-serif", 12), border_width=1, border_color="#2D2A32",
        command=voltar_inicio
    )
    btn_link.pack(pady=(0, 20))