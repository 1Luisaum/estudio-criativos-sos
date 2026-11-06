---
name: criativo-corrente-ong
description: >-
  Estilo "Corrente do bem" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Cópia da edição validada do anúncio 1444789200923601 da Causas do Bem (Kauê). Um texto só, parado no alto o vídeo todo, branco com contorno fino e trechos em amarelo ("Corrente do bem: Se você ajudar com R$10, vamo conseguir…"), sem caixa e sem legenda; a voz real da criança só nos primeiros 6-9 s; depois só música; b-roll em tela cheia com duas passagens rápidas pelo preto e um fim de cuidado e carinho. Use quando o usuário pedir "corrente do bem", "igual ao anúncio do texto amarelo", "igual ao Pedrinho_corrente", ou escolher "Corrente do bem" no Estúdio.
---

# Corrente do bem

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

Criado a pedido do usuário em 26/10/2026, copiando a edição do anúncio validado 1444789200923601 da Causas do Bem. O vídeo aprovado é `EDITADOS\CORRENTE DO BEM\LEVA 01\Pedrinho_corrente_v1.mp4` (28,9 s, o mesmo tempo da referência). O plano dele está em `references/exemplo-plano.json`. Fale com o usuário em português do Brasil.

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md`: falas reais com a fonte, ângulos já usados e regras. As transcrições prontas estão em `transcricoes\` ao lado. Ajustes pedidos no chat vão só no `plano.json` do vídeo; esta skill só muda quando o usuário pedir para salvar.

## A edição (copiada da referência)
| Trecho | O que tem |
|---|---|
| O vídeo todo | **Um texto só**, parado no alto (`texto_y` 255): Segoe UI Semibold 50, branco com contorno preto fino e sombra leve, centralizado, em 4 linhas. Os trechos do pedido ficam em **amarelo** (`["texto", "y"]`). Não há caixa nem legenda. |
| 0 a ~7 s | A **voz real da criança**, com falas curtas coladas (`falas`), por cima do b-roll. A boca não aparece falando. |
| ~7 s até o fim | **Só música**, mais alta (`musica_depois` 0,45 contra 0,12 sob a voz). |
| Imagens | b-roll em tela cheia, de 3,5 a 5 s por cena, **em cor**. Duas passagens rápidas pelo preto (`fade_out` numa cena e `fade_in` na seguinte, 0,3 s). Fecha com cuidado e carinho (no Kauê, a mãe carrega no colo; no Pedrinho, a foto sorrindo com a mãe). |

## O texto (mesmo molde, só fato real)
- A referência diz "Corrente do bem: **Se 10 mil** pessoas ajudarem **com R$10**, vamo conseguir dar uma máquina nova de presente do dia das crianças para o Kauê".
- **Não copie meta, presente nem prazo que não existem** para a criança. O aprovado ficou assim: "Corrente do bem: **Se você ajudar** **com R$10**, vamo conseguir os curativos que o Pedrinho precisa pra aliviar as dores dele". "Corrente do bem" e "aliviar as dores" são falas dele.
- O valor do texto é o que o pedido pede, R$ 10 por padrão. Para usar uma meta ("Se 10 mil pessoas…"), ela tem que ser real e dita pela ONG ou pela família.

## A voz
- Escolha 2 a 4 trechos de pedido dito pela criança, com 6 a 8 s no total. Cada trecho vai em `falas` como `{"fonte", "corte": [início, fim]}`, em segundos do bruto, com margem de uns 0,05 s.
- Para tirar uma pausa ou vício, quebre o trecho em dois.
- No aprovado: "Os meus curativos estão acabando e eu tô com medo." mais "Me ajude a passar essa noite sem dor."
- **Música:** a referência usa um louvor cantado, que tem direito autoral. Use uma trilha instrumental de `MÚSICAS`. Só use música cantada se o usuário mandar uma com licença.

## Fluxo
Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. Scripts em `$K = "$HOME\.claude\skills\criativo-corrente-ong\scripts"`. Crie e edite os JSON com Write/Edit ou com um script Python. Antes de transcrever, carregue a chave do Windows no mesmo comando: `$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')`.
1. **Falas:** use as transcrições prontas ou `& $PY -I "$K\transcrever.py" "<bruto>" "<plano>\tx\x.json"`.
2. **Plano:** copie `references/exemplo-plano.json` para `EDITADOS\_planos\<Criança>_corrente_vN\plano.json` e troque `nome`, `texto`, `falas`, `cenas` (`src`, `start`, `dur`, `fade_in`/`fade_out`) e `fatos`. A soma das durações das cenas é a duração do vídeo (uns 29 s).
3. **Montar:** `& $PY -I "$K\montar.py" "<plano>\plano.json"`. O vídeo sai em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, 5 por LEVA.
4. **Conferir o MP4 final:**
   - transcreva e compare com as falas;
   - folha com `& $PY -I "$K\folhas.py" timeline --every 2 --out <tmp>\f.jpg "<saida>"`. O texto do alto não pode cair no rosto da criança: se cair, troque a cena;
   - travadinha: `ffmpeg -i "<saida>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`.
5. **Entregar** com `SendUserFile`. Diga o texto, as falas e as cenas e avise que você não ouve o áudio.

## Regras que valem aqui
- Só fato real, dito pela família ou mostrado no banco.
- Banco do Pedrinho só em vídeo do Pedrinho.
- Nada de marca, logo ou chave Pix de outra ONG.
- O botão do anúncio é "Saiba mais".

## Pedido do Estúdio
Leia o JSON do pedido:
- os `brutos` são as fontes da voz;
- o `banco` é o b-roll;
- as `observacoes` têm prioridade, inclusive o valor.

Com `quantidade` maior que 1, cada vídeo tem texto, falas e cenas diferentes. No fim, grave com Edit `"status": "concluido"`, `"saida"` e `"saidas"`.
