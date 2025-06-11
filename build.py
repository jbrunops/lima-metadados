#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil

def verificar_dependencias():
    print("Verificando dependências...")
    
    try:
        import PyInstaller
        print("✓ PyInstaller instalado")
    except ImportError:
        print("✗ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    ffmpeg_path = "ffmpeg.exe"
    if not os.path.exists(ffmpeg_path):
        print(f"✗ {ffmpeg_path} não encontrado na pasta raiz")
        print("Baixe o FFmpeg em https://ffmpeg.org/download.html")
        print("Extraia o arquivo ffmpeg.exe para a pasta raiz do projeto")
        return False
    
    print(f"✓ {ffmpeg_path} encontrado")
    return True

def limpar_build():
    print("Limpando arquivos de build anteriores...")
    
    pastas_para_remover = ['build', 'dist', '__pycache__']
    
    for pasta in pastas_para_remover:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
            print(f"✓ Removido: {pasta}")
    
    arquivos_spec = [f for f in os.listdir('.') if f.endswith('.spec')]
    for arquivo in arquivos_spec:
        os.remove(arquivo)
        print(f"✓ Removido: {arquivo}")

def compilar_executavel():
    print("Compilando executável...")
    print("Isso pode demorar alguns minutos...")
    
    comando = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--add-data", "ffmpeg.exe;.",
        "--name", "LimpaMetadados",
        "--icon", "icon.ico" if os.path.exists("icon.ico") else None,
        "main.py"
    ]
    
    comando = [c for c in comando if c is not None]
    
    try:
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        print("✓ Compilação concluída com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro durante a compilação: {e}")
        print("Saída do erro:", e.stderr)
        return False

def verificar_executavel():
    executavel = os.path.join("dist", "LimpaMetadados.exe")
    
    if os.path.exists(executavel):
        tamanho = os.path.getsize(executavel) / (1024 * 1024)
        print(f"✓ Executável criado: {executavel} ({tamanho:.1f} MB)")
        return True
    else:
        print("✗ Executável não foi criado")
        return False

def main():
    print("=== BUILD LIMPA METADADOS ===\n")
    
    if not verificar_dependencias():
        return
    
    limpar_build()
    
    if compilar_executavel():
        if verificar_executavel():
            print("\n=== BUILD CONCLUÍDO ===")
            print("Executável disponível em: dist/LimpaMetadados.exe")
            print("Você pode distribuir este arquivo para qualquer computador Windows")
        else:
            print("\n=== BUILD FALHOU ===")
    else:
        print("\n=== BUILD FALHOU ===")

if __name__ == "__main__":
    main() 