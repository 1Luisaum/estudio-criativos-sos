---
name: elevenlabs-chave-antiga-na-sessao
description: "Erro 402 \"Free users cannot use library voices\" com conta paga = chave antiga presa no ambiente da sessão do Claude"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 671e808f-aec5-4292-93a6-ac14352a69d2
  modified: 2026-10-26T19:44:11.153Z
---

Em 26/10/2026 a sessão do Claude carregava uma `ELEVENLABS_API_KEY` antiga, de conta gratuita. A variável de usuário do Windows tinha a chave da conta paga (plano Creator, ~286 mil créditos/mês). Todos os scripts das skills leem primeiro o ambiente da sessão, então usavam a chave velha e davam 402 nas vozes Kaique/Leonardo.

**Why:** o usuário confirmou que a conta é paga. Eu tinha concluído errado que era gratuita, porque testei com a chave da sessão.
**How to apply:** antes de qualquer comando que use o ElevenLabs, rode no mesmo PowerShell `$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')`. Isso não mostra a chave. Com 402, compare as chaves por hash antes de culpar o plano. Reabrir o Claude também resolve. Ver [[estudio-ong-onde-fica]].
