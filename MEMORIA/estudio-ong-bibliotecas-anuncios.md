---
name: estudio-ong-bibliotecas-anuncios
description: "Criativos do Pedrinho modelados nas bibliotecas de anúncios de outras ONGs (PEB 202-211, 03/11/2026), montador bib.py e o que o usuário pediu ao ver"
metadata:
  node_type: memory
  type: project
  originSessionId: 671e808f-aec5-4292-93a6-ac14352a69d2
  modified: 2026-11-03T16:35:08.806Z
---

Em 03/11/2026 o usuário mandou um Google Doc com 8 bibliotecas da Meta (Lar Mãos Amigas, Lar Mãe Ritinha, Ampara, Movimento de Amor, Pedro Lima Silva SOS, Florisbela, Leão de Judá, Movimento da Paz) e pediu 10 criativos modelados para os brutos novos do Pedrinho (`VÍDEOS PARA EDITAR\PEDRINHO 02-11-2026`, transcritos em `transcricoes\pedrinho_0211`).

- Ampara e Pedro Lima estavam sem anúncio ativo. Os 10 MP4 de referência estão em `EDITADOS\_referencias\bibliotecas` (com tx_ e folhas).
- Montador genérico: `EDITADOS\_planos\_estilo_bib\bib.py`; planos gerados por `gerar_planos.py` (pastas `Pedrinho_bib_<ref>_v1`). Saída PEB 202-211, LEVAs 55-57.
- Depois da 1ª versão o usuário pediu: **músicas tristes da Magnific em todos** (baixadas em `MÚSICAS\magnific_tristes`, volume pelo LUFS), **replicar o estilo exato das referências** (posições, tamanhos e fontes medidos nos quadros) e **o 209 começar com takes mais fortes**.
- Ele liberou gerar vídeo na Magnific "caso precise"; não usei, porque a única cena de IA das referências (rosto de Jesus da Florisbela) foi trocada pela fala real dele.
- O banco `pedrinho_guerreiro_1763051547…` (9-12 s) mostra ferida aberta: não usar (regra da Meta).

Relacionados: [[magnific-musica-api]], [[estudio-ong-regras]], [[estudio-ong-armadilhas-banco]].

**2ª demanda (03/11/2026, PEB 212-225):** o usuário mandou outro Doc com 14 anúncios em LEVA 01/02/03 e pediu um de cada, **mantendo a música do próprio anúncio**. Ele também liberou baixar os vídeos e as músicas da biblioteca e pediu imagens de IA da Magnific na LEVA 02.
- Planos em `_estilo_bib\gerar_planos2.py` (pastas `Pedrinho_bib2_*`). As músicas ficam em `MÚSICAS\bibliotecas`: o áudio inteiro do anúncio quando ele só tem música, e `_musica.wav` separado da voz com Demucs (`separar_musica.py`, venv `~\.claude\estudio-ong\sep`).
- Imagens Seedream 4.5 (`/v1/ai/text-to-image/seedream-v4-5`, `social_story_9_16`) em `_estilo_bib\imagens`: leão, Jesus e Bíblia, simbólicas e sem o Pedrinho. O homem falando no carro (1658) virou a Bíblia, porque a regra é não criar pessoa com IA.
- Narrações do Leonardo, sem respiro, em `_estilo_bib\narracoes`.
- **Skill `criativo-bibliotecas-ong`** (criada a pedido do usuário em 03/11/2026): tem os 24 modelos (`modelos/peb202…225_*.json`, com `{RAIZ}`/`{SKILL}`), `scripts/novo_plano.py` e `bib.py`, e o catálogo `references/modelos.md`. As músicas ficaram em `MÚSICAS\ANÚNCIOS QUE DERAM CERTO` (MP3 com nome da ONG e tema) e `MÚSICAS\magnific_tristes`, cada pasta com um `musicas.json`. Os WAV de `MÚSICAS\bibliotecas` foram apagados, e os planos `bib2` apontam para os MP3. A skill também está no pacote do editor, já zipado.
