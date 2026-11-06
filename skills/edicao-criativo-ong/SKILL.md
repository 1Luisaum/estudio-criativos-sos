---
name: edicao-criativo-ong
description: >-
  Modelo de edição aprovado para os criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa / pele de borboleta). Corta pausas e vícios de fala ("é", "aaa", gaguejadas), muda o zoom a cada corte, coloca gancho em faixa vermelha estilo anúncio (degradê, letra Impact branca com sombra), faixa vermelha de doação ("APENAS R$ X / PODEM MUDAR A VIDA DO / PEDRINHO GUERREIRO!") depois do gancho, legenda palavra por palavra com destaque vermelho, b-roll do banco, sem selo no canto, piano e tela final "Clique em Saiba mais" (nunca "doe agora"), tudo com FFmpeg. Use sempre que o usuário pedir para editar, cortar, montar, legendar ou "aplicar o modelo" em um vídeo bruto (pasta VÍDEOS PARA EDITAR), fazer um criativo, anúncio ou vídeo de doação, criar outra versão ou outro gancho de um criativo, ou ajustar um vídeo já editado (pasta EDITADOS). Use mesmo que ele não cite a skill, o Pedrinho ou a ONG.
---

# Edição de criativo de doação: modelo aprovado

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Não altere esta skill durante a conversa.** Ajustes pedidos no chat vão só no `plano.json` daquele vídeo (em `EDITADOS\_planos\<nome>\`). Esta skill e o Estúdio de Criativos só mudam quando o usuário pedir explicitamente para **salvar** (regra do usuário, 26/10/2026). Quando ele pedir, leve para cá tudo o que foi aprovado e diga o que foi salvo.

> **Antes de criar, leia** $HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md: regras do usuário com data, vozes, falas reais com a fonte, ângulos já usados e problemas já resolvidos. As transcrições prontas dos brutos estão em 	ranscricoes\ ao lado.

O usuário aprovou este modelo em 25/10/2026 ("ficou perfeito!") no vídeo `EDITADOS/Pedrinho_5horas_v1.mp4` e pediu que ele seja aplicado sempre que pedir uma edição. Siga o modelo, a não ser que o usuário peça outra coisa. O plano completo desse vídeo, que é o exemplo concreto de tudo o que vem abaixo, está em `EDITADOS/_planos/Pedrinho_5horas_v1/plano.json` (cópia em `references/exemplo-pedrinho-5horas.json`).

Fale com o usuário em português do Brasil.

## Visual aprovado em 26/10/2026 (salvo a pedido do usuário)
- **Sem selo no canto superior esquerdo.** O `badge` agora é desligado por padrão; não ponha "DOE AGORA" nem "SAIBA MAIS" ali.
- **Gancho, faixa de doação e tela final no estilo "faixa de anúncio"** (cópia das referências que o usuário mandou, aprovado em 26/10/2026):
  - a faixa vermelha vai de ponta a ponta da tela, com degradê: vermelho médio no topo, vivo logo abaixo e escuro embaixo;
  - a letra é Impact, um pouco alargada, toda em maiúsculas, com as linhas bem juntas;
  - o texto é branco na metade de cima e cinza-claro na de baixo, com sombra escura para baixo e para a direita;
  - **não há caixa arredondada, amarelo nem risco por cima do texto**;
  - a linha mais longa ocupa cerca de 960 px, porque o script ajusta o tamanho sozinho.

  Tudo isso sai da função `faixa()` do `build.py`.
- **Faixa de doação depois do gancho**, do fim do gancho até a tela final, em y≈1300, abaixo da legenda. Campo `chamada` no plano. Os números dão só a proporção entre as linhas:
  ```json
  "chamada": {"linhas": [["APENAS R$5", 124], ["PODEM MUDAR A VIDA DO", 64], ["PEDRINHO GUERREIRO!", 84]], "y": 1300}
  ```
  Escreva "R$5", sem espaço, como na referência. O valor tem que ser um que alguém real disse: R$12 no "noite", R$3 no "esquecido"; sem valor no bruto, use R$5, que é o que a mãe diz.
- **Tela final:** `"cta": "CLIQUE EM SAIBA MAIS"`.
- Exemplos aprovados: `EDITADOS\CORTES COM GANCHO\LEVA 01\` (Pedrinho_5horas_v1, curativos_acabando_v1, noite_v1, espera_v1, esquecido_v1).

## Onde fica cada coisa

Base (abaixo, RAIZ): a pasta que tem `EDITADOS` e `ESTUDIO`. Ela muda de computador para computador: está no campo `raiz` do pedido e em `$HOME\.claude\estudio-ong.json` (o Estúdio grava ao abrir). Dentro dela, os nomes padrão são `VÍDEOS PARA EDITAR` (brutos), `banco de vídeos do <criança>` (b-roll e fotos), `MÚSICAS` e `EDITADOS`; se o pedido trouxer outras pastas, use as do pedido.

| Pasta | Conteúdo |
|---|---|
| `VÍDEOS PARA EDITAR` | brutos (vertical, celular, rotação -90 nos metadados) |
| `banco de vídeos do pedrinho` | b-rolls e fotos **só do Pedrinho** (curativo sendo feito, irmão no violão, eventos, fotos dos produtos `20260825_*.jpg`) |
| `MÚSICAS` | trilhas; a aprovada é `alex-morgan-sad-piano-emotional-rain-story-575883.mp3` |
| `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4` | vídeos prontos (`<Criança>_<ideia>_vN.mp4`), 5 por LEVA (veja "Onde salvar") |
| `EDITADOS\_planos\<nome>\` | `plano.json`, `transcricao.json`, `legendas.ass`, `linha_do_tempo.json` de cada vídeo, para refazer ajustes sem transcrever de novo |

Base de conhecimento do nicho (ganchos validados, formatos, regras da Meta): `references/pacote-criativos-ong-eb.md`. Leia a seção 6 (ganchos) e a 10 (regras) antes de escolher o gancho.

## Ferramentas

- Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. O `python` do PATH é o atalho da Microsoft Store e não roda.
- Rode os scripts pelo PowerShell, com `$env:PYTHONIOENCODING='utf-8'` antes, e passe caminhos no formato Windows.
- Scripts em `$K = "$HOME\.claude\skills\edicao-criativo-ong\scripts"`.
- `transcribe.py` acha a chave do ElevenLabs sozinho (ambiente ou variáveis do usuário). O SDK `elevenlabs` instalado está quebrado; não use.

## Fluxo

### 1. Escolher o bruto
Se o usuário disse qual, use esse. Senão, prefira o que tem fato concreto e forte dito pela criança (número de horas, de curativos, valor) e mais vícios para limpar, e diga por que escolheu. Edite um vídeo por vez, a não ser que peçam vários. Crie `EDITADOS\_planos\<nome>\`.

### 2. Transcrever
```
& $PY -I "$K\transcribe.py" "<bruto.mp4>" "<pasta do plano>\transcricao.json"
```
O Scribe mantém os vícios ("é,", "aaa", "Eee"), que é o que permite cortá-los.

### 3. Decidir os cortes
```
& $PY -I "$K\inspect_tx.py" "<pasta do plano>\transcricao.json" --words --draft
```
O `--draft` já sai sem vícios (V), falsos começos (F, "fe-"), repetições (R, "na, na") e pausas de 0,30 s ou mais. Revise como editor:
- **Corte também:** muletas no meio da frase ("pessoal", "galera", "então assim", "assim"), conectores soltos ("E" antes de pausa) e frases que só hesitam (no aprovado saiu "e eu não sei, pessoal, se é por causa do tempo ou não"). Mantenha o que dá ritmo e abre bem ("Pessoal, eu só tenho esses curativos aqui").
- **"é" sem vírgula costuma ser o verbo** ("Um pouco com Deus é muito"): fica.
- **Corte colado num vício:** confira o volume ao redor com `--env 7.0-7.4,54.5-55.1 --media "<bruto>"` e ponha o corte no vale (valores ~45+ = silêncio, ~30-40 = fala). Os tempos do Scribe erram por 50-100 ms.
- **Última palavra abafada ou ambígua:** corte. No aprovado, duas transcrições ouviram "Obrigado" e "Um abraço" no mesmo trecho; legendar o que talvez não foi dito é pior que perder a palavra.
- Alvo: 30-45 s de fala + 3,4 s de tela final.

### 4. Olhar o material gastando pouco
Uma folha de contato por grupo, nunca quadro a quadro:
```
& $PY -I "$K\sheets.py" videos --frames 16 --out <tmp>\bruto.jpg "<bruto>"
& $PY -I "$K\sheets.py" videos --out <tmp>\banco.jpg "<banco>\a.mp4" "<banco>\b.mp4" ...
& $PY -I "$K\sheets.py" timeline --every 12 --out <tmp>\b05.jpg "<b-roll longo>.mp4"
& $PY -I "$K\sheets.py" photos --out <tmp>\fotos.jpg "<banco>"
```
Para o zoom, meça onde fica o rosto no bruto (`face` = centro do rosto em pixels do quadro em pé, 1080x1920):
`ffmpeg -ss 6 -i "<bruto>" -frames:v 1 -vf "scale=540:960,drawgrid=w=54:h=96:t=1:c=yellow@0.4" <tmp>\grade.jpg` (cada quadrado = 108x192 px reais).

**Selfie em close** (rosto ocupando a metade de cima, como em `Pedrinho_curativos_acabando_v1`): o zoom padrão corta a testa e joga a boca para baixo da legenda (y=1010). Use zooms leves com `center`, calculados para a boca ficar em torno de y=820 na saída (boca em y≈740 no bruto: Z2 1,2x, Z3 1,35x, ZF 1,5x, todos com `"center": [x_rosto, 845]`). Sempre confira na folha de quadros se a legenda não cobre a boca.

### 5. Escrever o `plano.json`
Campos e padrões em `references/plano.md`. O que fez o modelo funcionar, e por quê:
- **Gancho (0-5,3 s), caixa vermelha no terço inferior** (era rosa; mudou em 26/10/2026). Logo depois dele entra a faixa de doação (`chamada`). Frase 1 (0-1,9 s) = pedido de tempo ("ME DÁ 30 SEGUNDOS", formato do criativo mais escalado de EB e do cartaz que já venceu na página). Frase 2 (1,9-5,3 s) = o motivo com um **fato real dito no vídeo** e o número em amarelo (`*5 HORAS*`). Escolha o formato na seção 6 do pacote; nunca invente número.
- **Primeiros ~9 s com a criança na câmera**, sem b-roll: 9 de 13 vencedores abrem com a pessoa olhando para a câmera.
- **Zoom muda a cada corte** (Z1 aberto, Z2 médio, Z3 meio corpo, ZF rosto, mais zooms de detalhe, como mãos segurando o curativo). Nunca repita o mesmo em cortes seguidos: o pulo de enquadramento esconde o corte e dá ritmo. Use ZF nas frases de dor e Z1 para mostrar o corpo enfaixado e a cadeira.
- **B-roll casado com a fala:** curativo sendo feito em "curativo", "feridas", "bolhas"; criança sendo criança (violão, passeio) em "batalha", "corrente do bem", "vamo comigo"; montagem rápida das fotos dos produtos (~0,37 s cada) em "necessidades" e "curativos"; volte para o rosto no pedido direto ("me ajude") e no agradecimento.
- **Cuidados:**
  - nada de foto de ferida aberta, que a Meta reprova;
  - nada de b-roll que contradiga a fala (estoque cheio de curativos enquanto ele diz "só tenho esses");
  - não atribua identidade a quem aparece no b-roll: comece a cena do curativo depois de "minha mãe";
  - o banco do Pedrinho é só para vídeos do Pedrinho.
- **Legenda é só o que foi falado.** Pode acertar plural com `fix` ("necessidade" → "necessidades"), nunca acrescentar palavra. Vermelho (`red`) em curativo(s), nos números, em uma ou duas expressões de dor (CARNE VIVA, SANGUE) e no pedido (ME AJUDE).
- **Tela final de 3,4 s** sobre um b-roll da criança sendo criança. O texto da caixa sai de uma fala dela: "entre junto nessa corrente do bem" virou "SEJA A CORRENTE DO BEM DO PEDRINHO". O CTA é "CLIQUE EM SAIBA MAIS ♥".

### 6. Montar
```
& $PY -I "$K\build.py" "<pasta do plano>\plano.json"
```
A saída termina com `audio: ... buracos=nenhum` e `OK ... duracao=XX tela_final=YY`. Anote o `tela_final`.

### 7. Conferir o arquivo final
Confira o MP4 final, não um intermediário: no primeiro vídeo o A-roll estava certo e o final tinha 5,6 s de fala faltando.
```
& $PY -I "$K\verify.py" "<saida.mp4>" "<pasta do plano>\legendas.ass" --tela-final YY
& $PY -I "$K\sheets.py" frames --at 0.4,3,<um b-roll>,<fotos>,<YY+2> --out <tmp>\conf.jpg "<saida.mp4>"
```
- **`verify.py`:** retranscreve o vídeo final e compara cada palavra com a legenda na tela. Diferenças de grafia da transcrição ("vamo"/"vamos") são aceitáveis; legenda sem fala por perto, fala acabando antes da tela final ou buraco no áudio são erro e precisam ser corrigidos antes de entregar.
- **Folha de quadros:** mostra se gancho, legenda, selo e tela final estão legíveis e sem se encostar.

### 8. Entregar
Mande com `SendUserFile` (`display: render`) e escreva curto, em português:
- qual bruto foi usado e por quê;
- o que foi cortado;
- de onde veio o fato do gancho;
- quais b-rolls entraram;
- que cuidados foram tomados;
- o que você não consegue garantir: você não ouve o áudio, então peça para ele conferir o volume da música.

## Regras de 26/10/2026, 2ª rodada (salvas a pedido do usuário)
- **Sem travadinha antes da troca de cena.** O script já faz: foto entra parada com aproximação suave (sem degraus de zoom), cena de vídeo sem zoom em degraus. Confira no MP4 final: `ffmpeg -i "<saida.mp4>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`. Congelamentos de 0,2 s ou mais em sequência são erro; a cartela preta parada é normal.
- **Nenhuma imagem deitada** (rotação de 90°). O script endireita a foto que tem a rotação gravada pela câmera. Mesmo assim, olhe a folha; se aparecer deitada, troque a imagem.
- **"Gaze" se fala "gáze"**, nunca "gueize". O script troca só na voz; a legenda continua "gaze".

## Onde salvar (LEVAs)
- **Não escolha a pasta do vídeo.** O script de montagem salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, com **5 vídeos por LEVA**: quando a LEVA atual já tem 5, ele cria a próxima (`LEVA 02`, `LEVA 03`…). Re-render de um vídeo que já existe substitui o arquivo na mesma LEVA.
- O caminho final aparece na linha `saida:` e no `OK` do script e fica gravado no `plano.json` (`out`). Use esse caminho em `saida`/`saidas` do pedido.
- O nome do arquivo é o `nome` do plano. Numere as versões olhando todas as LEVAs do estilo (depois do `_v6` vem o `_v7`); nunca repita um nome, senão o vídeo antigo é substituído.
- Pastas de todos os estilos em `EDITADOS`: `CORTES COM GANCHO`, `NARRADO DE IMPACTO`, `LISTA NARRADA`, `VSL COM VOZ DA CRIANÇA`, `REPORTAGEM`.

## Pedido do Estúdio
O usuário pode pedir pelo Estúdio (pasta `ESTUDIO` dentro da RAIZ, aberto pelo `ABRIR ESTUDIO.bat`) e colar algo como "Executa o pedido do Estúdio 2026-10-25_131210 (arquivo EDITADOS\_pedidos\....json)". Nesse caso:
1. Leia o JSON do pedido. Os campos são:
   - `brutos`: o(s) bruto(s) marcado(s); neste estilo, use o primeiro;
   - `banco`: pastas de b-roll;
   - `musica`: vazio = escolha você;
   - `crianca`;
   - `observacoes`: siga o que estiver ali.
2. Rode o fluxo normal acima com esse material.
3. No fim, atualize o pedido com a ferramenta Edit: `"status": "concluido"` e `"saida": "<caminho completo do MP4>"`. A fila do Estúdio passa a mostrar o vídeo como pronto, com botão para assistir.

4. **Pedido com `quantidade` maior que 1** (opção "5 criativos de uma vez" do Estúdio): faça esse número de criativos **diferentes entre si** (gancho, copy/falas, chamada ou manchete e cenas diferentes; nunca o mesmo vídeo com outra música). Cada um tem o próprio plano e a própria saída (`..._v1`, `_v2`...). No fim, grave `"saida"` com o primeiro MP4 e `"saidas"` com a lista de todos. A fila só mostra "pronto" quando todos existem.

## Ajustes e novas versões
- **Ajuste:** edite o `plano.json` do vídeo em `EDITADOS\_planos\<nome>\` e rode o build e a conferência de novo, sem transcrever de novo. Mexa só no que foi pedido.
- **Nova versão de gancho:** copie a pasta do plano para `<nome>_v2`, troque só `hook` e o `nome` (o `out` é escolhido pelo build) e mantenha o corpo. Assim o teste mede só o gancho (seção 8 do pacote).
- **Vídeo da Adrielly:** mesmo modelo. Se não houver banco dela, peça o material antes de usar b-roll; nunca use imagens do Pedrinho.

## Armadilhas já resolvidas (não desfaça)
- **Áudio em passe separado:** o `loudnorm` no mesmo grafo do vídeo abriu um buraco no áudio. Por isso o `build.py` mixa o áudio à parte, com ganho fixo medido para -15 LUFS.
- **Um bruto, várias leituras:** cada segmento lê o bruto com `-ss` antes do `-i`. Um `split` com vários `trim` da mesma entrada guarda o vídeo inteiro na memória.
- **Intermediários em MKV com áudio PCM:** AAC por segmento causa estalos e falhas na emenda.
- **Fontes no `drawtext`:** caminho absoluto `C:\...` quebra no escape do dois-pontos. Use a fonte copiada para a pasta de trabalho e um caminho relativo (o `sheets.py` já faz isso).
- **Fontes nas legendas:** o libass usa `fontsdir=fonts` com cópias das fontes do Windows, e a Arial Black carrega via DirectWrite.
- **Rotação:** os brutos de celular vêm com rotação -90. O FFmpeg gira sozinho, e o `build.py` lê a orientação real.
- **"Pausas" falsas:** o `silencedetect` a -32 dB marca fala baixa como pausa. Confirme pelos intervalos entre palavras da transcrição (o `verify.py` já mede assim) antes de cortar.
