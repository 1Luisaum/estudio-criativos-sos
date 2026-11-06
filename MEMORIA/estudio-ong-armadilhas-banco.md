---
name: estudio-ong-armadilhas-banco
description: "Clipes do banco do Pedrinho que o catálogo aprova mas dão problema, e colisão de LEVAs entre as crianças no comum.py"
metadata:
  node_type: memory
  type: project
  originSessionId: fb2275de-5513-43bf-b60f-24906f849bd9
  modified: 2026-11-01T20:10:42.140Z
---

Achados no lote PEB 172-201 (01/11/2026):

- `vídeo na Horizontal para o Site_.mp4`: no corte vertical o rosto da mãe fica cortado no topo e a manchete cobre os óculos. O detector não vê rosto cortado, então `catalogo.py livres` o marca como livre. Trocado por `20260824_182501.mp4`.
- `pedrinho_guerreiro_1747600910…`: tem texto gravado na imagem com "link da vakinha" e um pix antigo. Não usar.
- Em `destino()` do `comum.py`, a LEVA nova é `última da criança + 1`, sem olhar se o número já é da outra criança. PEB 186-196 caíram nas LEVAs 41-51 da Adrielly. Movidos para 53-55 à mão. O próximo a colidir: quando a LEVA 51 da Adrielly encher, o AEB seguinte cai na 52, do Pedrinho.

**Why:** a conferência automática não pega nenhum dos três; só olhar a imagem e listar as LEVAs.
**How to apply:** depois de cada lote, listar as LEVAs por prefixo. Ver também [[estudio-ong-conferencia]] e [[estudio-ong-lote-rapido]].
