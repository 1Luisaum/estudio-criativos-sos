---
name: criativo-reportagem-ong
description: >-
  Estilo "Reportagem" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). O vídeo parece uma matéria jornalística sobre a criança. Tem OFF do repórter (ElevenLabs) sobre b-roll e SONORAS com a criança e a mãe falando com o próprio áudio e tarja de nome (GC); manchete em caixa branca SÓ NO ALTO DA TELA (nunca no meio) com etiqueta vermelha "REPORTAGEM ESPECIAL • SOS HUMAN HELP"; legenda de jornal em faixa preta; etiqueta de valor e tela final "Clique em SAIBA MAIS"; nada em cima de rosto; sempre tela cheia; gancho com imagem forte em preto e branco. Use quando o usuário pedir "reportagem", "estilo jornal / matéria / notícia", "como se fosse uma reportagem do Pedrinho", ou escolher "Reportagem" no Estúdio. Não use para VSL com a voz da criança (criativo-vsl-voz-ong), lista narrada (criativo-lista-ong), narrado de impacto (criativo-narrado-ong) ou cortes (edicao-criativo-ong).
---

# Reportagem

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Não altere esta skill durante a conversa.** Ajustes pedidos no chat vão só no `plano.json` daquele vídeo (em `EDITADOS\_planos\<nome>\`). Esta skill e o Estúdio de Criativos só mudam quando o usuário pedir explicitamente para **salvar** (regra do usuário, 26/10/2026). Quando ele pedir, leve para cá tudo o que foi aprovado e diga o que foi salvo.

> **Antes de criar, leia** $HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md: regras do usuário com data, vozes, falas reais com a fonte, ângulos já usados e problemas já resolvidos. As transcrições prontas dos brutos estão em 	ranscricoes\ ao lado.

Aprovado como estilo em 26/10/2026. O exemplo é `EDITADOS/Pedrinho_reportagem_v1.mp4` (54 s); o plano está em `EDITADOS/_planos/Pedrinho_reportagem_v1/plano.json`, com cópia em `references/exemplo-plano-pedrinho-reportagem.json`. Fale com o usuário em português do Brasil.

## A ideia
É a linguagem de uma matéria de TV, adaptada ao celular. O repórter (OFF) dá o contexto e os números. A criança e a mãe (SONORAS) confirmam com a própria voz e o próprio rosto. A manchete fica fixa, como nos vídeos de portais de notícia. O pedido de doação entra no fim, como um "saiba como ajudar".

## Regras (não negociáveis)
1. **Nunca imite uma emissora ou um portal real.** Nada de nome, logo, vinheta ou cores que lembrem Globo, Record, SBT, g1, UOL etc. O selo é sempre "REPORTAGEM ESPECIAL • SOS HUMAN HELP". A Meta reprova anúncio que se passa por veículo de imprensa, e isso também enganaria o doador.
2. **Nenhum texto em cima do rosto da criança.** Nas sonoras, o rosto de quem fala também fica livre: se o detector não pegar, marque em `zonas_protegidas`.
3. Manchete, selo e tarja de nome ficam na **zona segura** (y entre 290 e 1250).
4. **Só fato real:** o OFF só diz o que a família falou nos brutos ou o que aparece no banco. Escreva a fonte de cada fato no campo `fatos` do plano.
5. **Narrador brasileiro** no OFF. A voz do exemplo (Brian, `nPczCjzI2devNBz1zQrb`) é provisória. Veja "Voz".
6. A etiqueta pede o mesmo valor que o OFF (R$ 10 no exemplo).
7. **Copy nova a cada vídeo:** a manchete, os OFFs, a escolha e a ordem das sonoras mudam.

## Estrutura (cerca de 55 s)
1. **OFF de abertura**, uma frase de impacto sobre o b-roll.
2. **SONORA da criança se apresentando**, com GC: nome e uma descrição.
3. **OFF de contexto**: a doença e a rotina.
4. **SONORA da mãe**, com GC.
5. **OFF com o número forte**: as horas de curativo e o custo por mês.
6. **SONORA da criança** com uma frase de força.
7. **SONORA da mãe**: "está acabando" e o que falta.
8. **OFF "como ajudar"**: a ONG está arrecadando, e o valor já ajuda. Nesse bloco entra a etiqueta.
9. **SONORA final da criança** com o pedido ("seja um anjo").
10. **Tela final** com OFF curto ("Clique em Saiba mais e veja como ajudar").

## Visual
- **Selo:** faixa vermelha `#CC101E` com "REPORTAGEM ESPECIAL" e faixa azul-marinho com a marca. Fica no topo da zona segura.
- **Manchete só no alto da tela** (y 290 a 470, `TOPO_MAX` no script), **nunca no meio da tela**. Se o rosto ocupar o alto, ela some naquela cena.
- **Manchete:** caixa branca com borda vermelha à esquerda e etiqueta vermelha "ESPECIAL", em Segoe UI Black. Use 2 linhas, no máximo 34 caracteres cada.
- **GC (tarja):** faixa vermelha com o NOME e faixa branca com a descrição. Só aparece na **primeira** sonora de cada pessoa. Fica num lugar livre de rosto (de preferência na zona segura); se não houver, some naquela cena.
- **Sempre tela cheia** (vídeo e foto). Nunca diminua o vídeo nem use fundo desfocado. Nas sonoras em close, a manchete some durante a fala (como na TV) e volta no OFF seguinte.
- O selo "REPORTAGEM ESPECIAL • SOS HUMAN HELP" agora é a etiqueta vermelha da própria manchete, para ocupar menos altura.
- **Legenda de jornal:** texto branco em faixa preta translúcida, frases de até 6 palavras, quebrando na pontuação. Nas sonoras usa o tempo real; nos OFFs, o tempo é aproximado.
- **Sonora:** o trecho do bruto entra com imagem e áudio. Os cortes são jump cuts dentro da fala, sem vícios.
- **Áudio:** OFF e sonoras nivelados, trilha bem baixa (0,07) e mix em -14 LUFS.

## Regras de 26/10/2026 (pedido do usuário)
- **O botão do anúncio é "Saiba mais".** Nunca escreva "Doar agora", "DOE AGORA" ou "Toque em Doar agora" na narração, na etiqueta, na legenda ou na tela final. Use `"etiqueta_final": "👇 Clique em SAIBA MAIS"` e CTA falado "Clique em Saiba mais…". Se uma fala real da criança disser "clique em Doar agora", corte esse trecho.
- **Gancho com a imagem mais forte que houver** (ex.: close do rosto com as lesões, curativo, corpo todo enfaixado), **em preto e branco**. Se a chamada sumir no 1º segundo por causa do close, tudo bem: ela entra na cena seguinte.
- **Preto e branco em toda imagem muito forte** (close do rosto com lesões, pele em carne viva, curativo sendo feito). Marque a cena com `"pb"` como 3º item (`[video, inicio, "pb"]`) ou o bloco/foto inteiro com `"pb": true`. Momentos de esperança (evento, violão, família sorrindo, final) ficam coloridos.

## Pastas e ferramentas
- Base (abaixo, RAIZ): a pasta que tem `EDITADOS` e `ESTUDIO`. Ela muda de computador para computador: está no campo `raiz` do pedido e em `$HOME\.claude\estudio-ong.json` (o Estúdio grava ao abrir). Dentro dela, os nomes padrão são `VÍDEOS PARA EDITAR` (brutos), `banco de vídeos do <criança>` (b-roll e fotos), `MÚSICAS` e `EDITADOS`; se o pedido trouxer outras pastas, use as do pedido.
- Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. Scripts em `$K = "$HOME\.claude\skills\criativo-reportagem-ong\scripts"`.
- Dependências: Pillow e OpenCV 4. A narração vai pela API REST do ElevenLabs (o SDK do Python do sistema está quebrado). A chave fica em `ELEVENLABS_API_KEY`.
- As transcrições prontas ficam em `EDITADOS\_planos\Pedrinho_narrado_*\tx\`:
  - `roteiro7.json` (Pedrinho);
  - `v1`, `v2` e `v4` (Pedrinho);
  - `v3_mae_calor.json` (mãe);
  - `roteiro2_mae.json`;
  - `roteiro3.json` e `roteiro4.json`: diálogos em que não dá para saber quem fala cada frase. Evite usar como sonora.
- Para transcrever um bruto novo: `& $PY -I "$K\transcrever.py" "<video>" "<plano>\tx\<nome>.json"`.

## Fluxo
1. Transcreva e liste os fatos com a fonte.
2. Escreva os OFFs (terceira pessoa, frases curtas de telejornal, números por extenso) e escolha as sonoras.
3. Escreva o `plano.json`. Os campos são:
   - `manchete` (2 linhas), `etiqueta_manchete`, `marca`;
   - `etiqueta`, `etiqueta_final`;
   - `narracao` (OFF1…), `voz`, `musica`, `musica_volume`, `fatos`;
   - `blocos[]`: OFF com `tipo: off`, `fala`, e `cenas` ou `foto`; SONORA com `tipo: sonora`, `fonte`, `tx`, `cortes` e `gc` opcional; e opcionalmente `etiqueta` e `final`;
   - `zonas_protegidas`, com chave `arquivo` + `inicio`. Numa sonora, o `inicio` é o primeiro número de `cortes`.
4. Monte: `& $PY -I "$K\reportagem.py" "<plano>\plano.json"`.
5. Confira: `& $PY -I "$K\folha.py" "<saida.mp4>" "<plano>\linha_do_tempo.json" "<plano>\render\folha.png"`. Veja:
   - nenhum texto em rosto;
   - o GC não encosta no selo nem na boca de quem fala;
   - a manchete está entre as linhas ciano.
6. Entregue com `SendUserFile` (`display: render`). Mostre a tabela de OFFs e sonoras (com a fonte de cada fato) e avise que a voz do repórter é provisória enquanto não for brasileira.

## Voz
O plano gratuito do ElevenLabs bloqueia as vozes brasileiras da biblioteca pela API (erro 402). Há duas saídas:
- o usuário gera os OFFs no site com uma voz brasileira e salva em `<plano>\audio_br\OFF1.mp3` etc. O script usa `audio_br` antes de `audio`;
- com plano pago, use **Leonardo - Deep & Resonant** (`4XmhZ74tBbUVCXIYNMMo`) e apague os mp3 de `audio\`.

## Regras de 26/10/2026, 2ª rodada (salvas a pedido do usuário)
- **Sem travadinha antes da troca de cena.** O script já faz: foto entra parada com aproximação suave (sem degraus de zoom), cena de vídeo sem zoom em degraus; a fala real (sonora) continua rodando, sem som, até a troca de cena, em vez de congelar o último quadro. Confira no MP4 final: `ffmpeg -i "<saida.mp4>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`. Congelamentos de 0,2 s ou mais em sequência são erro; a cartela preta parada é normal.
- **Nenhuma imagem deitada** (rotação de 90°). O script endireita a foto que tem a rotação gravada pela câmera. Mesmo assim, olhe a folha; se aparecer deitada, troque a imagem.
- **"Gaze" se fala "gáze"**, nunca "gueize". O script troca só na voz; a legenda continua "gaze".
- **Narrador sempre brasileiro e em português.** A conta agora é paga: **Leonardo** (`4XmhZ74tBbUVCXIYNMMo`). Nunca use Brian nem Matilda. Se o editor estiver no plano gratuito do ElevenLabs (erro 402 na voz), avise que a voz brasileira exige plano pago. Isto vale no lugar do que a seção de voz desta skill diz sobre voz provisória.
- **Sem pausa de respiração.** O script guarda a fala crua em `audio\raw\` e usa em `audio\` a versão sem respiros e sem silêncios. Para regravar uma fala, apague as duas.
- **Legenda, etiqueta e tarja (GC) sempre dentro da zona segura** (até y=1250). A manchete continua no alto.

## Onde salvar (LEVAs)
- **Não escolha a pasta do vídeo.** O script de montagem salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, com **5 vídeos por LEVA**: quando a LEVA atual já tem 5, ele cria a próxima (`LEVA 02`, `LEVA 03`…). Re-render de um vídeo que já existe substitui o arquivo na mesma LEVA.
- O caminho final aparece na linha `saida:` e no `OK` do script e fica gravado no `plano.json` (`saida`). Use esse caminho em `saida`/`saidas` do pedido.
- O nome do arquivo é o `nome` do plano. Numere as versões olhando todas as LEVAs do estilo (depois do `_v6` vem o `_v7`); nunca repita um nome, senão o vídeo antigo é substituído.
- Pastas de todos os estilos em `EDITADOS`: `CORTES COM GANCHO`, `NARRADO DE IMPACTO`, `LISTA NARRADA`, `VSL COM VOZ DA CRIANÇA`, `REPORTAGEM`.

## Nome da ONG na narração
A ONG é **S.O.S Human Help**, falado "ésse ô ésse". Escreva "SOS Human Help" na narração: o script manda "Ésse Ô Ésse Human Help" para o ElevenLabs e mostra "SOS" na legenda. Narração gerada antes dessa regra (mp3 em `audio\`) fala "sós": apague o mp3 da fala que cita a ONG para gerar de novo.

## Pedido do Estúdio
1. Leia `EDITADOS\_pedidos\<id>.json`. Os `brutos` são as fontes das sonoras e dos fatos, o `banco` é o b-roll, e as `observacoes` têm prioridade.
2. Se `quantidade` for maior que 1, faça esse número de reportagens **diferentes entre si**: muda a manchete, os OFFs, a abertura, a ordem e a escolha das sonoras e as cenas. Cada uma tem o próprio plano e a própria saída (`<Crianca>_reportagem_vN`).
3. No fim, atualize o pedido com Edit: `"status": "concluido"`, `"saida"` (o primeiro) e `"saidas"` (a lista de todos).
