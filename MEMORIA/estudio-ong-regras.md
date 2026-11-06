---
name: estudio-ong-regras
description: "Regras do usuário para os criativos da SOS Human Help que mais causaram retrabalho (CTA, rosto, zona segura, P&B, copy nova, vozes)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 671e808f-aec5-4292-93a6-ac14352a69d2
  modified: 2026-10-27T02:07:04.718Z
---

Regras aprovadas pelo usuário em 25-26/10/2026 (lista completa em CONHECIMENTO.md §2):

1. **Só fato real** dito pela criança/mãe nos brutos ou visto no banco. Nunca inventar número, idade, prazo, valor.
2. **CTA "Clique em SAIBA MAIS"** (desde 29/10/2026; antes "Toque em"), nunca "Doar agora"/"DOE AGORA". Cortar fala real com "clique em Doar agora".
3. **Nada de texto em cima do rosto** da criança (nem pequena ao fundo; use `zonas_protegidas`). Não proteja adulto por conta própria (usuário recusou proteger a testa da mãe na lista).
4. **Chamada/manchete só no alto** (y 290-470); legenda e etiqueta até y=1250. Se rosto ocupar o alto, a chamada some na cena.
5. **Sempre tela cheia**: nunca reduzir vídeo nem fundo desfocado.
6. **Gancho com a imagem mais forte em P&B**; toda imagem forte em P&B; esperança em cor.
7. **Copy totalmente nova** a cada vídeo (ângulo, gancho, manchete, narração, cartelas, virada, tela final). Ver ângulos usados em CONHECIMENTO §6.
8. **Narrador brasileiro, 3ª pessoa**, sem respiro: Kaique `Hmn4B9B77pf6ttydteJ8` (narrado), Leonardo `4XmhZ74tBbUVCXIYNMMo` (lista, reportagem). Nunca Brian/Matilda. Números por extenso.
9. "SOS" se fala "ésse ô ésse"; "gaze" se fala "gáze" (scripts já trocam).
10. Sem foto de ferida aberta (Meta reprova); nenhuma imagem deitada; produtos parados, sem panorâmica.
11. Reportagem nunca imita emissora real. Narrado não mostra nome na tela.
12. **Não alterar skills nem Estúdio na conversa**: ajuste vai só no `plano.json`; skills só mudam quando o usuário disser "salvar".
13. Saída (desde 27/10/2026): pasta única `EDITADOS\RENDERIZADOS\LEVA NN`, 5 por LEVA, a partir da LEVA 26; arquivo `PEB <n> - <ESTILO>.mp4` a partir do PEB 111 (comum.destino decide; os planos continuam em `_planos\<Criança>_<ângulo>_vN`). Adrielly: `AEB <n>` a partir do AEB 34, LEVAs a partir da 41 (pedido de 27/10/2026); Pedrinho continua PEB, LEVAs 26-33 em `RENDERIZADOS\TUDO BALBINO`.
15. **Quando o usuário mandar copiar uma referência validada** ("esqueça as skills"), copie formato, posições e textos no mesmo molde, mas só com fatos reais, sem marca de terceiros e sem pessoa feita com IA (apresentadora falsa de telejornal recusada em 26/10/2026). Ele quer ganchos curtos (3-5 s), takes de ~2 s e um take real da criança falando.
14. **Cortes com lettering** (skill `criativo-lettering-ong`, criada em 26/10/2026): sempre **um** lettering só por vídeo, tirado da pasta `lettings` da raiz (imagens que o usuário cria), parado o vídeo todo, no lugar de qualquer texto que eu desenharia. O valor do lettering deve bater com o pedido. Legenda em Poppins Black.

16. **Marca OBRIGATÓRIA em todo vídeo, de todo modelo e skill**: desde 29/10/2026 é o texto **@soshumanhelppt** (no lugar da logo SOS de 26/10/2026), semitransparente, andando pela tela o vídeo todo; os montadores aplicam no fim (`marca.py` + `marca_soshumanhelppt.png`) e param com erro se faltar. Pedido pontual de outra marca (ex.: @juntospelopedrinho) vale só para aquela demanda, com cópia do montador fora da skill. Não há como desligar. Vídeo feito por script próprio também passa por `marca.py` antes de entregar; confira na folha que a logo aparece.

17. **Nunca usar o vídeo da Adrielly na parede lilás** (`Rot 3 (1)` a `(6)`, pedido de 30/10/2026): estão em `evitar.json`, então o catálogo não sugere e o pré-voo para o plano. Sem eles, faltam cenas livres no banco da Adrielly: reparta as falas com fotos de curativo.

**Why:** cada item foi uma reprovação ou correção explícita do usuário; repetir o erro gera retrabalho e anúncio reprovado.
**How to apply:** checar esta lista ao escrever cada plano e na conferência [[estudio-ong-conferencia]]. Contexto em [[estudio-ong-onde-fica]].
