---
name: estudio-ong-conferencia
description: "Fluxo e conferência antes de entregar um criativo da SOS Human Help, com as armadilhas já vistas"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 671e808f-aec5-4292-93a6-ac14352a69d2
  modified: 2026-10-26T19:38:58.772Z
---

Fluxo de um pedido do Estúdio ("Executa o pedido do Estúdio…"): ler o JSON do pedido → ler CONHECIMENTO.md e a SKILL do estilo → reaproveitar transcrições prontas (`transcricoes\`, `_planos\*\tx\`) antes de gastar crédito → plano por vídeo, todos diferentes → conferir créditos ElevenLabs (`GET /v1/user/subscription`) antes de lote → gerar narração → montar um por vez em segundo plano → conferir → Edit no pedido (`status`, `saida`, `saidas`) → SendUserFile.

Conferir o MP4 final (nunca intermediário):
- folha de quadros: rosto livre, chamada no alto, legenda na zona segura, nada deitado, boca acima da legenda;
- verify.py / conferir.py: transcrição final x legenda (`RESULTADO: OK`, `buracos=nenhum`);
- `freezedetect=n=0.002:d=0.12`: parada ≥0,2 s é erro (cartela preta é normal);
- valor igual em chamada, etiqueta e narração.

Armadilhas já vistas: detector não pega rosto pequeno/de lado/com lesões (marcar à mão); vírgula decimal no PowerShell quebra `--at` (use InvariantCulture); JSON só com Write/Edit; caminho do MP4 para conferir.py exatamente como impresso; brutos renomeados com "_" no fim; caminhos >260 caracteres.

Na entrega, dizer o que não foi conferido: Claude não ouve o áudio (pedir para ouvir voz, cortes e volume da música).

**Why:** no 1º vídeo o intermediário estava certo e o final perdeu 5,6 s de fala; legenda já caiu na boca da mãe; manchete já cobriu os olhos do Pedrinho.
**How to apply:** rodar todas as checagens em todo vídeo, inclusive em lotes de 5. Ver [[estudio-ong-regras]].
