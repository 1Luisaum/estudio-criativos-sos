# Estilo "Lista narrada": referências e especificação

## De onde veio (Biblioteca de Anúncios, 26/10/2026)
O usuário achou feia a 1ª versão (papel, polaroid, faixa desenhada) e pediu para modelar o design em criativos de doação **escalados**. O que mais escalava naquele dia, todos com vídeo cru em tela cheia e texto nativo de TikTok:

| Anunciante | Cópias | O que modelamos |
|---|---|---|
| Florisbela Casa de Repouso | 96 | frase fixa em caixa amarela durante todo o b-roll, pedindo um valor |
| Ampara Brasil | 57 | vídeo cru sem filtro + **etiqueta branca** de valor embaixo |
| Lar de Idosos Leão de Judá | 40 | caixa amarela com texto preto, 2 a 3 linhas |
| UniAngola | 22 | legenda curta palavra por palavra, b-roll em tela cheia |
| Movimento Paz | 16 | legenda branca com contorno e palavra destacada em amarelo |

Conclusão: **nada de moldura, papel, polaroid, filtro ou "design montado"**. O que funciona é parecer um vídeo postado do celular.

## Especificação visual (aprovada em Pedrinho_lista_v2)
- **Quadro:** 1080x1920, 30 fps, vídeo em tela cheia (cobre e corta), aproximação lenta de 3% por cena, sem filtro de cor.
- **Chamada fixa:** caixa amarela `#FFD600`, texto preto Segoe UI Bold, até 60 px (diminui até a linha mais larga caber em 860 px), 2 linhas definidas no `plano.json`, emoji colorido (Segoe UI Emoji). **Sempre entre y=290 e y=1250** (zona segura) e nunca em cima de rosto.
  - Zona morta: os 14% de cima (barra do celular, nome do perfil) e os 35% de baixo (legenda do post, botões, CTA) do Reels/TikTok/Stories. O usuário exigiu a chamada fora dela.
- **Legenda:** até 3 palavras por vez, Segoe UI Black 84 px, branca com contorno preto de 9 px, palavras de `palavras_chave` em amarelo, sem ponto final. Tempo proporcional ao tamanho das palavras dentro da fala. Posição perto de y=1180, desviando de rosto.
- **Etiqueta:** pílula branca com texto preto Segoe UI Bold 54 px, perto de y=1720 (só nos blocos com `"etiqueta": true` e no final). Se não couber sem encostar em nada, ela some daquela cena.
- **Foto:** sempre em tela cheia. Foto de produto (sem rosto) passa devagar da esquerda para a direita, para aparecer inteira; foto com rosto fica parada, centralizada nos rostos.
- **Sempre tela cheia** (pedido do usuário em 26/10/2026). Nunca diminua o vídeo nem use fundo desfocado. Para encaixar a chamada, o script considera a posição horizontal dos rostos, tenta a chamada em 80% do tamanho e, se mesmo assim ela cobrir um rosto (close), a chamada some só naquela cena. Descer o vídeo cortava a boca e foi reprovado.
- **Tela final:** foto da família inteira + chamada + etiqueta "👇 Clique em SAIBA MAIS".
- **Áudio:** só narração (sem o áudio dos brutos) + piano a 12%, mix em -14 LUFS.

## Rostos
- Detector: OpenCV 4 (Haar frontal + frontal alt2 + perfil), 5 momentos por cena, só vale rosto que aparece em 2 ou mais momentos. Margem: 25% dos lados, 30% acima, 140% abaixo (queixo). A colocação considera também a posição horizontal do rosto.
- **O detector não pega rosto pequeno ao fundo nem de lado.** Por isso há `zonas_protegidas` no plano, marcadas à mão olhando a grade do quadro (cada quadrado da grade 27x48 numa miniatura 270x480 = 108x192 px reais).
- A regra do usuário é: **nenhum texto em cima do rosto do menino/da criança**. Na selfie da mãe do Pedrinho a chamada encosta na testa dela; o usuário viu e manteve (recusou a proteção extra do rosto dela em 26/10/2026). Não proteja o rosto de adultos por conta própria.

## Por que funciona
- Nativo = não parece anúncio: o espectador não pula.
- A frase fixa repete o pedido o vídeo inteiro, então quem entra no meio já sabe o que fazer.
- A lista de produtos com foto real torna a doação concreta (o dinheiro vira gaze, pomada, atadura).
- Narração em terceira pessoa contando fatos ditos pela própria família: prova sem precisar do áudio bruto.
