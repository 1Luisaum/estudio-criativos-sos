---
name: criativo-salva-vida-ong
description: >-
  Estilo "Salva vida" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Cópia da edição validada do anúncio 1473150411323796 da Ampara Brasil (9 cópias). SEM fala, só música; no alto, o vídeo todo, o valor grande "R$10,00" branco com contorno e uma faixa branca com "SALVA VIDA AJUDE O <CRIANÇA>❤️" em letra preta condensada; 6 cenas íntimas e lentas (4,5 a 6 s) em cor, que se misturam na troca. Use quando o usuário pedir "salva vida", "igual ao anúncio da Ampara", "só música com o valor no alto", "igual ao Pedrinho_salva_vida", ou escolher "Salva vida" no Estúdio.
---

# Salva vida

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

Criado a pedido do usuário em 26/10/2026, copiando a edição do anúncio validado 1473150411323796 da Ampara Brasil. O vídeo aprovado é `EDITADOS\SALVA VIDA\LEVA 01\Pedrinho_salva_vida_v1.mp4` (28,6 s; a referência tem 28,2 s). O plano dele está em `references/exemplo-plano.json`. Fale com o usuário em português do Brasil.

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md`: regras e ângulos já usados. Ajustes pedidos no chat vão só no `plano.json` do vídeo; esta skill só muda quando o usuário pedir para salvar.

## A edição (copiada da referência)
| Trecho | O que tem |
|---|---|
| Som | **Nenhuma fala.** Só música, do começo ao fim, normalizada em -14 LUFS. A referência usa um louvor cantado, que tem direito autoral: use uma trilha instrumental de `MÚSICAS`. Música cantada só se o usuário mandar uma com licença. |
| Alto da tela, o vídeo todo | `valor` grande, em Bahnschrift Bold Condensed 150, branco com contorno escuro. Embaixo, uma faixa branca arredondada com o `pedido` em preto, Bold Condensed 52, mais um emoji simples (❤️). Posição: `topo_y` 180. **Evite emoji composto** (❤️‍🩹): ele sai partido em dois. |
| Imagens | **6 cenas íntimas e lentas**, de 4,5 a 6 s, em cor: a criança deitada ou enfaixada, a mãe fazendo o curativo, os dois juntos. Elas se misturam na troca (`transicao` 0,6 s, xfade). Sem P&B, sem legenda e sem caixa. |

## Textos
- `valor`: o valor que o pedido pede, "R$10,00" por padrão. Escreva com centavos, como na referência.
- `pedido`: "SALVA VIDA AJUDE O PEDRINHO❤️" (ou "A ADRIELLY"). Curto, para caber numa faixa só.
- Nada de Pix, site ou nome de outra ONG.

## Cenas e rosto
- O texto do alto ocupa de y≈180 a y≈420. Se o rosto da criança ficar ali, use `zoom` (ex.: 1.4) com `"topo": true` e `"lado": "direita"` ou `"esquerda"`, para o corte descer e levar o rosto para baixo do texto. No aprovado, a 1ª cena (o Pedrinho deitado, `Vídeo Mostrando itens…` em 90 s) usa zoom 1.4, topo e direita.
- Banco do Pedrinho só em vídeo do Pedrinho. Nada de ferida aberta em close.
- Cena com estoque cheio de curativos contradiz um texto de "estão acabando"; neste estilo o texto não fala disso, mas evite se o usuário mudar o pedido.

## Fluxo
Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. Scripts em `$K = "$HOME\.claude\skills\criativo-salva-vida-ong\scripts"`. Crie e edite os JSON com Write/Edit ou com um script Python.
1. **Cenas:** monte uma folha do banco (`& $PY -I "$K\folhas.py" frames --at ... --out <tmp>\f.jpg "<video>"`) e escolha 6 trechos íntimos.
2. **Plano:** copie `references/exemplo-plano.json` para `EDITADOS\_planos\<Criança>_salva_vida_vN\plano.json` e troque `nome`, `valor`, `pedido` e `cenas` (`src`, `start`, `dur`, `zoom`, `topo`, `lado`). Duração ≈ soma das cenas − 0,6 s por troca (uns 28 s).
3. **Montar:** `& $PY -I "$K\montar.py" "<plano>\plano.json"`. O vídeo sai em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, 5 por LEVA.
4. **Conferir o MP4 final:**
   - folha de quadros: o texto não cobre o rosto da criança em nenhuma cena;
   - travadinha com `ffmpeg -i "<saida>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`.
5. **Entregar** com `SendUserFile`. Diga o texto e as cenas e avise que você não ouve o áudio.

## Pedido do Estúdio
Leia o JSON do pedido:
- o `banco` traz as cenas;
- os `brutos`, se houver, também podem dar cenas (sem o áudio);
- as `observacoes` têm prioridade, inclusive o valor.

Com `quantidade` maior que 1, cada vídeo tem cenas diferentes (e, se o usuário quiser, outro valor). No fim, grave com Edit `"status": "concluido"`, `"saida"` e `"saidas"`.
