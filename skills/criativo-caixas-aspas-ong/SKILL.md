---
name: criativo-caixas-aspas-ong
description: >-
  Estilo "Caixas – aspas" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Cópia da edição validada dos anúncios da Causas do Bem (caso Kauê) - gancho de conversa/entrevista com a mãe e a criança juntas e uma citação em faixas brancas com aspas ("PARA MUITOS, ... / PARA <CRIANÇA>, É UMA LUTA TODOS OS DIAS."); depois o mesmo corpo do estilo caixas (voz real da criança sobre b-roll curto, take de 3-5 s dela falando, caixa parada no alto com o fato e caixa "R$10,00" embaixo, sem legenda, sem P&B). Use quando o usuário pedir "gancho com aspas", "igual ao Kauê com a entrevista", "caixas com aspas", "igual ao Pedrinho_vsl_voz_v7", ou escolher "Caixas: aspas" no Estúdio. Para o pedido de tempo use criativo-caixas-pedido-ong; para o URGENTE use criativo-caixas-urgente-ong.
---

# Caixas – aspas

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md`. **Não altere esta skill durante a conversa:** ajustes vão só no `plano.json`; a skill muda só quando o usuário pedir para salvar.

Criada a pedido do usuário em 26/10/2026. O exemplo aprovado é `Pedrinho_vsl_voz_v7` (32 s, **em vermelho**). O plano está em `references/exemplo-plano.json`.

**O corpo, as cores, as regras e o fluxo são os mesmos de `criativo-caixas-pedido-ong`. Leia o SKILL.md dela.** Aqui está só o que muda.

## O gancho (referência 2 da Causas do Bem)
Na referência, um entrevistador pergunta à criança "qual é o seu sonho?", ao lado da mãe. Não temos entrevista gravada, então o usuário escolheu (26/10/2026) **a mãe e a criança juntas falando para a câmera**. No exemplo:
- mãe: "Pra vocês, ele é o Pedrinho Guerreiro."
- Pedrinho: "E pra ela, eu sou só o filho dela."

Fonte: banco `Roteiro 4.mp4` (transcrição `roteiro4.json`: `speaker_0` é a mãe, `speaker_1` é o Pedrinho). Cada fala é uma frase com um corte só e a cena no mesmo segundo, para a boca bater.

**A citação** (`aspas_ref`, nas frases do gancho): faixas brancas por linha, texto preto condensado com espaço entre as letras, alinhadas à esquerda em x=135 e com um quadradinho de aspas na cor da caixa. Fica em y≈1215, abaixo do queixo. O formato da referência é "PARA MUITOS, / <ALGO> É NATURAL. / PARA <CRIANÇA>, É UMA LUTA / TODOS OS DIAS." No exemplo: "PARA MUITOS, / UM CURATIVO É SIMPLES. / PARA PEDRINHO, É UMA LUTA / TODOS OS DIAS." O contraste tem que ser verdade (curativo todo dia, horas de curativo).

O gancho vai sem caixas (`sem_caixas: true`) e sem legenda. Se outra criança ou outro vídeo tiver o queixo mais baixo, desça `aspas_ref_y`.

## Onde salva
`& $PY -I "$HOME\.claude\skills\criativo-caixas-aspas-ong\scripts\caixas.py" "<plano>\plano.json"` salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4` (5 por LEVA). Nome do plano: `<Criança>_caixas_aspas_vN`.

## Cor
O exemplo está em vermelho: `visual_ref.cor_caixa: [200,16,28]` e `cor_texto: [235,40,40]`. Sem esses campos, sai verde como a referência.
