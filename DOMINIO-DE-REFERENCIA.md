# Domínio de referência: fintech fictícia

Fonte dos nomes usados nos exemplos e nos diagramas concretos do acervo. A proposta de cenário de cada padrão está em [REVISAO-EXEMPLOS-FINTECH.md](REVISAO-EXEMPLOS-FINTECH.md).

## A empresa

Uma instituição de pagamento brasileira com conta digital, Pix, boleto, cartão, crédito pessoal e consignado, e investimentos em renda fixa. Ela não tem nome: os textos dizem "a fintech" ou "o banco digital".

## Contextos e classes

| Contexto | O que faz | Classes e termos |
| --- | --- | --- |
| Onboarding | Abertura de conta e KYC | proponente, dossiê de KYC, `Cpf` |
| Conta Digital | Contas, saldo e extrato | `Account`, `Statement`, `AccountRepository`, `BusinessCalendar` |
| Ledger | Partida dobrada | `LedgerEntry`, `Money` |
| Pagamentos | Pix, TED e boleto | `PixCharge`, `PixKey`, `PaymentInstruction` (`PixTransfer`, `TedTransfer`), `Boleto`, `endToEndId`, `txid` |
| Cartões | Emissão, autorização e fatura | `Card`, `CardAccount`, `CardInvoice`, `InvoiceEntry`, `AuthorizationHold`, `Merchant` |
| Crédito | Decisão, contratação e cobrança | `CreditProposal`, `CreditPolicy`, `RiskScore`, `LoanContract`, `Installment`, `CreditBureau` |
| Investimentos | Carteira de renda fixa e variável | `Portfolio`, `Asset` (`Cdb`, `Stock`, `FundShare`) |
| Antifraude | Regras e sinais por transação | `FraudService` |
| Conciliação | Confere liquidações e arquivos | arquivos CNAB 240 e 400, `camt.053` |
| Notificações | Push, e-mail e webhook | `PushNotifier`, `MerchantWebhook` |

Sistemas externos: DICT e SPI (rede do Pix), bancos parceiros (arquivos CNAB), bureau de crédito, bandeira do cartão (ISO 8583), instituições de Open Finance (`Consent`) e o core bancário legado.

## Glossário

| Termo | Significado no acervo |
| --- | --- |
| Pix | Pagamento instantâneo. Cobrança é `PixCharge`; transferência é `PixTransfer` |
| DICT | Diretório que resolve uma chave Pix em dados da conta |
| SPI | Sistema que liquida as mensagens de Pix |
| TED | Transferência liquidada em dias úteis |
| Boleto | Cobrança com vencimento, multa, juros e desconto opcionais |
| CNAB | Layout de arquivo de remessa e de retorno trocado com bancos (240 e 400) |
| Devolução | Reversão de um Pix (`PixReturn`) |
| Estorno | Reversão de um lançamento de cartão ou do ledger (`Reversal`); é sempre um lançamento novo |
| Contestação | Disputa de uma compra no cartão (`Chargeback`) |
| Pré-autorização | Reserva de limite no cartão (`AuthorizationHold`) |
| SAC e Price | Sistemas de amortização: parcelas decrescentes e parcelas fixas |
| CET | Custo efetivo total de uma operação de crédito |
| IOF | Imposto sobre operações de crédito |
| KYC e PLD | Identificação do cliente e prevenção à lavagem de dinheiro |

## Regras para escrever os exemplos

1. **Identificadores em inglês**, também no texto em pt-BR, e idênticos nas duas línguas. Termos brasileiros sem tradução corrente ficam como são: `Pix`, `Boleto`, `Cnab`, `Cpf`, `Ted`.
2. **Dinheiro nunca é ponto flutuante.** Use `Money` quando a classe ajuda o exemplo, ou centavos inteiros com o sufixo `Cents` quando o exemplo precisa ficar curto. Taxas podem ser `number`.
3. **Mesmo nome, mesmo significado** em todos os documentos. Se o exemplo precisa de outro conceito, usa outro nome.
4. **Estorno é um lançamento novo**, nunca a remoção do original.
5. **Valores ilustrativos.** Alíquotas, limites, prazos e tarifas são exemplos. O texto não afirma regra regulatória como fato; quando ajudar, diz "valor ilustrativo".
6. **Variedade.** Padrões vizinhos alternam entre Pix, boleto, cartão, crédito e investimentos.
7. **A linguagem e o tamanho do exemplo são mantidos.** O exemplo novo tem a mesma linguagem do antigo, tamanho parecido, e continua mostrando o mesmo ponto do padrão.
8. **Exemplo e diagrama concreto usam as mesmas classes.** Diagramas genéricos (papéis do padrão) não mudam.
9. **Prosa.** Só muda o trecho que cita o cenário antigo. A primeira frase da Descrição não muda, porque alimenta a tabela da página do catálogo.
10. **Inglês.** A página em `i18n/en/docusaurus-plugin-content-docs/current/` é tradução fiel: mesmos blocos de código (só comentários e strings traduzidos), mesmos links, mesmos títulos. No Mermaid, traduzem-se rótulos, participantes, notas e comentários `%%`; ids de nó e sintaxe não mudam. Valores em reais continuam em reais (`R$ 10,000.00`).

## Modelo

O padrão-piloto é o Strategy: `docs/coding/gof/behavioral/strategy.md` e a tradução no mesmo caminho em `i18n/en/`.
