---
name: troca-de-cenario-ganchos
description: Como trocar o fundo dos vídeos da criança - modelos de vídeo recusam por moderação; o que funciona é recorte local com fundo gerado na Magnific
metadata:
  node_type: memory
  type: project
  originSessionId: fb2275de-5513-43bf-b60f-24906f849bd9
  modified: 2026-10-30T23:15:22.735Z
---

Em 30/10/2026 o usuário pediu para trocar o cenário dos ganchos do Pedrinho. Runway Aleph 2 e Gemini Omni 1.1 (Modify video, na Magnific) recusaram o vídeo por moderação, sem cobrar crédito. Não insistir com outros modelos nem disfarçar o vídeo para passar no filtro.

O que funciona: `EDITADOS\_planos\_cenarios\compor.py`, rodado com o Python de `~/.claude/estudio-ong/cen` (rembg isnet-general-use, só CPU, cerca de 4,5 s por quadro). Mantém a imagem e a voz reais e só troca o fundo, gerado sem pessoas por Seedream 4.5 via API da Magnific. Saída em `EDITADOS\GANCHOS COM CENÁRIO`; depois aplicar `marca.aplicar`.

**Why:** preserva a criança real, regra de não usar pessoa feita com IA ([[estudio-ong-regras]]).
**How to apply:** usar fundo de casa simples, sem hospital e sem exagerar pobreza, para não enganar o doador. A API da Magnific está em [[magnific-musica-api]]. O envio automático no Google Flow não funcionou (sem campo de arquivo comum e página travando).
