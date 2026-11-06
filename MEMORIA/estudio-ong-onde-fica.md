---
name: estudio-ong-onde-fica
description: "Onde estão o Estúdio de Criativos da SOS Human Help, as skills, o conhecimento e o material neste PC (instalado em 26/10/2026)"
metadata:
  node_type: memory
  type: reference
  originSessionId: 671e808f-aec5-4292-93a6-ac14352a69d2
  modified: 2026-10-30T19:32:22.395Z
---

Estúdio de Criativos da ONG S.O.S Human Help (Pedrinho Guerreiro e Adrielly, epidermólise bolhosa), instalado em 26/10/2026.

- Material (RAIZ): `C:\Users\EDITING_SECTOR\Desktop\EDIÇÃO COM CLAUDE` (também em `$HOME\.claude\estudio-ong.json`). No PowerShell, ache por `Get-ChildItem $HOME\Desktop -Directory | ? Name -like 'EDI*CLAUDE'` (acento corrompe no comando).
- Este PC é o mesmo do editor original: a RAIZ já tem `banco de vídeos do pedrinho`, 35 planos em `EDITADOS\_planos\` e LEVAs cheias. Leia esses planos antes de escrever copy nova.
- Próximos nomes: reportagem `_v11`, lista `_v6`, vsl_voz `_v6`; narrado e cortes usam nome de ângulo (`Pedrinho_narrado_<angulo>_v1`, `Pedrinho_<angulo>_v1`). Confira todas as LEVAs antes.
- Skills em `$HOME\.claude\skills\`: edicao-criativo-ong (Cortes), criativo-lettering-ong (Cortes com lettering, desde 26/10/2026), criativo-caixas-pedido-ong / -aspas-ong / -urgente-ong (estilo "caixas" copiado da Causas do Bem, desde 26/10/2026; montador caixas.py), criativo-corrente-ong e criativo-mae-desesperada-ong (cópias de outros 2 anúncios da Causas do Bem), criativo-salva-vida-ong (cópia de anúncio da Ampara Brasil; os 3 com montador montar.py), criativo-esperanca-ong ("Da dor à esperança", estilo próprio de 27/10/2026, montar.py com cartela/real/narr/vo/fim; próximo nome `Pedrinho_esperanca_v2`), criativo-unicef-ong ("UNICEF", 27/10/2026: gancho "pode parecer uma simples <item>" + cortes com lettering; montar.py faz o gancho, chama build_cortes.py sem logo/música e põe música e logo no vídeo inteiro; saída `EDITADOS\UNICEF`), criativo-narrado-ong, criativo-lista-ong, criativo-reportagem-ong, criativo-vsl-voz-ong. Ao mudar skill ou Estúdio, copie também para `Desktop\PARA O NOVO EDITOR` (skills\, ESTUDIO\), senão reinstalar desfaz.
- Letterings: `RAIZ\lettings` (imagens "Imagem do ChatGPT…", ler o texto numa folha). Fontes do usuário em `AppData\Local\Microsoft\Windows\Fonts` (Futura Extra Black `futuraxk.ttf`, Poppins).
- Conhecimento: `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md` (regras com data, falas reais com fonte, ângulos usados), `transcricoes\` (19 brutos já transcritos), `conversa-original.md` (o porquê).
- Depois de mudar `app.py`/`index.html`, reinicie o Estúdio que está rodando (o processo python na porta 8765 segura a versão velha e um novo atalho não consegue a porta): pare o processo e abra o atalho de novo.
- Pacote de instalação: `Desktop\PARA O NOVO EDITOR`. Nunca abra o Estúdio de dentro dele; use o atalho "Estudio de Criativos" (porta 8765).
- Python: `$env:LOCALAPPDATA\Programs\Python\Python312\python.exe` sempre com `-I`; FFmpeg ao lado dele; OpenCV 4 (nunca mediapipe).
- Chave `ELEVENLABS_API_KEY` já configurada (conta paga). Nunca peça, leia ou mostre.

- Drive da ONG: `ADS BR` (https://drive.google.com/drive/folders/1XHDbBerDvQZC_lIQyX6_BSOxMB3oFb2M) tem as LEVAs testadas e os vencedores; brutos em https://drive.google.com/drive/folders/1U47hJe1cQkST3ttEuK87XrNokiBrjFvz. A pasta é pública: `drive.google.com/embeddedfolderview?id=<id>` lista sem login. **A numeração AEB do Drive é outra, diferente da daqui:** o AEB 84 do Drive não é o nosso AEB 84; quando o usuário citar um vencedor, procure no Drive primeiro.
- Fórmula dos vencedores do Drive: gancho com placa "FICA SÓ 30 SEGUNDOS", ela falando com legenda e caixa vermelha R$5,00, fim em P&B. As 5 variações do AEB 66 só com visual novo não validaram: variação precisa mudar gancho ou fala.
- Brutos da viagem baixados em `RAIZ\adrielly\BRUTOS DA ADRIELY\DRIVE - VIAGEM` (placas IMG_8960-8982, sofá IMG_8943/8945, entrevistas IMG_9004/9005). Faltam IMG_9003, 9006, 9007, 9008, 9009, por download interrompido.

Regras: [[estudio-ong-regras]]. Conferência: [[estudio-ong-conferencia]].
