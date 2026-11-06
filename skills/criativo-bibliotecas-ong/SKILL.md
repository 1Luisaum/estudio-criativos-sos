---
name: criativo-bibliotecas-ong
description: >-
  Estilo "Bibliotecas" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). São 24 modelos aprovados (PEB 202 a 225), cada um copiando a edição de um anúncio ativo de outra ONG na Biblioteca de Anúncios da Meta: Lar Mãos Amigas, Lar Mãe Ritinha, Movimento de Amor, Florisbela e Lar Leão de Judá. Cada modelo copia a posição, o tamanho e a fonte dos textos, o ritmo dos cortes e a música do anúncio (ou uma música triste da Magnific), com os brutos reais da criança. Há modelos só com música e texto fixo, modelos com a fala real e legenda, e modelos com narração e imagem simbólica de IA no gancho. Use quando o usuário pedir "igual ao anúncio da Mãos Amigas / Mãe Ritinha / Florisbela / Leão de Judá / Movimento de Amor", "modele esse anúncio da biblioteca", "igual ao PEB 2xx", "estilo bibliotecas", "esqueceram da gente", "POV: seus reais", "esse é o seu sinal", "Dai e vos será dado", "VIRALIZOU", ou mandar um link da Biblioteca de Anúncios para copiar.
---

# Bibliotecas (24 modelos de anúncios que deram certo)

> **Regras que valem sempre:** a marca **@soshumanhelppt** é obrigatória (o `bib.py` aplica sozinho com `marca.py`). O CTA é **"Clique em SAIBA MAIS"**, nunca "Doe agora" nem "Doar agora". A ONG se fala "ésse ô ésse". Só fatos reais, ditos nos brutos ou escritos nas placas. Nenhum texto em cima do rosto da criança. Nenhuma pessoa feita com IA: imagem de IA só simbólica (leão, Jesus, Bíblia), nunca imitando a criança. Imagem forte em P&B. Nada de ferida aberta.

Antes de criar, leia `~/.claude/estudio-ong/CONHECIMENTO/CONHECIMENTO.md` (§2 regras e §7.3 deste estilo).

## Arquivos
- `references/modelos.md`: o catálogo dos 24 modelos, com o exemplo (PEB), o tipo (só música, fala real ou narração), a duração, a música e o que cada um copia do anúncio.
- `modelos/<id>.json`: o plano aprovado de cada modelo. Os caminhos usam `{RAIZ}` (pasta do material) e `{SKILL}` (esta skill).
- `scripts/novo_plano.py`: copia um modelo para uma pasta nova de plano.
- `scripts/bib.py`: o montador.
- `scripts/separar_musica.py`: tira a voz de um anúncio e deixa só a música (Demucs).
- `assets/imagens`: leão, Jesus e Bíblia, gerados na Magnific.
- `assets/narracoes`: as 3 narrações do Leonardo, já sem respiro e com a transcrição.

