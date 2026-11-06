# Pacote do Estúdio de Criativos – SOS Human Help

Esta pasta é o pacote que um novo editor recebeu para instalar o Estúdio de Criativos da ONG SOS Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Fale com o editor em português do Brasil, em frases curtas.

**Quando o editor abrir esta pasta e pedir qualquer coisa como "instale", "configure", "faça funcionar" ou só "oi", instale tudo sozinho, sem perguntas, e termine com o Estúdio aberto.** O editor só precisa autorizar os comandos. Rodar de novo atualiza as skills e o Estúdio sem mexer nos vídeos dele.

## Instalação (2 comandos)
Use o PowerShell. `$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`.

1. **Python 3.12.** Rode `Test-Path "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"`.
   - Se der `False`, instale com
     `winget install -e --id Python.Python.3.12 --scope user --accept-package-agreements --accept-source-agreements`
     e rode o `Test-Path` de novo.
   - Sem winget, ou se continuar `False`, peça para o editor instalar pelo python.org ("Install for me only") e depois continue.
2. **Todo o resto:** nesta pasta, rode `& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -I instalar.py`, com tempo limite de 10 minutos. Ele:
   - instala o FFmpeg pelo winget, se faltar, e o deixa ao lado do Python, para funcionar sem reabrir o Claude;
   - instala Pillow, NumPy e OpenCV 4;
   - copia as 15 skills para `$HOME\.claude\skills`;
   - cria a pasta do material (padrão: `Área de Trabalho\EDIÇÃO COM CLAUDE`) com `ESTUDIO`, `VÍDEOS PARA EDITAR`, `MÚSICAS` (já com as trilhas) e `EDITADOS` (com `RENDERIZADOS\LEVA 26`);
   - cria o atalho "Estudio de Criativos" na área de trabalho;
   - confere tudo e **abre o Estúdio** no navegador.

   Se o editor pediu outra pasta para o material, acrescente `--pasta "<caminho>"`. Se ele quiser escolher numa janela, acrescente `--escolher`.
   Se o comando terminar com erro, leia a mensagem, corrija a causa e rode de novo.

## Depois de instalar, diga ao editor (curto)
- O Estúdio está aberto. Da próxima vez, ele abre pelo atalho "Estudio de Criativos".
- **Chave do ElevenLabs:** só se o instalador disser `FALTA`. É ele quem coloca. Nunca peça, leia, mostre nem digite a chave.
  1. Criar a chave em elevenlabs.io > Developers > API Keys, na conta dele.
  2. No Windows: Iniciar > "Editar as variáveis de ambiente para sua conta" > Novo.
  3. Nome `ELEVENLABS_API_KEY`, valor a chave, OK.
  Sem a chave, o Estúdio abre, mas a narração e a transcrição não funcionam.
- Colocar os brutos em `VÍDEOS PARA EDITAR` e o b-roll numa pasta "banco de vídeos do <criança>" dentro da pasta do material.
- **Fechar e abrir o Claude antes do primeiro pedido**, para ele carregar as skills (e a chave).

