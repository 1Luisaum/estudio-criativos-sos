---
name: elevenlabs-leonardo-chiando
description: "Desde ~03/11/2026 a voz Leonardo (4XmhZ74tBbUVCXIYNMMo) sai do ElevenLabs com chiado (\"chuvisco\"); usar o Kaique"
metadata:
  node_type: memory
  type: project
  originSessionId: fb2275de-5513-43bf-b60f-24906f849bd9
  modified: 2026-11-05T20:33:53.827Z
---

Em 06/11/2026 o usuário reclamou que a narração estava "cheia de chuvisco, quase não dá pra entender" (vídeo da página de obrigado; antes, "chiando" no AEB 102).
Medido: a voz **Leonardo** (`4XmhZ74tBbUVCXIYNMMo`, eleven_multilingual_v2) gerada agora tem energia acima de 6 kHz de -14 a -17 dB em qualquer ajuste (stability, style, speaker boost, 128 ou 192 kbps). O Leonardo antigo (reportagem AEB 57, outubro) e o **Kaique** (`Hmn4B9B77pf6ttydteJ8`) medem -35/-36 dB. O defeito vem da voz no ElevenLabs, não da mixagem.

**Why:** a voz mudou do lado do ElevenLabs; nenhum ajuste resolve.
**How to apply:** para narração nova, usar o Kaique (ou testar outra voz BR medindo o agudo >6 kHz, alvo < -30 dB) até o Leonardo voltar ao normal. Os vídeos narrados com o Leonardo desde 03/11 (Bibliotecas Orações/Conselho/Lucas da Adrielly e do Pedrinho) têm o chiado. Medir com FFT na fala: 10*log10(energia>6k / total). Ver [[estudio-ong-regras]] (regra das vozes).
Também: o plano do ElevenLabs não libera `output_format=pcm_44100` (403); o melhor é `mp3_44100_192`.
