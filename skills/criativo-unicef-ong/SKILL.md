---
name: criativo-unicef-ong
description: >-
  Estilo "UNICEF" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Gancho de ~8 s modelado no anúncio 1669162520799709 da UNICEF Brasil ("Isso pode parecer um simples sachê…") - foto de um item real de curativo parada com zoom lento (crepe, gaze, pomada) e narrador brasileiro (ElevenLabs, Kaique) dizendo "Isso pode parecer uma simples <item>. Mas para o <criança>… é o que protege a pele… é o que alivia as dores", passando para a mãe fazendo o curativo e um close da criança; legenda pequena de 2 linhas no meio com a palavra falada numa caixinha vermelha; sem lettering no gancho. Depois, cortes com lettering bem simples (a criança falando, sem pausas, zoom a cada corte, legenda em Poppins Black, UM lettering da pasta "lettings" parado, b-roll, tela final "CLIQUE EM SAIBA MAIS"). Use quando o usuário pedir "estilo unicef", "igual ao anúncio da UNICEF", "isso pode parecer um simples…", "igual ao Pedrinho_atadura", ou escolher "UNICEF" no Estúdio.
---

# UNICEF (gancho "pode parecer simples" + cortes com lettering)

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O `montar.py` aplica no vídeo inteiro (gancho + cortes), uma vez só, no fim (`scripts/marca.py` + `scripts/logo_sos.png`), e **para com erro se a logo faltar**. Não existe opção para tirar a logo. O `build_cortes.py` não põe logo de propósito: nunca o use sozinho para entregar um vídeo.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

Criado a pedido do usuário em 27/10/2026 ("crie uma nova skill com esse estilo chamado unicef"), a partir do vídeo aprovado `EDITADOS\CORTES COM LETTERING\LEVA 01\Pedrinho_atadura_v1.mp4` (43 s). O plano dele está em `references/exemplo-plano.json` e a narração em `references/exemplo-roteiro-audio.json`. Fale com o usuário em português do Brasil.

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md`: falas reais com a fonte, ângulos já usados e regras. As transcrições prontas estão em `transcricoes\` ao lado. Ajustes pedidos no chat vão só no `plano.json` do vídeo; esta skill só muda quando o usuário pedir para salvar.

## O gancho (modelado na referência)
| Tempo | Referência UNICEF | Aqui |
|---|---|---|
| 0-~2,1 s (N0) | Sachê parado sobre fundo rústico: "Isso pode parecer um simples sachê…" | **Foto de um item real de curativo** do banco (`crepe bandagem.png`, `GAZE.png`, `Pomada.png`, `esparadrapo impermeável.png`, `soro fisiológico.png`…), recortada em 9:16, zoom lento e **linear**, **só durante a 1ª frase**: "Isso pode parecer uma simples atadura." |
| ~2,1-5 s (N1 até "bolhosa,") | "…mas para crianças que enfrentam fome…" | **Regra do usuário (27/10/2026): o gancho tem 2 imagens.** No momento em que o narrador começa a citar a criança ("Mas para o Pedrinho, que tem epidermólise bolhosa,"), entra **um vídeo (de preferência) ou uma foto forte do Pedrinho**: close do rosto deitado (bruto "não conseguir dormir"), ele inteiro enfaixado na cadeira de rodas (`20260916_234157`), `foto em close.png`… Cada vídeo usa uma cena forte diferente. Sem ferida aberta em close. |
| ~5-6,4 s | Mãe com o filho: "…é um pacotinho de esperança." | **A mãe fazendo o curativo** (vídeo do banco; `Vídeo Mostrando itens…`, ex.: 250 s): "…é o que protege a pele." |
| 6,4-8,3 s | Criança deitada: "É uma segunda chance na vida." | **Close da criança** (foto ou vídeo, sem ferida aberta): "É o que alivia as dores dele." |

- **Narração:** Kaique (`Hmn4B9B77pf6ttydteJ8`), 3 falas (N0, N1, N2), em 3ª pessoa. Só fato real; no aprovado, "alivia as dores" vem de "com os meus curativos, alivia bastante as minhas dores" (roteiro 7) e "protege" de 20260917_000819. Troque o item e a frase a cada vídeo.
- **Legenda do gancho:** Segoe UI Black 56, em 2 linhas no máximo, centro em y=1190, branca com contorno escuro; a palavra falada fica numa **caixinha vermelha** (`#D90429`, no lugar do azul da UNICEF). Os blocos de texto (`gancho.blocos`) têm que somar exatamente as palavras da narração (o script confere).
- **Sem lettering no gancho**, como na referência; o lettering entra junto com os cortes.
- **Nada da UNICEF:** sem logo, sem cor azul, sem sachê, sem dados deles. Só a estrutura da frase.

