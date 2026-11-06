---
name: estudio-ong-producao-ao-vivo
description: "Toda demanda de vídeos tem que aparecer na aba 'Produção ao vivo' do Estúdio: gravar EDITADOS\\_demanda_atual.json no início e marcar concluída no fim"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 671e808f-aec5-4292-93a6-ac14352a69d2
  modified: 2026-10-27T15:53:06.656Z
---

O usuário quer acompanhar em tempo real, no Estúdio, a demanda que o Claude estiver fazendo: quantos vídeos prontos, qual está sendo feito e a % de cada um (pedido de 27/10/2026). O Estúdio tem a aba "Produção ao vivo" no topo, que lê `EDITADOS\_demanda_atual.json`, os planos, os processos do Windows e `EDITADOS\RENDERIZADOS`.

**Why:** ele pediu "para sempre se atualizar a demanda que você estiver realizando" e para ver "qual vídeo está sendo realizado e a % que ele está".

**How to apply:**
- Ao começar qualquer demanda de vídeos (um ou vários), grave `EDITADOS\_demanda_atual.json` com `titulo`, `pedido`, `inicio` (ISO, hora local), `total`, `status: "em andamento"` e `grupos` (`[{"nome", "estilos": {"<ESTILO como no nome PEB>": quantidade}}]`). Isso substitui a demanda anterior.
- Ao terminar, troque `status` para `"concluída"`.
- A % vem das etapas: plano escrito 15%, transcrição 20%, narração 30-40%, montagem 50-94% (pelo processo do montador com o caminho do plano), logo/finalização 96%, pronto 100%. Para isso funcionar, rode os montadores com o caminho do `plano.json` na linha de comando, como as skills já fazem.
- O código fica em `ESTUDIO\app.py` (`producao()`, `/api/producao`) e `index.html` (seção `#prod`); ao mudar, copie para o pacote.

Relacionado: [[estudio-ong-onde-fica]], [[estudio-ong-regras]].
