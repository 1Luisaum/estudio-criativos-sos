---
name: criativo-esperanca-ong
description: >-
  Estilo "Da dor à esperança" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Vídeo em arco de história, de uns 40 s - começa MUITO impactante (cartela em P&B com batida de coração, narrador dizendo uma frase curta e palavras gigantes entrando no tempo da voz, a última em vermelho com boom; depois a fala real mais dolorida da criança), desenvolve em P&B com música tensa (narrador + falas reais da criança e da mãe), vira com clarão branco e whoosh para COR e música esperançosa, e acaba feliz/emocionante (momentos alegres, fala de força da criança, pedido de R$10 e tela final "O FINAL FELIZ COMEÇA COM VOCÊ" + "CLIQUE EM SAIBA MAIS"). Legenda sempre em uma linha. Use quando o usuário pedir "da dor à esperança", "começa impactante e acaba feliz", "vídeo com virada", "igual ao Pedrinho_esperanca", ou escolher "Da dor à esperança" no Estúdio.
---

# Da dor à esperança

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

Estilo criado a pedido do usuário em 27/10/2026: "comece muito impactante, desenvolva um pouco e acabe feliz/emocionante para a pessoa doar". O vídeo aprovado é `EDITADOS\DA DOR À ESPERANÇA\LEVA 01\Pedrinho_esperanca_v1.mp4` (41,6 s). Ele saiu sem a logo por exceção pedida pelo usuário só naquele vídeo; a skill sempre põe a logo. O plano está em `references/exemplo-plano.json` e a narração em `references/exemplo-roteiro-audio.json`. Fale com o usuário em português do Brasil.

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md`: falas reais com a fonte, ângulos já usados e regras. As transcrições prontas estão em `transcricoes\` ao lado. Ajustes pedidos no chat vão só no `plano.json` do vídeo; esta skill só muda quando o usuário pedir para salvar.

## O arco (aprovado)
| Ato | Tempo | O que tem |
|---|---|---|
| **1. Impacto** | 0-2,4 s | `cartela`: close forte da criança em **P&B** com aproximação rápida, `fx` batida de coração no 0 s. O narrador (`audio` N0, entra em `audio_inicio` 0,25 s) fala uma frase curta e as **palavras gigantes** entram no tempo da voz, em y=1350 (no peito, nunca no rosto). A última palavra vai em vermelho e maior, com `boom`. No aprovado: "Todo dia, ele sente dor." → "TODO DIA" / "ELE SENTE" / "DOR". |
| **1. Impacto** | ~2,5-8 s | `real` em P&B: a fala mais dolorida da criança, com o próprio rosto, cortes secos e zoom alternando. ("Tem noites que eu chego até a chorar por causa das feridas doloridas.") |
| **2. Desenvolve** | ~8-22 s | Em **P&B**, música tensa: `narr` com fatos reais sobre o curativo e falas `real` da mãe e da criança ("Eu faço tudo, mas a EB… é terrível"; "a gente não tem como comprar… atadura"). |
| **Virada** | ~22 s | `narr` em **cor** (`virada_bloco` aponta para ele): clarão branco + whoosh, a música tensa sai e entra a esperançosa. Frase curta de contradição ("Mas tem uma coisa que a dor nunca tirou dele."). |
| **3. Esperança** | ~25-38 s | `vo`: a fala de força da criança (só o áudio) sobre **momentos felizes** em cor (fantasia de herói, irmão no violão, foto sorrindo com a mãe). Depois o `narr` do pedido: "Com dez reais, você ajuda a dar um final feliz para essa história. Clique em Saiba mais." |
| **Tela final** | 3,6 s | `fim`: foto feliz, fundo levemente escurecido, "O FINAL FELIZ / **COMEÇA COM VOCÊ**" (a linha com `*` sai amarela) e "CLIQUE EM SAIBA MAIS ♥"; a música sobe (`vol_fim`). |

- **Legenda:** palavra por palavra, **sempre em uma linha** (a letra diminui até caber), a palavra falada em amarelo, em y=1150, e quebra sempre entre blocos. Nas cartelas e na tela final não há legenda.
- **Músicas:** `musica_tensa` até a virada (aprovado: `paulyudin-sad-sad-music`) e `musica_esperanca` depois (aprovado: `rockymetal-ambient-acoustic`). Instrumentais.

## Regras do estilo
- **Só fato real** em narração, palavras grandes e tela final. As palavras do impacto vêm de fala real ("dores do dia a dia" → "TODO DIA ELE SENTE DOR").
- Narrador Kaique (`Hmn4B9B77pf6ttydteJ8`), em 3ª pessoa. Escreva "SOS" e números por extenso.
- **Confira a narração gerada pela transcrição**: no aprovado a voz tropeçou duas vezes ("es-escrever", "dessa, dessa"). Se tropeçar, troque a palavra e gere de novo (apague `audio\N*.mp3` e `audio\raw\N*.mp3`).
- Nada de texto no rosto da criança. Nada de foto com texto gravado que a tela cheia corte (o "Pedrinho Guerreiro" da foto do Homem-Aranha saiu cortado).
- Copy nova a cada vídeo: rode `copias_usadas.py --checar` (o verificador é rígido; "Clique em Saiba mais" e expressões curtas como "todos os dias" podem repetir).

## Fluxo
Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. Scripts em `$K = "$HOME\.claude\skills\criativo-esperanca-ong\scripts"`. Crie e edite os JSON com Write/Edit ou com um script Python. Antes de usar o ElevenLabs, no mesmo comando: `$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')`.
1. **Falas:** escolha uma fala de dor (impacto), uma da mãe e uma da criança sobre o que falta (desenvolve) e uma de força (esperança). Use as transcrições prontas ou `& $PY -I "$K\transcrever.py" "<bruto>" "<plano>\tx\x.json"`. Cada corte vai do início da 1ª palavra -0,04 s ao fim da última +0,04 s, e evita vícios colados ("é", "né").
2. **Rostos:** monte a grade de cada vídeo de fala e escolha `crops` com a boca acima de y≈1000.
3. **Narração e efeitos:** copie `references/exemplo-roteiro-audio.json` para o plano, escreva N0 a N3 novos e rode `& $PY -I "$K\gerar_audio.py" "<plano>\roteiro_audio.json" "<plano>\audio"`. Os efeitos (`coracao`, `boom`, `whoosh`) podem ser copiados de outro plano.
4. **Plano:** copie `references/exemplo-plano.json` para `EDITADOS\_planos\<Criança>_esperanca_vN\plano.json`, ponha `gancho_dor.png` (um quadro forte) na pasta, troque blocos, `virada_bloco` e músicas. Ajuste os tempos das palavras da cartela pelos tempos do `audio\N0.json` (+ `audio_inicio`).
5. **Montar:** `& $PY -I "$K\montar.py" "<plano>\plano.json"`. Sai em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, 5 por LEVA, com a logo.
6. **Conferir o MP4 final:** transcreva e compare com o roteiro; folha de quadros (impacto, P&B, virada, esperança, tela final, logo aparecendo); `freezedetect`.
7. **Entregar** com `SendUserFile`. Mostre o arco em tabela e avise que você não ouve o áudio (as músicas foram escolhidas pelo nome).

## Pedido do Estúdio
Leia o JSON do pedido: os `brutos` trazem as falas, o `banco` os momentos e o b-roll, e as `observacoes` têm prioridade (inclusive o valor). Com `quantidade` maior que 1, cada vídeo tem impacto, falas, virada e final diferentes. No fim, grave com Edit `"status": "concluido"`, `"saida"` e `"saidas"`.
