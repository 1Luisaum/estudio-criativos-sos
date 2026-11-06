---
name: criativo-mae-desesperada-ong
description: >-
  Estilo "Mãe desesperada" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Cópia da edição validada do anúncio 1428626718623984 da Causas do Bem (Kauê). Gancho de ~6 s com a MÃE falando para a câmera ao lado da criança, com o próprio áudio e cortes secos; depois a voz real da criança (e um "que Deus abençoe") por cima de b-roll curto (~2,6 s por cena); no fim só música; o vídeo todo com uma caixa vermelha parada de 3 linhas brancas ("ESSA MÃE ESTÁ DESESPERADA... / O <CRIANÇA> PRECISA DESSES CURATIVOS / R$5,00 SE TORNA VIDA🙏") e "👇 CLIQUE EM SAIBA MAIS" embaixo. Use quando o usuário pedir "mãe desesperada", "gancho com a mãe falando e caixa vermelha", "igual ao Pedrinho_mae_desesperada", ou escolher "Mãe desesperada" no Estúdio.
---

# Mãe desesperada

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

Criado a pedido do usuário em 26/10/2026, copiando a edição do anúncio validado 1428626718623984 da Causas do Bem. O vídeo aprovado é `EDITADOS\MÃE DESESPERADA\LEVA 01\Pedrinho_mae_desesperada_v1.mp4` (32,4 s; a referência tem 31,8 s). O plano dele está em `references/exemplo-plano.json`. Fale com o usuário em português do Brasil.

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md`: falas reais com a fonte, ângulos já usados e regras. As transcrições prontas estão em `transcricoes\` ao lado. Ajustes pedidos no chat vão só no `plano.json` do vídeo; esta skill só muda quando o usuário pedir para salvar.

## A edição (copiada da referência)
| Trecho | O que tem |
|---|---|
| 0 a ~6 s | **A mãe falando para a câmera**, com a criança junto ou ao fundo, com o próprio áudio. Cortes secos no mesmo vídeo (`gancho.cortes`), com o zoom alternando entre 1,0 e 1,15 para esconder a emenda. Na referência: "Se você é mãe, não pula esse vídeo. Eu estou desesperada pra ajudar meu filho." |
| ~6 a ~15 s | **A voz da criança por cima do b-roll** (`voz_off`): o pedido com valor ("qualquer valor… já vai tá me ajudando") e um fecho de fé ou gratidão ("Que Deus te abençoe"). |
| Até o fim | **Só música** (`musica_depois` 0,40 contra 0,10 sob a voz). |
| Imagens | b-roll curto, de **~2,6 s por cena**, em cor: a mãe cuidando, os dois juntos, um abraço ou foto de carinho no fim. |
| O vídeo todo | **Caixa vermelha parada** (`caixa_y` 1344) com 3 linhas brancas em Bahnschrift Bold Condensed e um emoji 🙏. Embaixo, a chamada branca com contorno: `"cta": "👇 CLIQUE EM SAIBA MAIS"`. |

## Os textos (mesmo molde, só fato real)
- **Caixa:** "ESSA MÃE ESTÁ DESESPERADA... / O <CRIANÇA> PRECISA DESSES CURATIVOS / R$X SE TORNA VIDA🙏".
  - "Desesperada" só se a mãe disser isso no bruto. A do Pedrinho diz "estou ficando desesperada" no `Roteiro_ esse calor…`.
  - O valor vem do que a família diz (R$ 5, porque ela fala em "dois ou cinco reais") ou do pedido.
- **A linha de baixo da referência** é uma chave Pix (`🔑 DOE@AJUDEKAUE.ORG`). **Nunca copie Pix ou site de outra ONG.** Use "👇 CLIQUE EM SAIBA MAIS", que é o botão do anúncio.

## Falas do Pedrinho usadas no aprovado
- **Gancho (mãe, `Roteiro_ esse calor…`):** [0,74-3,12] "Esse calor tá acabando com a pele do meu filho."; [8,06-9,72] "e estou ficando desesperada,"; [10,44-11,50] "porque as coisas dele"; [11,82-12,84] "estão acabando."
- **Voz por cima (Pedrinho, `20260917_000819.mp4`):** [56,04-58,30] "Seja com dois ou cinco reais,"; [58,36-59,46] "não importa o valor,"; [60,68-62,26] "já vai tá ajudando muito"; [70,14-71,80] "E meu muito obrigado."
- **Fecho (mãe, `Roteiro_ esse calor…`):** [34,60-35,64] "que Deus abençoe".

Para outra mãe ou outra criança, procure no bruto uma fala da mãe com emoção forte ("desesperada", "nenhuma mãe deveria ouvir isso…") e, da criança, um pedido com valor.

## Fluxo
Python: `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`, sempre com `-I`. Scripts em `$K = "$HOME\.claude\skills\criativo-mae-desesperada-ong\scripts"`. Crie e edite os JSON com Write/Edit ou com um script Python. Antes de transcrever, carregue a chave do Windows no mesmo comando: `$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')`.
1. **Falas:** use as transcrições prontas ou `& $PY -I "$K\transcrever.py" "<bruto>" "<plano>\tx\x.json" --diarize`. Cada corte vai do início da 1ª palavra -0,06 s ao fim da última +0,06 s.
2. **Rosto:** na selfie da mãe, confira numa grade onde fica o rosto da criança. A caixa (y 1344-1580) não pode cobrir o rosto dela. Se cobrir, mude `caixa_y` ou use outro bruto.
3. **Plano:** copie `references/exemplo-plano.json` para `EDITADOS\_planos\<Criança>_mae_desesperada_vN\plano.json` e troque `nome`, `gancho`, `voz_off`, `caixa`, `cenas` e `fatos`. O b-roll cobre do fim do gancho até o fim (uns 26 s).
4. **Montar:** `& $PY -I "$K\montar.py" "<plano>\plano.json"`. O vídeo sai em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4`, 5 por LEVA. A saída mostra o fim do gancho e o trecho da voz em off.
5. **Conferir o MP4 final:**
   - transcreva e compare com as falas;
   - folha de quadros: nada em cima do rosto da criança;
   - travadinha com `freezedetect`;
   - evite b-roll com ferida aberta.
6. **Entregar** com `SendUserFile`. Diga as falas, a caixa e as cenas e avise que você não ouve o áudio.

## Regras que valem aqui
- Só fato real.
- Banco do Pedrinho só em vídeo do Pedrinho.
- Nada de marca, logo ou Pix de outra ONG.
- Música instrumental de `MÚSICAS`; música cantada só se o usuário mandar uma com licença.

## Pedido do Estúdio
Leia o JSON do pedido:
- os `brutos` trazem o vídeo da mãe e as falas da criança;
- o `banco` é o b-roll;
- as `observacoes` têm prioridade.

Com `quantidade` maior que 1, cada vídeo tem gancho, falas e cenas diferentes. No fim, grave com Edit `"status": "concluido"`, `"saida"` e `"saidas"`.
