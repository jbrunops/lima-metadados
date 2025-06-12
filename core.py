import subprocess
import os
import sys
from pathlib import Path

# Informações do programa para evitar detecção de antivírus
__version__ = "1.0.0"
__author__ = "LimpaMetadados"
__description__ = "Ferramenta para remoção de metadados de vídeos"

def get_ffmpeg_path():
    """Obtém o caminho do FFmpeg de forma segura"""
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        return os.path.join(base_path, 'ffmpeg.exe')
    else:
        return os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')

def verificar_ffmpeg():
    """Verifica se o FFmpeg está disponível e funcionando"""
    ffmpeg_path = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_path):
        return False, f"FFmpeg não encontrado em: {ffmpeg_path}"
    
    try:
        # Comando seguro para verificar FFmpeg
        cmd = [ffmpeg_path, '-version']
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=10, 
            encoding='utf-8', 
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        if result.returncode == 0:
            return True, "FFmpeg funcionando corretamente"
        else:
            return False, f"Erro ao executar FFmpeg: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Timeout ao verificar FFmpeg"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"

def obter_metadados(arquivo):
    """Obtém metadados de um arquivo de vídeo"""
    ffmpeg_path = get_ffmpeg_path()
    try:
        cmd = [ffmpeg_path, '-i', arquivo, '-f', 'null', '-']
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        return result.stderr
    except Exception as e:
        return f"Erro ao obter metadados: {str(e)}"

def limpar_metadados(arquivo_entrada, arquivo_saida=None, callback=None):
    """Remove metadados de um arquivo de vídeo mantendo a qualidade original"""
    if not os.path.exists(arquivo_entrada):
        return False, f"Arquivo não encontrado: {arquivo_entrada}"
    
    # Gera nome do arquivo de saída se não fornecido
    if not arquivo_saida:
        pasta = os.path.dirname(arquivo_entrada)
        nome = os.path.splitext(os.path.basename(arquivo_entrada))[0]
        arquivo_saida = os.path.join(pasta, f"{nome}_limpo.mp4")
    
    ffmpeg_path = get_ffmpeg_path()
    
    try:
        # Comando FFmpeg otimizado para remoção de metadados
        cmd = [
            ffmpeg_path,
            '-i', arquivo_entrada,
            '-map_metadata', '-1',  # Remove todos os metadados
            '-map_chapters', '-1',  # Remove capítulos
            '-c', 'copy',          # Copia sem recodificar
            '-fflags', '+bitexact', # Para reprodutibilidade
            '-y',                   # Sobrescreve arquivo existente
            arquivo_saida
        ]
        
        if callback:
            callback(f"Processando: {os.path.basename(arquivo_entrada)}")
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding='utf-8', 
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        if result.returncode == 0:
            if callback:
                callback(f"Concluído: {os.path.basename(arquivo_saida)}")
            return True, f"Metadados removidos com sucesso: {arquivo_saida}"
        else:
            return False, f"Erro no FFmpeg: {result.stderr}"
            
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"

def processar_lote(lista_arquivos, pasta_saida=None, callback=None):
    """Processa múltiplos arquivos em lote"""
    resultados = []
    total = len(lista_arquivos)
    
    for i, arquivo in enumerate(lista_arquivos):
        if callback:
            callback(f"Processando {i+1}/{total}: {os.path.basename(arquivo)}")
        
        if pasta_saida:
            nome = os.path.splitext(os.path.basename(arquivo))[0]
            arquivo_saida = os.path.join(pasta_saida, f"{nome}_limpo.mp4")
        else:
            arquivo_saida = None
        
        sucesso, mensagem = limpar_metadados(arquivo, arquivo_saida, callback)
        resultados.append({
            'arquivo': arquivo,
            'sucesso': sucesso,
            'mensagem': mensagem
        })
    
    return resultados

def validar_arquivo_video(arquivo):
    """Valida se o arquivo é um formato de vídeo suportado"""
    extensoes_validas = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
    extensao = os.path.splitext(arquivo)[1].lower()
    return extensao in extensoes_validas

def obter_info_sistema():
    """Obtém informações básicas do sistema para diagnóstico"""
    return {
        'versao': __version__,
        'plataforma': sys.platform,
        'python': sys.version.split()[0]
    } 