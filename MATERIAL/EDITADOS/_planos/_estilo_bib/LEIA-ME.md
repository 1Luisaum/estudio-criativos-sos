# Estilo "Bibliotecas" (03/11/2026)

São 10 criativos do Pedrinho copiados de anúncios ativos de outras ONGs, achados nas bibliotecas de anúncios da Meta (Lar Mãos Amigas, Lar Mãe Ritinha, Movimento de Amor, Florisbela e Lar Leão de Judá). Os vídeos de referência estão em `EDITADOS\_referencias\bibliotecas`. Os finais entregues foram do PEB 202 ao PEB 211.

## Arquivos
- `gerar_planos.py`: escreve os 10 `plano.json` em `EDITADOS\_planos\Pedrinho_bib_<referência>_v1`. Todos os ajustes ficam aqui: tempos das falas, b-roll, textos, posição, tamanho, fonte, música e volume.
- `bib.py`: o montador. Ele lê um `plano.json`, monta o vídeo, escolhe o próximo PEB e a LEVA e aplica a marca @soshumanhelppt.
- `fontes\`: a Poppins, que vai junto porque outro PC pode não ter a fonte.

## Como usar
```
python -I gerar_planos.py
python -I bib.py "..\Pedrinho_bib_maos_amigas_coragem_v1\plano.json"
```
Use sempre o Python 3.12 do Estúdio. Cada vídeo leva uns 2 min e meio. Dá para montar dois ao mesmo tempo.

## Material usado
- Brutos: `VÍDEOS PARA EDITAR\PEDRINHO 02-11-2026`, gravados em 02/11/2026. As transcrições já estão em `~\.claude\estudio-ong\CONHECIMENTO\transcricoes\pedrinho_0211`. Os 6 vídeos sem som são de curativo e produtos.
- Banco: só os trechos usados, recortados em `banco de vídeos do pedrinho\_clipes_bib`.
- Músicas: `MÚSICAS\magnific_tristes`. São 10 faixas tristes da Magnific, uma por vídeo. O volume sai do volume medido de cada faixa (tabela `LUFS` no `gerar_planos.py`).

## Pedidos do usuário que já estão aplicados
- Música triste da Magnific em todos os vídeos.
- Copiar o estilo exato de edição de cada referência: posição, tamanho e fonte dos textos medidos nos quadros.
- O "OBRIGADO" (PEB 209) abre com as tomadas mais fortes: as pernas enfaixadas em P&B e depois a placa "MEUS CURATIVOS ESTÃO ACABANDO".
- A referência da Florisbela usa um rosto de Jesus feito por IA. Aqui entra a fala real do Pedrinho, porque a regra é não criar cena falsa.
- O CTA é sempre "Clique em SAIBA MAIS".
- Não usar o trecho de 9 a 12 s do `pedrinho_guerreiro_1763051547…`, porque mostra ferida aberta e a Meta reprova.
- Nenhum texto em cima do rosto. Nos brutos da cadeira de rodas, o rosto vai de y 384 a 860. No sofá, vai de 190 a 576. Na cama, de 576 a 860.
