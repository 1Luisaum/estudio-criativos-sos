# Passagem de trabalho — Estúdio de Criativos SOS Human Help (até 05/11/2026)

Este repositório tem **tudo o que foi feito na conversa** até 05/11/2026, para outro Claude continuar de onde parou.
Leia nesta ordem: este arquivo → `CLAUDE.md` → `MEMORIA/MEMORY.md` (e os arquivos que ele lista) → `CONHECIMENTO/CONHECIMENTO.md`.
A conversa inteira, transcrita (o que o usuário pediu e o que o Claude respondeu), está em `CONVERSAS/`.
A mais recente é `conversa_fb2275de-5513-43bf-b60f-24906f849bd9.md`.

## Como instalar no outro PC
1. Baixe o repositório (Code > Download ZIP, ou `git clone`) e descompacte.
2. Abra a pasta no app do Claude (aba Code) e escreva: **Instale o Estúdio**. O `instalar.py` copia as skills para
   `~/.claude/skills`, o conhecimento e as ferramentas para `~/.claude/estudio-ong`, os agentes, o Estúdio e o MATERIAL
   para a pasta do material (`Área de Trabalho\EDIÇÃO COM CLAUDE`).
3. Copie a memória: o conteúdo de `MEMORIA/` vai para a pasta de memória do projeto do Claude
   (`~/.claude/projects/<pasta do projeto>/memory/`), ou peça ao Claude para ler `MEMORIA/` no começo da conversa.
4. As chaves **não** estão aqui (nunca suba chaves): crie as variáveis de ambiente `ELEVENLABS_API_KEY` e `magnific`
   (Iniciar > "Editar as variáveis de ambiente para sua conta").
5. `ESTUDIO_ONG_RAIZ/` vai para `~/.claude/estudio-ong/` (biblioteca de falas, catálogo de rostos, marca).

## O que NÃO está no repositório (grande demais para o GitHub)
Leve por pendrive ou Google Drive, mantendo as mesmas pastas dentro de `EDIÇÃO COM CLAUDE`:
- `VÍDEOS PARA EDITAR\PEDRINHO 02-11-2026` (brutos de 02/11 do Pedrinho, 448 MB).
- `adrielly\` (banco e brutos da Adrielly) e `Desktop\TODAS AS PASTAS\adriely` (brutos de 30/10, IMG_64xx, com o terço).
- `banco de vídeos do pedrinho` completo (aqui vai só a parte do pacote), `EDITADOS\RENDERIZADOS` (vídeos prontos),
  `EDITADOS\_referencias`, `EDITADOS\PREMIERE` (sequências do Premiere; refazer com `premiere_xml.py`).
- Os ambientes Python grandes de `~/.claude/estudio-ong` (`cen`, `sep` = Demucs para separar música): recriar se precisar.
Os `plano.json` guardam caminhos absolutos deste PC (`C:\Users\EDITING_SECTOR\...`). Se o usuário do Windows for outro,
troque o começo dos caminhos (o `bib.py` também aceita `{RAIZ}`).

## O que foi feito nesta conversa (resumo)
- **Adrielly (AEB 91–102)**: 8 Bibliotecas + 4 novos com vídeo de IA da Magnific; marca **@juntospelaadrielly**
  (em vez de @soshumanhelppt, só para a Adrielly); sem idade, sem citar a SOS; legenda UNICEF; feridas com borrão leve;
  sem P&B; sem pernas enfaixadas; LEVAs 63–65 só dela (havia colisão de LEVAs com o Pedrinho).
- **Ajustes AEB 54–57, 60, 63** (marca, sem idade, menos P&B, CTA, mais curtos).
- **12 modelos novos na skill `criativo-bibliotecas-ong`** (`modelos/adr*.json`), que aparecem no Estúdio.
- **Pedrinho PEB 240–254**: os 12 modelos refeitos para ele com as gravações de 02/11 + 3 extras
  (gerador: `MATERIAL/EDITADOS/_planos/_estilo_bib/gerar_planos5_pedrinho.py`).
- **Vídeo da página de obrigado** (`Obrigado_pedrinho_doe_adrielly_v1`, gerador `video_pagina_obrigado.py`):
  agradece quem doou ao Pedrinho e convida a doar para a Adrielly ("toque no botão abaixo"). O usuário trocou o áudio
  final por um MP3 exportado por ele (`Desktop\Obrigado Pedrinho - doe tambem para a Adrielly.mp3`).
- **Premiere**: `premiere_xml.py` (uma sequência XML editável por vídeo, copia HEVC para H.264, converte imagens
  JPG-com-nome-.png) e `premiere_juntar.py` (junta várias sequências num XML só).
- **Skill bib.py**: legenda `unicef` (`scripts/leg_unicef.py`), caixa vermelha padrão no Conselho, mixagem de áudio com
  ganho seguro (sem loudnorm dinâmico e sem estourar no limitador), AAC do Windows (`aac_mf`) a 256 kbps.

## Regras novas que o usuário deu (já na memória e na skill)
- Imagens/vídeos de IA dos ganchos: **cara cristã** (cruz, crucifixo, Bíblia, terço, igreja, vitral). Poucas velas
  (muitas pareceram umbanda). **Nada de animais, plantações, plantas.** Não reaproveitar vídeo de IA de outro vídeo.
- Adrielly: sem pernas enfaixadas, pouco/nenhum P&B, mais takes das feridas com borrão leve, menos takes falando.
- Montar **um vídeo por vez** (dois `bib.py` juntos travavam o ffmpeg).

## Pendências / problemas abertos
1. **Chiado na narração** — o usuário ouve "chuvisco" na narração. Descobertas:
   - A voz **Leonardo** (`4XmhZ74tBbUVCXIYNMMo`) piorou no ElevenLabs desde ~03/11 (agudo >6 kHz em -15 dB; antes -36).
   - O usuário ouviu no Premiere: **até os arquivos crus do ElevenLabs (Kaique) chiam** (trilha A2).
   - Foi gerada a mesma frase em 8 versões em `EDITADOS\RENDERIZADOS\PAGINA DE OBRIGADO\teste de vozes` (Kaique v2/v3/v4,
     Carlos, Lucas, **Dyego** — a mais limpa medida —, Juliano, Kaique com redução de ruído). **O usuário ainda não
     escolheu a voz.** Depois de escolher: refazer as narrações de todos os vídeos narrados (Bibliotecas da Adrielly
     AEB 92–94, 99–102 e do Pedrinho PEB 221–229, 240–246, 252) e remontar.
2. Os vídeos montados antes da correção de áudio do `bib.py` (06/11) ainda têm a mixagem antiga: remontar quando a voz
   for escolhida.
3. **Magnific sem créditos** (erro 402). As 5 imagens cristãs novas já estão descritas em `gerar_planos5_pedrinho.py`
   (`p_nossa_senhora2`, `p_crucifixo_parede`, `p_biblia_cruz_janela`, `a_capela_colina`, `a_capela_altar_biblia`);
   gerar quando houver crédito (por ora os PEB 243–245 e AEB 99/101 usam vídeos de IA cristãos que já existiam).
4. O postador automático (`Desktop\tiktok\postador`, tarefa `postador-sos`) continua no PC original; não está aqui.
