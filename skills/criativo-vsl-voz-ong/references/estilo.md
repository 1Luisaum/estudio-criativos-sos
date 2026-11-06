# VSL com a voz da criança: especificação

## Visual (o mesmo do estilo Lista narrada, núcleo em `scripts/nucleo.py`)
- 1080x1920, 30 fps, b-roll cru em tela cheia, aproximação de 3% por cena, sem filtro.
- **Chamada:** caixa amarela `#FFD600` com texto preto, 2 linhas, sempre entre y=290 e y=1250, nunca em cima de rosto. Exemplo: "ESSA É A VOZ DO PEDRINHO 💔 / DOE R$ 10 PRO CURATIVO DELE 👼". Abrir com "Essa é a voz…" deixa claro para quem vê que quem fala é a própria criança.
- **Legenda:** até 3 palavras, Segoe UI Black 84, branca com contorno preto, `palavras_chave` em amarelo, **com o tempo real de cada palavra** (vem da transcrição).
- **Etiqueta** branca com o valor (blocos com `"etiqueta": true`) e "👇 Clique em SAIBA MAIS" no final.
- **Sempre tela cheia:** vídeo e foto ocupam a tela inteira. Foto de produto passa devagar na horizontal, e foto com rosto fica centralizada nos rostos. Nos closes em que o rosto ocupa a zona segura, a chamada tenta 80% do tamanho e, se ainda cobrir o rosto, some só naquela cena. Nunca reduza o vídeo nem desfoque o fundo.
- **Rosto:** detector OpenCV com margem de 30% acima e 140% da altura abaixo do rosto, considerando também a posição horizontal, mais `zonas_protegidas` para rosto pequeno ou de lado.

## Áudio
- Cada trecho: `highpass=80`, `afftdn` (tira o chiado), fade de 20 a 40 ms nas pontas (evita estalo), depois `loudnorm -16` por frase.
- Respiro de 0,18 s entre frases. Música baixa (0,09) e mix final em -14 LUFS.

## B-roll do banco do Pedrinho (sem ninguém falando para a câmera)
- `20260410_210553.mp4`: Pedrinho enfaixado na cama enquanto um rapaz toca violão. Bom para o gancho e para momentos ternos.
- `20241110_104724.mp4`: Pedrinho de cadeira de rodas num evento, sendo empurrado. Serve para "eu sou", "escolhi lutar" e "seja um anjo". **Cuidado:** nele, o rosto do Pedrinho é pequeno e o detector não pega. Confira com zoom.
- `20260824_182501.mp4`: mãe e Pedrinho sentados na cama (os rostos são detectados).
- `Vídeo Mostrando itens de curativos ... .mp4`: o curativo sendo feito (160, 205, 232 e 290 s) e os itens na cama (15 s).
- Fotos: produtos (Remédios Pomadas e Cremes, GAZE, Pomada, crepe bandagem, soro, esparadrapo, óleo de girassol, Curativos 2 x ao Dia) e "Ana e Pedro sorrindo" para o final.
- **Evite** como b-roll os vídeos em que ele aparece de perto falando outra coisa (Roteiro 3, Roteiro 4, os brutos): a boca não bate com a voz.

## Folha de contato do banco
```
ffmpeg -ss <t> -i "<video>" -frames:v 1 -vf "scale=160:284:force_original_aspect_ratio=decrease,pad=160:284:(ow-iw)/2:(oh-ih)/2" r_<n>.png
ffmpeg -i r_%d.png -vf tile=6x1 linha.png
```
