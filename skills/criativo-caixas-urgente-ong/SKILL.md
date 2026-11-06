---
name: criativo-caixas-urgente-ong
description: >-
  Estilo "Caixas – urgente" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Cópia da edição validada dos anúncios da Causas do Bem (caso Kauê) - gancho curto (3-4 s) com narrador brasileiro (ElevenLabs, Kaique) em off sobre um close REAL da criança e a faixa "URGENTE!!" com caixa branca ("CASO DO <CRIANÇA>, ... MOBILIZA PEDIDO DE AJUDA NAS REDES"); depois o mesmo corpo do estilo caixas (voz real da criança sobre b-roll curto, take de 3-5 s dela falando, caixa parada no alto e caixa "R$10,00" embaixo, sem legenda, sem P&B). Nunca usa apresentadora de IA nem logo de jornal. Use quando o usuário pedir "gancho urgente com caixas", "igual ao Kauê da manchete", "caixas urgente", "igual ao Pedrinho_vsl_voz_v8", ou escolher "Caixas: urgente" no Estúdio. Para o pedido de tempo use criativo-caixas-pedido-ong; para aspas, criativo-caixas-aspas-ong.
---

# Caixas – urgente

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md`. **Não altere esta skill durante a conversa:** ajustes vão só no `plano.json`; a skill muda só quando o usuário pedir para salvar.

Criada a pedido do usuário em 26/10/2026. O exemplo aprovado é `Pedrinho_vsl_voz_v8` (30 s). O plano está em `references/exemplo-plano.json`.

**O corpo, as cores, as regras e o fluxo são os mesmos de `criativo-caixas-pedido-ong`. Leia o SKILL.md dela.** Aqui está só o que muda.

## O gancho (referência 3 da Causas do Bem)
A referência abre com uma **apresentadora de telejornal feita com IA**, o logo "JORNAL SP" e a faixa "URGENTE!! CASO DE KAUÊ, 14 ANOS, MOBILIZA PEDIDO DE AJUDA NAS REDES". **Isso nós não copiamos:** passar o anúncio por reportagem de TV engana o doador e a Meta reprova. O usuário aprovou (26/10/2026) a versão honesta:
- **Imagem:** o close real mais forte da criança, em cor (no exemplo, o quadro de 241 s do "Um Vídeo Novo pra campanha", salvo como `gancho_dor.png` na pasta do plano). Foto parada pede `"zoom": 0.14`, senão treme.
- **Voz:** o narrador **Kaique** (`Hmn4B9B77pf6ttydteJ8`), em terceira pessoa, com **uma frase de 3 a 4 s**. Gancho longo (9 s) foi reprovado como "muito longo". No exemplo: "Os cuidados do Pedrinho passam de quarenta mil reais por mês." (fato dos Roteiros 2, 3, 4 e 7). Números vão por extenso.
- **Faixa** (`urgente_ref`, y≈1300): etiqueta vermelha "URGENTE!!" e caixa branca com texto preto, alinhadas à esquerda. Formato: "CASO DO <CRIANÇA>, COM PELE DE BORBOLETA, / MOBILIZA PEDIDO DE AJUDA NAS REDES". Não invente idade.
- Sem caixas (`sem_caixas: true`) e sem legenda.

## Como a narração entra no plano
```json
"narracao": {"N1": "Os cuidados do Pedrinho passam de quarenta mil reais por mês."},
"voz": {"voice_id": "Hmn4B9B77pf6ttydteJ8"},
"frases": [{"nome": "h1", "narracao": "N1", "foto": "<plano>/gancho_dor.png", "zoom": 0.14,
            "sem_caixas": true, "urgente_ref": ["CASO DO PEDRINHO, COM PELE DE BORBOLETA,", "MOBILIZA PEDIDO DE AJUDA NAS REDES"]}, ...]
```
O `caixas.py` gera a fala no ElevenLabs se faltar e tira os respiros. A crua fica em `audio\raw`; para regravar, apague `audio\N1.mp3` e `audio\raw\N1.mp3`. Carregue a chave do Windows no mesmo comando: `$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')`. Escreva "SOS Human Help" e a voz fala "ésse ô ésse".

## Onde salva
`& $PY -I "$HOME\.claude\skills\criativo-caixas-urgente-ong\scripts\caixas.py" "<plano>\plano.json"` salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4` (5 por LEVA). Nome do plano: `<Criança>_caixas_urgente_vN`.
