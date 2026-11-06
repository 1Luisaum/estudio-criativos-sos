# plano.json: campos e padrões

O `build.py` lê um JSON por vídeo. Os padrões são os do vídeo aprovado (Pedrinho_5horas_v1); só escreva o que muda. Exemplo completo: `exemplo-pedrinho-5horas.json`.

## Obrigatórios

| Campo | O que é |
|---|---|
| `nome` | nome do vídeo, igual ao da pasta do plano (ex.: `Pedrinho_5horas_v1`) |
| `raw` | caminho do bruto |
| `transcript` | `transcricao.json` (relativo à pasta do plano) |
| `out` | caminho do MP4 final em `EDITADOS` |
| `segments` | lista dos trechos de fala, na ordem em que entram |

## Segmentos

```json
{"in": 4.78, "out": 7.10, "zoom": "ZH", "txt": "eu só tenho esses curativos aqui,"}
{"in": 19.64, "out": 23.10, "broll": [{"src": "video_do_banco.mp4", "start": 152.0}]}
{"in": 39.92, "out": 44.76, "broll": [{"src": "a.mp4", "start": 272.0, "until": 42.62}, {"src": "a.mp4", "start": 300.0}]}
{"in": 54.93, "out": 57.56, "fix": {"CURATIVO": "CURATIVOS"}, "broll": [{"src": "foto1.jpg"}, {"src": "foto2.jpg"}]}
```
- `in`/`out`: tempos no bruto. O áudio sempre vem do bruto, inclusive quando há b-roll por cima.
- `zoom`: `Z1` (inteiro), `Z2` (1,3x), `Z3` (1,7x), `ZF` (2x, rosto), ou um zoom criado em `zooms`. Sem `zoom`, o script alterna Z2, Z3, ZF e Z1 sozinho.
- `broll`: peças em sequência cobrindo o segmento. `src` é relativo a `bank` (ou absoluto). `start` é o segundo do b-roll onde a peça começa. `until` é o tempo do bruto em que a peça termina. Peças sem `until` dividem igualmente o tempo que sobra. Fotos (`.jpg`/`.png`) viram imagem parada.
- `fix`: troca de palavra só nesse segmento (soma-se ao `fix` global).
- `txt`: anotação livre para quem lê o plano; o script ignora.

## Enquadramento

| Campo | Padrão | Uso |
|---|---|---|
| `face` | `[largura/2, altura*0,2]` | centro do rosto no quadro em pé (px). Z2, Z3 e ZF põem o rosto a 25% da altura |
| `zooms` | — | zooms extras, ex.: `{"ZH": {"z": 1.9, "center": [550, 560]}}` (centralizado nesse ponto) |

## Texto na tela

| Campo | Padrão | Observação |
|---|---|---|
| `hook` | — | lista de `{"t0", "t1", "lines", "fs"}`; faixa vermelha de ponta a ponta com degradê e letra Impact branca/cinza com sombra (estilo das referências, 26/10/2026), centro em y=1290. Os asteriscos são ignorados: não há mais destaque amarelo. Aprovado: `ME DÁ 30 SEGUNDOS` (0-1,9 s, fs 100), depois 3 linhas fs 92 até 5,3 s |
| `chamada` | — | faixa vermelha de doação do fim do gancho até a tela final: `{"linhas": [["APENAS R$ 5", 124], ["PODEM MUDAR A VIDA DO", 64], ["PEDRINHO GUERREIRO!", 84]], "y": 1300}`. Sem risco por cima do texto |
| `red` | `["CURATIVO","CURATIVOS"]` | palavras da legenda em vermelho `#FF2A2A` |
| `fix` | — | trocas globais na legenda, ex.: `{"NECESSIDADE": "NECESSIDADES"}` |
| `badge` | desligado (26/10/2026) | selo preto no canto superior esquerdo; o usuário pediu para tirar. Só use se ele pedir de volta |
| `caption_y` / `caption_fs` | 1010 / 100 | legenda palavra por palavra, blocos de até 3 palavras/15 letras, contorno preto 7 |
| `hook_y` | 1290 | não desça: abaixo de ~1500 entra a interface do Reels |

## Tela final

```json
"endcard": {"src": "20260410_210553.mp4", "start": 30.0, "dur": 3.4,
            "lines": ["SEJA A CORRENTE", "DO BEM DO PEDRINHO"], "cta": "CLIQUE EM SAIBA MAIS"}
```
Fundo escurecido, caixa vermelha (fs 76) em y=860 e o CTA (fs 62) com ♥ vermelho embaixo. As legendas acabam quando a tela final começa.

## Som e cor

| Campo | Padrão |
|---|---|
| `music` | caminho da trilha (sem `music`, sai só a voz) |
| `music_start` | 0 (segundo da trilha onde começa) |
| `music_vol` / `music_end_vol` | 0,12 sob a voz e 0,32 na tela final (sobe em 0,8 s); fade-in 0,4 s, fade-out 1,3 s |
| `voice_lufs` | -15 (ganho fixo medido; o final fica em torno de -14,4 LUFS) |
| `saturation` | 0,70 (30% dessaturado, como o criativo de EB mais escalado) |

Saída: 1080x1920, 30 fps, H.264 CRF 19, AAC 192k, `+faststart`.
