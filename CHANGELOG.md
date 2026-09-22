# Changelog

## [0.8.6] - 2026-09-07
### Added
- Reescrita completa da interface e lógica do projeto utilizando **PyQt6**

### Changed
- Atualização e modernização dos controles e widgets da interface gráfica
- Refatoração estrutural do código para compatibilidade com o novo framework

### Fixed
- Ajustes finos nos controles de exibição e layout dos slides
- Reparos internos de estabilidade decorrentes da migração

## Removed
- Hino 141, removido ultima estrofe repetida

## Adjusted
- Aumentado um pouco o tamanho da letra do título dos Hinos

---

## [0.7.5] - 2026-09-01
### Changed
- Modificado visual para um mais moderno
- Criado novo slide para os Hinos e músicas com o título e quantidade de estrófes
- Aumentado o padding do topo
- Ajustado o tamanho da letra para a nova configuração
- Adicionado `janela_logs.py`
- Adicionado menu para abrir a pasta das músicas para editar e excluir

### Fixed
- Corrigido Hino 198
- Pequenos ajustes para funcionar no Windows

---

## [0.6.4] - 2026-08-05
### Changed
- Criado pasta para organizar as músicas
- Adicionado janela para músicas
- Adicionado Músicas à busca

### Fixed
- Melhorado verificação dos monitores para visualizar no segundo monitor correto

---

## [0.5.3] - 2026-07-05
### Changed
- Alterado para verificar a quantidade de monitores ao iniciar o slide

---

## [0.5.2] - 2026-06-28
### Changed
- Reescrito código para melhor manutenção
- Ajustado padding-top

---

## [0.4.1] - 2026-06-18
### Changed
- Modificado visualização do slide, melhorado proporção e justificado o texto

### Fixed
- Corrigido Ageu-001
- Corrigido Ester-008
- Corrigido Hino-038
- Configurado para encerrar o slide nos textos da Bíblia

---

## [0.4.0] - 2026-06-12
### Changed
- Alterado separadores verticais, adicionado separador horizontal
- Ajustado tamanho da janela
- Criado janela lateral de busca
- Adicionado funcionalidade de busca

### Fixed
- Corrigido para mostrar o último versículo de cada livro e carregar corretamente

---

## [0.3.9] - 2026-06-12
### Fixed
- Corrigido hinos 60, 323, 334
- Corrigido Malaquias 3

---

## [0.3.8] - 2026-05-01
### Fixed
- Feito pequenos ajustes no código para um melhor funcionamento
- Ajustado tamanho das letras no slide
- Corrigido Hino 545
- Verificado e corrigido Atos 27

---

## [0.3.7] - 2026-04-20
### Fixed
- Verificado todo o livro do Apocalipse

### Changed
- Adicionado no menu notas da versão para visualizar

---

## [0.3.6] - 2026-04-12
### Fixed
- Ajustado tamanho da janela principal

### Changed
- Configurado para funcionar no Windows
- Adicionado barra de menus
- Movido verificação de atualização do botão para a barra de menu
- Bloqueado redimensionamento da janela, removido botão maximizar

---

## [0.3.5] - 2026-04-10
### Fixed
- Corrigido quebra de linha na segunda tela

---

## [0.3.4] - 2026-04-08
### Fixed
- Corrigido ajuste da quebra de linha que deixou o texto no meio da tela com resolução maior
- Pequenas melhorias no código

### Changed
- Adicionado relógio na primeira tela do slide

---

## [0.3.3] - 2026-04-06
### Changed
- Pré-configurado lista dos livros, colocado em ordem
- Removido `.txt` de aparecer na lista
- Colocado nova pasta da Bíblia para funcionar
- Adicionado controle para selecionar versículo

---

## [0.3.2] - 2026-04-01
### Fixed
- Ajustado texto do hino 256
- Ajustado texto do hino 302
- Padronizado título dos hinos
- Corrigido filtro dos capítulos, que filtrava os Livros juntos

### Changed
- Ajustado tamanho da janela ao iniciar

---

## [0.3.1] - 2026-03-29
### Fixed
- Ajustado preview do slide para não ir para a segunda tela

### Changed
- Adicionado cor ao fundo
- Adicionado contador para os slides
- Modificado ajuste de resolução para ficar direto em fullscreen

---

## [0.3.0] - 2026-03-10
### Fixed
- Hino 476 adicionado refrão ao final
- Lucas 7-15 corrigido dizeres
- Jó 42-8,11 corrigido dizeres
- Hino 485 Colocado Coro em ordem
- Hino 491 Coloca frase que faltava

### Changed
- Preparado para mudar a apresentação da bíblia em andamento

---

## [0.2.4] - 2025-12-19
### Changed
- Adicionado botão para verificar a versão do programa

### Fixed
- Removido parágrafos duplicados no fim de alguns hinos

---

## [0.2.3] - 2025-12-14
### Changed
- Modificado o modo de carregamento dos hinos, abrindo um arquivo por vez

### Fixed
- Corrigido erro ao carregar os hinos, que mostrava os hinos errados na tela

---

## [0.2.2] - 2025-12-13
### Fixed
- Ajustado arquivo de texto dos hinos da Harpa

---

## [0.2.0] - 2025-12-12
### Changed
- Adicionado Módulos auxiliares `dados.py` e `slide.py`
- Removido pasta `Harpa Crista 640 DataShow – PowerPoint`
- Pasta mantida `BS Para DataShow – PowerPoint` 
- Adicionado pasta `HarpaTexto`
- Melhorias na leitura de arquivos da pasta HarpaTexto
- Atualização da interface de slides

### Fixed
- Ajustado tamanho de letras na segunda tela para tamanho 4:3

---

## [0.1.0] - 2025-11-20
### Added
- Criado programa para Data show
- Arquivo principal `programaigreja.py`