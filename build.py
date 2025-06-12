#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
import zipfile
from datetime import datetime

def verificar_dependencias():
    """Verifica e instala dependências necessárias"""
    print("Verificando dependencias...")
    
    try:
        import PyInstaller
        print("PyInstaller instalado")
    except ImportError:
        print("PyInstaller nao encontrado. Instalando...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller==6.11.0"], check=True)
            print("PyInstaller instalado com sucesso")
        except subprocess.CalledProcessError:
            print("Falha ao instalar PyInstaller")
            return False
    
    ffmpeg_path = "ffmpeg.exe"
    if not os.path.exists(ffmpeg_path):
        print(f"❌ {ffmpeg_path} não encontrado na pasta raiz")
        print("   Download FFmpeg em: https://ffmpeg.org/download.html")
        return False
    
    print(f"✅ {ffmpeg_path} encontrado")
    return True

def limpar_build():
    """Remove arquivos de build anteriores"""
    print("🧹 Limpando arquivos de build anteriores...")
    
    pastas_para_remover = ['build', 'dist', '__pycache__']
    
    for pasta in pastas_para_remover:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
            print(f"✅ Removido: {pasta}")
    
    # Remove arquivos .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def compilar_executavel():
    """Compila o executável com PyInstaller"""
    print("🔨 Compilando executável...")
    print("⏳ Isso pode demorar alguns minutos...")
    
    # Usa o arquivo .spec customizado
    comando = [
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "LimpaMetadados.spec"
    ]
    
    try:
        print(f"🚀 Executando: {' '.join(comando)}")
        resultado = subprocess.run(
            comando, 
            check=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        print("✅ Compilação concluída com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante a compilação:")
        print(f"   STDOUT: {e.stdout}")
        print(f"   STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def verificar_executavel():
    """Verifica se o executável foi criado corretamente"""
    executavel = os.path.join("dist", "LimpaMetadados.exe")
    
    if os.path.exists(executavel):
        tamanho = os.path.getsize(executavel) / (1024 * 1024)
        print(f"✅ Executável criado: {executavel} ({tamanho:.1f} MB)")
        return True, executavel
    else:
        print("❌ Executável não foi criado")
        return False, None

def criar_readme_distribuicao():
    """Cria README para distribuição"""
    readme_content = """# LimpaMetadados v1.0.3

## 📋 Sobre
Ferramenta para remoção completa de metadados de arquivos de vídeo com melhorias críticas de segurança.

## 🚀 Como Usar
1. Execute LimpaMetadados.exe
2. Adicione seus arquivos de vídeo
3. Clique em "Processar"
4. Aguarde a conclusão

## 📁 Formatos Suportados
- MP4, AVI, MKV, MOV
- WMV, FLV, WebM, M4V

## 🛡️ Segurança
- Funciona 100% offline
- Não envia dados para internet
- Mantém qualidade original dos vídeos
- Remove completamente todos os metadados

## ⚠️ Importante
- Faça backup dos arquivos originais
- Alguns antivírus podem dar falso positivo
- O programa é completamente seguro

## 🆘 Suporte
Se o Windows Defender bloquear o programa:
1. É um falso positivo comum
2. Adicione exceção no antivírus
3. O programa não acessa a internet

## 📄 Licença
Software gratuito para uso pessoal e comercial.
"""
    
    with open('README_DISTRIBUICAO.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README de distribuição criado")

def criar_pacote_zip(executavel_path):
    """Cria arquivo ZIP para distribuição"""
    data_atual = datetime.now().strftime("%Y%m%d")
    nome_zip = f"LimpaMetadados_v1.0.3_{data_atual}.zip"
    
    print(f"📦 Criando pacote: {nome_zip}")
    
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        # Adiciona o executável
        zipf.write(executavel_path, "LimpaMetadados.exe")
        
        # Adiciona README
        if os.path.exists('README_DISTRIBUICAO.txt'):
            zipf.write('README_DISTRIBUICAO.txt', 'README.txt')
    
    tamanho_zip = os.path.getsize(nome_zip) / (1024 * 1024)
    print(f"✅ Pacote criado: {nome_zip} ({tamanho_zip:.1f} MB)")
    return nome_zip

def main():
    """Função principal de build"""
    print("=" * 50)
    print("BUILD LIMPA METADADOS v1.0.3 - VERSAO COM CORRECAO CRITICA DE CAMINHOS")
    print("=" * 50)
    print()
    
    if not verificar_dependencias():
        print("\n" + "=" * 50)
        print("❌ BUILD FALHOU")
        print("   Resolva os problemas acima e tente novamente")
        print("=" * 50)
        return False
    
    limpar_build()
    
    if not compilar_executavel():
        print("\n" + "=" * 50)
        print("❌ BUILD FALHOU")
        print("=" * 50)
        return False
    
    sucesso, executavel_path = verificar_executavel()
    if not sucesso:
        print("\n" + "=" * 50)
        print("❌ BUILD FALHOU")
        print("=" * 50)
        return False
    
    # Cria arquivos de distribuição
    criar_readme_distribuicao()
    nome_zip = criar_pacote_zip(executavel_path)
    
    print("\n" + "=" * 50)
    print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print(f"📁 Executável: {executavel_path}")
    print(f"📦 Pacote ZIP: {nome_zip}")
    print("\n💡 Dicas:")
    print("   • Teste o executável antes de distribuir")
    print("   • O ZIP está pronto para distribuição")
    print("   • Alguns antivírus podem dar falso positivo")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    sucesso = main()
    if not sucesso:
        sys.exit(1) 