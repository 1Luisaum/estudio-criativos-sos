---
name: criativo-vsl-voz-ong
description: >-
  Estilo "VSL com a voz da criança" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). A narração é a PRÓPRIA FALA da criança, cortada dos brutos sem pausas nem vícios, e por cima passam só b-rolls (vídeos e fotos do banco), como numa VSL. Visual nativo de TikTok: vídeo cru em tela cheia, chamada amarela de doação na zona segura e nunca em cima de rosto, legenda palavra por palavra com o tempo real da fala, etiqueta de valor e tela final "Clique em SAIBA MAIS"; sempre tela cheia; gancho com imagem forte em preto e branco. Use quando o usuário pedir "VSL", "só a voz do Pedrinho com b-roll", "narração da própria criança", "vídeos passando por cima da fala dele", ou escolher "VSL com a voz da criança" no Estúdio. Não use para narrador do ElevenLabs (criativo-lista-ong / criativo-narrado-ong), reportagem (criativo-reportagem-ong) ou cortes da criança falando na tela (edicao-criativo-ong).
---

# VSL com a voz da criança

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Não altere esta skill durante a conversa.** Ajustes pedidos no chat vão só no `plano.json` daquele vídeo (em `EDITADOS\_planos\<nome>\`). Esta skill e o Estúdio de Criativos só mudam quando o usuário pedir explicitamente para **salvar** (regra do usuário, 26/10/2026). Quando ele pedir, leve para cá tudo o que foi aprovado e diga o que foi salvo.

> **Antes de criar, leia** $HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md: regras do usuário com data, vozes, falas reais com a fonte, ângulos já usados e problemas já resolvidos. As transcrições prontas dos brutos estão em 	ranscricoes\ ao lado.

Aprovado como estilo em 26/10/2026. O exemplo é `EDITADOS/Pedrinho_vsl_voz_v1.mp4` (49 s); o plano dele está em `EDITADOS/_planos/Pedrinho_vsl_voz_v1/plano.json`, com cópia em `references/exemplo-plano-pedrinho-vsl.json`. Fale com o usuário em português do Brasil.

## A ideia
- **O espectador ouve a criança, mas vê a vida dela.** A voz é a prova de que é real. O b-roll mostra o que ela está dizendo: o curativo, a mãe, a cadeira de rodas, um momento feliz.
- A boca da criança **não aparece falando outra frase**. Use b-roll em que ninguém esteja falando para a câmera, ou em que a fala não apareça.
- O visual é o mesmo da skill `criativo-lista-ong`: nativo, sem moldura, chamada na zona segura, rosto livre. Os detalhes estão em `references/estilo.md`.

## Regras do usuário
1. Só a voz real da criança, tirada de um bruto, mais b-roll. Nada de narrador de IA.
2. Nenhum texto em cima do rosto da criança.
3. A chamada fica na zona segura (y entre 290 e 1250), é persuasiva e pede um valor (R$ 10 no exemplo).
4. A etiqueta tem o mesmo valor da chamada.
5. Copy nova a cada vídeo: a ordem das falas, a chamada e as cenas mudam.

## Regras de 26/10/2026 (pedido do usuário)
- **O botão do anúncio é "Saiba mais".** Nunca escreva "Doar agora", "DOE AGORA" ou "Toque em Doar agora" na narração, na etiqueta, na legenda ou na tela final. Use `"etiqueta_final": "👇 Clique em SAIBA MAIS"` e CTA falado "Clique em Saiba mais…". Se uma fala real da criança disser "clique em Doar agora", corte esse trecho.
- **Gancho com a imagem mais forte que houver** (ex.: close do rosto com as lesões, curativo, corpo todo enfaixado), **em preto e branco**. Se a chamada sumir no 1º segundo por causa do close, tudo bem: ela entra na cena seguinte.
- **Preto e branco em toda imagem muito forte** (close do rosto com lesões, pele em carne viva, curativo sendo feito). Marque a cena com `"pb"` como 3º item (`[video, inicio, "pb"]`) ou o bloco/foto inteiro com `"pb": true`. Momentos de esperança (evento, violão, família sorrindo, final) ficam coloridos.

## Pastas e ferramentas
- Base (abaixo, RAIZ): a pasta que tem `EDITADOS` e `ESTUDIO`. Ela muda de computador para computador: está no campo `raiz` do pedido e em `$HOME\.claude\estudio-ong.json` (o Estúdio grava ao abrir). Dentro dela, os nomes padrão são `VÍDEOS PARA EDITAR` (brutos), `banco de vídeos do <criança>` (b-roll e fotos), `MÚSICAS` e `EDITADOS`; se o pedido trouxer outras pastas, use as do pedido.
- `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. Scripts em `$K = "$HOME\.claude\skills\criativo-vsl-voz-ong\scripts"`.
- Dependências: Pillow e OpenCV 4 (`opencv-python-headless<5`; não instale `mediapipe`, que troca pelo 5).
- **Sempre tela cheia** (vídeo e foto). Nunca diminua o vídeo nem use fundo desfocado. Se a chamada sair `ESCONDIDA` numa cena do gancho, troque a cena.
- Crie e edite os JSON com Write/Edit, nunca com `Set-Content`.

## Fluxo
1. **Transcrever** cada bruto em que a criança fala (tempo por palavra):
   `& $PY -I "$K\transcrever.py" "<video>" "<plano>\tx\<nome>.json"`
   As transcrições prontas do Pedrinho ficam em `EDITADOS\_planos\Pedrinho_narrado_*\tx\`:
   - `roteiro7.json`, de `banco\Roteiro 7.mp4`: a fala mais limpa, com apresentação, batalha, R$ 40 mil e "se você puder lutar comigo" (não use o trecho "clique em Doar agora": o botão virou "Saiba mais");
   - `v1_cinco_horas.json`;
   - `v2_dormir.json`;
   - `v4_curativos_acabando.json`.
2. **Gancho:** use o close do rosto da própria fala do gancho (o mesmo vídeo de onde sai a voz, um corte só) em preto e branco, para a boca bater com a voz.
3. **Montar o roteiro com as falas reais.** Escolha de 8 a 10 frases fortes e corte os vícios ("é", "aaa", gaguejadas) dividindo a frase em vários `cortes`. Cada corte é `[início da 1ª palavra, início da última palavra]`, copiados da transcrição. O script estende até o fim da última palavra.
   A estrutura que funcionou: pedido de tempo → quem ele é → a rotina de curativo → o número forte → a dor → a frase de força → "estão acabando" → "seja um anjo" → "se você puder lutar comigo… minha gratidão".
3. **Escolher o b-roll de cada frase,** casando com o que é dito:
   - curativo em "curativo";
   - evento ou cadeira de rodas em "quem eu sou" e "eu escolhi lutar";
   - foto dos produtos em "estão acabando";
   - foto da família no final.

   Monte uma folha de contato do banco antes de escolher (exemplo de comando em `references/estilo.md`).
4. **Escrever o `plano.json`** (veja o exemplo). Os campos são `frases[]` (com `nome`, `fonte`, `tx`, `cortes`, `cenas` ou `foto`, `etiqueta` e `final`), `chamada`, `etiqueta`, `etiqueta_final`, `palavras_chave`, `musica`, `musica_volume` e `zonas_protegidas`.
5. **Montar:** `& $PY -I "$K\vsl.py" "<plano>\plano.json"`. A saída mostra o texto de cada frase como ficou depois dos cortes. Leia e confira se nenhuma palavra foi cortada no meio.
6. **Conferir:** `& $PY -I "$K\folha.py" "<saida.mp4>" "<plano>\linha_do_tempo.json" "<plano>\render\folha.png"`. Abra a folha e veja:
   - nenhum texto no rosto, inclusive da criança pequena ao fundo (dê zoom nessas cenas);
   - a chamada entre as linhas ciano.

   Se o rosto não for detectado (ele é pequeno, está de lado ou tem muitas lesões), troque a cena ou marque `zonas_protegidas`.
7. **Entregar** com `SendUserFile` (`display: render`). Mostre a tabela de falas (frase, bruto de onde veio e cena por cima) e peça para o usuário ouvir os cortes da voz, porque você não ouve áudio.

## Regras de 26/10/2026, 2ª rodada (salvas a pedido do usuário)
- **Sem travadinha antes da troca de cena.** O script já faz: foto entra parada com aproximação suave (sem degraus de zoom), cena de vídeo sem zoom em degraus. Confira no MP4 final: `ffmpeg -i "<saida.mp4>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`. Congelamentos de 0,2 s ou mais em sequência são erro; a cartela preta parada é normal.
- **Nenhuma imagem deitada** (rotação de 90°). O script endireita a foto que tem a rotação gravada pela câmera. Mesmo assim, olhe a folha; se aparecer deitada, troque a imagem.
- **"Gaze" se fala "gáze"**, nunca "gueize". O script troca só na voz; a legenda continua "gaze".
- **Chamada só no alto da tela** (y 290 a 470). Se um rosto ocupar o alto, ela some naquela cena; nunca vai para o meio do vídeo.
- **Legenda e etiqueta sempre dentro da zona segura do Instagram** (até y=1250).

## Onde salvar (LEVAs)
- **Não escolha a pasta do vídeo.** O script de montagem salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, com **5 vídeos por LEVA**: quando a LEVA atual já tem 5, ele cria a próxima (`LEVA 02`, `LEVA 03`…). Re-render de um vídeo que já existe substitui o arquivo na mesma LEVA.
- O caminho final aparece na linha `saida:` e no `OK` do script e fica gravado no `plano.json` (`saida`). Use esse caminho em `saida`/`saidas` do pedido.
- O nome do arquivo é o `nome` do plano. Numere as versões olhando todas as LEVAs do estilo (depois do `_v6` vem o `_v7`); nunca repita um nome, senão o vídeo antigo é substituído.
- Pastas de todos os estilos em `EDITADOS`: `CORTES COM GANCHO`, `NARRADO DE IMPACTO`, `LISTA NARRADA`, `VSL COM VOZ DA CRIANÇA`, `REPORTAGEM`.

## Pedido do Estúdio
O pedido chega como "Executa o pedido do Estúdio <id> ... com a skill criativo-vsl-voz-ong". Siga estes passos:
1. Leia o `EDITADOS\_pedidos\<id>.json`. Os `brutos` são as fontes da voz, o `banco` é o b-roll, e as `observacoes` têm prioridade.
2. Se `quantidade` for maior que 1, faça esse número de criativos **diferentes entre si**: muda a ordem das falas, o gancho de abertura, a chamada e as cenas. Cada um tem o próprio plano e a própria saída (`<Crianca>_vsl_voz_vN`).
3. No fim, atualize o pedido com Edit: `"status": "concluido"`, `"saida"` (o primeiro MP4) e `"saidas"` (a lista de todos).
