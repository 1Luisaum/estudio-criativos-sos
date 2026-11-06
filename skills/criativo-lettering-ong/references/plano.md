# plano.json do Cortes com lettering

Os campos de corte (`raw`, `transcript`, `bank`, `music`, `face`, `zooms`, `segments` com `in`/`out`/`zoom`/`broll`/`fix`, `fix`, `red`, `music_vol`, `saturation`) são os mesmos do `build.py` dos Cortes com gancho. Veja `plano.md` da skill `edicao-criativo-ong`.

O que é próprio deste estilo:

| Campo | Padrão | O que é |
|---|---|---|
| `chamada.imagem` | **obrigatório** | caminho de UMA imagem da pasta `lettings` |
| `chamada.texto_do_lettering` | — | o que está escrito no lettering (anotação para quem lê o plano) |
| `chamada.largura` | 760 | largura do lettering na tela, em px (a altura segue a proporção da imagem) |
| `chamada.y` | 1290 | centro vertical do lettering |
| `chamada.ate_o_fim` | true | fica até o último quadro, inclusive na tela final |
| `hook` | `[]` | sem ganchos de texto neste estilo |
| `caption_y` | 950 | altura da legenda do meio (acima do lettering) |
| `caption_font` / `caption_font_nome` | Poppins Black achada sozinha | fonte da legenda |
| `endcard` | — | `{"src", "start", "dur": 3.4, "y": 760, "lines": [], "cta": "CLIQUE EM SAIBA MAIS"}`; o CTA fica em `y + 220` |

O lettering entra no último passe, por cima das legendas e da tela final escurecida. Assim ele não escurece e não perde cor com a dessaturação do vídeo.
