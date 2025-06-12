# 📁 Documentação - LimpaMetadados

Esta pasta contém toda a documentação adicional do projeto, mantendo o repositório principal limpo e organizado.

## 📋 Conteúdo

### 📝 **Release Notes**
- `RELEASE_NOTES.md` - Histórico completo de versões
- `RELEASE_NOTES_v1.0.2.md` - Detalhes específicos da v1.0.2

### 🛡️ **Segurança**
- `SEGURANCA_v1.0.2.md` - Relatório completo de melhorias de segurança

### 🚀 **Setup e Distribuição**
- `SETUP.md` - Instruções de setup para desenvolvimento
- `README_DISTRIBUICAO.txt` - README para pacotes de distribuição

## 🎯 **Organização**

### **Arquivos mantidos na raiz:**
```
├── README.md              # Documentação principal (visível no GitHub)
├── main.py                # Ponto de entrada da aplicação
├── core.py                # Lógica principal e funções de segurança
├── interface.py           # Interface gráfica do usuário
├── build.py               # Script de build e empacotamento
├── requirements.txt       # Dependências Python
├── version_info.txt       # Informações de versão para Windows
├── LimpaMetadados.spec    # Configuração PyInstaller
├── ffmpeg.exe            # Binário FFmpeg (ignorado no git)
└── .gitignore            # Configurações do git
```

### **Arquivos organizados em docs/:**
```
docs/
├── README.md                    # Este arquivo
├── RELEASE_NOTES.md            # Histórico de versões
├── RELEASE_NOTES_v1.0.2.md     # Detalhes v1.0.2
├── SEGURANCA_v1.0.2.md         # Relatório de segurança
├── SETUP.md                    # Setup de desenvolvimento
└── README_DISTRIBUICAO.txt     # README de distribuição
```

### **Arquivos ignorados (.gitignore):**
```
# Logs e arquivos temporários
*.log
limpa_metadados_security.log
*.tmp
*.temp
test_*.py

# Builds e distribuição
*.zip
*.exe (exceto ffmpeg.exe)
build/
dist/

# Arquivos de desenvolvimento
__pycache__/
.vscode/
```

## ✅ **Benefícios da Organização**

1. **Repositório limpo**: Apenas código e arquivos essenciais na raiz
2. **Documentação organizada**: Fácil navegação na pasta docs/
3. **GitHub mais profissional**: Interface limpa sem poluição visual
4. **Manutenção simplificada**: Documentação centralizada
5. **Contribuição facilitada**: Estrutura clara para novos contribuidores

---

**💡 Esta organização segue as melhores práticas de projetos open source profissionais.** 