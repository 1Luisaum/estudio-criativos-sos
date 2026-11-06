---
name: criativo-lettering-ong
description: >-
  Estilo "Cortes com lettering" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). É o modelo de cortes da criança falando (sem pausas nem vícios, zoom a cada corte, legenda palavra por palavra, b-roll do banco), mas sem ganchos de texto, com UMA imagem de lettering pronta (pasta "lettings" do material, ex.: "R$ 10,00 PODEM AJUDAR NO CUIDADO DO PEDRINHO") parada o vídeo todo; legenda do meio em Poppins Black; tela final "CLIQUE EM SAIBA MAIS". Use quando o usuário pedir "cortes com lettering", "com o lettering", "use os letterings da pasta", "igual ao Pedrinho_ajuda_de_verdade", ou escolher "Cortes com lettering" no Estúdio. Não use para os cortes com faixa de gancho (edicao-criativo-ong) nem para os estilos com narrador, VSL ou reportagem.
---

# Cortes com lettering

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Não altere esta skill durante a conversa.** Ajustes pedidos no chat vão só no `plano.json` daquele vídeo (em `EDITADOS\_planos\<nome>\`). Esta skill e o Estúdio de Criativos só mudam quando o usuário pedir explicitamente para **salvar** (regra do usuário, 26/10/2026).

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md`: regras do usuário com data, falas reais com a fonte, ângulos já usados e problemas já resolvidos. As transcrições prontas dos brutos estão em `transcricoes\` ao lado.

Criado a pedido do usuário em 26/10/2026, a partir do vídeo aprovado `Pedrinho_ajuda_de_verdade_v1` (41 s, bruto `roteiro 7.mp4`). O plano dele está em `references/exemplo-plano-pedrinho-ajuda-de-verdade.json`. Fale com o usuário em português do Brasil.

O corte é o mesmo da skill `edicao-criativo-ong`. Leia as seções 2 a 4 dela, que tratam de transcrever, decidir os cortes e olhar o material: os scripts `transcribe.py`, `inspect_tx.py`, `sheets.py` e `verify.py` estão copiados aqui. O que muda é só o texto na tela.

## O que este estilo tem (aprovado em 26/10/2026)
- **Um lettering só por vídeo, sempre.** Regra do usuário: "sempre você irá escolher apenas um lettering para o vídeo". É uma imagem pronta que o usuário cria e põe na pasta `lettings` da RAIZ. Ela fica **parada do primeiro ao último segundo**, inclusive na tela final. Fica por cima de tudo e não recebe a dessaturação do vídeo, centralizada, com 760 px de largura (sobra nos cantos) e centro em y=1290.
- **Sem ganchos que trocam de texto** e sem faixa de doação desenhada. O lettering substitui tudo isso.
- **Legenda do meio em Poppins Black**, em y=950, com contorno preto e destaque vermelho (`red`). O script acha a Poppins sozinho e avisa se ela não estiver instalada.
- **Tela final** sobre um b-roll da criança, escurecido, só com "CLIQUE EM SAIBA MAIS ♥" acima do lettering (`endcard.lines` vazio e `endcard.y` 760).
- O resto é igual aos cortes:
  - corta pausas e vícios;
  - o zoom muda a cada corte;
  - os primeiros ~9 s ficam com a criança na câmera;
  - o b-roll casa com a fala;
  - a música é o piano `alex-morgan…`.

## Escolher o lettering (1 por vídeo)
1. Ache a pasta: `Get-ChildItem "<RAIZ>" -Directory | ? Name -like 'lett*'`. O nome do exemplo é `lettings`, mas aceite `letterings` ou `lettrings`.
2. **Leia o texto de cada imagem**, porque o nome do arquivo não diz nada (são "Imagem do ChatGPT …"). Monte uma folha numa chamada só: `ffmpeg -i a.png -i b.png ... -filter_complex "[0]scale=560:-1[a];...;[a][b]...xstack=inputs=N:layout=...:fill=white" folha.jpg`.
3. **Escolha um** e diga por quê:
   - o valor tem que bater com o que o vídeo pede. Se o pedido ou as `observacoes` trouxerem um valor (ex.: R$ 10), use um lettering com esse valor. Sem valor pedido, prefira o que a criança ou a mãe falam no bruto; sem valor no bruto, use R$ 5, que é o que a mãe diz;
   - o texto tem que casar com o ângulo (ex.: fala de curativo → "podem ajudar no cuidado do Pedrinho");
   - **o lettering é da criança do vídeo:** nunca use lettering que cite o Pedrinho num vídeo da Adrielly. Se não houver um da criança certa, peça ao usuário.
4. Grave no plano `"chamada": {"imagem": "<caminho>", "texto_do_lettering": "<o que está escrito>"}`.
5. **Pedido com `quantidade` > 1:** cada vídeo usa um lettering diferente, enquanto houver. Se faltar, diga quantos repetiram. Nunca ponha dois letterings no mesmo vídeo.
6. Se a pasta não existir ou estiver vazia, pare e peça ao usuário para criar os letterings. Não desenhe a tarja por conta própria.

## Fluxo
Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. Scripts em `$K = "$HOME\.claude\skills\criativo-lettering-ong\scripts"`. Use `$env:PYTHONIOENCODING='utf-8'`, e crie e edite os JSON só com Write/Edit ou com um script Python, nunca com `Set-Content`. Antes de transcrever ou conferir, carregue a chave do Windows no mesmo comando: `$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')`. A sessão pode ter uma chave velha.

1. **Bruto e ângulo:** escolha um bruto e um ângulo que ainda não entraram em Cortes com gancho nem em Cortes com lettering. Veja os planos em `EDITADOS\_planos\`. Reaproveite a transcrição pronta, se houver; senão: `& $PY -I "$K\transcribe.py" "<bruto>" "<plano>\transcricao.json"`.
2. **Cortes:**
   - rode `& $PY -I "$K\inspect_tx.py" "<plano>\transcricao.json" --words --draft`;
   - cada corte vai do início da 1ª palavra -0,03 s ao fim da última +0,06 s;
   - nos cortes colados num vício, confira o vale com `--env a-b,... --media "<bruto>"`;
   - alvo: 30 a 45 s de fala.
3. **Rosto e b-roll:** monte a grade do bruto para achar o `face` e folhas do banco com `sheets.py`. **O lettering ocupa y≈1076-1504 e a legenda fica em 950:** escolha b-roll com o rosto da criança acima de y≈1000. No vídeo do evento (`20241110_104724.mp4`) o Pedrinho fica embaixo e o lettering cobriria o rosto dele; o do violão (`20260410_210553.mp4`) funciona.
4. **Lettering:** veja "Escolher o lettering" acima.
5. **Plano:** copie `references/exemplo-plano-pedrinho-ajuda-de-verdade.json` e troque `nome`, `raw`, `segments`, `fix`, `red`, `chamada.imagem`, `endcard.src`/`start` e `fatos`. Campos: veja `references/plano.md`.
6. **Montar:** `& $PY -I "$K\build.py" "<plano>\plano.json"`. A saída mostra a linha `lettering: …` e termina com `buracos=nenhum` e `OK … tela_final=YY`.
7. **Conferir o MP4 final:**
   - `& $PY -I "$K\verify.py" "<saida>" "<plano>\legendas.ass" --tela-final YY`;
   - folha de quadros com `sheets.py frames --at ...`: o lettering não cobre nenhum rosto, a legenda não encosta nele e nada está deitado;
   - travadinha: `ffmpeg -i "<saida>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`. Parada de 0,2 s ou mais é erro.
8. **Entregar** com `SendUserFile` (`display: render`). Diga qual bruto e qual lettering foram usados e por quê, o que foi cortado, os b-rolls e o que você não garante (você não ouve o áudio).

## Regras que continuam valendo
- Legenda é só o que foi falado. O `fix` pode trocar número por algarismo e acertar plural.
- Nada de foto de ferida aberta. Nada de imagem deitada. Nada em cima do rosto da criança.
- O CTA é "Saiba mais", nunca "Doar agora".
- Banco do Pedrinho só em vídeo do Pedrinho.

## Onde salvar (LEVAs)
O script salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, 5 por LEVA, e cria a próxima sozinho. Nomes: `<Criança>_<ângulo>_vN`; nunca repita um nome.

## Pedido do Estúdio
Pelo Estúdio, o usuário escolhe "Cortes com lettering" e cola "Executa o pedido do Estúdio <id> (arquivo …) com a skill criativo-lettering-ong". Leia o JSON: use o primeiro de `brutos`, o `banco` e as `observacoes`, que têm prioridade (inclusive o valor). Rode o fluxo. No fim, grave com Edit `"status": "concluido"`, `"saida"` e, se `quantidade` > 1, `"saidas"`, com vídeos diferentes entre si: bruto ou trechos, ângulo, b-roll e lettering.

## Armadilhas já resolvidas (não desfaça)
- **O build regrava o `plano.json`** (grava `out`) com outra formatação. Edite o plano com Edit ou com um script Python que carrega e salva o JSON. Um `sed` com o texto antigo não acha nada.
- **Fonte instalada só para o usuário** (`AppData\Local\Microsoft\Windows\Fonts`) vem como somente leitura. O script apaga a cópia antiga antes de copiar de novo.
- As armadilhas de áudio, MKV, rotação e fontes do `edicao-criativo-ong` valem aqui também.
