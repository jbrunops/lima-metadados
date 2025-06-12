#!/usr/bin/env python3

import os
import zipfile
import subprocess
from datetime import datetime

def verificar_git_repo():
    """Verifica se estamos em um repositório Git"""
    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Não é um repositório Git válido")
        return False

def obter_versao_atual():
    """Obtém a versão atual do projeto"""
    try:
        with open('LimpaMetadados.spec', 'r', encoding='utf-8') as f:
            content = f.read()
            # Procura pela versão no arquivo spec
            if '1, 0, 3, 0' in content:
                return "v1.0.3"
        return "v1.0.3"  # versão padrão
    except:
        return "v1.0.3"

def criar_release_assets():
    """Cria os arquivos necessários para o release"""
    print("📦 Preparando assets do release...")
    
    versao = obter_versao_atual()
    data_atual = datetime.now().strftime("%Y%m%d")
    
    # Verifica se o executável existe
    if not os.path.exists('dist/LimpaMetadados.exe'):
        print("❌ Executável não encontrado. Execute 'py build.py' primeiro")
        return None
    
    # Nome dos arquivos de release
    exe_name = f"LimpaMetadados_{versao}_{data_atual}.exe"
    zip_name = f"LimpaMetadados_{versao}_{data_atual}.zip"
    
    # Copia o executável com nome versionado
    import shutil
    shutil.copy2('dist/LimpaMetadados.exe', exe_name)
    print(f"✅ Executável criado: {exe_name}")
    
    # Cria ZIP se não existir ou se estiver desatualizado
    if not os.path.exists(zip_name) or os.path.getmtime('dist/LimpaMetadados.exe') > os.path.getmtime(zip_name):
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            zipf.write('dist/LimpaMetadados.exe', 'LimpaMetadados.exe')
            
            # Adiciona README se existir
            if os.path.exists('README_DISTRIBUICAO.txt'):
                zipf.write('README_DISTRIBUICAO.txt', 'README.txt')
        
        print(f"✅ ZIP criado: {zip_name}")
    
    return {
        'versao': versao,
        'executavel': exe_name,
        'zip': zip_name,
        'data': data_atual
    }

def criar_release_notes(versao, data):
    """Cria notas de release"""
    notes = f"""# LimpaMetadados {versao}

## 🎯 O que há de novo
- Melhorias críticas de segurança
- Interface otimizada
- Processamento mais rápido
- Redução de falsos positivos em antivírus

## 📁 Arquivos disponíveis
- **LimpaMetadados_{versao}_{data}.exe** - Executável standalone (Windows)
- **LimpaMetadados_{versao}_{data}.zip** - Pacote completo com documentação
- **Source code** - Código fonte

## 🚀 Como usar
1. Baixe o arquivo `.exe` ou `.zip`
2. Execute LimpaMetadados.exe
3. Adicione seus vídeos e processe

## 🛡️ Segurança
- Funciona 100% offline
- Não acessa a internet
- Código open source verificável
- Alguns antivírus podem dar falso positivo (é normal)

## 📋 Requisitos
- Windows 7/8/10/11
- Não requer instalação do Python
"""
    return notes

def instruções_manual():
    """Mostra instruções para criar release manual"""
    assets = criar_release_assets()
    if not assets:
        return
    
    print("\n" + "="*60)
    print("🎯 ASSETS PRONTOS PARA RELEASE")
    print("="*60)
    print(f"📁 Executável: {assets['executavel']}")
    print(f"📦 ZIP: {assets['zip']}")
    print(f"🏷️  Versão: {assets['versao']}")
    
    print("\n" + "="*60)
    print("📋 INSTRUÇÕES PARA CRIAR RELEASE NO GITHUB")
    print("="*60)
    print("1. Acesse: https://github.com/SEU_USUARIO/SEU_REPO/releases/new")
    print(f"2. Tag: {assets['versao']}")
    print(f"3. Título: LimpaMetadados {assets['versao']}")
    print("4. Anexe os arquivos:")
    print(f"   - {assets['executavel']}")
    print(f"   - {assets['zip']}")
    print("5. Cole as release notes abaixo:")
    
    print("\n" + "-"*40)
    print("RELEASE NOTES:")
    print("-"*40)
    print(criar_release_notes(assets['versao'], assets['data']))
    print("-"*40)
    
    print("\n✅ Seus usuários poderão baixar o .exe diretamente!")

def main():
    """Função principal"""
    print("🚀 CRIADOR DE RELEASE - LIMPA METADADOS")
    print("="*50)
    
    if not verificar_git_repo():
        return
    
    instruções_manual()

if __name__ == "__main__":
    main() 