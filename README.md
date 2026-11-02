# Design Patterns

Catálogo pessoal de design patterns em formato wiki, publicado em **https://designpatterns.alancesar.org**.

Feito com [Docusaurus](https://docusaurus.io), com a identidade visual do [alancesar.dev](https://alancesar.dev) (Catppuccin Latte/Mocha, destaque mauve, JetBrains Mono no código). Deploy na [Netlify](https://www.netlify.com).

## Desenvolvimento

```bash
npm install
npm start          # servidor local em http://localhost:3000
npm run build      # build de produção em build/ (falha em links quebrados)
npm run serve      # serve o build localmente (necessário para testar a busca)
npm run typecheck
```

## Deploy

A Netlify faz o build a cada push na `main` (configuração em `netlify.toml`) e gera deploy previews para pull requests.

Configuração do domínio (uma vez):

1. Na Netlify: **Add new site → Import from GitHub →** `alancesar/designpatterns`. As configurações de build vêm do `netlify.toml`.
2. Em **Domain management → Add a domain**, informe `designpatterns.alancesar.org` e mantenha o DNS externo.
3. No Cloudflare (zona `alancesar.org`), crie o registro:

   | Tipo | Nome | Destino | Proxy |
   | --- | --- | --- | --- |
   | CNAME | `designpatterns` | `<nome-do-site>.netlify.app` | **DNS only** (nuvem cinza) |

   Com o proxy ligado, a Netlify não consegue emitir o certificado.
4. Quando o certificado Let's Encrypt for emitido, ative **Force HTTPS** na Netlify.

Para conferir: `dig +short designpatterns.alancesar.org CNAME` deve retornar `<nome-do-site>.netlify.app`.
