---
name: pattern-catalog
description: Incorpora um novo catálogo de design patterns ao site Docusaurus, em pt-BR e inglês (páginas por padrão, página do catálogo, sidebar, cards e home). Use quando o usuário pedir para adicionar, importar ou documentar um catálogo de padrões, ou para revisar a estrutura de um catálogo existente.
---

# Adicionar um catálogo de design patterns

O site tem dois idiomas: **pt-BR** (padrão, servido em `/`) e **inglês** (servido em `/en/`). Todo catálogo novo é publicado nos dois idiomas no mesmo PR. Siga as etapas em ordem. Este fluxo tem passos que exigem decisão do usuário: não pule as perguntas da etapa 1.

A hierarquia é **domínio → catálogo → grupo → padrão**. Nos exemplos abaixo, `<dir>` é `<domínio>/<catálogo>`, por exemplo `application/poeaa`.

## Onde fica cada coisa

| O quê | pt-BR | Inglês |
| --- | --- | --- |
| Página do padrão | `docs/<dir>/<grupo>/<slug>.md` | `i18n/en/docusaurus-plugin-content-docs/current/<dir>/<grupo>/<slug>.md` |
| Página do catálogo | `docs/<dir>/index.md` | `i18n/en/.../current/<dir>/index.md` |
| Página do domínio | `docs/<domínio>/index.md` | `i18n/en/.../current/<domínio>/index.md` |
| Home (tabela de catálogos) | `docs/index.mdx` | `i18n/en/.../current/index.mdx` |
| Estrutura: grupos, ordem, padrões compartilhados | `sidebars.ts` (vale para os dois idiomas) | — |
| Cards da home | `src/data/catalogs.json` | título traduzido em `i18n/en/code.json` (`catalogCards.title.<href>`), se o título não for em inglês |
| Rodapé e navbar | `docusaurus.config.ts` | `i18n/en/docusaurus-theme-classic/footer.json` e `navbar.json` |

Script de apoio: `.claude/skills/pattern-catalog/scripts/catalog.py`. Rode a partir da raiz do repositório com `python3 -I`. Subcomandos:

- `validate <dir>`: confere arquivos, frontmatter, seções, Mermaid, links, paridade pt-BR/inglês, sidebar e card da home.
- `index <dir>`: regenera as tabelas das páginas de catálogo nos dois idiomas a partir do `sidebars.ts` e do frontmatter dos padrões.

O `sidebars.ts` é a fonte da verdade da estrutura e o script o lê como JSON: mantenha o objeto em JSON válido (aspas duplas, sem vírgula sobrando, sem comentários dentro dele).

## 1. Levantamento e decisões (com o usuário)

1. Leia a página índice da fonte com WebFetch e liste todos os padrões, com o nome e a URL de cada um, agrupados como a fonte agrupa.
2. Defina o **domínio** do catálogo pelo foco principal dele:
   - `coding`: classes e objetos.
   - `application`: estrutura interna da aplicação e modelagem de domínio.
   - `architecture`: arquitetura de sistemas (estilos arquiteturais, distribuição, integração, consistência e concorrência).
   - `cloud`: aplicações e operação em nuvem e contêineres.
   - `ai`: sistemas com LLMs e agentes de IA.
   - Crie um domínio novo só com a aprovação do usuário.
3. Proponha uma **partição em grupos** em que cada padrão fique em exatamente um grupo. Prefira os grupos da própria fonte. Nomes dos grupos em inglês; slugs em kebab-case.
4. Detecte **sobreposições** com os catálogos existentes, comparando com os títulos e `pattern_slug` em `docs/*/*/*/*.md` e com o `sidebars.ts`. Classifique cada caso:
   - **mesmo padrão**: vira um link compartilhado no sidebar (★) e o arquivo existente é revisado;
   - **parecido, mas distinto**: vira padrão novo, com link em "Padrões relacionados".
5. Defina as **etiquetas**, que são multivaloradas e atravessam os grupos:
   - Reaproveite um conjunto existente quando fizer sentido (veja os `tags` dos catálogos parecidos). Os pilares WAF (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency) servem para padrões de arquitetura e de serviços; os objetivos de design do GoF servem para padrões de código.
   - Se nenhum servir, proponha um conjunto novo de 5 a 7 etiquetas, em inglês, com a distribuição prevista.
