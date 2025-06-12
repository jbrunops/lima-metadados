# Setup do Projeto LimpaMetadados

## 📋 Pré-requisitos

### FFmpeg
Este projeto requer o FFmpeg para funcionar. Por questões de tamanho do repositório, o arquivo `ffmpeg.exe` não está incluído.

**Download do FFmpeg:**
1. Acesse: https://ffmpeg.org/download.html
2. Baixe a versão para Windows
3. Extraia o arquivo `ffmpeg.exe`
4. Coloque o arquivo na pasta raiz do projeto

### Python
- Python 3.7 ou superior
- Instalar dependências: `pip install -r requirements.txt`

## 🚀 Build

Para compilar o executável:
```bash
python build.py
```

## 🔒 Arquivos Sensíveis

Os seguintes arquivos são gerados localmente e não devem ser versionados:
- `ffmpeg.exe` - Binário do FFmpeg (83MB)
- `LimpaMetadados.spec` - Configuração do PyInstaller (contém caminhos locais)
- `version_info.txt` - Informações de build
- `README_DISTRIBUICAO.txt` - Arquivo de distribuição
- `*.zip` - Arquivos compilados
- `build/` e `dist/` - Pastas de build

## 🛡️ Segurança

Para manter o repositório limpo e seguro:
- Arquivos binários grandes ficam no `.gitignore`
- Configurações locais não são versionadas  
- Apenas código fonte essencial é incluído 