import subprocess
import os
import sys
from pathlib import Path

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'ffmpeg.exe')
    else:
        return os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')

def verificar_ffmpeg():
    ffmpeg_path = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_path):
        return False, f"FFmpeg não encontrado em: {ffmpeg_path}"
    
    try:
        result = subprocess.run([ffmpeg_path, '-version'], 
                              capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
        if result.returncode == 0:
            return True, "FFmpeg funcionando corretamente"
        else:
            return False, f"Erro ao executar FFmpeg: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Timeout ao verificar FFmpeg"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"

def obter_metadados(arquivo):
    ffmpeg_path = get_ffmpeg_path()
    try:
        cmd = [ffmpeg_path, '-i', arquivo, '-f', 'null', '-']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.stderr
    except Exception as e:
        return f"Erro ao obter metadados: {str(e)}"

def limpar_metadados(arquivo_entrada, arquivo_saida=None, callback=None):
    if not os.path.exists(arquivo_entrada):
        return False, f"Arquivo não encontrado: {arquivo_entrada}"
    
    if not arquivo_saida:
        pasta = os.path.dirname(arquivo_entrada)
        nome = os.path.splitext(os.path.basename(arquivo_entrada))[0]
        arquivo_saida = os.path.join(pasta, f"{nome}_limpo.mp4")
    
    ffmpeg_path = get_ffmpeg_path()
    
    try:
        cmd = [
            ffmpeg_path,
            '-i', arquivo_entrada,
            '-map_metadata', '-1',
            '-map_chapters', '-1',
            '-c', 'copy',
            '-y',
            arquivo_saida
        ]
        
        if callback:
            callback(f"Processando: {os.path.basename(arquivo_entrada)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            if callback:
                callback(f"Concluído: {os.path.basename(arquivo_saida)}")
            return True, f"Metadados removidos com sucesso: {arquivo_saida}"
        else:
            return False, f"Erro no FFmpeg: {result.stderr}"
            
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"

def processar_lote(lista_arquivos, pasta_saida=None, callback=None):
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
    extensoes_validas = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
    extensao = os.path.splitext(arquivo)[1].lower()
    return extensao in extensoes_validas 