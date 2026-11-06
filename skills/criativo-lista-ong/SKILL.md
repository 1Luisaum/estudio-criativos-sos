---
name: criativo-lista-ong
description: >-
  Estilo "Lista narrada" (nativo TikTok) aprovado para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Só narração do ElevenLabs + b-roll (os brutos entram sem o áudio deles); vídeo cru em tela cheia sem moldura nem filtro; chamada fixa em caixa amarela pedindo doação, sempre na zona segura e nunca em cima de rosto; legenda curta de até 3 palavras com destaque amarelo; fotos dos produtos de curativo; etiqueta branca de valor; tela final "Clique em SAIBA MAIS"; sempre tela cheia; gancho com imagem forte em preto e branco. Use quando o usuário pedir o "estilo lista", "igual ao Pedrinho_lista", "só narração e b-roll", "vídeo nativo / estilo TikTok", ou escolher "Lista narrada" no Estúdio. Não use para o narrado que alterna com falas reais (criativo-narrado-ong) nem para o de cortes da criança falando (edicao-criativo-ong).
---

# Criativo "Lista narrada": narração + b-roll em visual nativo de TikTok

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Não altere esta skill durante a conversa.** Ajustes pedidos no chat vão só no `plano.json` daquele vídeo (em `EDITADOS\_planos\<nome>\`). Esta skill e o Estúdio de Criativos só mudam quando o usuário pedir explicitamente para **salvar** (regra do usuário, 26/10/2026). Quando ele pedir, leve para cá tudo o que foi aprovado e diga o que foi salvo.

> **Antes de criar, leia** $HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md: regras do usuário com data, vozes, falas reais com a fonte, ângulos já usados e problemas já resolvidos. As transcrições prontas dos brutos estão em 	ranscricoes\ ao lado.

Aprovado em 26/10/2026 no vídeo `EDITADOS/Pedrinho_lista_v2.mp4` (45 s). O plano dele está em `EDITADOS/_planos/Pedrinho_lista_v2/plano.json` (cópia em `references/exemplo-plano-pedrinho-lista-v2.json`) e o `scripts/lista.py` reproduz esse vídeo pixel por pixel. As especificações e as referências da Biblioteca de Anúncios estão em `references/estilo.md`. Leia antes de mudar qualquer coisa visual.

Fale com o usuário em português do Brasil. Este estilo é independente das skills `criativo-narrado-ong` e `edicao-criativo-ong`; não misture.

## Regras do usuário (não negociáveis)
1. **Só narração + b-roll.** Pode usar os vídeos brutos, mas **sem o áudio deles**.
2. **Narrador brasileiro.** Veja a seção Voz.
3. **Nada de texto em cima do rosto da criança.** Conferir quadro a quadro.
4. **Chamada na zona segura** (entre y=290 e y=1250 num quadro 1080x1920), nunca no topo nem embaixo.
5. **Chamada persuasiva, que toque o coração, pedindo um valor** (no aprovado: R$ 10).
6. **Visual nativo:** sem moldura, papel, polaroid, filtro ou faixa desenhada. A 1ª versão com esses elementos foi reprovada como "muito feia".
7. **Só fato dito por alguém real** (criança ou mãe) ou mostrado no banco entra na copy.

## Regras de 26/10/2026 (pedido do usuário)
- **O botão do anúncio é "Saiba mais".** Nunca escreva "Doar agora", "DOE AGORA" ou "Toque em Doar agora" na narração, na etiqueta, na legenda ou na tela final. Use `"etiqueta_final": "👇 Clique em SAIBA MAIS"` e CTA falado "Clique em Saiba mais…". Se uma fala real da criança disser "clique em Doar agora", corte esse trecho.
- **Gancho com a imagem mais forte que houver** (ex.: close do rosto com as lesões, curativo, corpo todo enfaixado), **em preto e branco**. Se a chamada sumir no 1º segundo por causa do close, tudo bem: ela entra na cena seguinte.
- **Preto e branco em toda imagem muito forte** (close do rosto com lesões, pele em carne viva, curativo sendo feito). Marque a cena com `"pb"` como 3º item (`[video, inicio, "pb"]`) ou o bloco/foto inteiro com `"pb": true`. Momentos de esperança (evento, violão, família sorrindo, final) ficam coloridos.

## Pastas e ferramentas
- Base (abaixo, RAIZ): a pasta que tem `EDITADOS` e `ESTUDIO`. Ela muda de computador para computador: está no campo `raiz` do pedido e em `$HOME\.claude\estudio-ong.json` (o Estúdio grava ao abrir). Dentro dela, os nomes padrão são `VÍDEOS PARA EDITAR` (brutos), `banco de vídeos do <criança>` (b-roll e fotos), `MÚSICAS` e `EDITADOS`; se o pedido trouxer outras pastas, use as do pedido.
- Cada vídeo ganha `EDITADOS\_planos\<nome>\` com `plano.json`, `audio\` (narração gerada), `audio_br\` (narração brasileira gerada no site, se houver) e `render\` (intermediários).
- Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I` (o `python` do PATH pode ser o atalho da Microsoft Store). Scripts em `$K = "$HOME\.claude\skills\criativo-lista-ong\scripts"`.
- Dependências: Pillow e **OpenCV 4**; a narração vai pela API REST do ElevenLabs (o SDK do Python do sistema está quebrado). OpenCV 4 (`opencv-python-headless<5`). O OpenCV 5 não tem o detector de rosto usado; o `mediapipe` instala o OpenCV 5 e quebra tudo, então não instale.
- **Crie e edite os JSON com a ferramenta Write/Edit, nunca com `Set-Content`**: o PowerShell 5 grava os acentos errado.

## Fluxo

### 1. Levantar os fatos
Transcreva os brutos com falas da criança ou da mãe:
```
& $PY -I "$K\transcrever.py" "<video>" "<pasta do plano>\tx\<nome>.json"
```
Anote cada fato com a fonte (vai no campo `fatos` do plano). Do Pedrinho já se sabe:
- o último curativo levou 5 horas;
- todo dia aparecem bolhas de sangue e de água que a mãe rompe;
- as feridas estão cada vez mais abertas;
- ele não consegue dormir de dor;
- o curativo é feito 2 vezes por dia;
- a mãe disse que 2 ou 5 reais já ajudam demais;
- o Pedrinho pede "seja um anjo na minha vida".

As fotos de produto do banco são: crepe bandagem, GAZE, Pomada, soro fisiológico, esparadrapo impermeável, OLeo de girassol, Curativos 2 x ao Dia, Remédios Pomadas e Cremes, e Cubitan.

### 2. Escrever a copy (nova a cada vídeo)
São criativos de teste: cada vídeo novo precisa de **ângulo, gancho, narração e chamada novos**. Não reaproveite frases dos planos anteriores; leia `EDITADOS\_planos\*\plano.json` antes. Formatos de gancho validados estão na seção 6 de `references/pacote-criativos-ong-eb.md`.

**Estrutura que funcionou (em ~45 s):**
1. gancho, em uma frase;
2. a lista de itens, uma palavra por foto;
3. a frequência;
4. a doença em uma frase concreta;
5. o número forte;
6. a dor;
7. a virada ("está acabando");
8. o pedido com a fala real da mãe;
9. a tela final.

**A chamada fixa** tem 2 linhas: um apelo emocional e o pedido com valor e destino. Exemplo aprovado: "SEJA O ANJO DO PEDRINHO 👼 / DOE R$ 10 PRO CURATIVO DELE 💔". O emoji 🙏 sai feio na caixa amarela; prefira 👼 💔 ❤️.

**A etiqueta** precisa ter o **mesmo valor** da chamada. No aprovado ficou R$ 5 contra R$ 10, e eu avisei o usuário do conflito.

**A narração** é sempre em terceira pessoa. Nunca narre como se fosse a criança, nem imite a voz dela ou da mãe. Escreva os números por extenso ("cinco horas").

### 3. Voz (narrador brasileiro)
- A conta ElevenLabs está no **plano gratuito**. Pela API, ele **não libera vozes da biblioteca** (erro 402) **nem criação de voz** (403). Com isso, nenhuma voz brasileira funciona pela API.
- O aprovado ainda usa a voz **provisória** Matilda (`XrExE9yKIg1WjnnlVkGX`), que não é brasileira, e o usuário quer narrador brasileiro.
- **Caminho que funciona sem pagar:** o usuário gera as falas no site do ElevenLabs com uma voz brasileira e salva em `<plano>\audio_br\<CHAVE>.mp3` (ex.: `N01.mp3`, `I1.mp3`). O `lista.py` usa `audio_br` antes de `audio` e reajusta o tempo de tudo sozinho. Deixe na pasta um `LEIA-ME.txt` com a lista de chaves e textos (modelo em `EDITADOS\_planos\Pedrinho_lista_v1\audio_br\LEIA-ME.txt`).
- **Se o usuário assinar um plano pago:** use **Leonardo - Deep & Resonant** (`4XmhZ74tBbUVCXIYNMMo`, a voz masculina brasileira mais usada, que já está na biblioteca da conta) e apague os mp3 de `audio\`.
- **A chave** fica em `ELEVENLABS_API_KEY` (variável de usuário do Windows). Nunca digite, mostre ou peça a chave no chat.

### 4. Escolher as cenas
- Para cada fala, escolha 1 a 3 trechos de vídeo (`"cenas": [[arquivo, início], ...]`) ou uma foto (`"foto"`). A duração do bloco é a da fala mais a pausa, dividida igualmente entre as cenas.
- Para ver os vídeos sem abrir quadro a quadro, monte uma folha: `ffmpeg -ss <t> -i <video> -frames:v 1 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=270:480,drawgrid=w=27:h=48:t=1:c=red@0.35" g.png`, depois junte com `tile`.
- **Criança pequena ao fundo ou de lado:** o detector não pega. Marque em `zonas_protegidas` com a caixa em pixels reais (cada quadrado da grade = 108x192 px).
- Nada de ferida aberta em close (a Meta reprova). Nada de b-roll que contradiga a fala.

### 5. Escrever o `plano.json` e montar
Use o exemplo em `references/exemplo-plano-pedrinho-lista-v2.json`. Os campos são:
- `saida`, `voz`, `musica`, `musica_volume`;
- `chamada` (lista de 2 linhas), `etiqueta`, `etiqueta_final`, `palavras_chave`;
- `narracao` (chave → texto), `fatos`;
- `blocos`: cada um com `nome`, `fala`, `pausa`, `cenas` ou `foto`, e opcionalmente `etiqueta: true` e `final: true`;
- `zonas_protegidas`.

```
& $PY -I "$K\lista.py" "<pasta do plano>\plano.json"
```
O script imprime a posição de cada cena (`chamada=` ou `ESCONDIDA`, `legenda=`, `etiqueta=`) e termina com `OK <saida> duracao=XXs`.

### 6. Conferir
```
& $PY -I "$K\folha.py" "<saida.mp4>" "<pasta do plano>\linha_do_tempo.json" "<pasta do plano>\render\folha.png"
```
Abra a folha. As linhas ciano marcam a zona segura. Confira:
- a chamada está entre as duas linhas em todas as cenas;
- nenhum texto está no rosto da criança, inclusive quando ela aparece pequena no fundo (dê zoom nessas cenas);
- o vídeo está em tela cheia em todas as cenas, inclusive nas fotos;
- a legenda não encosta na chamada.

Se a chamada aparecer `ESCONDIDA` no gancho (primeiros 2 s), troque essa cena por uma em que o rosto não ocupe a zona segura: a chamada precisa estar visível desde o primeiro quadro.

### 7. Entregar
Mande com `SendUserFile` (`display: render`). Mostre a copy (chamada, narração, fonte de cada fato) e diga o que você não garante:
- que a voz não é brasileira, enquanto ela for a provisória;
- que você não ouve o áudio, então o usuário deve conferir;
- qualquer conflito de valor entre chamada, etiqueta e narração.

## Regras de 26/10/2026, 2ª rodada (salvas a pedido do usuário)
- **Sem travadinha antes da troca de cena.** O script já faz: foto entra parada com aproximação suave (sem degraus de zoom), cena de vídeo sem zoom em degraus. Confira no MP4 final: `ffmpeg -i "<saida.mp4>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`. Congelamentos de 0,2 s ou mais em sequência são erro; a cartela preta parada é normal.
- **Nenhuma imagem deitada** (rotação de 90°). O script endireita a foto que tem a rotação gravada pela câmera. Mesmo assim, olhe a folha; se aparecer deitada, troque a imagem.
- **"Gaze" se fala "gáze"**, nunca "gueize". O script troca só na voz; a legenda continua "gaze".
- **Narrador sempre brasileiro e em português.** A conta agora é paga: **Leonardo** (`4XmhZ74tBbUVCXIYNMMo`). Nunca use Brian nem Matilda. Se o editor estiver no plano gratuito do ElevenLabs (erro 402 na voz), avise que a voz brasileira exige plano pago. Isto vale no lugar do que a seção de voz desta skill diz sobre voz provisória.
- **Sem pausa de respiração.** O script guarda a fala crua em `audio\raw\` e usa em `audio\` a versão sem respiros e sem silêncios. Para regravar uma fala, apague as duas.
- **Chamada só no alto da tela** (y 290 a 470). Se um rosto ocupar o alto, ela some naquela cena; nunca vai para o meio do vídeo.
- **Legenda e etiqueta sempre dentro da zona segura do Instagram** (até y=1250).
- **Produtos:** foto parada, sem panorâmica lateral, e mais tempo na tela: `pausa` 0,45 nos blocos de item (`i1`, `i2`...). Os outros blocos usam `pausa` 0,08 e a tela final 1,6.

## Onde salvar (LEVAs)
- **Não escolha a pasta do vídeo.** O script de montagem salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, com **5 vídeos por LEVA**: quando a LEVA atual já tem 5, ele cria a próxima (`LEVA 02`, `LEVA 03`…). Re-render de um vídeo que já existe substitui o arquivo na mesma LEVA.
- O caminho final aparece na linha `saida:` e no `OK` do script e fica gravado no `plano.json` (`saida`). Use esse caminho em `saida`/`saidas` do pedido.
- O nome do arquivo é o `nome` do plano. Numere as versões olhando todas as LEVAs do estilo (depois do `_v6` vem o `_v7`); nunca repita um nome, senão o vídeo antigo é substituído.
- Pastas de todos os estilos em `EDITADOS`: `CORTES COM GANCHO`, `NARRADO DE IMPACTO`, `LISTA NARRADA`, `VSL COM VOZ DA CRIANÇA`, `REPORTAGEM`.

## Nome da ONG na narração
A ONG é **S.O.S Human Help**, falado "ésse ô ésse". Escreva "SOS Human Help" na narração: o script manda "Ésse Ô Ésse Human Help" para o ElevenLabs e mostra "SOS" na legenda. Narração gerada antes dessa regra (mp3 em `audio\`) fala "sós": apague o mp3 da fala que cita a ONG para gerar de novo.

## Pedido do Estúdio
Pelo Estúdio (pasta `ESTUDIO` dentro da RAIZ, aberto pelo `ABRIR ESTUDIO.bat`), o usuário escolhe "Lista narrada" e cola algo como "Executa o pedido do Estúdio <id> (arquivo EDITADOS\_pedidos\<id>.json) com a skill criativo-lista-ong". Nesse caso:
1. Leia o JSON. Os campos são:
   - `brutos`: as fontes de fatos e de cenas, usadas sem o áudio;
   - `banco`: fotos e b-roll;
   - `musica`: vazio = piano aprovado;
   - `crianca`;
   - `observacoes`: siga o que estiver ali, como o valor do pedido ou o ângulo.
2. Rode o fluxo acima.
3. No fim, atualize o pedido com a ferramenta Edit: `"status": "concluido"` e `"saida": "<caminho do MP4>"`.

4. **Pedido com `quantidade` maior que 1** (opção "5 criativos de uma vez" do Estúdio): faça esse número de criativos **diferentes entre si** (gancho, copy/falas, chamada ou manchete e cenas diferentes; nunca o mesmo vídeo com outra música). Cada um tem o próprio plano e a própria saída (`..._v1`, `_v2`...). No fim, grave `"saida"` com o primeiro MP4 e `"saidas"` com a lista de todos. A fila só mostra "pronto" quando todos existem.

## Ajustes
Mexa só no que o usuário pedir e rode o `lista.py` de novo. Ele é determinístico: o mesmo plano gera o mesmo vídeo. Exemplos já feitos:
- "headline na zona morta": a chamada foi presa entre y=290 e y=1250;
- "não tampar o rosto": entraram o detector e as zonas protegidas;
- "deixe sempre o vídeo em tela cheia, não diminua o vídeo e desfoque o fundo" (26/10/2026): vídeo e foto sempre ocupam a tela inteira. Nos closes em que o rosto ocupa a zona segura, a chamada some só naquela cena. **Nunca** reduza o vídeo nem use fundo desfocado.
