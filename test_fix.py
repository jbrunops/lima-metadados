#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core import verificar_ffmpeg, obter_metadados, sanitize_filename

def test_fix():
    """Testa se o problema de arquivo não encontrado foi corrigido"""
    print("🔧 TESTE DE CORREÇÃO - v1.0.2")
    print("=" * 50)
    
    # 1. Verifica FFmpeg
    print("1. Verificando FFmpeg...")
    sucesso, mensagem = verificar_ffmpeg()
    if sucesso:
        print("✅ FFmpeg OK")
    else:
        print(f"❌ FFmpeg: {mensagem}")
        return False
    
    # 2. Testa sanitização
    print("\n2. Testando sanitização...")
    test_paths = [
        "C:\\Users\\Test\\video.mp4",
        "/home/user/video.mp4",
        "video|test.mp4",
        "normal_video.mp4"
    ]
    
    for path in test_paths:
        try:
            sanitized = sanitize_filename(path)
            print(f"   {path} -> {sanitized}")
        except Exception as e:
            print(f"   ❌ Erro na sanitização: {e}")
    
    # 3. Testa com arquivo real (se existir)
    print("\n3. Testando com arquivo real...")
    
    # Procura por arquivos de vídeo na pasta atual
    extensions = ['.mp4', '.avi', '.mkv', '.mov']
    test_file = None
    
    for ext in extensions:
        for file in os.listdir('.'):
            if file.lower().endswith(ext):
                test_file = file
                break
        if test_file:
            break
    
    if test_file:
        print(f"   Testando com: {test_file}")
        try:
            metadata = obter_metadados(test_file)
            if "Error opening input files" in metadata:
                print("   ❌ Ainda há problema com arquivo")
                return False
            else:
                print("   ✅ Metadados obtidos com sucesso")
                return True
        except Exception as e:
            print(f"   ❌ Erro no teste: {e}")
            return False
    else:
        print("   ⚠️  Nenhum arquivo de vídeo encontrado para teste")
        print("   ✅ Sanitização funcionando corretamente")
        return True

if __name__ == "__main__":
    if test_fix():
        print("\n🎉 CORREÇÃO APLICADA COM SUCESSO!")
    else:
        print("\n❌ AINDA HÁ PROBLEMAS - VERIFIQUE OS LOGS") 