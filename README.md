# LimpaMetadados

![GitHub release (latest by date)](https://img.shields.io/github/v/release/jbrunops/limpa-metadados)
![GitHub downloads](https://img.shields.io/github/downloads/jbrunops/limpa-metadados/total)

**Ferramenta para remoção segura de metadados de arquivos de vídeo**

O LimpaMetadados é uma aplicação desktop desenvolvida para remover completamente informações pessoais, dados de localização e metadados sensíveis de arquivos de vídeo, garantindo maior privacidade ao compartilhar conteúdo digital.

## Download

### Versão v1.0.3 - Última versão estável

**Download direto:**
- [LimpaMetadados.exe](https://github.com/jbrunops/limpa-metadados/releases/download/v1.0.3/LimpaMetadados_v1.0.3_20250612.exe) - Executável para Windows
- [Pacote completo](https://github.com/jbrunops/limpa-metadados/releases/download/v1.0.3/LimpaMetadados_v1.0.3_20250612.zip) - Inclui documentação

**Outras opções:**
- [Todas as versões](https://github.com/jbrunops/limpa-metadados/releases)
- [Código fonte](https://github.com/jbrunops/limpa-metadados/archive/refs/heads/main.zip)

## Instalação e Uso

### Requisitos do Sistema
- Windows 7, 8, 10 ou 11
- Nenhuma instalação adicional necessária
- Funciona completamente offline

### Instalação
1. Baixe o arquivo `LimpaMetadados.exe`
2. Salve em qualquer pasta de sua preferência
3. Execute o arquivo diretamente (duplo clique)

Não é necessária instalação tradicional. O programa é portátil e autocontido.

### Como Usar
1. Abra o programa LimpaMetadados.exe
2. Clique em "Adicionar Arquivos" para selecionar os vídeos
3. Configure a pasta de destino (opcional)
4. Clique em "Processar Arquivos"
5. Aguarde a conclusão do processamento

## Funcionalidades

### Recursos Principais
- **Remoção completa de metadados**: Elimina todas as informações incorporadas
- **Processamento em lote**: Processa múltiplos arquivos simultaneamente
- **Preservação da qualidade**: Mantém a qualidade original dos vídeos
- **Interface intuitiva**: Design simples e funcional
- **Operação offline**: Não requer conexão com a internet
- **Log detalhado**: Registro completo das operações realizadas

### Formatos Suportados
- MP4 (.mp4)
- AVI (.avi)
- MKV (.mkv)
- MOV (.mov)
- WMV (.wmv)
- FLV (.flv)
- WebM (.webm)

## Segurança e Privacidade

### Tipos de Metadados Removidos
- **Localização GPS**: Coordenadas geográficas de gravação
- **Informações do dispositivo**: Modelo de câmera, smartphone ou equipamento
- **Dados do usuário**: Nome de usuário e configurações do sistema
- **Timestamps**: Datas e horários específicos de criação/modificação
- **Software utilizado**: Informações sobre programas de edição
- **Configurações de câmera**: ISO, abertura, velocidade do obturador
- **Outros metadados técnicos**: Codecs, bitrate, resolução original

### Melhorias de Segurança (v1.0.2+)
- Sanitização automática de nomes de arquivos
- Validação MIME por assinatura binária
- Sistema de auditoria com hash SHA-256
- Controle de recursos com timeouts configuráveis
- Limite de tamanho por arquivo (10GB)
- Proteção contra injeção de comandos

### Arquivos de Log
O programa gera logs de segurança em `limpa_metadados_security.log` contendo:
- Hash SHA-256 de todos os arquivos processados
- Registro temporal de operações
- Detecção de tentativas de acesso suspeitas

## Resolução de Problemas

### Falsos Positivos em Antivírus
Alguns antivírus podem detectar erroneamente o programa como ameaça. Isso é comum em executáveis Python compilados. O programa:
- É completamente seguro e open source
- Não acessa a internet
- Não modifica arquivos de sistema
- Todo código é verificável neste repositório

### Problemas de Performance
- **Arquivos grandes**: O processamento pode demorar dependendo do tamanho
- **Múltiplos arquivos**: Processe em lotes menores se necessário
- **Recursos limitados**: Aguarde a conclusão antes de processar novos arquivos

### Arquivos Corrompidos
Se um arquivo não for processado:
- Verifique se o arquivo não está corrompido
- Confirme se o formato é suportado
- Tente processar individualmente

## Desenvolvimento

### Tecnologias Utilizadas
- **Python 3.11+**: Linguagem principal
- **Tkinter**: Interface gráfica
- **FFmpeg**: Engine de processamento de vídeo
- **PyInstaller**: Compilação para executável

### Estrutura do Projeto
- `main.py`: Ponto de entrada da aplicação
- `interface.py`: Interface gráfica do usuário
- `core.py`: Lógica principal de processamento
- `build.py`: Script de compilação
- `LimpaMetadados.spec`: Configuração do PyInstaller

## Changelog

### v1.0.3 (2024-06-12) - Correções Críticas
- Correção no manuseio de caminhos com caracteres especiais
- Melhoria na detecção de diretórios de saída
- Processamento mais robusto de nomes de arquivos
- Correção de bugs relacionados a caminhos em diferentes sistemas

### v1.0.2 (2024-06-11) - Melhorias de Segurança
- Sistema de sanitização de nomes de arquivos
- Validação MIME real com verificação de assinatura binária
- Controle de recursos com timeouts configuráveis
- Sistema de auditoria com hash SHA-256
- Limite de 10GB por arquivo
- Proteção contra injeção de comandos

### v1.0.1 (2024-06-11) - Otimizações de Interface
- Interface otimizada com altura de 800px
- Janela não redimensionável para melhor UX
- Melhor visualização de todos os elementos

### v1.0.0 (2024-06-11) - Versão Inicial
- Primeira versão estável
- Remoção completa de metadados
- Processamento em lote
- Interface gráfica intuitiva
- Suporte a múltiplos formatos

## Licença

Este software é distribuído gratuitamente para uso pessoal e comercial.

## Suporte

Para reportar problemas ou sugerir melhorias, utilize as [Issues](https://github.com/jbrunops/limpa-metadados/issues) do GitHub.

---

**Desenvolvido com foco em privacidade e segurança digital.**