## Conhecimento acumulado
A pasta `CONHECIMENTO` traz tudo o que foi decidido com o editor original. O instalador copia para `$HOME\.claude\estudio-ong\CONHECIMENTO`:
- `CONHECIMENTO.md`: as regras com data, os estilos aprovados, as vozes, as falas reais com a fonte, os ângulos já usados e os problemas já resolvidos;
- `transcricoes\`: os brutos do Pedrinho já transcritos, para não gastar crédito de novo;
- `biblioteca-de-anuncios-pesquisa.md`: os ganchos e os formatos validados de ONGs concorrentes;
- `conversa-original.md`: o chat inteiro em que o Estúdio foi criado, com os pedidos do usuário e as respostas, sem chaves. Use para entender o porquê de uma regra. As regras que valem estão no `CONHECIMENTO.md`.

As skills mandam ler esse documento antes de criar. Se o editor perguntar "por que é assim?", a resposta está lá.

## Como se usa depois
- No Estúdio, o editor escolhe estilo, criança, pasta e brutos, cria o pedido e cola no Claude a mensagem "Executa o pedido do Estúdio…".
- As skills (`criativo-reportagem-ong`, `criativo-lista-ong`, `criativo-vsl-voz-ong`, `criativo-narrado-ong`, `edicao-criativo-ong`, `criativo-lettering-ong`, `criativo-caixas-pedido-ong`, `criativo-caixas-aspas-ong`, `criativo-caixas-urgente-ong`, `criativo-corrente-ong`, `criativo-mae-desesperada-ong`, `criativo-salva-vida-ong`, `criativo-esperanca-ong`, `criativo-unicef-ong` e `criativo-bibliotecas-ong`) têm todas as regras.
- O estilo Cortes com lettering usa as imagens que o editor cria na pasta `lettings` da pasta do material (uma por vídeo) e a fonte Poppins Black, se instalada.
- Todos os estilos salvam juntos em `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 por LEVA, a partir da `LEVA 26`, com o nome `PEB <número> - <ESTILO>.mp4` a partir do PEB 111 para o Pedrinho e `AEB <número> - <ESTILO>.mp4` a partir do AEB 34 (LEVAs a partir da 41) para a Adrielly (regras de 27/10/2026); cada criança tem a sua numeração e as suas LEVAs, que podem estar em subpastas; os scripts fazem isso sozinhos.
- **Produção ao vivo:** ao começar qualquer demanda de vídeos, grave `EDITADOS\_demanda_atual.json` (`titulo`, `pedido`, `inicio` em ISO, `total`, `status: "em andamento"`, `grupos` com `{"nome", "estilos": {"<ESTILO>": quantidade}}`) e, no fim, troque o `status` para `"concluída"`. A aba "Produção ao vivo" do Estúdio mostra a demanda, o vídeo que está sendo feito e a % de cada um.
- **Lote de vários vídeos (processo rápido):** escreva os planos com o agente `roteirista-ong`, consultando `~/.claude/estudio-ong/ferramentas/biblioteca.py` (falas reais) e `catalogo.py livres` (fotos sem rosto nas faixas de texto); monte com `fila.py <pastas dos planos> --paralelo 2` (pré-voo antes de montar, placa de vídeo, só refaz o que mudou e conferência automática); revise só os vídeos com aviso, com o agente `revisor-ong`. Detalhes na seção 7.1 do `CONHECIMENTO.md`. Se o PC do editor não tiver placa NVIDIA, a montagem volta sozinha para o processador.
- **Estilo "Bibliotecas" (03/11/2026):** são 10 criativos do Pedrinho copiados de anúncios de outras ONGs (PEB 202 a 211). O instalador já copia para a pasta do material os brutos de 02/11/2026, as músicas tristes da Magnific (`MÚSICAS\magnific_tristes`), as referências (`EDITADOS\_referencias\bibliotecas`), os trechos do banco (`banco de vídeos do pedrinho\_clipes_bib`) e os 10 vídeos prontos de exemplo (`EDITADOS\EXEMPLOS BIBLIOTECAS`). O montador fica em `EDITADOS\_planos\_estilo_bib`: os ajustes vão no `gerar_planos.py`, e depois roda `python -I gerar_planos.py` e `python -I bib.py <pasta do plano>\plano.json`. O passo a passo está no `LEIA-ME.md` dessa pasta. Desde 03/11/2026, a skill `criativo-bibliotecas-ong` reúne os 24 modelos (PEB 202 a 225) para refazer com outros brutos ou com a Adrielly. As músicas ficam em `MÚSICAS\ANÚNCIOS QUE DERAM CERTO` e `MÚSICAS\magnific_tristes`, cada pasta com um `musicas.json` que diz o volume.
- **A marca @soshumanhelppt é obrigatória em todo vídeo, de todo modelo** (no lugar da logo da SOS desde 29/10/2026): os montadores aplicam sozinhos (texto branco semitransparente, andando pela tela). Nunca entregue vídeo sem ela.
- O CTA é "Clique em SAIBA MAIS" (regra de 29/10/2026), nunca "Doar agora" nem "Doe agora".
- A ONG se fala "ésse ô ésse" (S.O.S), nunca "sós".
- Não altere as skills durante a conversa. Ajustes de um vídeo vão só no `plano.json` dele.
