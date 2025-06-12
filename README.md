# Limpa Metadados

![GitHub release (latest by date)](https://img.shields.io/github/v/release/jbrunops/limpa-metadados)
![GitHub downloads](https://img.shields.io/github/downloads/jbrunops/limpa-metadados/total)

**Removedor de metadados de arquivos de vídeo**

Remove informações pessoais, localização GPS e outros dados sensíveis de vídeos baixados da internet.

## 📥 Download

### ⬇️ Download Direto - Versão v1.0.2

**Para usar o programa imediatamente:**

🔗 **[Baixar LimpaMetadados.exe](https://github.com/jbrunops/limpa-metadados/releases/download/v1.0.2/LimpaMetadados_v1.0.2_20250612.exe)**

🔗 **[Baixar ZIP Completo](https://github.com/jbrunops/limpa-metadados/releases/download/v1.0.2/LimpaMetadados_v1.0.2_20250612.zip)**

> 🛡️ **Novo na v1.0.2:** MELHORIAS CRÍTICAS DE SEGURANÇA - Sanitização de arquivos, validação MIME real, controle de recursos aprimorado e sistema de auditoria completo

---

### 📦 Outras opções:
- 🔍 [Ver todas as versões](https://github.com/jbrunops/limpa-metadados/releases)
- 📋 [Código fonte completo](https://github.com/jbrunops/limpa-metadados/archive/refs/heads/main.zip)

## 🚀 Como Instalar e Usar

### Instalação (Método 1 - Recomendado):
1. **Baixe** o arquivo `LimpaMetadados.exe` usando o link acima
2. **Salve** em uma pasta de sua escolha
3. **Execute** clicando duas vezes no arquivo
4. **Pronto!** Não precisa instalar nada

### Instalação (Método 2 - ZIP Completo):
1. **Baixe** o arquivo ZIP completo
2. **Extraia** para uma pasta
3. **Execute** o `LimpaMetadados.exe`
4. **Leia** o arquivo README.txt incluído

### Como Usar o Programa:
1. **Abra** o LimpaMetadados.exe
2. **Clique** em "Adicionar Arquivos" e selecione seus vídeos
3. **Configure** a pasta de saída (ou deixe automático)
4. **Clique** em "Processar Arquivos"
5. **Aguarde** o processamento terminar

## 📹 Formatos Suportados

| Formato | Extensão | Status |
|---------|----------|--------|
| MP4     | `.mp4`   | ✅ Suportado |
| AVI     | `.avi`   | ✅ Suportado |
| MKV     | `.mkv`   | ✅ Suportado |
| MOV     | `.mov`   | ✅ Suportado |
| WMV     | `.wmv`   | ✅ Suportado |
| FLV     | `.flv`   | ✅ Suportado |
| WebM    | `.webm`  | ✅ Suportado |

## ✨ Recursos

- 🧹 **Remove todos os metadados** dos vídeos
- 📦 **Processamento em lote** (múltiplos arquivos)
- 🎯 **Mantém a qualidade original** do vídeo
- 🔒 **Funciona offline** (sem conexão à internet)
- 🖥️ **Interface simples e intuitiva**
- ⚡ **Processamento rápido** com FFmpeg
- 📊 **Log detalhado** do processamento
- 🔧 **Não requer instalação**

## Por que Usar

### Informações que podem estar nos seus vídeos:
- Localização GPS onde foi gravado
- Modelo do dispositivo usado
- Nome do usuário do sistema
- Data e hora exatas
- Software utilizado
- Outros dados pessoais

### Benefícios:
- Protege sua privacidade
- Remove rastros pessoais
- Elimina dados de localização
- Permite compartilhamento seguro

## Requisitos

- Windows 7, 8, 10 ou 11
- Não requer instalação
- Funciona sem conexão à internet

## Importante

- Sempre faça backup dos arquivos originais
- O programa não altera a qualidade do vídeo
- Completamente gratuito

## Problemas Comuns

**Windows Defender bloqueia o programa:**
- É um falso positivo comum
- O programa é seguro e não acessa a internet

**Arquivo grande demora para processar:**
- Normal para arquivos grandes
- Aguarde o processamento completar

**Erro ao processar arquivo:**
- Verifique se o arquivo não está corrompido
- Alguns formatos específicos podem não ser suportados

## 🛡️ Segurança

### Melhorias de Segurança v1.0.2
- **Sanitização de arquivos**: Remove caracteres perigosos que poderiam ser explorados
- **Validação MIME real**: Verifica se arquivos são realmente vídeos através de assinatura binária
- **Controle de recursos**: Timeout de 5s para verificações, 5min para processamento
- **Auditoria completa**: Log SHA-256 de todos os arquivos processados
- **Limite de tamanho**: Máximo 10GB por arquivo
- **Proteção contra injeção**: Neutraliza tentativas de execução de comandos maliciosos

### Arquivos de Log
- `limpa_metadados_security.log`: Auditoria completa de todas as operações
- Logs incluem: hash de arquivos, tempo de execução, tentativas de acesso suspeitas

## 📋 Changelog

### v1.0.2 (2024-06-11) - VERSÃO COM MELHORIAS CRÍTICAS DE SEGURANÇA
- 🛡️ **CRÍTICO:** Sistema de sanitização de nomes de arquivos
- 🛡️ **CRÍTICO:** Validação MIME real com verificação de assinatura binária
- 🛡️ **CRÍTICO:** Controle de recursos com timeout de 5s (verificação) e 5min (processamento)
- 🛡️ **CRÍTICO:** Sistema de auditoria com hash SHA-256 de todos os arquivos
- 🛡️ **CRÍTICO:** Limite de 10GB por arquivo
- 📊 **Novo:** Interface com feedback de segurança detalhado
- 📝 **Novo:** Log completo de operações em `limpa_metadados_security.log`
- ⚡ **Melhoria:** Timeout otimizado de 10s para 5s
- 🔒 **Melhoria:** Proteção contra injeção de comandos

### v1.0.1 (2025-06-11)
- ✨ **Novo:** Janela com altura otimizada (800px) para mostrar todos os campos
- 🔒 **Novo:** Janela agora é fixa (não redimensionável)
- 🐛 **Correção:** Melhor visualização da interface
- 📦 **Build:** Nova versão compilada disponível

### v1.0.0 (2025-06-11)
- 🎉 **Inicial:** Primeira versão estável
- ✨ **Recursos:** Remoção completa de metadados
- ✨ **Recursos:** Processamento em lote
- ✨ **Recursos:** Interface gráfica intuitiva
- ✨ **Recursos:** Suporte a múltiplos formatos de vídeo

---

<div align="center">

**⭐ Se este projeto foi útil para você, considere dar uma estrela!**

**🤝 Contribuições são bem-vindas!**

</div>