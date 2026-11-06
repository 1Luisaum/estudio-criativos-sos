---
name: criativo-caixas-pedido-ong
description: >-
  Estilo "Caixas – pedido de tempo" para criativos de doação da ONG Sos Human Help (Pedrinho e Adrielly, epidermólise bolhosa). Cópia da edição validada dos anúncios da Causas do Bem (caso Kauê) - gancho com a criança em close pedindo tempo para a câmera ("Por favor, fica só 30 segundos") com uma frase real dela em texto verde de contorno preto; depois o corpo com a voz real da criança sobre b-roll curto (~2 s por cena), um take de 3-5 s dela falando na câmera, caixa verde (ou vermelha) parada no alto com o fato e caixa de valor "R$10,00" parada embaixo, sem legenda e sem P&B. Use quando o usuário pedir "estilo caixas", "igual ao Kauê", "igual à Causas do Bem", "gancho pedindo tempo com caixas", "igual ao Pedrinho_vsl_voz_v6", ou escolher "Caixas: pedido de tempo" no Estúdio. Para o gancho de aspas use criativo-caixas-aspas-ong; para o URGENTE use criativo-caixas-urgente-ong.
---

# Caixas – pedido de tempo

> **Marca @soshumanhelppt e CTA (regra do usuário, 29/10/2026):** a logo da SOS foi trocada pelo texto **@soshumanhelppt** (branco, contorno preto, semitransparente), andando pela tela o vídeo inteiro. A regra da logo abaixo vale para ele: é obrigatório, o montador aplica sozinho (`scripts/marca.py` + `scripts/marca_soshumanhelppt.png`) e para com erro se faltar. O CTA na tela e na narração é **"Clique em SAIBA MAIS"**, nunca "Doar agora" nem "Doe agora".

> **Logo obrigatória (regra do usuário, 26/10/2026):** todo vídeo deste modelo sai com a logo da SOS Human Help, semitransparente, andando pela tela o vídeo inteiro. O montador aplica sozinho no fim (`scripts/marca.py` + `scripts/logo_sos.png`) e **para com erro se a logo faltar**. Não existe opção para tirar a logo, nem a pedido de um plano. Na conferência, confira na folha de quadros que ela aparece. Um vídeo montado por outro caminho (script próprio, cópia de referência) também tem que passar por `marca.py` antes de ser entregue.

> **Onde salvar (regra do usuário, 27/10/2026):** todos os estilos salvam juntos numa pasta única, `EDITADOS\RENDERIZADOS\LEVA NN`, com 5 vídeos por LEVA, a partir da `LEVA 26`. O arquivo se chama `PEB <número> - <ESTILO>.mp4` para o Pedrinho (a partir do PEB 111, LEVAs a partir da 26, hoje dentro de `RENDERIZADOS\TUDO BALBINO`) e `AEB <número> - <ESTILO>.mp4` para a Adrielly (a partir do AEB 34, LEVAs a partir da 41; regra do usuário de 27/10/2026). Cada criança tem a sua numeração e as suas LEVAs, e as LEVAs podem estar em subpastas. O montador faz isso sozinho pelo `comum.destino()`: não escolha pasta nem nome. Re-render de um plano que já tem PEB substitui o mesmo arquivo. A pasta do plano continua `EDITADOS\_planos\<Criança>_<ângulo>_vN`. Vídeos antigos citados abaixo como exemplo continuam onde estão.

