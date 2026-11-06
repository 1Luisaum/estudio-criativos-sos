---
name: magnific-musica-api
description: Como buscar e baixar música na API da Magnific (filtros que funcionam) e onde ficam as faixas gospel já baixadas
metadata:
  node_type: memory
  type: reference
  originSessionId: fb2275de-5513-43bf-b60f-24906f849bd9
  modified: 2026-10-30T17:48:32.257Z
---

Banco de música da Magnific, sem navegador. Variável de usuário do Windows `magnific`, header `x-magnific-api-key`.

- Busca: `GET https://api.magnific.com/v1/music`. A lista vem em `results`. Filtros que funcionam: `q` (texto), `genre` (ex.: `Soul`), `mood` (ex.: `hopeful`), `limit`, `offset`. `term`, `page`, `query` e `search` são ignorados.
- Download: `GET /v1/music/<id>/download` devolve `download_url`.
- Gospel: `q=gospel` traz 42 faixas (30/10/2026). As lentas de jazz/soul do Kike Gutz combinam com pedido de ajuda. Baixadas em `RAIZ\MÚSICAS\gospel`.
- As faixas têm volumes bem diferentes: meça o LUFS e ajuste `musica_volume` em cada plano (mira de -31 LUFS na faixa, antes da mixagem).
