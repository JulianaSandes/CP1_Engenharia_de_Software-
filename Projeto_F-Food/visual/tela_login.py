import customtkinter as ctk

def criar_tela_login(janela, voltar_inicio, fazer_login, ir_para_cadastro):
    for widget in janela.winfo_children():
        widget.destroy()

    frame_bg = ctk.CTkFrame(janela, fg_color="#0F0C13")
    frame_bg.pack(fill="both", expand=True)

    # Botão Voltar
    ctk.CTkButton(frame_bg, text="←", width=30, fg_color="transparent", text_color="#D81B60", 
                  font=("sans-serif", 24, "bold"), command=voltar_inicio).place(x=20, y=20)

    card = ctk.CTkFrame(frame_bg, fg_color="#1A1D26", corner_radius=20, width=320, height=450)
    card.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(card, text="Login", font=("sans-serif", 24, "bold")).pack(pady=(30, 20), padx=25, anchor="w")

    # RM
    ctk.CTkLabel(card, text="RM:", text_color="#B0B0B0").pack(padx=25, anchor="w")
    entry_rm = ctk.CTkEntry(card, placeholder_text="Digite seu RM", fg_color="#000000", width=270, height=45)
    entry_rm.pack(pady=(5, 15))

    # SENHA COM OLHINHO
    ctk.CTkLabel(card, text="Senha:", text_color="#B0B0B0").pack(padx=25, anchor="w")
    
    frame_senha = ctk.CTkFrame(card, fg_color="transparent")
    frame_senha.pack(pady=(5, 30))

    entry_senha = ctk.CTkEntry(frame_senha, placeholder_text="Digite sua senha", show="*", 
                               fg_color="#000000", width=225, height=45)
    entry_senha.pack(side="left")

    def alternar_senha():
        if entry_senha.cget("show") == "*":
            entry_senha.configure(show="")
            btn_olho.configure(text="👁️")
        else:
            entry_senha.configure(show="*")
            btn_olho.configure(text="🔒")

    btn_olho = ctk.CTkButton(frame_senha, text="🔒", width=40, height=45, fg_color="#2D2A32", 
                             command=alternar_senha)
    btn_olho.pack(side="left", padx=5)

    # Botão Entrar
    ctk.CTkButton(card, text="→ Entrar", fg_color="#D81B60", hover_color="#AD1457", 
                  width=270, height=45, font=("sans-serif", 16, "bold"),
                  command=lambda: fazer_login(entry_rm.get(), entry_senha.get())).pack(pady=10)