# Estúdio de Criativos – SOS Human Help: tudo o que foi decidido

Este documento junta todas as decisões, regras e o histórico de criação do Estúdio (outubro de 2026). O chat completo, sem chaves, está em `conversa-original.md`, ao lado. **Leia antes de criar qualquer criativo.** Ele complementa as skills (`criativo-*-ong` e `edicao-criativo-ong`); quando houver conflito, vale a regra mais recente daqui ou da skill.

## 1. A ONG e as crianças
- **ONG:** S.O.S Human Help. Na narração, o nome se fala **"ésse ô ésse"**, nunca "sós". Na tela, escreva "SOS Human Help". Os scripts já trocam o texto na voz.
- **Pedrinho Guerreiro:** menino com epidermólise bolhosa (EB, "pele de borboleta"). Usa cadeira de rodas e tem o corpo quase todo enfaixado. A mãe faz todos os curativos.
- **Adrielly** (com **y**): também tem EB. Nunca use imagens do Pedrinho em vídeo da Adrielly; se não houver banco dela, peça o material.
- Os criativos são anúncios de doação na Meta (Instagram/Facebook). **O botão do anúncio é "Saiba mais".**

## 2. Regras do usuário (todas valem)
| Data | Regra |
|---|---|
| 25/10 | **Só fato real:** tudo o que se afirma vem da fala da criança ou da mãe nos vídeos, ou do que aparece no banco. Nunca invente número, idade, prazo ou valor. |
| 25/10 | **Narrador brasileiro**, em português, sempre na terceira pessoa. Nunca imite a voz da criança ou da mãe. |
| 25/10 | **Nada de texto em cima do rosto** da criança, nem quando ela aparece pequena ao fundo. Na fala real da mãe, o rosto dela também fica livre. |
| 25/10 | **Visual nativo de TikTok/Reels.** O primeiro design (lista em papel, polaroid, moldura, filtro) foi reprovado como "muito feio". Use vídeo cru em tela cheia e texto simples. |
| 25/10 | **Chamada/headline na zona segura** (y entre 290 e 1250 num quadro 1080x1920), com pedido de valor persuasivo que toque o coração. |
| 25/10 | **Copy totalmente nova a cada vídeo:** ângulo, gancho, manchete, frases do narrador, cartelas e tela final. Variação do anterior não serve; são criativos de teste. |
| 25/10 | **Não mostrar o nome na tela** (etiqueta "PEDRINHO" / "MÃE DO PEDRINHO") no estilo narrado. |
| 26/10 | **Sempre tela cheia.** Nunca diminuir o vídeo nem usar fundo desfocado. |
| 26/10 | **CTA "Saiba mais"**, nunca "Doar agora", "DOE AGORA" nem "Toque em Doar agora". Use `👇 Clique em SAIBA MAIS`. Se uma fala real disser "clique em Doar agora", corte esse trecho. |
| 26/10 | **Manchete da reportagem só no alto da tela**, nunca no meio. |
| 26/10 | **Gancho com a imagem mais forte** (close com lesões, curativo, corpo enfaixado), **em preto e branco**. Toda imagem muito forte vai em P&B; momentos de esperança ficam coloridos. |
| 26/10 | **Não alterar as skills durante a conversa.** Ajustes de um vídeo vão só no `plano.json` dele. As skills e o Estúdio só mudam quando o usuário pede para **salvar**. |
| 26/10 | **Vídeos prontos em `EDITADOS\<ESTILO>\LEVA NN`**, com **5 vídeos por LEVA**. Quando enche, abre a próxima (os scripts fazem isso sozinhos). |
| 26/10 | **Cortes com gancho:** sem selo no canto superior esquerdo. Depois do gancho, **faixa vermelha de doação** "APENAS R$X / PODEM MUDAR A VIDA DO / PEDRINHO GUERREIRO!", **sem risco branco por cima do texto**. Gancho, faixa e tela final ficam **exatamente no estilo das referências** do usuário: faixa vermelha de ponta a ponta com degradê, letra Impact larga em maiúsculas, branca em cima e cinza embaixo, com sombra e linhas juntas. A primeira versão, com caixa vermelha arredondada e Arial Black, foi considerada "pouco parecida". |
| 26/10 | **Lista narrada:** narrador em português (brasileiro) e **sem pausas de respiração**. |
| 26/10 | **Produtos sem zoom/panorâmica lateral** (ficava rápido demais), com mais tempo na tela. |
| 26/10 | **"Gaze" se fala "gáze"**, não "gueize". |
| 26/10 | **Nenhuma imagem deitada** (rotação de 90°) que obrigue a virar o celular. |
| 26/10 | **Tirar o respiro do narrador em todos os vídeos** com narrador. |
| 26/10 | **Chamada/headline no alto**, não no meio do vídeo. **Legenda dentro da zona segura** do Instagram. |
| 26/10 | **Sem travadinha** na imagem um ou dois takes antes da transição. |
| 26/10 | **Novo estilo Cortes com lettering:** o usuário cria os letterings (imagens prontas, ex.: "R$ 10,00 PODEM AJUDAR NO CUIDADO DO PEDRINHO") na pasta `lettings` da raiz. **Sempre um lettering só por vídeo**, parado o vídeo todo, no lugar de qualquer texto desenhado pelo Claude. Legenda do meio em Poppins Black. |
| 26/10 | **Estilo "caixas" (3 skills):** o usuário pediu para **copiar a edição validada** de três anúncios da Causas do Bem (caso Kauê) e depois esquecer as regras das skills nesses vídeos. O mesmo corpo serve para testar só o gancho. Ajustes aprovados: gancho urgente curto (3-4 s, 9 s foi "muito longo"); takes de ~2 s; **um take de 3-5 s do Pedrinho falando na câmera**; vermelho "em um ou outro vídeo". Nunca copiamos a apresentadora de IA nem o logo "JORNAL SP" da referência 3. |
| 26/10 | **"Faça exatamente igual a esse anúncio":** copie a estrutura, os tempos, as posições e o molde do texto, mas troque meta, presente, prazo, Pix e site da outra ONG por fatos reais (ou por "Clique em Saiba mais"). Música cantada da referência tem direito autoral: use trilha instrumental. Viraram as skills "Corrente do bem" e "Mãe desesperada". |
| 26/10 | O Estúdio não mostra mais "Lista narrada" nem "VSL com a voz da criança" (pedido do usuário). As skills continuam instaladas. |
| 26/10 | **Logo da SOS Human Help em todos os vídeos:** semitransparente (45%), 260 px de largura, andando devagar pela tela o vídeo inteiro, batendo nas bordas, entre y=200 e y=1500. Todos os montadores aplicam sozinhos no fim (`marca.py` + `logo_sos.png` na pasta de scripts de cada skill). **É OBRIGATÓRIA em todos os modelos e skills** (regra do usuário): não existe opção para tirar, e o montador para com erro se a logo faltar. Vídeo feito por script próprio também passa por `marca.py` antes de entregar. Não rode `marca.py` duas vezes no mesmo arquivo. |
| 29/10 | **Marca e CTA:** a logo da SOS foi trocada pelo texto **@soshumanhelppt** em todos os vídeos de todos os estilos (branco com contorno, 55% de opacidade, 405 px, andando pela tela como a logo andava; arquivo `marca_soshumanhelppt.png` ao lado de cada `marca.py`). O CTA passa a ser **"Clique em SAIBA MAIS"** (antes "Toque em SAIBA MAIS"); "Doar agora"/"Doe agora" continua proibido. Vídeos antigos ficaram como estavam. |
| 27/10 | **Pasta única de render:** todos os estilos juntos em `EDITADOS\RENDERIZADOS\LEVA NN`, 5 por LEVA, começando na `LEVA 26`; nome do arquivo `PEB <número> - <ESTILO>.mp4`, número seguido a partir do PEB 111. Não separa mais por estilo. Fica no `comum.destino()` de todas as skills; os vídeos antigos continuam nas pastas por estilo. |
| 27/10 | **Numeração por criança:** Adrielly = `AEB <n> - <ESTILO>.mp4` a partir do AEB 34, LEVAs a partir da 41 (os 30 primeiros dela viraram AEB 34-63, LEVAs 41-46). Pedrinho continua `PEB`, a partir do 111, LEVAs a partir da 26; o usuário pôs as LEVAs 26-33 dele em `RENDERIZADOS\TUDO BALBINO` e a LEVA nova dele vai para lá. O `comum.destino()` acha as LEVAs em qualquer subpasta, pela criança do plano (campo `crianca`, nome da pasta `Adrielly_...` ou o bruto), e um re-render mantém o vídeo onde ele estiver. |
| 27/10 | **Produção ao vivo no Estúdio:** o usuário acompanha em tempo real a demanda (quantos prontos, qual vídeo está sendo feito e a %). Ao começar uma demanda, grave `EDITADOS/_demanda_atual.json` (titulo, pedido, inicio, total, status, grupos) e marque `status: concluída` no fim. |