6. Use **AskUserQuestion** para confirmar o domínio (se houver dúvida), as etiquetas e os casos de sobreposição ambíguos. Recomende uma opção em cada pergunta.
7. Para catálogos grandes, escreva um plano curto (domínio, grupos, contagem e sobreposições) e peça aprovação antes de criar arquivos.

## 2. Preparação (você, sem subagentes)

1. Crie um branch a partir do `main` atualizado. O PR vai direto para o `main`; não empilhe PRs sobre outros branches.
2. Crie `docs/<dir>/<grupo>/` e `i18n/en/docusaurus-plugin-content-docs/current/<dir>/<grupo>/` para cada grupo.
3. Escreva o **cabeçalho** da página do catálogo nos dois idiomas. O script `index` preenche o resto depois. Use uma página de catálogo existente como modelo (`docs/cloud/cloud-design-patterns/index.md` e a versão em inglês):
   - frontmatter com `title` e `sidebar_label`;
   - `# <Nome do catálogo>`;
   - introdução: a fonte (com link), o que cada padrão traz e o que as etiquetas representam;
   - se houver padrões compartilhados, a nota sobre ★ (copie a frase de um catálogo que já a tem);
   - a linha `Total: 0 padrões em 0 grupos. Etiquetas: <rótulo>.` (em inglês: `Total: 0 patterns in 0 groups. Tags: <label>.`). O script corrige os números;
   - por último, o título `## Grupos` (em inglês: `## Groups`), que marca o fim do cabeçalho.
4. Adicione o catálogo ao **`sidebars.ts`**, dentro do domínio, seguindo o formato dos catálogos existentes:
   - categoria do catálogo com `key: "<slug>"`, `label` curto e `link: {"type": "doc", "id": "<dir>/index"}`;
   - uma categoria por grupo, com `label` (nome do grupo), `key: "<slug>-<grupo>"` e `collapsed: true`;
   - cada padrão novo é o id do documento: `"<dir>/<grupo>/<slug>"`;
   - cada padrão compartilhado é um link: `{"type": "link", "label": "<nome nesta fonte>", "href": "/<caminho do documento original>?catalogo=<slug>", "className": "sidebar-shared", "key": "<slug>-<slug-do-padrão>"}`.
5. Adicione o **card** em `src/data/catalogs.json` (`domain`, `domainLabel`, `title`, `href: "/<dir>"`, `source`, `patterns` = total do sidebar, incluindo os compartilhados, e `groups`). Se o `title` não estiver em inglês, adicione `catalogCards.title./<dir>` em `i18n/en/code.json`.
6. Atualize nos dois idiomas a **página do domínio** (lista de catálogos) e a **home** (tabela de catálogos). Atualize o rodapé em `docusaurus.config.ts` (catálogos e fontes) e o `footer.json` em inglês. Domínio novo também precisa de item na navbar (`domains` no `docusaurus.config.ts`), da página do domínio nos dois idiomas e de entrada na lista de domínios da home.

## 3. Conteúdo: um subagente POR GRUPO, nos dois idiomas

- Dispare **um subagente `general-purpose` por grupo**, todos na mesma mensagem, em paralelo, com **`model: "sonnet"`**.
  - O Sonnet basta para escrita técnica estruturada e para tradução com formato fixo, e custa bem menos que o Opus. Use o Opus só se o usuário pedir.
  - O limite é de 20 subagentes simultâneos. Se houver mais grupos, dispare os restantes conforme os primeiros terminarem.
  - Não crie um subagente por padrão: isso estoura o limite de uso.
  - Se o usuário pedir um número específico de subagentes, siga o pedido.
- Cada subagente escreve primeiro a versão em pt-BR de cada padrão e depois a versão em inglês, gravando cada arquivo assim que terminar (se for interrompido, ele retoma dos arquivos que já existem).
- O prompt de cada subagente deve trazer:
  - o caminho do repositório e o branch, com a proibição de comandos git que mudam estado;
  - a lista de padrões do grupo: caminho pt-BR, caminho em inglês, URL da fonte e se é NOVO ou EXISTENTE (com o caminho real do arquivo existente);
  - um padrão já publicado como modelo, nos dois idiomas (ex.: `docs/cloud/cloud-design-patterns/resiliency/retry.md` e a versão em inglês);
  - as etiquetas permitidas e o valor exato de `category` (o nome do grupo);
  - a lista de URLs válidas para links (as páginas existentes mais as novas do catálogo).
