#!/usr/bin/env python3

import subprocess
import sys
import os

def run_command(cmd, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - OK")
        if result.stdout:
            print(f"📄 Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - ERRO")
        if e.stderr:
            print(f"📄 Erro: {e.stderr.strip()}")
        return False

def main():
    print("🚀 DEPLOY VERSÃO 1.0.3 - LIMPA METADADOS")
    print("="*60)
    
    versao = "v1.0.3"
    
    print(f"📋 Versão: {versao}")
    print("📋 Este script irá:")
    print("   1. Fazer commit das alterações")
    print("   2. Criar/atualizar a tag v1.0.3")
    print("   3. Fazer push para o GitHub")
    print("   4. O GitHub Actions criará o release automaticamente")
    
    resposta = input("\n❓ Deseja continuar? (s/N): ").lower()
    if resposta != 's':
        print("❌ Operação cancelada")
        return
    
    # 1. Add e commit das alterações
    if not run_command("git add .", "Adicionando todas as alterações"):
        return
    
    if not run_command('git commit -m "feat: atualiza para versão 1.0.3 com correções críticas de caminhos"', "Fazendo commit das alterações"):
        return
    
    # 2. Criar/atualizar tag
    run_command(f"git tag -d {versao}", "Removendo tag existente (se houver)")
    
    if not run_command(f'git tag -a {versao} -m "Release {versao} - Correção crítica de caminhos"', f"Criando tag {versao}"):
        return
    
    # 3. Push das alterações e tags
    if not run_command("git push origin main", "Fazendo push das alterações"):
        return
    
    if not run_command(f"git push origin {versao} --force", f"Fazendo push da tag {versao}"):
        return
    
    print("\n" + "="*60)
    print("🎉 DEPLOY DA V1.0.3 CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("📋 O que aconteceu:")
    print(f"   ✅ Versão atualizada para {versao}")
    print("   ✅ README atualizado com links corretos")
    print("   ✅ Todos os arquivos de build atualizados")
    print(f"   ✅ Tag {versao} criada e enviada")
    print("   🔄 GitHub Actions está executando o build...")
    
    print("\n📍 Próximos passos:")
    print("   1. Aguarde ~5-10 minutos para o GitHub Actions terminar")
    print("   2. Acesse: https://github.com/jbrunops/lima-metadados/releases")
    print("   3. Verifique se o release v1.0.3 foi criado")
    print("   4. Os links no README agora estarão funcionando!")
    
    print("\n🔗 Links úteis:")
    print("   📦 Releases: https://github.com/jbrunops/lima-metadados/releases")
    print("   🔄 Actions: https://github.com/jbrunops/lima-metadados/actions")
    
    print("\n💡 Agora os usuários poderão baixar:")
    print(f"   📱 LimpaMetadados_v1.0.3_20250612.exe")
    print(f"   📦 LimpaMetadados_v1.0.3_20250612.zip")

if __name__ == "__main__":
    main() 