## Músicas para reutilizar
Ficam na pasta do material e aparecem no Estúdio:
- `MÚSICAS\ANÚNCIOS QUE DERAM CERTO\`: as 14 músicas dos anúncios, com o nome "<ONG> <número> - <tema>". As que dizem "(fundo sem voz)" tiveram a fala do anúncio removida.
- `MÚSICAS\magnific_tristes\`: as 10 músicas tristes da Magnific.

Cada pasta tem um `musicas.json` com o anúncio de origem, o clima, a duração, onde a música já foi usada e o `volume` que vai no plano. Sem fala no vídeo, o volume é 1.0 nas músicas dos anúncios e `volume_so_musica` nas da Magnific. Com fala por cima, use o volume indicado (as "fundo sem voz" já vêm medidas) ou `volume_sob_fala`.

## Como fazer um vídeo novo
1. **Escolha o modelo.** Se o usuário citar um anúncio, um PEB ou uma frase, procure em `references/modelos.md`.
2. **Copie o modelo:**
   `python -I scripts/novo_plano.py <id ou número do PEB> <Criança>_bib_<tema>_v1 [--crianca Adrielly]`
3. **Troque o conteúdo no `plano.json`** e mantenha a estrutura do modelo:
   - `base`: os pedaços em sequência, no formato `{arq, ini, fim, som, pb?, zoom?, topo?, kb?}`. Com `som: true` entra a fala real (a legenda sai da transcrição do bruto). Com `som: false` o pedaço entra mudo. Imagem `.png` entra parada, e `kb: true` dá um zoom lento.
   - `broll`: `[t0, t1, arquivo, início, {pb?}]`, por cima da base. O som da base continua.
   - `textos`: `{de, ate, linhas, estilo: caixa|seco, fg, bg, size, y, alinha: centro|esq, x, pad, lh, fonte, por_linha, barra, destaque, cor_destaque, contorno, cor_contorno}`. As fontes são `bold`, `black`, `medium`, `regular` (Poppins), `impact`, `italico`, `serif`, `serif_bold` e `arial`. As cores são nomes (`branco`, `preto`, `amarelo`, `vermelho`, `verde`) ou `[R, G, B(, A)]`.
   - `legenda`: `{estilo: palavra|amarelo|pequena|unicef|nenhuma, y, size, fonte, caixa_alta, contorno, cor}`. `unicef` (padrão desde 05/11/2026) é a do estilo UNICEF: 2 linhas no meio (y 1190), a palavra falada numa caixinha vermelha; o `bib.py` põe por cima no fim (`scripts/leg_unicef.py`). Se houver texto perto de y 1190, mude o `y`.
   - `voz`: `{arq, tx, de}` para uma narração por cima.
   - `musica`, `musica_volume`, `musica_depois: [t, volume]` (a música sobe quando a fala acaba) e `fim: {de, linhas, cor, sub, setas}`.
   - **Rosto:** confira onde fica o rosto em cada bruto. Nos de 02/11/2026, ele fica em y 384-860 na cadeira de rodas, 190-576 no sofá e 576-860 na cama. Tire o texto do caminho ou troque a cena.
   - **Não repita a mesma cena no mesmo vídeo.**
4. **Brutos novos:** transcreva com `transcrever.py … --diarize` (scripts de qualquer skill da ONG). Salve em `~/.claude/estudio-ong/CONHECIMENTO/transcricoes/<pasta>/<nome do bruto>.json`, porque o `bib.py` acha sozinho.
5. **Monte:** `python -I scripts/bib.py "<pasta do plano>\plano.json"`. Ele escolhe o próximo PEB/AEB e a LEVA, grava o caminho no plano (remontar mantém o número) e aplica a marca. Leva uns 2 min e meio por vídeo. Monte um de cada vez (dois juntos já travaram o ffmpeg).
6. **Confira:** rode `~/.claude/estudio-ong/ferramentas/conferir_auto.py <mp4>` e olhe uma folha de quadros (rosto livre, texto legível, marca, CTA). Uma "travadinha" em imagem parada é esperada. Diga ao usuário que você não ouviu o áudio.

## Copiar um anúncio novo da biblioteca
1. Abra a página da Biblioteca no navegador. Pegue o `src` do `<video>` do cartão com o mesmo "Identificação da biblioteca". Baixe para `EDITADOS\_referencias\bibliotecas\<ong>_<id>.mp4`, só com a permissão do usuário.
2. Faça a folha de quadros e transcreva. Meça a posição (y em % de 1920), o tamanho e a fonte de cada texto num quadro com grade de 10%.
3. **Música:** se o anúncio só tem música, use o áudio dele inteiro. Se tem fala, rode
   `~/.claude/estudio-ong/sep/Scripts/python.exe scripts/separar_musica.py <anúncio.mp4> <saída.wav>`.
   Esse Python tem o Demucs. Se ele não existir, crie um venv e instale `torch torchaudio` (CPU) e depois `demucs soundfile`.
   Converta para MP3, salve em `MÚSICAS\ANÚNCIOS QUE DERAM CERTO` com o nome "<ONG> <número> - <tema>" e acrescente no `musicas.json`. Para ficar por baixo da fala, o volume é o que deixa a faixa em -27 LUFS.
4. **Narração**, quando o anúncio é narrado: use o Leonardo (`4XmhZ74tBbUVCXIYNMMo`, `eleven_multilingual_v2`), tire o respiro com `comum.sem_respiro` e transcreva para ter a legenda.
5. **Imagem de IA**, quando o anúncio usa: Seedream 4.5 na Magnific (`POST /v1/ai/text-to-image/seedream-v4-5`, `aspect_ratio: social_story_9_16`, header `x-magnific-api-key` com a variável `magnific`). A imagem é simbólica e nunca mostra uma pessoa se passando por real.
6. Escreva o plano no mesmo molde e acrescente o modelo novo em `modelos/` e no `references/modelos.md`.

## Ajustes pedidos pelo usuário (não desfaça)
- Copiar o estilo exato do anúncio: posições, tamanhos e fontes medidos nos quadros.
- Manter a música do anúncio que deu certo. Quando não for possível, usar uma música triste da Magnific.
- Começar com as tomadas mais fortes (pedido no PEB 209). Desde 05/11/2026, sem P&B, salvo pedido do usuário.
- Não usar o trecho de 9 a 12 s do `pedrinho_guerreiro_1763051547…` (ferida aberta).
- **Caixa "DOE … e AJUDE …" do modelo Conselho (peb223)**: o padrão é a caixa vermelha chamativa do PEB 227 (`bg vermelho`, `fg branco`, `fonte black`, `size 50`, `y 185`, `raio 16`, `sombra_caixa`), não mais a rosa (pedido de 05/11/2026). Ela só entra depois que o versículo sai: se o versículo vai até 4,5 s, a caixa começa em 4,6 s. Senão uma cobre a outra.
- **Legenda UNICEF em todos os vídeos com fala** (`"legenda": {"estilo": "unicef"}`), pedido de 05/11/2026.
- **Menos takes da criança falando, mais takes das feridas** com um borrão leve (dá para ver que é ferida, mas borrada). Para a Adrielly, os clipes prontos estão em `EDITADOS\_planos\_clipes_adrielly\ferida_*.mp4` e `foto_ferida_*.mp4`. Sem P&B (só se o usuário pedir). Nunca as pernas enfaixadas da Adrielly (`adrielly_pernas_faixas`).
- **Vídeo de IA no gancho** (Orações e Conselho): imagem Seedream 4.5 + vídeo Kling 2.5 Pro na Magnific (`POST /v1/ai/image-to-video/kling-v2-5-pro`, `duration "5"`, `cfg_scale 0.5`). As imagens têm de parecer cristãs (cruz, crucifixo, Bíblia, terço, igreja, vitral, capela), com poucas velas ou nenhuma: muitas velas pareceram umbanda ao usuário. Nada de animais, plantações, plantas ou trigais (pedido de 05/11/2026). Não reaproveite os vídeos de IA de outro vídeo. O gerador de exemplo está em `EDITADOS\_planos\_estilo_bib\gerar_planos4_adrielly.py`.
- **Monte um vídeo por vez.** Dois `bib.py` juntos (ou legenda palavra por palavra com 80+ entradas) já travaram o ffmpeg sem erro; se um passar de 10 min parado, mate e remonte sozinho.