> **Antes de criar, leia** `$HOME\.claude\estudio-ong\CONHECIMENTO\CONHECIMENTO.md` (falas reais com a fonte, transcrições prontas em `transcricoes\`). **Não altere esta skill durante a conversa:** ajustes vão só no `plano.json` do vídeo; a skill muda só quando o usuário pedir para salvar.

Criada a pedido do usuário em 26/10/2026. O exemplo aprovado é `Pedrinho_vsl_voz_v6` (30 s). O plano está em `references/exemplo-plano.json`. Fale com o usuário em português do Brasil.

## De onde vem
O usuário pediu para **copiar a edição já validada** de três anúncios da Causas do Bem (caso Kauê, AME). Os três tinham o mesmo corpo e só trocavam o gancho. Esta skill é o gancho 1 (a criança pede tempo para a câmera). As skills irmãs são `criativo-caixas-aspas-ong` (gancho com aspas) e `criativo-caixas-urgente-ong` (gancho URGENTE). Por isso o corpo é o mesmo nas três: dá para testar só o gancho.

## Visual (medido nas referências, quadro 360x640 × 3)
- **Gancho (3-5 s):** a criança em close falando o pedido de tempo, com a voz e a imagem do mesmo trecho (um corte só, para a boca bater). Por cima, uma **outra frase real dela** em texto verde `(70,232,70)` com contorno preto, em Bahnschrift Bold Condensed, centralizada em y≈1310 (`texto_verde`). No exemplo: "OS MEUS CURATIVOS ESTÃO ACABANDO / E EU TÔ COM MEDO". O gancho não tem caixas (`sem_caixas: true`).
- **Corpo:**
  - a voz real da criança, cortada sem pausas;
  - b-roll curto, de uns 2 s por cena (várias `cenas` por frase);
  - **um take de 3 a 5 s da criança falando na câmera**, com um corte único e a cena começando no mesmo segundo do corte (`cortes: [[a, b]]`, `cenas: [[mesmo bruto, a-0,06]]`). Nesse take vai `"sem_topo": true`, para a caixa do alto não cobrir o rosto.
- **Caixa do alto, parada o corpo todo** (`visual_ref.topo`, y=240): caixa verde `(34,170,52)` com texto branco condensado, 2 linhas. Formato da referência: "<CRIANÇA> TEM <DOENÇA> E PRECISA DE / <O QUE PRECISA> PARA <MOTIVO>". No exemplo: "PEDRINHO TEM EPIDERMÓLISE BOLHOSA E PRECISA DE / CURATIVOS PARA ALIVIAR AS DORES".
- **Caixa de valor, parada embaixo** (`visual_ref.valor` + `valor_linhas`, y=1300): "R$10,00" grande e duas linhas pequenas. Formato: "DEIXAM <CRIANÇA> MAIS PERTO DE COMPRAR / <O QUE COMPRA>".
- **Cor:** verde por padrão. Para vermelho, use `visual_ref.cor_caixa: [200,16,28]` e `cor_texto: [235,40,40]`. O usuário pediu "vermelho em um ou outro vídeo".
- **Sem legenda palavra por palavra** (`sem_legenda: true`) e **sem P&B**, como nas referências.
- Música: piano `alex-morgan…` a 0,09.

## Regras que continuam valendo (não são de skill, são de honestidade)
- **Só fato real:** as frases na tela e os textos das caixas saem do que a criança ou a mãe disseram. Nunca invente idade, aparelho, valor ou prazo. O valor da caixa deve aparecer numa fala, se possível (no exemplo, "quatro, cinco reais, dez reais").
- **Nunca copie marca nem pessoa:** nada de logo, nome ou cores próprias de outra ONG ou de jornal. Copie só o formato.
- **Nada em cima do rosto da criança:** use `sem_topo` no take falando, `zonas_protegidas` em cenas com a criança de perfil e confira na folha.
- O CTA do anúncio é "Saiba mais"; a ONG se fala "ésse ô ésse".

## Fluxo
`$PY = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"` (sempre com `-I`). Scripts em `$K = "$HOME\.claude\skills\criativo-caixas-pedido-ong\scripts"`. Edite JSON só com Write/Edit ou com script Python. Antes de transcrever, carregue a chave no mesmo comando: `$env:ELEVENLABS_API_KEY = [Environment]::GetEnvironmentVariable('ELEVENLABS_API_KEY','User')`.
1. **Falas:** use as transcrições prontas (`CONHECIMENTO\transcricoes`) ou `& $PY -I "$K\transcrever.py" "<bruto>" "<plano>\tx\<nome>.json"`. Cada corte é `[início da 1ª palavra, início da última]`. Corte vícios dividindo a frase em vários cortes, menos no gancho e no take falando, que têm um corte só.
2. **Plano:** copie `references/exemplo-plano.json` para `EDITADOS\_planos\<Criança>_caixas_pedido_vN\plano.json` e troque `nome`, as `frases` (fonte, tx, cortes, cenas/foto) e os textos. A frase `final: true` ganha 1,4 s no fim.
3. **Montar:** `& $PY -I "$K\caixas.py" "<plano>\plano.json"`. Ele salva em `EDITADOS\RENDERIZADOS\LEVA NN\PEB <n> - <ESTILO>.mp4` (5 por LEVA).
4. **Conferir o MP4 final:**
   - transcrição: `transcrever.py` no MP4 final; o texto precisa bater com as frases;
   - quadros: `& $PY -I "$K\folhas.py" frames --at <meio de cada bloco> --out <tmp>\conf.jpg "<saida>"`. Nada no rosto da criança e caixas legíveis;
   - travadinha: `ffmpeg -i "<saida>" -vf freezedetect=n=0.002:d=0.12 -map 0:v -f null -`. Foto parada longa (mais de 4 s) treme: troque por cenas de vídeo ou suba `"zoom"` da foto para 0,12.
5. **Entregar** com `SendUserFile`. Diga as falas, os textos das caixas e a fonte de cada fato, e avise que você não ouve o áudio.

## Pedido do Estúdio
Leia `EDITADOS\_pedidos\<id>.json`: `brutos` (falas), `banco` (b-roll), `observacoes` (têm prioridade). Com `quantidade` > 1, mude o gancho, a frase verde, as cenas e a ordem das falas. No fim, grave com Edit `status: concluido`, `saida` e `saidas`.

## Armadilhas já resolvidas
- **Caminho com emoji** ("Um Vídeo Novo pra campanha 💚.mp4"): o PowerShell não acha com `-like`. Use Python com `glob` e `sys.stdout.reconfigure(encoding="utf-8")`. O `-I` ignora `PYTHONIOENCODING`.
- **A cópia de fonte de `AppData\Local\Microsoft\Windows\Fonts` vem somente leitura;** apague antes de copiar de novo.
- **Detector de rosto falha em perfil e em fotos:** use `zonas_protegidas` (vídeo) ou `legenda_y` / `sem_topo`.
