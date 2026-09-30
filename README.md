# Mega Man Zero — PS2 Port Project

Projeto experimental para reimplementar/adaptar **Mega Man Zero (GBA)** para PlayStation 2.

> A ROM original fornecida pelo usuário é tratada como material de referência local. Ela não é redistribuída pelo projeto.

## Objetivo

Criar uma versão nativa para PS2, preservando a lógica e o conteúdo essencial do jogo, mas substituindo o runtime GBA por uma arquitetura adequada ao PS2.

### Alvos

- PlayStation 2 real
- PCSX2 para desenvolvimento/testes
- 60 FPS como objetivo inicial
- 240p/480i/480p conforme o modo escolhido
- controles DualShock 2
- áudio e efeitos nativos do PS2
- carregamento por dados próprios, sem executar código ARM da ROM

## Arquitetura inicial

```text
GBA ROM / referências
        |
        +--> tools/rom_analyzer.py
        |
        +--> dados extraídos (futuro)
                    |
                    v
              game data layer
                    |
        +-----------+-----------+
        |                       |
        v                       v
  game logic               PS2 renderer/audio/input
        |                       |
        +-----------+-----------+
                    v
              PS2 executable
```

A ideia é **reimplementar** a máquina de jogo, não emular o GBA inteiro. Um emulador GBA dentro do PS2 continua sendo uma possível rota de protótipo, mas não é a arquitetura-alvo.

## Estrutura

- `src/` — runtime nativo PS2
- `include/` — headers do projeto
- `tools/` — ferramentas de análise/conversão
- `docs/` — especificação e descobertas
- `assets/` — dados convertidos; a ROM original não é copiada para distribuição
- `build/` — artefatos locais

## Primeiro marco

1. Identificar a ROM e seu cabeçalho.
2. Criar um executável PS2 mínimo.
3. Criar uma camada de input/render independente do jogo.
4. Mapear gráficos, mapas, animações e tabelas da ROM.
5. Reimplementar player/física.
6. Reimplementar inimigos, armas e chefes.
7. Menus, missões, save e áudio.
8. Otimização e testes no PCSX2/console.

## Build PS2

O build nativo depende de um ambiente PS2Dev/PS2SDK configurado. O Makefile detecta `PS2SDK`/`PS2DEV` quando disponíveis.

## Build do analisador

O analisador da ROM é Python puro:

```bash
python3 tools/rom_analyzer.py "/caminho/Mega Man Zero (USA, Europe).gba"
```