## 3. Os estilos (e o que foi aprovado)
| Estilo | Skill | Pasta | Como é |
|---|---|---|---|
| Cortes com gancho | `edicao-criativo-ong` | `CORTES COM GANCHO` | A criança falando, sem pausas nem vícios, zoom a cada corte, gancho em caixa vermelha, faixa vermelha de doação, legenda palavra por palavra, b-roll, tela final. Exemplo: `Pedrinho_5horas_v1`. |
| Narrado de impacto | `criativo-narrado-ong` | `NARRADO DE IMPACTO` | Narrador (Kaique) alternando a cada poucos segundos com falas reais. Narração em P&B até a frase de virada, depois cor. Manchete URGENTE, cartelas com número e boom, botão SAIBA MAIS. Exemplo: `Pedrinho_narrado_v1`. |
| Lista narrada | `criativo-lista-ong` | `LISTA NARRADA` | Só narração (Leonardo) + b-roll; os brutos entram sem o áudio deles. Chamada amarela no alto, legenda curta com destaque amarelo, fotos dos produtos, etiqueta de valor. Exemplo: `Pedrinho_lista_v2`. |
| Cortes com lettering | `criativo-lettering-ong` | `CORTES COM LETTERING` | Igual aos cortes (criança falando, sem pausas nem vícios, zoom a cada corte, b-roll), mas sem ganchos de texto: **um lettering da pasta `lettings`** fica parado o vídeo todo (760 px, centro em y=1290), legenda em Poppins Black em y=950 e tela final só com "CLIQUE EM SAIBA MAIS". Antes de chegar nisso, a tarja foi desenhada (retângulo vermelho chapado, depois em Futura Extra Black); o usuário trocou por imagens prontas. Exemplo: `Pedrinho_ajuda_de_verdade_v1`. |
| VSL com a voz da criança | `criativo-vsl-voz-ong` | `VSL COM VOZ DA CRIANÇA` | A narração é a própria fala do Pedrinho, cortada sem pausas; por cima, só b-roll. Exemplo: `Pedrinho_vsl_voz_v1`. |
| Reportagem | `criativo-reportagem-ong` | `REPORTAGEM` | Parece matéria de TV: repórter em off (Leonardo), sonoras da criança e da mãe com tarja de nome (GC), manchete no alto com "REPORTAGEM ESPECIAL • SOS HUMAN HELP". **Nunca imite emissora ou portal real.** Exemplo: `Pedrinho_reportagem_v1`. |
| Caixas: pedido de tempo | `criativo-caixas-pedido-ong` | `CAIXAS PEDIDO DE TEMPO` | Gancho com a criança pedindo tempo na câmera e uma frase real dela em verde com contorno; corpo com a voz dela sobre b-roll de ~2 s, take falando de 3-5 s, caixa verde (ou vermelha) parada no alto com o fato e caixa "R$10,00" embaixo; sem legenda, sem P&B, Bahnschrift Condensed. Exemplo: `Pedrinho_caixas_pedido_v1` (= `Pedrinho_vsl_voz_v6`). |
| Caixas: aspas | `criativo-caixas-aspas-ong` | `CAIXAS ASPAS` | Gancho com a mãe e o Pedrinho juntos (Roteiro 4) e a citação em faixas brancas "PARA MUITOS, … / PARA PEDRINHO, É UMA LUTA / TODOS OS DIAS."; mesmo corpo. Exemplo em vermelho: `Pedrinho_caixas_aspas_v1` (= `Pedrinho_vsl_voz_v7`). |
| Caixas: urgente | `criativo-caixas-urgente-ong` | `CAIXAS URGENTE` | Gancho de 3-4 s com o Kaique em off sobre close real e a faixa "URGENTE!!" + caixa branca; mesmo corpo. Exemplo: `Pedrinho_caixas_urgente_v1` (= `Pedrinho_vsl_voz_v8`). |
| Corrente do bem | `criativo-corrente-ong` | `CORRENTE DO BEM` | Cópia do anúncio 1444789200923601: um texto só, parado no alto (y 255), branco com contorno e trechos em amarelo ("Corrente do bem: Se você ajudar com R$10, vamo conseguir os curativos…"); voz real da criança só nos primeiros ~7 s; depois só música; b-roll em cor com duas passagens pelo preto. Exemplo: `Pedrinho_corrente_v1` (28,9 s). |
| Mãe desesperada | `criativo-mae-desesperada-ong` | `MÃE DESESPERADA` | Cópia do anúncio 1428626718623984: gancho de ~6 s com a mãe falando na selfie com o Pedrinho ao fundo ("Esse calor… estou ficando desesperada…"); voz do Pedrinho sobre b-roll de ~2,6 s ("Seja com dois ou cinco reais… meu muito obrigado") e o "que Deus abençoe" da mãe; depois só música; caixa vermelha fixa "ESSA MÃE ESTÁ DESESPERADA… / O PEDRINHO PRECISA DESSES CURATIVOS / R$5,00 SE TORNA VIDA🙏" + "👇 CLIQUE EM SAIBA MAIS". Exemplo: `Pedrinho_mae_desesperada_v1` (32,4 s). |
| Salva vida | `criativo-salva-vida-ong` | `SALVA VIDA` | Cópia do anúncio 1473150411323796 da Ampara Brasil: sem fala, só música; "R$10,00" grande branco com contorno e faixa branca "SALVA VIDA AJUDE O PEDRINHO❤️" no alto (y 180), o vídeo todo; 6 cenas íntimas e lentas (4,5-6 s) em cor, com fusão de 0,6 s. Emoji composto (❤️‍🩹) sai partido: use ❤️. Exemplo: `Pedrinho_salva_vida_v1` (28,6 s). |
| Da dor à esperança | `criativo-esperanca-ong` | `DA DOR À ESPERANÇA` | Arco de ~40 s criado em 27/10/2026: cartela P&B com coração, narrador (Kaique) e palavras gigantes no tempo da voz (a última vermelha com boom); falas reais em P&B com música tensa; virada com clarão + whoosh para cor e música esperançosa; momentos felizes, pedido de R$10 e tela final "O FINAL FELIZ COMEÇA COM VOCÊ". Legenda de uma linha. Logo obrigatória. Exemplo: `Pedrinho_esperanca_v1` (41,6 s). |
| UNICEF | `criativo-unicef-ong` | `UNICEF` | Criado em 27/10/2026. Gancho de ~8 s modelado no anúncio 1669162520799709 da UNICEF Brasil: foto de um item real de curativo (zoom linear) + Kaique "Isso pode parecer uma simples atadura. Mas para o Pedrinho… é o que protege a pele" → mãe fazendo o curativo → close "É o que alivia as dores dele."; legenda Segoe UI Black de 2 linhas em y 1190 com a palavra numa caixinha vermelha; sem lettering no gancho. Depois cortes com lettering simples; piano contínuo; logo no vídeo inteiro. Nada da marca UNICEF. Exemplo: `Pedrinho_atadura_v1` (43 s; está em `CORTES COM LETTERING\LEVA 01`, os próximos saem em `UNICEF`). |

