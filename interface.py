import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import logging
from core import verificar_ffmpeg, limpar_metadados, processar_lote, validar_arquivo_video, obter_metadados, security_logger

class LimpaMetadadosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Limpa Metadados")
        self.root.geometry("750x800")
        self.root.resizable(False, False)
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
        
        # Botões de arquivo com tamanhos adequados
        botoes_arquivo_frame = ttk.Frame(arquivo_frame)
        botoes_arquivo_frame.pack(fill=tk.X)
        
        ttk.Button(botoes_arquivo_frame, text="Adicionar Arquivos", 
                  command=self.selecionar_arquivos, width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botoes_arquivo_frame, text="Remover", 
                  command=self.remover_arquivo, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botoes_arquivo_frame, text="Limpar Tudo", 
                  command=self.limpar_lista, width=15).pack(side=tk.LEFT)
        
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
                  width=12).pack(side=tk.RIGHT)
        
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
        
        self.btn_processar = ttk.Button(botoes_frame, text="Processar Arquivos", 
                                       command=self.processar_arquivos, width=20)
        self.btn_processar.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(botoes_frame, text="Ver Metadados", 
                  command=self.visualizar_metadados, width=20).pack(side=tk.LEFT)
        
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
            self.log("Sistema pronto - Versão 1.0.3 com correção crítica de caminhos")
            security_logger.info("Interface iniciada com sucesso")
        else:
            self.log(f"ERRO: {mensagem}")
            security_logger.error(f"Falha na inicialização: {mensagem}")
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
        rejeitados = 0
        for arquivo in arquivos:
            if arquivo not in self.arquivos_selecionados:
                if validar_arquivo_video(arquivo):
                    self.arquivos_selecionados.append(arquivo)
                    nome = os.path.basename(arquivo)
                    self.lista_arquivos.insert(tk.END, nome)
                    adicionados += 1
                    security_logger.info(f"Arquivo aceito: {nome}")
                else:
                    rejeitados += 1
                    self.log(f"Arquivo rejeitado por segurança: {os.path.basename(arquivo)}")
                    security_logger.warning(f"Arquivo rejeitado: {os.path.basename(arquivo)}")
        
        if adicionados > 0:
            self.log(f"{adicionados} arquivo(s) adicionado(s)")
            self.atualizar_status(f"{len(self.arquivos_selecionados)} arquivo(s) selecionado(s)")
        
        if rejeitados > 0:
            messagebox.showwarning("Arquivos Rejeitados", 
                                 f"{rejeitados} arquivo(s) foram rejeitados por não passarem na validação de segurança.")
    
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
            
            resultados = []
            try:
                total = len(self.arquivos_selecionados)
                sucessos = 0
                erros = 0
                
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
                        pasta_original = os.path.dirname(arquivo)
                        nome_limpo = os.path.splitext(nome)[0] + "_limpo.mp4"
                        arquivo_saida = os.path.join(pasta_original, nome_limpo)
                    
                    sucesso, mensagem = limpar_metadados(arquivo, arquivo_saida)
                    
                    resultado = {
                        'arquivo_original': nome,
                        'arquivo_limpo': os.path.basename(arquivo_saida) if sucesso else None,
                        'sucesso': sucesso,
                        'mensagem': mensagem,
                        'tamanho_original': self.obter_tamanho_arquivo(arquivo),
                        'tamanho_limpo': self.obter_tamanho_arquivo(arquivo_saida) if sucesso and os.path.exists(arquivo_saida) else None
                    }
                    
                    resultados.append(resultado)
                    
                    if sucesso:
                        sucessos += 1
                        self.log(f"OK: {nome}")
                    else:
                        erros += 1
                        self.log(f"ERRO: {nome} - {mensagem}")
                
                self.atualizar_status("Processamento concluído", 100)
                self.log(f"Concluído: {sucessos} sucessos, {erros} erros")
                
                # Mostrar modal de resultados
                self.mostrar_resultados_finais(resultados, sucessos, erros)
                
            except Exception as e:
                self.log(f"ERRO CRÍTICO: {str(e)}")
                messagebox.showerror("Erro", f"Erro durante processamento:\n{str(e)}")
                self.atualizar_status("Erro no processamento", 0)
            
            finally:
                self.processando = False
                self.btn_processar.config(state='normal', text="Processar Arquivos")
        
        thread = threading.Thread(target=processar, daemon=True)
        thread.start()
    
    def obter_tamanho_arquivo(self, caminho):
        try:
            if os.path.exists(caminho):
                tamanho = os.path.getsize(caminho)
                return self.formatar_tamanho(tamanho)
            return "N/A"
        except:
            return "N/A"
    
    def formatar_tamanho(self, bytes):
        for unidade in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unidade}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"
    
    def mostrar_resultados_finais(self, resultados, sucessos, erros):
        # Criar janela modal de resultados
        janela = tk.Toplevel(self.root)
        janela.title("Resultados do Processamento")
        janela.geometry("800x600")
        janela.resizable(True, True)
        janela.transient(self.root)
        janela.grab_set()
        
        # Centralizar janela
        janela.update_idletasks()
        x = (janela.winfo_screenwidth() // 2) - (800 // 2)
        y = (janela.winfo_screenheight() // 2) - (600 // 2)
        janela.geometry(f"800x600+{x}+{y}")
        
        main_frame = ttk.Frame(janela, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Processamento Concluído", 
                          font=("Segoe UI", 16, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Resumo
        resumo_frame = ttk.Frame(main_frame)
        resumo_frame.pack(fill=tk.X, pady=(0, 20))
        
        total = len(resultados)
        
        if sucessos == total:
            cor_status = "green"
            texto_status = "Todos os arquivos processados com sucesso!"
        elif sucessos > 0:
            cor_status = "orange"
            texto_status = f"{sucessos} de {total} arquivos processados com sucesso"
        else:
            cor_status = "red"
            texto_status = "Nenhum arquivo foi processado com sucesso"
        
        status_label = ttk.Label(resumo_frame, text=texto_status, 
                                font=("Segoe UI", 12, "bold"), foreground=cor_status)
        status_label.pack()
        
        stats_label = ttk.Label(resumo_frame, 
                               text=f"Total: {total} | Sucessos: {sucessos} | Erros: {erros}",
                               font=("Segoe UI", 10))
        stats_label.pack(pady=(5, 0))
        
        # Tabela de resultados
        tabela_frame = ttk.Frame(main_frame)
        tabela_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Criar treeview para mostrar resultados detalhados
        colunas = ("status", "original", "limpo", "tamanho_antes", "tamanho_depois")
        tree = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=15)
        
        # Configurar colunas
        tree.heading("status", text="Status")
        tree.heading("original", text="Arquivo Original")
        tree.heading("limpo", text="Arquivo Limpo")
        tree.heading("tamanho_antes", text="Tamanho Antes")
        tree.heading("tamanho_depois", text="Tamanho Depois")
        
        tree.column("status", width=80, anchor="center")
        tree.column("original", width=200)
        tree.column("limpo", width=200)
        tree.column("tamanho_antes", width=100, anchor="center")
        tree.column("tamanho_depois", width=100, anchor="center")
        
        # Adicionar resultados
        for resultado in resultados:
            status = "✓ OK" if resultado['sucesso'] else "✗ ERRO"
            original = resultado['arquivo_original']
            limpo = resultado['arquivo_limpo'] or "N/A"
            tamanho_antes = resultado['tamanho_original']
            tamanho_depois = resultado['tamanho_limpo'] or "N/A"
            
            tree.insert("", "end", values=(status, original, limpo, tamanho_antes, tamanho_depois))
        
        # Scrollbar para tabela
        scrollbar_tabela = ttk.Scrollbar(tabela_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_tabela.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar_tabela.pack(side="right", fill="y")
        
        # Botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X)
        
        ttk.Button(botoes_frame, text="Abrir Pasta de Destino", 
                  command=lambda: self.abrir_pasta_destino(), width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(botoes_frame, text="Fechar", 
                  command=janela.destroy, width=15).pack(side=tk.RIGHT)
    
    def abrir_pasta_destino(self):
        if self.pasta_saida and os.path.exists(self.pasta_saida):
            os.startfile(self.pasta_saida)
        elif self.arquivos_selecionados:
            pasta = os.path.dirname(self.arquivos_selecionados[0])
            if os.path.exists(pasta):
                os.startfile(pasta)
    
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
                janela.geometry("700x500")
                janela.resizable(True, True)
                
                frame = ttk.Frame(janela, padding=15)
                frame.pack(fill=tk.BOTH, expand=True)
                
                ttk.Label(frame, text=f"Arquivo: {nome}", 
                         font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
                
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