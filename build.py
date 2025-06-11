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
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✓ PyInstaller instalado com sucesso")
        except subprocess.CalledProcessError:
            print("✗ Falha ao instalar PyInstaller")
            return False
    
    ffmpeg_path = "ffmpeg.exe"
    if not os.path.exists(ffmpeg_path):
        print(f"✗ {ffmpeg_path} não encontrado na pasta raiz")
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
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--add-data", "ffmpeg.exe;.",
        "--name", "LimpaMetadados",
        "main.py"
    ]
    
    try:
        print("Executando:", " ".join(comando))
        resultado = subprocess.run(comando, check=True, capture_output=False, text=True)
        print("✓ Compilação concluída com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro durante a compilação: {e}")
        return False
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
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
        print("\n=== BUILD FALHOU ===")
        print("Resolva os problemas acima e tente novamente")
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