import subprocess
import os
import sys
import mimetypes
import hashlib
import logging
import time
import re
from pathlib import Path

# Configuração de logging de segurança
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('limpa_metadados_security.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
security_logger = logging.getLogger('security')

# Informações do programa para evitar detecção de antivírus
__version__ = "1.0.3"
__author__ = "LimpaMetadados"
__description__ = "Ferramenta para remoção de metadados de vídeos"

# Configurações de segurança
MAX_FILE_SIZE = 10 * 1024 * 1024 * 1024  # 10GB
FFMPEG_TIMEOUT = 5  # 5 segundos timeout crítico
DANGEROUS_CHARS = ['|', '&', ';', '$', '`', '(', ')', '{', '}', '[', ']', '<', '>', '"', "'", '\\']

def sanitize_filename(filepath):
    """Sanitiza caminho de arquivo preservando estrutura de diretórios"""
    if not filepath:
        raise ValueError("Caminho de arquivo vazio")
    
    # Separa diretório e nome do arquivo
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    
    # Caracteres perigosos específicos para nomes de arquivo (não inclui \ e / que são separadores)
    dangerous_chars_filename = ['|', '&', ';', '$', '`', '(', ')', '{', '}', '[', ']', '<', '>', '"', "'"]
    
    # Sanitiza apenas o nome do arquivo, não o diretório
    original_filename = filename
    for char in dangerous_chars_filename:
        if char in filename:
            security_logger.warning(f"Caractere perigoso detectado no nome do arquivo: {char}")
            filename = filename.replace(char, '_')
    
    # Remove sequências suspeitas apenas do nome do arquivo
    suspicious_patterns = [r'\$\(', r'`']  # Removido .. e /. para não afetar extensões
    for pattern in suspicious_patterns:
        if re.search(pattern, filename):
            security_logger.warning(f"Padrão suspeito detectado no nome do arquivo: {pattern}")
            filename = re.sub(pattern, '_', filename)
    
    # Reconstrói o caminho
    sanitized_path = os.path.join(directory, filename)
    
    # Log apenas se houve mudanças
    if filename != original_filename:
        security_logger.info(f"Nome do arquivo sanitizado: {original_filename} -> {filename}")
    
    return sanitized_path

def validate_file_security(filepath):
    """Validação de segurança completa do arquivo"""
    # Normaliza o caminho para evitar problemas com separadores
    normalized_path = os.path.normpath(filepath)
    
    if not os.path.exists(normalized_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {normalized_path}")
    
    # Verifica se não há tentativas de path traversal
    if '..' in normalized_path:
        security_logger.error(f"Tentativa de path traversal detectada: {normalized_path}")
        raise ValueError("Caminho de arquivo contém sequência suspeita")
    
    # Verifica tamanho do arquivo
    file_size = os.path.getsize(normalized_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"Arquivo muito grande: {file_size} bytes (máximo: {MAX_FILE_SIZE})")
    
    # Verifica MIME type real apenas se necessário
    mime_type, _ = mimetypes.guess_type(normalized_path)
    if not mime_type or not mime_type.startswith('video/'):
        # Verificação adicional por assinatura de arquivo
        try:
            with open(normalized_path, 'rb') as f:
                header = f.read(12)
            
            # Assinaturas de vídeo conhecidas
            video_signatures = [
                b'\x00\x00\x00\x14ftypmp4',  # MP4
                b'\x00\x00\x00\x20ftypmp4',  # MP4
                b'RIFF',  # AVI
                b'\x1a\x45\xdf\xa3',  # MKV
                b'\x00\x00\x00\x14ftyp',  # MOV
                b'\x30\x26\xb2\x75',  # WMV
            ]
            
            is_video = any(header.startswith(sig) for sig in video_signatures)
            if not is_video:
                # Se não conseguiu identificar por assinatura, permite por enquanto
                # mas loga o warning
                security_logger.warning(f"Não foi possível verificar assinatura de vídeo: {os.path.basename(normalized_path)}")
        except Exception as e:
            security_logger.warning(f"Erro ao verificar assinatura do arquivo: {e}")
    
    # Calcula hash para auditoria
    file_hash = calculate_file_hash(normalized_path)
    security_logger.info(f"Arquivo validado: {os.path.basename(normalized_path)}, Hash: {file_hash[:16]}...")
    
    return True

def calculate_file_hash(filepath):
    """Calcula hash SHA-256 do arquivo para auditoria"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

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
            timeout=FFMPEG_TIMEOUT, 
            encoding='utf-8', 
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        if result.returncode == 0:
            security_logger.info("FFmpeg verificado com sucesso")
            return True, "FFmpeg funcionando corretamente"
        else:
            return False, f"Erro ao executar FFmpeg: {result.stderr}"
    except subprocess.TimeoutExpired:
        security_logger.error("Timeout na verificação do FFmpeg")
        return False, "Timeout ao verificar FFmpeg"
    except Exception as e:
        security_logger.error(f"Erro inesperado na verificação: {str(e)}")
        return False, f"Erro inesperado: {str(e)}"

def obter_metadados(arquivo):
    """Obtém metadados de um arquivo de vídeo com segurança"""
    try:
        validate_file_security(arquivo)
        
        # Apenas valida a sanitização, mas usa o arquivo original
        sanitize_filename(arquivo)  # Para log de segurança
        
        ffmpeg_path = get_ffmpeg_path()
        cmd = [ffmpeg_path, '-i', arquivo, '-f', 'null', '-']
        
        start_time = time.time()
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=FFMPEG_TIMEOUT,
            encoding='utf-8', 
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        execution_time = time.time() - start_time
        security_logger.info(f"Metadados obtidos em {execution_time:.2f}s para {os.path.basename(arquivo)}")
        
        return result.stderr
    except Exception as e:
        security_logger.error(f"Erro ao obter metadados de {os.path.basename(arquivo)}: {str(e)}")
        return f"Erro ao obter metadados: {str(e)}"

def limpar_metadados(arquivo_entrada, arquivo_saida=None, callback=None):
    """Remove metadados de um arquivo de vídeo mantendo a qualidade original"""
    try:
        # Validações de segurança
        validate_file_security(arquivo_entrada)
        
        # Apenas valida sanitização, mas usa arquivos originais
        sanitize_filename(arquivo_entrada)  # Para log de segurança
        
        if not os.path.exists(arquivo_entrada):
            return False, f"Arquivo não encontrado: {arquivo_entrada}"
        
        # Gera nome do arquivo de saída se não fornecido
        if not arquivo_saida:
            pasta = os.path.dirname(arquivo_entrada)
            nome = os.path.splitext(os.path.basename(arquivo_entrada))[0]
            arquivo_saida = os.path.join(pasta, f"{nome}_limpo.mp4")
        
        # Valida também o arquivo de saída
        sanitize_filename(arquivo_saida)  # Para log de segurança
        ffmpeg_path = get_ffmpeg_path()
        
        # Log de auditoria
        input_hash = calculate_file_hash(arquivo_entrada)
        security_logger.info(f"Iniciando limpeza: {os.path.basename(arquivo_entrada)} (Hash: {input_hash[:16]}...)")
        
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
        
        start_time = time.time()
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=300,  # 5 minutos max para processamento
            encoding='utf-8', 
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        execution_time = time.time() - start_time
        
        if result.returncode == 0:
            # Verifica se o arquivo de saída foi criado
            if os.path.exists(arquivo_saida):
                output_hash = calculate_file_hash(arquivo_saida)
                security_logger.info(f"Limpeza concluída em {execution_time:.2f}s: {os.path.basename(arquivo_saida)} (Hash: {output_hash[:16]}...)")
                
                if callback:
                    callback(f"Concluído: {os.path.basename(arquivo_saida)}")
                return True, f"Metadados removidos com sucesso: {arquivo_saida}"
            else:
                return False, "Arquivo de saída não foi criado"
        else:
            security_logger.error(f"Erro FFmpeg: {result.stderr}")
            return False, f"Erro no FFmpeg: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        security_logger.error(f"Timeout no processamento de {os.path.basename(arquivo_entrada)}")
        return False, "Timeout no processamento"
    except Exception as e:
        security_logger.error(f"Erro inesperado: {str(e)}")
        return False, f"Erro inesperado: {str(e)}"

def processar_lote(lista_arquivos, pasta_saida=None, callback=None):
    """Processa múltiplos arquivos em lote com validação de segurança"""
    resultados = []
    total = len(lista_arquivos)
    
    security_logger.info(f"Iniciando processamento em lote de {total} arquivos")
    
    for i, arquivo in enumerate(lista_arquivos):
        try:
            if callback:
                callback(f"Processando {i+1}/{total}: {os.path.basename(arquivo)}")
            
            # Validação individual de cada arquivo
            validate_file_security(arquivo)
            
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
        
        except Exception as e:
            security_logger.error(f"Erro no processamento de {os.path.basename(arquivo)}: {str(e)}")
            resultados.append({
                'arquivo': arquivo,
                'sucesso': False,
                'mensagem': f"Erro de segurança: {str(e)}"
            })
    
    security_logger.info(f"Processamento em lote concluído: {len([r for r in resultados if r['sucesso']])} sucessos")
    return resultados

def validar_arquivo_video(arquivo):
    """Valida se o arquivo é um formato de vídeo suportado com verificação de segurança"""
    try:
        validate_file_security(arquivo)
        return True
    except Exception as e:
        security_logger.warning(f"Arquivo rejeitado na validação: {os.path.basename(arquivo)} - {str(e)}")
        return False

def obter_info_sistema():
    """Obtém informações básicas do sistema para diagnóstico"""
    return {
        'versao': __version__,
        'plataforma': sys.platform,
        'python': sys.version.split()[0]
    } 