## Os cortes (igual a "Cortes com lettering", bem simples)
- A criança falando, sem pausas nem vícios, zoom a cada corte, legenda Poppins Black em y=950 com destaque vermelho, b-roll casando com a fala, tela final "CLIQUE EM SAIBA MAIS ♥".
- **Um lettering só** da pasta `lettings`, parado do início dos cortes até o fim. O valor tem que bater com a fala (no aprovado ele diz "dois, três, cinco reais" → lettering R$ 5 "alívio"). As regras de escolha estão na skill `criativo-lettering-ong`, seção "Escolher o lettering".
- Comece os cortes com a criança na câmera e continue o assunto do gancho (no aprovado: "A minha mamãe precisa fazer os meus curativos todos os dias…").
- 30 a 35 s de fala; o vídeo inteiro fica com uns 40-45 s.
- **Música:** o piano `alex-morgan…` toca do gancho até o fim, sem corte na emenda (o `montar.py` mixa a música uma vez só; os cortes saem sem música).

## Fluxo
Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. Scripts em `$K = "$HOME\.claude\skills\criativo-unicef-ong\scripts"`. Crie e edite os JSON com Write/Edit ou com um script Python. Antes de usar o ElevenLabs, no mesmo comando: `$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')`.
1. **Bruto e ângulo:** um bruto e um ângulo ainda não usados em Cortes com gancho, Cortes com lettering nem UNICEF (veja `EDITADOS\_planos\`). Reaproveite a transcrição pronta ou rode `& $PY -I "$K\transcribe.py" "<bruto>" "<plano>\transcricao.json"`.
2. **Cortes:** `& $PY -I "$K\inspect_tx.py" "<transcrição>" --words --draft`; cada corte vai do início da 1ª palavra -0,03 s ao fim da última +0,06 s. Ache o `face` numa grade do bruto.
3. **Item e cenas do gancho:** escolha o item (de preferência um que a criança cite no bruto) e as três cenas seguintes: a **cena forte do Pedrinho** (entra exatamente no "Mas" do N1 e vai até o fim de "bolhosa,"), a mãe fazendo o curativo e o close final. São 4 cenas em `gancho.cenas`; a cena de vídeo aceita caminho completo (bruto de `VÍDEOS PARA EDITAR`). Monte folhas do banco para achar os trechos (sem ferida aberta à mostra).
4. **Narração:** copie `references/exemplo-roteiro-audio.json` para `<plano>\roteiro_audio.json`, escreva N0-N2 novos e rode `& $PY -I "$K\gerar_audio.py" "<plano>\roteiro_audio.json" "<plano>\audio"`. **Confira pela transcrição** (`transcrever.py`) que a voz não tropeçou; se tropeçar, troque a palavra e gere de novo (apague `audio\N*.mp3` e `audio\raw\N*.mp3`).
5. **Plano:** copie `references/exemplo-plano.json` para `EDITADOS\_planos\<Criança>_<ângulo>_vN\plano.json` e troque `nome`, `angulo`, `gancho` (tempos de `narracao` pelas durações dos N, `fim` ≈ fim do N2 + 0,35 s, `cenas`, `blocos`), `raw`, `transcript`, `face`, `segments`, `red`, `fix`, `chamada`, `endcard`, `fatos`. `music_start` = `gancho.fim`.
6. **Montar:** `& $PY -I "$K\montar.py" "<plano>\plano.json"`. Sai em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, 5 por LEVA, com a logo.
7. **Conferir o MP4 final:** transcrição contra o roteiro; folha de quadros (gancho, lettering sem cobrir rosto, logo aparecendo); travadinha com `ffmpeg -i "<saida>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -` (o zoom das fotos tem que ser linear: curva suave parou 0,15 s nas pontas); buracos no áudio.
8. **Entregar** com `SendUserFile`. Mostre o gancho em tabela (referência × nosso), diga bruto, lettering e b-rolls, e avise que você não ouve o áudio.

## Pedido do Estúdio
Leia o JSON do pedido: os `brutos` trazem as falas dos cortes, o `banco` as fotos de item e as cenas, e as `observacoes` têm prioridade (inclusive o valor). Com `quantidade` maior que 1, cada vídeo tem outro item no gancho, outra frase, outro bruto ou trecho e outro lettering. No fim, grave com Edit `"status": "concluido"`, `"saida"` e `"saidas"`.