## 4. Voz (ElevenLabs)
- A chave fica na variável de usuário `ELEVENLABS_API_KEY` do Windows. **Nunca peça, mostre, leia nem digite a chave no chat.** Cada editor usa a própria conta.
- **Plano gratuito:** a API bloqueia as vozes brasileiras da biblioteca (erro 402) e tem só 10 mil créditos por mês. Os créditos acabaram no meio de um lote de 5 vídeos; por isso o usuário trocou para uma conta paga (Creator).
- **Vozes aprovadas (conta paga):**
  - **Kaique** `Hmn4B9B77pf6ttydteJ8`: narrado;
  - **Leonardo** `4XmhZ74tBbUVCXIYNMMo`: lista e reportagem.
- Brian (`nPczCjzI2devNBz1zQrb`) e Matilda (`XrExE9yKIg1WjnnlVkGX`) eram provisórias e **não são mais usadas**.
- Para conferir os créditos sem expor a chave: `GET https://api.elevenlabs.io/v1/user/subscription` (campos `character_count` e `character_limit`).
- **Escreva números por extenso** na narração ("quarenta mil reais"); a legenda troca para algarismo.

## 5. Fatos reais disponíveis (com a fonte)
Todos foram ditos em vídeo. As transcrições estão em `transcricoes\` (tempo por palavra; `speaker_0`/`speaker_1` quando há duas pessoas).

**Pedrinho:**
- **`20260916_234157.mp4`:**
  - "Um pouco com Deus é muito";
  - "eu só tenho esses curativos aqui, que estão na minha mão";
  - "da última vez, minha mãe precisou de cinco horas pra fazer todo o meu curativo, por conta de lesões e ferimentos bem abertos, na carne viva";
  - "os meus ferimentos estão cada vez mais abertos";
  - "a cada dia aparece mais bolhas de sangue e bolhas de água pra minha mamãe romper";
  - "vamo comigo nessa batalha, entre junto nessa corrente do bem".
- **`20260916_235338.mp4`:**
  - "eu só tenho cinco dias pra conseguir pelo menos seis pessoas pra me ajudar, com pelo menos R$ 12";
  - "a noite passada eu passei ela em claro, eu vi o dia amanhecer";
  - "me ajude a passar essa noite sem dor".
- **`20260917_000819.mp4`:**
  - "É o quê, mãe? Os curativo tão acabando? Meu Deus, e agora?";
  - "a minha mãe acabou de me dar a pior notícia que eu poderia receber dessa semana";
  - o curativo protege de mosquito e de poeira;
  - "na verdade, acabou";
  - "a gente não tem como comprar nem uns dois, três pacotes de atadura";
  - "seja com dois ou cinco reais, não importa o valor".
- **`20260917_001530.mp4`:**
  - a mãe faz os curativos todos os dias, duas vezes ao dia;
  - "não é algo que compra e depois não precisa mais"; "a gente usa curativo e logo depois acaba rapidamente";
  - "já não basta as dores do dia a dia e durante a noite";
  - "os custos são muito alto, de cada atadura, de cada gazes";
  - "seja com um, dois, três, cinco reais… o que importa é ajudar nas minhas dores";
  - "seja um anjo na minha vida".
- **`roteiro 7.mp4` (bruto de 152 s):**
  - "as pessoas veem vaquinhas de quase três anos atrás e acham que eu tô bem de ajuda. Só que não é bem assim";
  - "comentam 'Deus te abençoe', 'vai dar tudo certo'… o que Jesus ensinou é ajudar ao próximo";
  - "com os meus curativos, alivia bastante as minhas dores";
  - "minha eterna gratidão".
- **`roteiro 8.mp4`:**
  - "há quase quatro anos eu fiz uma vaquinha que comprou quase um ano de curativos";
  - "esse ano… as pessoas se esqueceram de mim; até pessoas que me ajudaram sumiram";
  - calor de quase 46 graus na cidade dele, ruim pra pele;
  - "as minhas ataduras estão acabando e eu estou com muito medo";
  - as bolhas estão ficando piores;
  - "dois ou três reais, ou uma faixa, um gaze".
- **`roteiro 9.mp4`:**
  - "eu sei que não pode usar o mesmo curativo";
  - "a gente até entrou com processos contra o governo, mas demora muito";
  - "quem é EB não pode esperar. Os meus ferimentos não podem esperar";
  - "tem noites que eu chego a chorar por causa das feridas doloridas";
  - dores musculares.
- **`Roteiro_ peço perdão…`:**
  - é uma selfie da mãe; a primeira frase é dela, e depois quem fala é o Pedrinho, ao lado;
  - "se não tiver um soro fisiológico, minha mãe vai ter que usar água pra me dar banho; e a água arde muito";
  - "cada item de curativo é importante em uma troca";
  - "quatro, cinco, dez reais parece pouco, mas pra mim é uma nova esperança de um dia sem dor".
- **`Roteiro_ os meus curativos estão acabando…`:**
  - "Por favor, fica só 30 segundos";
  - "os meus curativos estão acabando e eu tô com medo";
  - "seja um anjo na minha vida".
- **`Roteiro_ Eu não aguento mais não conseguir dormir…`:** não consegue dormir de dor. A transcrição ouviu "pelomenetes" no lugar de "ferimentos".
- **Banco `Roteiro 7.mp4` (44 s):**
  - "Eu sou o Pedrinho Guerreiro e eu tenho epidermólise bolhosa";
  - "horas e horas de curativo";
  - "eu não escolhi essa batalha";
  - os cuidados passam de R$ 40 mil por mês.
  - Corte o "clique em Doar agora".

**Mãe:**
- **`Roteiro_ esse calor…`:**
  - "esse calor tá acabando com a pele do meu filho";
  - segundo curativo do dia;
  - "as coisas dele estão acabando"; precisa de atadura e pomada;
  - "quem quiser doar dois ou cinco reais vai tá ajudando demais".
  - É uma selfie: Pedrinho aparece pequeno ao fundo, à direita; proteja o rosto dele.
- **`Roteiro_ Nenhuma mãe deveria ouvir isso…`:**
  - "nenhuma mãe deveria ouvir isso: você é culpada pelo que o seu filho passa";
  - "faço tudo o que está no meu alcance, mas a EB é terrível";
  - "pela minha condição, não consigo nem o básico pra ele";
  - "você não tem obrigação, mas ajude a salvar o meu filho".
- **`Roteiro_ os curativos e cuidados do pedrinho são um absurdo de caro…`:**
  - "os curativos são absurdo de caro";
  - o Pedro recebe o LOAS, R$ 1.500: "o que eu faço com mil e quinhentos? Não consigo fazer nada";
  - "nunca pensei que fosse precisar vir pedir ajuda".
  - **Atenção:** o rosto dela fica baixo no quadro; enquadre para a boca ficar acima da legenda. A transcrição escreveu "luvas" no lugar de "LOAS".
- **Banco `Roteiro 2/3/4.mp4`:**
  - "por trás da internet existe meu filho de verdade";
  - "os curativos são de verdade";
  - 4 a 5 horas de curativo por dia;
  - "24 horas, todos os meses";
  - "pra vocês ele é o Pedrinho Guerreiro; pra ela, eu sou só o filho dela";
  - "essa luta ficou cara demais pra nossa família".
  - Nos Roteiros 3 e 4 falam duas pessoas: `speaker_0` é a mãe e `speaker_1` é o Pedrinho.
- **`Um Vídeo Novo pra campanha 💚.mp4`** (355 s):
  - Pedrinho conta a noite em que a casca da ferida grudou na almofada do Homem-Aranha;
  - fala dos "anjos da SOS Human Help";
  - fala de suplemento e alimentação.
  - Tem muita ferida aberta: evite usar a imagem.

**Banco de b-roll:**
- **Vídeos:**
  - curativo sendo feito: `Vídeo Mostrando itens de curativos…`, de ~140 s em diante;
  - evento, Pedrinho na cadeira: `20241110_104724`;
  - irmão tocando violão: `20260410_210553`;
  - mãe e Pedrinho na cama: `20260824_182501`;
  - mãe e Pedrinho no sofá: `VID-20260702-WA0016`.
- **Fotos dos produtos:** crepe bandagem, GAZE, Pomada, soro fisiológico, esparadrapo impermeável, OLeo de girassol, Cubitan, Curativos 2 x ao Dia.
- **Fotos de esperança:**
  - Homem-Aranha: `20221127_220927`;
  - Capitão América: `20241107_202353`;
  - heróis no evento: `20241109_123330`;
  - Ana e Pedro: `20250401_204159` e `Ana e Pedro sorrindo.png`.
- **Algumas fotos .jpg vêm deitadas** pela rotação da câmera. Os scripts endireitam, mas confira na folha.
- **Não use foto de ferida aberta** (costas, pernas em carne viva): a Meta reprova.

## 6. O que já foi feito (não repita ângulo, gancho nem frase)
| Estilo | Vídeos e ângulos |
|---|---|
| Narrado | v1 horas de curativo; calor; "é de verdade"; acabou ("Os curativos acabaram"); noite em claro; "culpada?"; esquecido; não pode esperar; oração ("Deus te abençoe"); alívio |
| Reportagem | v1 apresentação; v2 noite sem dormir; v3 curativos no fim; v4 cinco horas; v5 calor (R$ 5); v6 fé; v7 esquecido; v8 Justiça demora; v9 mãe e R$ 1.500; v10 sem soro, o banho arde |
| Lista | v1 calor de 46 °C; v2 lista de compras; v3 itens de um banho; v4 noite em claro; v5 R$ 1.500 não dão conta |
| VSL | v1 voz do Pedrinho (base); v2 acabou; v3 6 pessoas em 5 dias; v4 esquecido; v5 não pode esperar |
| Cortes | 5horas; curativos_acabando; noite; espera; esquecido |
| Cortes com lettering | ajuda_de_verdade_v1 (roteiro 7: "acham que eu tô bem de ajuda… não é bem assim"; lettering R$ 10 "cuidado"); atadura_v1 (27/10: gancho de 8 s modelado no anúncio 1669162520799709 da UNICEF, narrador "Isso pode parecer uma simples atadura… é o que protege a pele… alivia as dores dele" sobre foto do crepe → mãe enfaixando → close; cortes do 20260917_001530: mãe faz 2x ao dia, curativo acaba rápido, custo de cada atadura e gaze, "seja um anjo"; lettering R$ 5 "alívio") |
| Caixas (3 ganchos, mesmo corpo) | pedido_v1 ("Por favor, fica só 30 segundos"), aspas_v1 (Roteiro 4, "curativo é simples… é uma luta"), urgente_v1 ("cuidados passam de quarenta mil reais por mês"); corpo: Roteiro 7 + curativos acabando + "quatro, cinco, dez reais" + "seja um anjo" |
| Corrente do bem | corrente_v1 (falas: "os meus curativos estão acabando e eu tô com medo" + "me ajude a passar essa noite sem dor") |
| Mãe desesperada | mae_desesperada_v1 (mãe: calor + "desesperada"; Pedrinho: "dois ou cinco reais… meu muito obrigado") |
| Salva vida | salva_vida_v1 (6 cenas íntimas, "SALVA VIDA AJUDE O PEDRINHO❤️", R$10,00) |
| Da dor à esperança | esperanca_v1 ("Todo dia, ele sente dor." → TODO DIA / ELE SENTE / DOR; noites chorando; mãe "a EB é terrível"; virada "Mas tem uma coisa que a dor nunca tirou dele."; Roteiro 7 de força; "dar um final feliz para essa história"; fim "O FINAL FELIZ COMEÇA COM VOCÊ"). Saiu sem logo por exceção pedida só nele. |

Antes de escrever uma copy nova, leia os `plano.json` em `EDITADOS\_planos\` e, no narrado, rode `copias_usadas.py`. Esse verificador é rígido: ele marca como repetição trechos obrigatórios ("Clique em Saiba mais", "do Pedrinho"); isso pode ser ignorado.

## 7. Como trabalhar
1. O editor monta o pedido no **Estúdio** (atalho "Estudio de Criativos") e cola no Claude a mensagem "Executa o pedido do Estúdio…".
2. Leia o JSON do pedido. Ele traz `raiz`, `brutos`, `banco`, `musica`, `observacoes` e `quantidade`.
3. Transcreva os brutos novos com `transcrever.py … --diarize` e liste os fatos com a fonte.
4. Escreva os planos: um por vídeo, todos diferentes entre si.
5. Monte com o script da skill. Ele escolhe sozinho a LEVA e grava o caminho no plano.
6. **Confira antes de entregar:**
   - folha de quadros: rosto livre, chamada no alto, legenda dentro da zona segura, nada deitado;
   - transcrição do vídeo final contra a legenda;
   - `freezedetect` para a travadinha.
7. Atualize o pedido (`status`, `saida`, `saidas`) e entregue, dizendo o que não foi conferido (você não ouve o áudio).
- Para fazer vários vídeos, rode em segundo plano, um por vez, e confira no fim.

### 7.1 Lote rápido (desde 27/10/2026, depois do lote de 30)
O lote de 30 levou ~4h10 e ~44 mil tokens por vídeo. O tempo foi embora em remontagens (texto em cima de rosto descoberto só depois de montar), em cada frente lendo tudo do zero e mandando ~118 imagens para análise, e na montagem no processador. O processo agora é:
1. **Registre a demanda** em `EDITADOS\_demanda_atual.json` (a aba "Produção ao vivo" do Estúdio mostra tudo).
2. **Planos:** o agente `roteirista-ong` (ou você) escreve todos os planos de uma vez, consultando `~/.claude/estudio-ong/ferramentas/biblioteca.py` (falas reais com bruto, tempo e uso; `buscar`, `livres`) e `catalogo.py livres --zona Y0-Y1` (fotos e trechos com o rosto fora das faixas de texto do estilo). Não leia transcrições nem planos inteiros.
3. **Montagem:** `fila.py <pastas dos planos> --paralelo 2`. Sem IA. Usa a placa de vídeo (NVENC, ~4x mais rápido; volta ao x264 sem NVIDIA ou com `ESTUDIO_CPU=1`) e confere cada MP4 com `conferir_auto.py` (duração, travadinha, buracos no áudio, marca da logo gravada no arquivo, rosto x faixas de texto). Resumo em `EDITADOS\_planos\_fila\resumo_*.json`.
4. **Revisão:** só os vídeos com aviso, pelo agente `revisor-ong`, olhando só a folha de suspeitos. Ajuste no plano e remonte o mesmo plano (mesmo PEB).
5. Atualize a biblioteca (`biblioteca.py atualizar`) e, se entrar material novo no banco, o catálogo (`catalogo.py atualizar`).
- O detector de rostos (OpenCV alt2) acha a maioria, mas não todos: um rosto muito de lado pode passar. O aviso é "olhe aqui", não garantia.
- A transcrição continua no ElevenLabs (decisão do usuário, 27/10/2026).
- Teste em 27/10: os 3 UNICEF (PEB 125, 135 e 140) remontados pela fila em 8 min 41 s, 2 por vez, com o catálogo rodando junto.

### 7.2 Correção rápida (27/10/2026)
- **Pré-voo** (`prevoo.py`, roda sozinho na `fila.py` antes de montar): rosto de foto ou b-roll na faixa de texto do estilo (pelo catálogo), arquivo que não existe, `.jpg` na Mãe desesperada, música faltando, narração não gerada. Plano com erro ou aviso **não é montado**; o resumo traz até 3 fotos sugeridas. Aviso conferido que não é real: `fila.py ... --ignorar-prevoo`.
- **Logo sem codificação extra:** os montadores fazem a passada final rápida e quase sem perda (`comum.enc_antes_da_logo()`), e só o `marca.py` codifica com qualidade (`enc_final()`). Qualidade igual (SSIM 0,990 contra o vídeo entregue).
- **Só refaz o que mudou:** nos Cortes com gancho, Cortes com lettering e UNICEF, cada parte (corte, b-roll, tela final, gancho do UNICEF) guarda uma impressão digital (`comum.ffmpeg_cache`, arquivo `.chave` ao lado). Os outros estilos ainda refazem tudo, mas já com a passada rápida.
- **Áudio:** a fila grava `audio_mudou` no resumo; se for `false`, não transcreva de novo na conferência.
- **Revisor:** o agente `revisor-ong` aplica receitas prontas por tipo de aviso e remonta todos os corrigidos numa fila só.
- Medido no UNICEF da pomada: montagem do zero **88 s** (antes 171-257 s), correção da tela final **25 s**, remontagem sem mudança **22 s**.
- A fila escolhe o montador pelo nome da pasta do plano (`Pedrinho_<estilo>_…`) e, no UNICEF e no lettering, também pelo conteúdo; mantenha o estilo no nome da pasta.

### 7.3 Estilo "Bibliotecas" (03/11/2026)
- O usuário mandou um Google Doc com 8 bibliotecas de anúncios da Meta de outras ONGs e pediu 10 criativos modelados para os brutos do Pedrinho gravados em 02/11/2026. Ampara e Pedro Lima estavam sem anúncio ativo. Saíram o PEB 202 ao 211.
- Montador e planos: `EDITADOS\_planos\_estilo_bib` (`gerar_planos.py`, `bib.py`, `LEIA-ME.md`). Referências: `EDITADOS\_referenciasibliotecas`.
- Falas reais novas (transcrições em `transcricoes\pedrinho_0211`): "Eu deito pra dormir e meu corpo todo dói"; "minha pele é toda cheia de feridas"; "Cinco reais pode parecer pouco pra você, mas pra mim é sempre mais um dia sem dor e mais um dia de vida"; "o meu tratamento é caro, mas é ele que faz amenizar todas as minhas dores". Placas: "MEUS CURATIVOS ESTÃO ACABANDO", "UMA CAIXA DE CURATIVOS CUSTA R$1.500", "AJUDA NO MEU TRATAMENTO", e os pedidos de "fica 30 segundos nesse vídeo".
- Pedidos do usuário ao ver a primeira versão: música triste da Magnific em todos; replicar o estilo exato de cada referência (posição, tamanho e fonte dos textos); o PEB 209 abrir com tomadas fortes.
- No `lv_0_20261102155438`, ele diz "aumento das queimadas" entre 18,4 e 23,7 s. Esse trecho ficou de fora.

- 2ª demanda (03/11/2026, PEB 212 a 225): outro Doc com 14 anúncios em LEVA 01, 02 e 03, um de cada, **com a música do próprio anúncio**. Quando o anúncio tem fala, a música foi separada da voz com Demucs. A LEVA 02 tem narração do Leonardo e imagens simbólicas de IA (leão, Jesus e Bíblia). O homem falando no carro virou a Bíblia, porque a regra é não criar pessoa com IA.
- **Skill `criativo-bibliotecas-ong`** (03/11/2026): reúne os 24 modelos (`modelos/peb2xx_*.json`), o montador e o catálogo (`references/modelos.md`). As músicas para reutilizar ficam em `MÚSICAS\ANÚNCIOS QUE DERAM CERTO` e `MÚSICAS\magnific_tristes`, cada pasta com um `musicas.json` (anúncio de origem, clima, volume).

## 8. Problemas já resolvidos (não desfaça)
- **OpenCV 4** (`opencv-python-headless<5`): o 5 não tem o detector de rosto. Não instale `mediapipe`, que troca para o 5.
- **Caminhos com acento ("EDIÇÃO"):** o `cv2.imread` não abre, use `imdecode`. No PowerShell 5, caminhos com acento escritos direto no comando se corrompem: ache a pasta com `Get-ChildItem … -like 'EDI*CLAUDE'`. Crie e edite JSON com Write/Edit, nunca com `Set-Content`.
- **Python sempre com `-I`.** Os scripts põem a própria pasta no `sys.path`.
- **PowerShell em português usa vírgula decimal:** ao montar listas de tempos (`--at 1.5,2.5`), formate com `InvariantCulture`.
- **Caminho longo demais** (mais de 260 caracteres) quebra cópias na pasta temporária. Use pastas curtas.
- **Brutos renomeados:** o usuário renomeou vários brutos (ganharam "_" no fim). Plano antigo que não acha o bruto: procure pelo começo do nome.
- **Não abra o Estúdio de dentro da pasta do pacote** (`PARA O NOVO EDITOR`). Ele grava a pasta errada e cria `EDITADOS` lá dentro. Use o Estúdio da pasta do material.
- **Créditos do ElevenLabs:** gere a narração antes de renderizar e confira os créditos quando for fazer lotes.
- **Conferidor do narrado** (`conferir.py`): passe o caminho do MP4 exatamente como o script imprimiu, sem juntar espaços.

- **Corrigido em 27/10/2026 (nas skills):** Corrente do bem: com uma foto no meio das cenas, o texto do alto sumia até o fim (as cenas eram coladas com "-c copy"); agora junta recodificando e o texto vale em todos os quadros. Mãe desesperada: foto .jpg cortava o vídeo (formato de cor yuvj420p + colagem "-c copy"); agora converte e recodifica. Narrado: um "until" além do fim do bloco derrubava a montagem; agora é limitado ao bloco.
