---
name: criativo-narrado-ong
description: >-
  Estilo "narrado" aprovado para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Narrador do ElevenLabs alternando poucos segundos com falas reais da criança e da mãe; narração em preto e branco e falas reais em cor, com virada para cor no fim; manchete vermelha de telejornal com etiqueta URGENTE; cartelas de impacto com boom; muito b-roll sincronizado com a narração; tela final com botão SAIBA MAIS. Use quando o usuário pedir um vídeo narrado, com narração do ElevenLabs, com narrador, "no estilo narrado", "igual ao Pedrinho_narrado", ou um criativo de doação com copy e narração. Não use para o modelo simples de cortes sem narrador (esse é a skill edicao-criativo-ong).
---

# Criativo narrado: narrador + falas reais + b-roll

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Não altere esta skill durante a conversa.** Ajustes pedidos no chat vão só no `plano.json` daquele vídeo (em `EDITADOS\_planos\<nome>\`). Esta skill e o Estúdio de Criativos só mudam quando o usuário pedir explicitamente para **salvar** (regra do usuário, 26/10/2026). Quando ele pedir, leve para cá tudo o que foi aprovado e diga o que foi salvo.

> **Antes de criar, leia** $HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md: regras do usuário com data, vozes, falas reais com a fonte, ângulos já usados e problemas já resolvidos. As transcrições prontas dos brutos estão em 	ranscricoes\ ao lado.

O usuário aprovou este estilo em 25/10/2026 no vídeo `EDITADOS/Pedrinho_narrado_v1.mp4` (70 s) e pediu uma skill só dele para replicar. O plano completo desse vídeo está em `EDITADOS/_planos/Pedrinho_narrado_v1/` (cópias em `references/exemplo-*.json`). É o exemplo concreto de tudo o que vem abaixo.

Fale com o usuário em português do Brasil. Este estilo é independente da skill `edicao-criativo-ong`; não misture os dois.

## A ideia do estilo (por que funciona)
- **Duas vozes alternando a cada poucos segundos.** O narrador (terceira pessoa) dá contexto e números. A criança e a mãe confirmam com a própria voz. A fala real é a prova, e a narração é o ritmo.
- **Preto e branco para o narrador, cor para as pessoas reais.** Em "Ele não." (a frase de virada) a narração também ganha cor, e o vídeo termina colorido: da dor para a esperança.
- **Impacto:** manchete de telejornal com URGENTE no primeiro quadro, cartelas pretas com o número gigante e um boom, clarão branco com whoosh em cada troca, palavra falada em amarelo.

## Pastas e ferramentas
- Base (abaixo, RAIZ): a pasta que tem `EDITADOS` e `ESTUDIO`. Ela muda de computador para computador: está no campo `raiz` do pedido e em `$HOME\.claude\estudio-ong.json` (o Estúdio grava ao abrir). Dentro dela, os nomes padrão são `VÍDEOS PARA EDITAR` (brutos), `banco de vídeos do <criança>` (b-roll e fotos), `MÚSICAS` e `EDITADOS`; se o pedido trouxer outras pastas, use as do pedido.
- Cada vídeo ganha `EDITADOS\_planos\<nome>\` com `plano.json`, `roteiro_audio.json`, `tx\` (transcrições das falas reais) e `audio\` (narração e efeitos).
- Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I` (o `python` do PATH é o atalho da Microsoft Store). Scripts em `$K = "$HOME\.claude\skills\criativo-narrado-ong\scripts"`.
- Rode pelo PowerShell com `$env:PYTHONIOENCODING='utf-8'`. **Crie e edite os JSON com a ferramenta Write/Edit, nunca com `Set-Content`**: o PowerShell 5 grava os acentos errado ("Ã‰" no lugar de "É").
- No PowerShell, `$T` e `$t` são a mesma variável. Use nomes diferentes nos laços.

## Fluxo

### 1. Levantar as falas reais
Transcreva os brutos e os vídeos do banco em que a criança ou a mãe falam (os "Roteiro N.mp4" do banco têm falas fortes):
```
& $PY -I "$K\transcrever.py" "<video>" "<pasta do plano>\tx\<nome>.json"
```
Liste as frases com fato concreto: horas de curativo, custo por mês, "estão acabando", pedidos ("seja um anjo"), frases de luta. **Só fato dito por alguém real entra na copy.** Fatos usados no aprovado: até 4 a 5 horas de curativo por dia (mãe, Roteiro 3); o último curativo durou 5 horas (Pedrinho, 20260916_234157); os cuidados passam de R$ 40 mil por mês (Roteiros 2, 3, 4 e 7); o botão do anúncio agora é "Saiba mais" (o "clique em Doar agora" do Roteiro 7 não pode mais ser usado).

### 2. Escrever uma copy TOTALMENTE NOVA
O usuário pediu (25/10/2026) que **todo vídeo novo tenha copy e narração totalmente novas**. Uma variação do anterior não serve. O motivo: são criativos de teste, e cada vídeo precisa trazer um ângulo, um gancho e frases diferentes. No 2º vídeo (Pedrinho_narrado_calor_v1) repeti narrações, cartela, tela final e abertura do 1º, e ele reclamou.

Antes de escrever, veja tudo o que já foi usado:
```
& $PY -I "$K\copias_usadas.py"
```
Depois escreva a copy seguindo `references/copy.md` (regras, menu de variação e as copys anteriores) e os formatos validados da seção 6 de `references/pacote-criativos-ong-eb.md`.

Tem que ser novo em relação a todos os vídeos anteriores:
- **ângulo central** (ex.: horas de curativo → calor → noite sem dormir → a mãe → o custo → "a primeira vez"…);
- **formato e texto da manchete**;
- **bloco de abertura** (não abra de novo com "Por favor, fica só 30 segundos");
- **todas as frases do narrador**, inclusive a lista de produtos, a frase de virada e o CTA;
- **cartelas**;
- **tela final**.

As falas reais são limitadas, então priorize as que ainda não entraram em nenhum vídeo. Repetir uma fala real só vale quando não houver alternativa, e nunca como abertura.

Narrador sempre em terceira pessoa. Nunca narre como se fosse a criança nem imite a voz dela ou da mãe.

### 3. Gerar narração e efeitos (ElevenLabs)
Escreva `roteiro_audio.json` (modelo em `references/exemplo-roteiro-audio.json`) e rode:
```
& $PY -I "$K\gerar_audio.py" "<pasta do plano>\roteiro_audio.json" "<pasta do plano>\audio"
```
Antes de gerar, confira se nada repete (o script ignora o próprio vídeo):
```
& $PY -I "$K\copias_usadas.py" --checar "<pasta do plano>\roteiro_audio.json"
```
O resultado precisa ser `copy toda nova`. Se aparecer `REPETE`, reescreva a frase. Rode de novo depois de escrever o `plano.json`, que aí ele também confere manchete, cartelas, tela final, abertura e falas reais.

Sai `N1.mp3` + `N1.json` (tempo de cada palavra) por linha, e `fx_boom.mp3` / `fx_whoosh.mp3`. Arquivo que já existe não é gerado de novo; apague o mp3 para regravar uma linha. **Nunca copie mp3 de narração de outro vídeo**; só os efeitos (`fx_*.mp3`) podem ser reaproveitados.
- **Voz:** a conta está no plano gratuito, que não libera as vozes da biblioteca pela API (erro 402) nem `mp3_44100_192` (erro 403). A aprovada é **Brian** (`nPczCjzI2devNBz1zQrb`, padrão, verificada para português). Se o usuário assinar um plano pago, a preferida é **Kaique** (`Hmn4B9B77pf6ttydteJ8`, brasileira). Troque o `voice_id`, apague os mp3 e gere de novo.
- Escreva números por extenso na narração ("quarenta mil reais"); a legenda troca para "40" com `fix`/`caption_fix`.

### 4. Escolher as imagens
Uma folha de contato por grupo, sem abrir quadro a quadro:
```
& $PY -I "$K\folhas.py" videos --out <tmp>\banco.jpg "<banco>\a.mp4" ...
& $PY -I "$K\folhas.py" timeline --every 12 --out <tmp>\b05.jpg "<b-roll longo>.mp4"
& $PY -I "$K\folhas.py" photos --out <tmp>\fotos.jpg "<banco>"
```
Para cada fala real, meça onde fica o rosto (grade: `ffmpeg -ss 3 -i "<video>" -frames:v 1 -vf "scale=360:640,drawgrid=w=36:h=64:t=1:c=yellow@0.35" grade.jpg`, cada quadrado = 108x192 px reais). Escolha zooms que deixem a boca acima de y≈1050 na saída (a legenda fica em 1150). Não há mais etiqueta de nome ("PEDRINHO" / "MÃE DO PEDRINHO") na tela: o usuário pediu para tirar em 25/10/2026.
Imagem casada com a palavra da narração:
- foto de cada produto no nome dele;
- curativo sendo feito em "tira / lava / enfaixa";
- criança sendo criança (Homem-Aranha, violão, passeio) na virada e no CTA.

Nada de ferida aberta (a Meta reprova). Nada de b-roll que contradiga a fala. Não afirme quem é a pessoa que aparece no b-roll.

### 5. Escrever o `plano.json` e montar
Campos em `references/estilo.md`. Depois:
```
& $PY -I "$K\narrado.py" "<pasta do plano>\plano.json"
```
Termina com `audio: ... buracos=nenhum` e `OK ... duracao=XX`.

### 6. Conferir o MP4 final
```
& $PY -I "$K\conferir.py" "<saida.mp4>" "<pasta do plano>\linha_do_tempo.json"
```
- **Resultado esperado:** `RESULTADO: OK`. No aprovado deu 156 palavras faladas, todas com legenda.
- **Narração:** a transcrição também mostra se o narrador ficou inteligível.
- **Quadros:** tire uma folha cobrindo cada bloco (gancho, P&B, cartelas, mãe, virada, tela final) e veja se:
  - a legenda não cobre a boca;
  - a manchete não encosta na legenda;
  - o botão "SAIBA MAIS" está centralizado. O botão do anúncio agora é **"Saiba mais"** (26/10/2026): nunca use "Doar agora" / "Toque em Doar agora" na narração, na tela final nem na legenda.

### 7. Entregar
Mande com `SendUserFile` (`display: render`). Na resposta, mostre a copy em tabela (quem fala, o texto e o formato validado de onde veio) e liste o que você não consegue garantir:
- você não ouve o áudio, então peça para ele conferir o sotaque da voz e o volume da música;
- os fatos que vieram de arquivo e não de fala, se houver.

## Regras de 26/10/2026, 2ª rodada (salvas a pedido do usuário)
- **Sem travadinha antes da troca de cena.** O script já faz: foto entra parada com aproximação suave (sem degraus de zoom), cena de vídeo sem zoom em degraus. Confira no MP4 final: `ffmpeg -i "<saida.mp4>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`. Congelamentos de 0,2 s ou mais em sequência são erro; a cartela preta parada é normal.
- **Nenhuma imagem deitada** (rotação de 90°). O script endireita a foto que tem a rotação gravada pela câmera. Mesmo assim, olhe a folha; se aparecer deitada, troque a imagem.
- **"Gaze" se fala "gáze"**, nunca "gueize". O script troca só na voz; a legenda continua "gaze".
- **Narrador sempre brasileiro e em português.** A conta agora é paga: **Kaique** (`Hmn4B9B77pf6ttydteJ8`) no `roteiro_audio.json`. Nunca use Brian nem Matilda. Se o editor estiver no plano gratuito do ElevenLabs (erro 402 na voz), avise que a voz brasileira exige plano pago. Isto vale no lugar do que a seção de voz desta skill diz sobre voz provisória.
- **Sem pausa de respiração.** O script guarda a fala crua em `audio\raw\` e usa em `audio\` a versão sem respiros e sem silêncios, com o tempo de cada palavra reajustado para a legenda continuar sincronizada. Para regravar uma fala, apague as duas.

## Onde salvar (LEVAs)
- **Não escolha a pasta do vídeo.** O script de montagem salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, com **5 vídeos por LEVA**: quando a LEVA atual já tem 5, ele cria a próxima (`LEVA 02`, `LEVA 03`…). Re-render de um vídeo que já existe substitui o arquivo na mesma LEVA.
- O caminho final aparece na linha `saida:` e no `OK` do script e fica gravado no `plano.json` (`out`). Use esse caminho em `saida`/`saidas` do pedido.
- O nome do arquivo é o `nome` do plano. Numere as versões olhando todas as LEVAs do estilo (depois do `_v6` vem o `_v7`); nunca repita um nome, senão o vídeo antigo é substituído.
- Pastas de todos os estilos em `EDITADOS`: `CORTES COM GANCHO`, `NARRADO DE IMPACTO`, `LISTA NARRADA`, `VSL COM VOZ DA CRIANÇA`, `REPORTAGEM`.

## Nome da ONG na narração
A ONG é **S.O.S Human Help**, falado "ésse ô ésse". Escreva "SOS Human Help" na narração: o script manda "Ésse Ô Ésse Human Help" para o ElevenLabs e mostra "SOS" na legenda. Narração gerada antes dessa regra (mp3 em `audio\`) fala "sós": apague o mp3 da fala que cita a ONG para gerar de novo.

## Pedido do Estúdio
O usuário pode pedir pelo Estúdio (pasta `ESTUDIO` dentro da RAIZ, aberto pelo `ABRIR ESTUDIO.bat`) e colar algo como "Executa o pedido do Estúdio 2026-10-25_131210 (arquivo EDITADOS\_pedidos\....json)". Nesse caso:
1. Leia o JSON do pedido. Os campos são:
   - `brutos`: os vídeos com falas reais que ele marcou (são as fontes da etapa 1);
   - `banco`: pastas de b-roll;
   - `musica`: vazio = use a trilha aprovada;
   - `crianca`;
   - `observacoes`: siga o que estiver ali, como um gancho específico ou trechos a evitar.
2. Rode o fluxo normal acima com esse material.
3. No fim, atualize o pedido com a ferramenta Edit: `"status": "concluido"` e `"saida": "<caminho completo do MP4>"`. A fila do Estúdio passa a mostrar o vídeo como pronto, com botão para assistir.

4. **Pedido com `quantidade` maior que 1** (opção "5 criativos de uma vez" do Estúdio): faça esse número de criativos **diferentes entre si** (gancho, copy/falas, chamada ou manchete e cenas diferentes; nunca o mesmo vídeo com outra música). Cada um tem o próprio plano e a própria saída (`..._v1`, `_v2`...). No fim, grave `"saida"` com o primeiro MP4 e `"saidas"` com a lista de todos. A fila só mostra "pronto" quando todos existem.

## Ajustes
Mexa só no que o usuário pedir. Edite o `plano.json` (ou o `roteiro_audio.json` e apague o mp3 da linha), rode o `narrado.py` e o `conferir.py` de novo. Exemplo: o pedido "headline mais chamativa" virou fonte 150 em "ATÉ *5 HORAS*", fonte 74 na 2ª linha, faixa em y=1258 e a etiqueta URGENTE. Isso hoje é o padrão em `references/estilo.md`.

## Armadilhas já resolvidas (não desfaça)
- **Áudio em passe separado:** a voz, a música e os efeitos são mixados à parte com ganho fixo medido. Filtro pesado no mesmo grafo do vídeo já abriu buraco no áudio de outro vídeo.
- **Desenhos no ASS:** use coordenada absoluta (`\an7\pos(0,0)`) e `\org` para animar. Com `\an5` e coordenada negativa, o botão saiu deslocado para a esquerda.
- **Intermediários em MKV com PCM; cada corte lê o bruto com `-ss` antes do `-i`.** Assim não há estalo nem estouro de memória.
- **Fontes:** o `narrado.py` copia Arial Black e Segoe UI Symbol para a pasta de trabalho e usa `fontsdir=fonts`.
