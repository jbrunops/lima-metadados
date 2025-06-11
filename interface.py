import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from core import verificar_ffmpeg, limpar_metadados, processar_lote, validar_arquivo_video, obter_metadados

class LimpaMetadadosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Limpa Metadados - Removedor de Metadados de Vídeos")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.arquivos_selecionados = []
        self.pasta_saida = None
        
        self.criar_interface()
        self.verificar_ffmpeg_startup()
    
    def criar_interface(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        titulo = ttk.Label(main_frame, text="Limpa Metadados", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Label(main_frame, text="Arquivos Selecionados:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        frame_arquivos = ttk.Frame(main_frame)
        frame_arquivos.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        frame_arquivos.columnconfigure(0, weight=1)
        frame_arquivos.rowconfigure(0, weight=1)
        
        self.lista_arquivos = tk.Listbox(frame_arquivos, height=8)
        self.lista_arquivos.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar_arquivos = ttk.Scrollbar(frame_arquivos, orient="vertical", command=self.lista_arquivos.yview)
        scrollbar_arquivos.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.lista_arquivos.configure(yscrollcommand=scrollbar_arquivos.set)
        
        frame_botoes = ttk.Frame(main_frame)
        frame_botoes.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(frame_botoes, text="Selecionar Arquivos", command=self.selecionar_arquivos).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(frame_botoes, text="Remover Selecionado", command=self.remover_arquivo).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(frame_botoes, text="Limpar Lista", command=self.limpar_lista).pack(side=tk.LEFT, padx=(0, 10))
        
        frame_opcoes = ttk.LabelFrame(main_frame, text="Opções", padding="10")
        frame_opcoes.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_opcoes.columnconfigure(1, weight=1)
        
        ttk.Label(frame_opcoes, text="Pasta de Saída:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.label_pasta_saida = ttk.Label(frame_opcoes, text="Mesma pasta dos arquivos originais", foreground="gray")
        self.label_pasta_saida.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        ttk.Button(frame_opcoes, text="Escolher Pasta", command=self.escolher_pasta_saida).grid(row=0, column=2)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        frame_acoes = ttk.Frame(main_frame)
        frame_acoes.grid(row=6, column=0, columnspan=3, pady=(0, 10))
        
        self.btn_processar = ttk.Button(frame_acoes, text="Limpar Metadados", command=self.processar_arquivos)
        self.btn_processar.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(frame_acoes, text="Visualizar Metadados", command=self.visualizar_metadados).pack(side=tk.LEFT)
        
        frame_log = ttk.LabelFrame(main_frame, text="Log", padding="5")
        frame_log.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        frame_log.columnconfigure(0, weight=1)
        frame_log.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(frame_log, height=8, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def log(self, mensagem):
        self.log_text.insert(tk.END, f"{mensagem}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def verificar_ffmpeg_startup(self):
        sucesso, mensagem = verificar_ffmpeg()
        if sucesso:
            self.log(f"✓ {mensagem}")
        else:
            self.log(f"✗ {mensagem}")
            messagebox.showerror("Erro", f"FFmpeg não está funcionando:\n{mensagem}")
    
    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecionar Arquivos de Vídeo",
            filetypes=[
                ("Arquivos de Vídeo", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                ("MP4", "*.mp4"),
                ("Todos os Arquivos", "*.*")
            ]
        )
        
        for arquivo in arquivos:
            if arquivo not in self.arquivos_selecionados:
                if validar_arquivo_video(arquivo):
                    self.arquivos_selecionados.append(arquivo)
                    self.lista_arquivos.insert(tk.END, os.path.basename(arquivo))
                    self.log(f"Adicionado: {os.path.basename(arquivo)}")
                else:
                    self.log(f"Arquivo ignorado (formato não suportado): {os.path.basename(arquivo)}")
    
    def remover_arquivo(self):
        selecionado = self.lista_arquivos.curselection()
        if selecionado:
            index = selecionado[0]
            arquivo_removido = self.arquivos_selecionados.pop(index)
            self.lista_arquivos.delete(index)
            self.log(f"Removido: {os.path.basename(arquivo_removido)}")
    
    def limpar_lista(self):
        self.arquivos_selecionados.clear()
        self.lista_arquivos.delete(0, tk.END)
        self.log("Lista de arquivos limpa")
    
    def escolher_pasta_saida(self):
        pasta = filedialog.askdirectory(title="Escolher Pasta de Saída")
        if pasta:
            self.pasta_saida = pasta
            self.label_pasta_saida.config(text=pasta, foreground="black")
            self.log(f"Pasta de saída definida: {pasta}")
    
    def processar_arquivos(self):
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo!")
            return
        
        def processar():
            self.btn_processar.config(state='disabled')
            self.progress.start()
            
            try:
                resultados = processar_lote(self.arquivos_selecionados, self.pasta_saida, self.log)
                
                sucessos = sum(1 for r in resultados if r['sucesso'])
                total = len(resultados)
                
                self.log(f"\n=== PROCESSAMENTO CONCLUÍDO ===")
                self.log(f"Sucessos: {sucessos}/{total}")
                
                for resultado in resultados:
                    status = "✓" if resultado['sucesso'] else "✗"
                    nome = os.path.basename(resultado['arquivo'])
                    self.log(f"{status} {nome}: {resultado['mensagem']}")
                
                messagebox.showinfo("Concluído", f"Processamento finalizado!\nSucessos: {sucessos}/{total}")
                
            except Exception as e:
                self.log(f"Erro durante o processamento: {str(e)}")
                messagebox.showerror("Erro", f"Erro durante o processamento:\n{str(e)}")
            
            finally:
                self.progress.stop()
                self.btn_processar.config(state='normal')
        
        thread = threading.Thread(target=processar)
        thread.daemon = True
        thread.start()
    
    def visualizar_metadados(self):
        selecionado = self.lista_arquivos.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um arquivo na lista!")
            return
        
        arquivo = self.arquivos_selecionados[selecionado[0]]
        
        def obter_info():
            self.log(f"Obtendo metadados de: {os.path.basename(arquivo)}")
            metadados = obter_metadados(arquivo)
            
            def mostrar_janela():
                janela = tk.Toplevel(self.root)
                janela.title(f"Metadados - {os.path.basename(arquivo)}")
                janela.geometry("600x400")
                
                text_widget = scrolledtext.ScrolledText(janela, wrap=tk.WORD)
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                text_widget.insert('1.0', metadados)
                text_widget.config(state=tk.DISABLED)
            
            self.root.after(0, mostrar_janela)
        
        thread = threading.Thread(target=obter_info)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = LimpaMetadadosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 