- Regras que o prompt deve passar:
  - Carregar o WebFetch via `ToolSearch` (`select:WebFetch`) e ler a página de cada padrão.
  - **Frontmatter**, idêntico nos dois idiomas: `title`, `pattern_slug`, `category`, `tags`, `source` e `sidebar_label` (entre aspas). `origin` e `also_in` quando se aplicarem. Não usar linhas `**Etiquetas:**` nem `**Categoria:**` no corpo: o site já mostra as etiquetas e o grupo.
  - **Seções** em pt-BR: Descrição, Problemas que resolve, Quando usar, ### Quando evitar, Trade-offs (tabela `| Ganho | Custo / Risco |` e bullets em negrito), Diagrama, Exemplo (quando a fonte tiver código ou cenário), Padrões relacionados e Referência. Em inglês: Description, Problems it solves, When to use, ### When to avoid, Trade-offs (`| Benefit | Cost / Risk |`), Diagram, Example, Related patterns e Reference.
  - pt-BR em português; nomes de padrões, categoria, etiquetas e identificadores de código ficam em inglês. A versão em inglês é tradução fiel da pt-BR, sem acrescentar nem omitir conteúdo, com as mesmas seções, links e blocos de código.
  - **Diagrama Mermaid** válido, sem HTML. Em `flowchart`, rótulos com acentos, parênteses ou pontuação vão entre aspas duplas. Na versão em inglês, traduza só os textos (rótulos, participantes, notas e comentários `%%`); a sintaxe e os ids dos nós ficam iguais.
  - **Links internos** sempre como URL absoluta da página, sem `.md`: `/<domínio>/<catálogo>/<grupo>/<slug>`. Nunca links relativos para arquivos `.md`: o Docusaurus não resolve um link `.md` entre uma página traduzida e uma não traduzida. A mesma URL serve aos dois idiomas, porque o Docusaurus acrescenta `/en` sozinho. Etiquetas: `/tags/<etiqueta-em-kebab-case>`.
  - **Exemplo com código**: identificadores, linguagem e estrutura iguais nos dois idiomas; traduza só comentários e strings exibidas ao usuário.
  - **Padrões EXISTENTES**:
    - editar o arquivo real nos dois idiomas, revisando com a nova fonte, sem reescrever do zero;
    - não mudar `title`, `pattern_slug`, `category` nem `tags`;
    - adicionar `also_in:` com `- <dir>/<grupo>` antes de `source:`, nos dois idiomas;
    - adicionar o link da fonte em "Referência" / "Reference".
  - Editar apenas os arquivos do próprio grupo.
  - Resposta final: uma linha `ok: <caminho>` por arquivo, mais um resumo da revisão para os existentes.
- Enquanto os agentes rodam, informe o progresso em uma linha por grupo concluído.
- Se o limite de uso for atingido, retome os agentes interrompidos com `SendMessage` em vez de criar novos. Eles devem reler os próprios arquivos e completar o que falta.

## 4. Índices, validação e build

```bash
python3 -I .claude/skills/pattern-catalog/scripts/catalog.py index <dir>
python3 -I .claude/skills/pattern-catalog/scripts/catalog.py validate <dir>
npm run build
```

- `index` monta as tabelas por grupo (resumo = primeira frase da Descrição/Description de cada padrão) e a seção por etiqueta, e corrige a linha `Total`.
- `validate` confere, entre outras coisas, se a versão em inglês tem o mesmo frontmatter, os mesmos links, o mesmo número de títulos e de blocos de código que a pt-BR, e se o texto em inglês não tem acentos. Também avisa quando o tamanho da tradução foge de 0,8–1,25x o original, sinal de trecho faltando: abra o arquivo e confira.
- O build gera os dois idiomas e falha em link quebrado (`onBrokenLinks: 'throw'`).
- Corrija os erros (por conta própria ou retomando o subagente do grupo) até tudo passar. Se algum arquivo existente foi revisado, rode `index` e `validate` também no catálogo dono desse arquivo.

## 5. Fechamento

- Atualize o `README.md` da raiz e o `TODO.md`, se mencionarem os catálogos.
- Commite seguindo o padrão do histórico (`git log`): um commit para o catálogo novo e outro para revisões em catálogos existentes, se houver.
- Abra o PR contra o `main`.
- Relate ao usuário:
  - o que foi criado e revisado, nos dois idiomas;
  - o resultado do `validate` e do build;
  - que o conteúdo não foi lido por uma pessoa e vale uma revisão rápida nas páginas `/<dir>` e `/en/<dir>`.
