---
name: estudio-ong-lote-rapido
description: "Processo rápido para lotes de vídeos da ONG (desde 27/10/2026): roteirista-ong + biblioteca/catálogo, fila.py na placa de vídeo com conferência automática, revisor-ong só nos avisos"
metadata:
  node_type: memory
  type: project
  originSessionId: 671e808f-aec5-4292-93a6-ac14352a69d2
  modified: 2026-10-30T17:05:43.172Z
---

Depois do lote de 30 (PEB 111-140, ~4h10, ~44 mil tokens/vídeo, muitas remontagens por texto em cima de rosto), o usuário pediu para produzir mais rápido e gastando menos (27/10/2026). Ficou assim:
- Ferramentas em `~/.claude/estudio-ong/ferramentas/`: `fila.py` (monta N por vez com o montador certo e confere), `conferir_auto.py` (duração, travadinha, áudio, marca da logo, rosto x faixas de texto por estilo), `catalogo.py` (rostos do banco e brutos; `livres --zona`), `biblioteca.py` (falas reais com uso; `buscar`, `livres`), `rostos.py`.
- Agentes em `~/.claude/agents/`: `roteirista-ong` (opus, só escreve planos) e `revisor-ong` (sonnet, só vídeos com aviso).
- Todos os montadores usam `comum.enc_final()` (NVENC na RTX 3050, ~4x mais rápido; x264 sem NVIDIA). O `marca.py` grava `comment=logo SOS Human Help` no MP4.
- Correção rápida (27/10/2026): `prevoo.py` roda na fila antes de montar e para o plano com rosto no texto, arquivo faltando ou .jpg na Mãe; montadores usam `enc_antes_da_logo()` e só o marca.py codifica com qualidade; cortes/lettering/UNICEF reaproveitam partes sem mudança (`comum.ffmpeg_cache`, arquivo .chave); a fila grava `audio_mudou`. UNICEF pomada: 88 s do zero (antes 171-257), correção 25 s. Detalhes: CONHECIMENTO 7.2.
- A transcrição continua no ElevenLabs: o usuário não quis trocar de API.
- Em 30/10/2026 o usuário pediu 4 agentes editores paralelos (2 orgânico, 2 ads) e desistiu logo depois: foram removidos. Não recrie sem pedido.
- O usuário se irrita com remontagem de vídeo pronto: não remonte sem pedido; aviso da conferência é para relatar.

**Why:** pedido explícito de velocidade e economia; os 3 últimos do lote demoraram por remontagens repetidas.
**How to apply:** em qualquer lote, siga a seção 7.1 do CONHECIMENTO.md; registre a demanda ([[estudio-ong-producao-ao-vivo]]); não rode 4 frentes generalistas lendo tudo.

Relacionado: [[estudio-ong-onde-fica]], [[estudio-ong-conferencia]].
