# Estilo narrado: plano.json e especificação visual

Exemplo completo e aprovado: `exemplo-plano-pedrinho-narrado.json`.

## Campos gerais

| Campo | O que é |
|---|---|
| `nome` | nome do vídeo e da pasta do plano (`Pedrinho_narrado_v1`) |
| `out` | MP4 final em `EDITADOS` |
| `bank` | pasta do banco; `src` relativo procura primeiro na pasta do plano, depois no banco |
| `music` / `music_start` | trilha e segundo onde começa (aprovado: `echoes_of_lumen-sad-piano-591198.mp3`, 1,2 s) |
| `music_vol` / `music_lift` | 0,10 sob as vozes; +0,14 nas cartelas e na tela final |
| `red` | palavras da legenda em vermelho (curativo, feridas, acabando, medo, sofrendo, números) |
| `caption_fix` | troca na legenda, ex.: `{"QUARENTA": "40"}` |
| `hook` | manchete de abertura (abaixo) |
| `blocks` | a sequência do vídeo |

## Blocos

**real**: fala real, em cor, sem etiqueta de nome na tela.
```json
{"type": "real", "tag": "PEDRINHO", "src": "Roteiro 7.mp4", "tx": "tx/roteiro7.json",
 "cuts": [[6.20, 7.14], [8.02, 8.86]], "crops": [{"z": 1.3, "center": [510, 850]}, {"z": 1.0}]}
```
- `cuts`: [início da 1ª palavra, início da última] de cada pedaço, tirados da transcrição. O script põe a folga e corta as pausas entre os pedaços.
- `crops`: um por corte, em ciclo (`z` = zoom, `center` = ponto no quadro em pé). Variar o zoom a cada corte esconde a emenda.
- `tag`: quem fala (`PEDRINHO` ou `MÃE DO PEDRINHO`). Fica só como anotação no plano: o usuário pediu (25/10/2026) para **não mostrar o nome na tela**, então a etiqueta vermelha está desligada. Ela só aparece com `"etiquetas": true` no plano, e só se ele pedir de volta.

**narr**: narração em cima de b-roll.
```json
{"type": "narr", "audio": "audio/N3.mp3", "look": "pb", "fix": {"quarenta": "40"},
 "broll": [{"src": "20260825_134438.jpg", "until": 0.95}, {"src": "b05.mp4", "start": 15.0}]}
```
- `look`: `pb` (preto e branco, contraste 1,18, vinheta) ou `cor`. Use `pb` até a frase de virada e `cor` dela em diante.
- `until` = segundo dentro da narração em que a peça termina (pegue no `N3.json`). Peças sem `until` dividem o resto.
- Cada peça tem aproximação lenta de 8% (`"zoom": 0.12` muda).

**card**: tela preta com número gigante vermelho (fonte 230, ou `fs`), 2ª linha branca, entrada com pop e boom.
```json
{"type": "card", "lines": ["5 HORAS", "DE CURATIVO"], "dur": 1.3}
```

**end**: tela final colorida, escurecida, com texto (`*palavra*` em amarelo) e botão vermelho pulsando.
```json
{"type": "end", "dur": 3.6, "broll": {"src": "20260729_164523.jpg", "look": "cor"},
 "lines": ["SEJA O *ANJO*", "DO PEDRINHO"], "button": "SAIBA MAIS"}
```

## Manchete de abertura (aprovada após o ajuste "mais chamativa")
```json
"hook": {"t1": 4.6, "y": 1258, "label": "URGENTE",
         "lines": [{"text": "ATÉ *5 HORAS*", "fs": 150}, {"text": "DE CURATIVO. TODO DIA.", "fs": 74}]}
```
- **Faixa:** vermelha (#D90429), com listras amarelas de 8 px em cima e embaixo, entrando da esquerda em 0,18 s.
- **1ª linha:** entra com pop (140% → 100%). O `*trecho*` fica amarelo e pulsa (112%) a cada 0,7 s.
- **Etiqueta:** "URGENTE" branca com letra vermelha sobre a borda de cima da faixa, piscando (0,45 s acesa, 0,2 s apagada).
- **Posição:** não suba a faixa (a legenda está em y=1150) nem desça além de ~1540 (interface do Reels).

## Legenda e transições
- **Legenda:** Arial Black 84, branca, contorno 6, em y=1150, blocos de até 3 palavras / 16 letras. O bloco aparece inteiro, e a palavra falada fica amarela e 12% maior.
- **Trocas:** clarão branco de 0,16 s em toda troca de tipo de bloco (real ↔ narr ↔ card ↔ end); whoosh 0,25 s antes de cada narração; boom no início de cada cartela.
- **Som:** voz real a -16 LUFS (cadeia passa-alta, redução de ruído, compressor); narração a -16 LUFS; limitador final em 0,89.
- **Saída:** 1080x1920, 30 fps, H.264 CRF 19, AAC 192k.
