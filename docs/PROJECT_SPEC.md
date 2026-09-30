# Especificação inicial

## Estado atual

ROM recebida: `Mega Man Zero (USA, Europe).gba`

- tamanho: 8 MiB
- título GBA: `MEGAMAN ZERO`
- game code: `AZCE`
- entry point: `0xEA00002E` (bytes little-endian no cabeçalho)
- SHA-256: `cf505422d68295fba36136a49a3c9dedb104ab16aa542edaeecbb89efdd57807`

## Decisão de arquitetura

### Opção A — emulador GBA no PS2

Prós: preserva comportamento original rapidamente.
Contras: limita melhorias, exige emulação de CPU/memória/periféricos e ainda precisa de integração PS2.

### Opção B — reimplementação nativa PS2

Prós: melhor integração com GS, áudio, controle, resolução e memória; permite uma edição visualmente ambiciosa.
Contras: exige reconstrução sistemática da lógica e dos formatos de dados.

**Direção do projeto: B**, usando A apenas como referência/possível ferramenta de validação.

## Metas técnicas

- Game loop estável a 60 Hz.
- Render 2D acelerado pelo GS usando texturas/tiles e sprites em VRAM.
- Upload de dados em lotes para reduzir custo de DMA.
- Pool de objetos para inimigos/projéteis/efeitos.
- Streaming ou carregamento por blocos para fases maiores que os dados de origem.
- Sistema de câmera separado da lógica do player.
- Camadas de colisão independentes do desenho visual.
- Abstração de input para permitir teste no PC e DualShock 2.

## Próxima engenharia de dados

O próximo passo é localizar automaticamente:

1. tabelas de ponteiros;
2. tilesets e paletas;
3. mapas de salas;
4. sprites/animações;
5. tabelas de inimigos;
6. dados de armas e dano;
7. scripts/eventos;
8. música/SFX.

A ferramenta de análise deve produzir offsets e assinaturas, sem assumir antecipadamente que todo bloco binário é um formato conhecido.
