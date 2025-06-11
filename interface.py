import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from core import verificar_ffmpeg, limpar_metadados, processar_lote, validar_arquivo_video, obter_metadados

class LimpaMetadadosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Limpa Metadados")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')
        
        self.arquivos_selecionados = []
        self.pasta_saida = None
        self.processando = False
        
        self.criar_interface()
        self.verificar_ffmpeg_startup()
    
    def criar_interface(self):
        # Container principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = ttk.Label(titulo_frame, text="Limpa Metadados", font=("Segoe UI", 18, "bold"))
        titulo.pack()
        
        subtitulo = ttk.Label(titulo_frame, text="Remover metadados de arquivos de vídeo", 
                             font=("Segoe UI", 10), foreground="gray")
        subtitulo.pack()
        
        # Seção de arquivos
        arquivo_frame = ttk.LabelFrame(main_frame, text="Arquivos", padding=15)
        arquivo_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Lista de arquivos
        lista_frame = ttk.Frame(arquivo_frame)
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.lista_arquivos = tk.Listbox(lista_frame, height=8, font=("Segoe UI", 9),
                                        selectmode=tk.SINGLE, relief=tk.FLAT, bd=1)
        self.lista_arquivos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.lista_arquivos.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_arquivos.configure(yscrollcommand=scrollbar.set)
        
        # Botões de arquivo
        botoes_arquivo_frame = ttk.Frame(arquivo_frame)
        botoes_arquivo_frame.pack(fill=tk.X)
        
        ttk.Button(botoes_arquivo_frame, text="Adicionar Arquivos", 
                  command=self.selecionar_arquivos, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botoes_arquivo_frame, text="Remover", 
                  command=self.remover_arquivo, width=10).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botoes_arquivo_frame, text="Limpar Tudo", 
                  command=self.limpar_lista, width=10).pack(side=tk.LEFT)
        
        # Seção de configurações
        config_frame = ttk.LabelFrame(main_frame, text="Configurações", padding=15)
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Pasta de saída
        pasta_frame = ttk.Frame(config_frame)
        pasta_frame.pack(fill=tk.X)
        
        ttk.Label(pasta_frame, text="Pasta de saída:").pack(side=tk.LEFT)
        self.label_pasta_saida = ttk.Label(pasta_frame, text="Mesma pasta dos arquivos originais", 
                                          foreground="gray", font=("Segoe UI", 9))
        self.label_pasta_saida.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        ttk.Button(pasta_frame, text="Alterar", command=self.escolher_pasta_saida, 
                  width=8).pack(side=tk.RIGHT)
        
        # Seção de processamento
        processo_frame = ttk.LabelFrame(main_frame, text="Processamento", padding=15)
        processo_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(processo_frame, variable=self.progress_var, 
                                       maximum=100, length=400)
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(processo_frame, text="Pronto para processar", 
                                     font=("Segoe UI", 9))
        self.status_label.pack()
        
        # Botões principais
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.btn_processar = ttk.Button(botoes_frame, text="Processar", 
                                       command=self.processar_arquivos, width=15)
        self.btn_processar.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(botoes_frame, text="Ver Metadados", 
                  command=self.visualizar_metadados, width=15).pack(side=tk.LEFT)
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, font=("Consolas", 9),
                                                 wrap=tk.WORD, relief=tk.FLAT, bd=1)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def log(self, mensagem):
        self.log_text.insert(tk.END, f"{mensagem}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def atualizar_status(self, texto, progresso=None):
        self.status_label.config(text=texto)
        if progresso is not None:
            self.progress_var.set(progresso)
        self.root.update_idletasks()
    
    def verificar_ffmpeg_startup(self):
        sucesso, mensagem = verificar_ffmpeg()
        if sucesso:
            self.log("Sistema pronto")
        else:
            self.log(f"ERRO: {mensagem}")
            messagebox.showerror("Erro", f"Sistema não está funcionando:\n{mensagem}")
    
    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecionar Arquivos de Vídeo",
            filetypes=[
                ("Vídeos", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                ("Todos", "*.*")
            ]
        )
        
        adicionados = 0
        for arquivo in arquivos:
            if arquivo not in self.arquivos_selecionados:
                if validar_arquivo_video(arquivo):
                    self.arquivos_selecionados.append(arquivo)
                    nome = os.path.basename(arquivo)
                    self.lista_arquivos.insert(tk.END, nome)
                    adicionados += 1
                else:
                    self.log(f"Formato não suportado: {os.path.basename(arquivo)}")
        
        if adicionados > 0:
            self.log(f"{adicionados} arquivo(s) adicionado(s)")
            self.atualizar_status(f"{len(self.arquivos_selecionados)} arquivo(s) selecionado(s)")
    
    def remover_arquivo(self):
        selecionado = self.lista_arquivos.curselection()
        if selecionado:
            index = selecionado[0]
            arquivo_removido = self.arquivos_selecionados.pop(index)
            self.lista_arquivos.delete(index)
            self.log(f"Removido: {os.path.basename(arquivo_removido)}")
            self.atualizar_status(f"{len(self.arquivos_selecionados)} arquivo(s) selecionado(s)")
    
    def limpar_lista(self):
        self.arquivos_selecionados.clear()
        self.lista_arquivos.delete(0, tk.END)
        self.log("Lista limpa")
        self.atualizar_status("Pronto para processar", 0)
    
    def escolher_pasta_saida(self):
        pasta = filedialog.askdirectory(title="Escolher Pasta de Saída")
        if pasta:
            self.pasta_saida = pasta
            nome_pasta = os.path.basename(pasta) or pasta
            self.label_pasta_saida.config(text=nome_pasta, foreground="black")
            self.log(f"Pasta de saída: {nome_pasta}")
    
    def processar_arquivos(self):
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo")
            return
        
        if self.processando:
            return
        
        def processar():
            self.processando = True
            self.btn_processar.config(state='disabled', text="Processando...")
            
            try:
                total = len(self.arquivos_selecionados)
                sucessos = 0
                
                self.atualizar_status("Iniciando processamento...", 0)
                self.log(f"Processando {total} arquivo(s)...")
                
                for i, arquivo in enumerate(self.arquivos_selecionados):
                    nome = os.path.basename(arquivo)
                    progresso = (i / total) * 100
                    
                    self.atualizar_status(f"Processando: {nome}", progresso)
                    
                    if self.pasta_saida:
                        nome_limpo = os.path.splitext(nome)[0] + "_limpo.mp4"
                        arquivo_saida = os.path.join(self.pasta_saida, nome_limpo)
                    else:
                        arquivo_saida = None
                    
                    sucesso, mensagem = limpar_metadados(arquivo, arquivo_saida)
                    
                    if sucesso:
                        sucessos += 1
                        self.log(f"OK: {nome}")
                    else:
                        self.log(f"ERRO: {nome} - {mensagem}")
                
                self.atualizar_status("Processamento concluído", 100)
                self.log(f"Concluído: {sucessos}/{total} arquivos processados")
                
                if sucessos == total:
                    messagebox.showinfo("Sucesso", f"Todos os {total} arquivos foram processados")
                else:
                    messagebox.showwarning("Concluído com Avisos", 
                                         f"{sucessos} de {total} arquivos processados.\nVerifique o log para detalhes.")
                
            except Exception as e:
                self.log(f"ERRO CRÍTICO: {str(e)}")
                messagebox.showerror("Erro", f"Erro durante processamento:\n{str(e)}")
                self.atualizar_status("Erro no processamento", 0)
            
            finally:
                self.processando = False
                self.btn_processar.config(state='normal', text="Processar")
        
        thread = threading.Thread(target=processar, daemon=True)
        thread.start()
    
    def visualizar_metadados(self):
        selecionado = self.lista_arquivos.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um arquivo na lista")
            return
        
        arquivo = self.arquivos_selecionados[selecionado[0]]
        
        def obter_info():
            nome = os.path.basename(arquivo)
            self.log(f"Obtendo metadados: {nome}")
            metadados = obter_metadados(arquivo)
            
            def mostrar_janela():
                janela = tk.Toplevel(self.root)
                janela.title(f"Metadados - {nome}")
                janela.geometry("600x450")
                janela.resizable(True, True)
                
                frame = ttk.Frame(janela, padding=15)
                frame.pack(fill=tk.BOTH, expand=True)
                
                ttk.Label(frame, text=f"Arquivo: {nome}", font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
                
                text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Consolas", 9))
                text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
                text_widget.insert('1.0', metadados)
                text_widget.config(state=tk.DISABLED)
                
                ttk.Button(frame, text="Fechar", command=janela.destroy).pack()
            
            self.root.after(0, mostrar_janela)
        
        thread = threading.Thread(target=obter_info, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = LimpaMetadadosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 