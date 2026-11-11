# Revisão dos exemplos: cenários fintech

Proposta para trocar os exemplos do acervo por cenários do mundo financeiro brasileiro, com o plano de execução em ondas (seção 8).

**Escopo.** As seções `## Exemplo` (GoF, PoEAA e DDD) e os diagramas que mostram uma implementação concreta, com nomes de domínio em vez dos papéis do padrão. Diagramas genéricos (`Context`, `Strategy`, "Serviço A", "Nó 1") ficam como estão.

**Duas línguas.** O site é bilíngue, e cada troca vale para a página em pt-BR (`docs/...`) e para a tradução em inglês no mesmo caminho relativo (`i18n/en/docusaurus-plugin-content-docs/current/...`), no mesmo PR. As contagens e os caminhos deste documento se referem à árvore `docs/`; a árvore em inglês espelha cada item.

**Legenda.**

- Coluna **Exemplo**: `trocar` (cenário novo), `ajustar` (já é financeiro ou é o exemplo canônico; só refinar) ou `manter`.
- Coluna **Diagrama**: `redesenhar` (é concreto e usa o cenário antigo), `manter` (é concreto e já serve) ou `genérico` (papéis do padrão; nada a fazer).

## 1. Resumo

Dos 307 documentos do acervo, 122 têm seção Exemplo e 87 têm um diagrama concreto a redesenhar.

| Catálogo | Docs | Exemplo: trocar | Exemplo: ajustar | Exemplo: manter | Diagramas a redesenhar |
| --- | --- | --- | --- | --- | --- |
| GoF e clássicos | 28 | 24 | 4 | 0 | 2 |
| PoEAA | 51 | 37 | 11 | 3 | 30 |
| DDD | 41 | 29 | 5 | 7 | 22 |
| Microservices | 43 | 1 (Domain Event) | – | – | 14 |
| EIP | 56 | – | – | – | 6 |
| Cloud Design Patterns | 44 | 1 (Anti-Corruption Layer) | – | – | 6 |
| Distributed Systems | 29 | – | – | – | 0 |
| AI Agent Design Patterns | 15 | – | – | – | 7 |
| **Total** | **307** | **92** | **20** | **10** | **87** |

O que a leitura mostrou, além da troca de cenário:

- **Exemplo e diagrama divergem em vários documentos do PoEAA.** O exemplo fala de `Order` ou `Customer`, e o diagrama usa os nomes do livro do Fowler (`Person`, `Album`/`Track`, `Player`). A revisão resolve isso de passagem: os dois passam a usar as mesmas classes.
- **No GoF, só 2 dos 28 diagramas são concretos** (Factory e Telescoping Constructor). Os outros 26 usam os participantes do padrão e não mudam.
- **Patterns of Distributed Systems não tem nada a trocar.** Os 29 diagramas usam só cliente, líder, seguidor, nó e log.
- **Alguns exemplos já são financeiros** e ficam como `ajustar` ou `manter`: Adapter, Chain of Responsibility, Unit of Work, Money, Gateway, Domain Service, Knowledge Level, Drawing on Established Formalisms, entre outros.

## 2. Domínio de referência

Todos os cenários saem de uma mesma fintech fictícia: uma instituição de pagamento com conta digital, Pix, boleto, cartão, crédito pessoal e investimentos em renda fixa.

O glossário e as regras para escrever os exemplos estão em [DOMINIO-DE-REFERENCIA.md](DOMINIO-DE-REFERENCIA.md), que é a fonte dos nomes. O resumo abaixo reúne os mais usados.

| Contexto | Classes recorrentes |
| --- | --- |
| Conta Digital e ledger | `Account`, `LedgerEntry`, `Money`, `Statement`, `Cpf`, `BusinessCalendar` |
| Pagamentos (Pix, TED, boleto) | `PixCharge`, `PixKey`, `PaymentInstruction` (`PixTransfer`, `TedTransfer`), `Boleto`, `endToEndId` |
| Cartões | `Card`, `CardAccount`, `CardInvoice`, `InvoiceEntry`, `AuthorizationHold`, `Merchant` |
| Crédito | `LoanContract`, `Installment`, `CreditProposal`, `CreditPolicy`, `RiskScore`, `CreditBureau` |
| Investimentos | `Portfolio`, `Asset` (`Cdb`, `Stock`, `FundShare`) |
| Apoio | Onboarding e KYC, Antifraude, Conciliação, Notificações, Open Finance (`Consent`) |
| Externos | DICT e SPI (rede do Pix), bancos parceiros (CNAB), bureau de crédito, bandeira do cartão, core bancário legado |

Regras que valem para todos os exemplos:

- Identificadores de código em inglês, também no texto em pt-BR, e idênticos nas duas línguas. Termos do mercado brasileiro sem tradução corrente ficam como são (`Pix`, `Boleto`, `Cnab`, `Cpf`).
- Valores monetários sempre em `Money`, nunca em ponto flutuante.
- A mesma classe tem o mesmo significado em todos os documentos. Se um exemplo precisar de outro conceito, usa outro nome.
- Alíquotas, limites e prazos são ilustrativos (ver seção 7).

## 3. GoF e clássicos (`docs/coding/gof`)

A linguagem de cada exemplo é mantida. Os diagramas genéricos não mudam; só o texto e o código da seção Exemplo.

### 3.1 Visão geral

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Abstract Factory | Botões e checkboxes nativos por sistema operacional | Família de arquivos CNAB por banco parceiro | trocar | genérico |
| Builder | `HttpRequest` com cabeçalhos e timeout opcionais | Cobrança Pix imutável com campos opcionais | trocar | genérico |
| Factory Method | Notificação por e-mail ou SMS | Processador de transferência que cria a instrução de Pix ou TED | trocar | genérico |
| Prototype | Formas pré-configuradas de um editor gráfico | Pagamento favorito clonado para um novo agendamento | trocar | genérico |
| Singleton | `AppConfig` carregado do disco | Calendário de dias úteis e feriados bancários | ajustar | genérico |
| Factory | Notificador escolhido pela preferência do usuário | Meio de pagamento escolhido no checkout | trocar | redesenhar |
| Object Pool | Pool de conexões de banco de dados | Pool de sessões de HSM para assinar mensagens | ajustar | genérico |
| Telescoping Constructor | `NutritionFacts` | `Boleto` com encargos opcionais | trocar | redesenhar |
| Adapter | SDK `AcmePayClient` atrás de `PaymentGateway` | SDK de um parceiro de Pix atrás de `PixGateway` | ajustar | genérico |
| Bridge | Tipo de mensagem × canal de envio | Tipo de cobrança × trilho de liquidação | trocar | genérico |
| Composite | Arquivos e pastas | Carteira de investimentos com subcarteiras | trocar | genérico |
| Decorator | Canais extras de notificação | Verificações empilhadas sobre o serviço de transferência | trocar | genérico |
| Facade | `OrderFacade` (estoque, pagamento, entrega) | `PixTransferFacade` (DICT, antifraude, ledger, SPI) | trocar | genérico |
| Flyweight | Um milhão de árvores em um jogo | Milhões de lançamentos de cartão que compartilham o estabelecimento | trocar | genérico |
| Proxy | Imagem em alta resolução carregada sob demanda | Consulta ao bureau de crédito sob demanda e com cache | trocar | genérico |
| Private Class Data | `CircleData` | `CardData` somente leitura | trocar | genérico |
| Chain of Responsibility | Alçadas de reembolso de despesas | Alçadas de aprovação de crédito | ajustar | genérico |
| Command | Editor de texto com desfazer | Lançamento no ledger com estorno | trocar | genérico |
| Interpreter | Regras booleanas de promoção | Regras booleanas de antifraude | trocar | genérico |
| Iterator | Playlist em ordem normal ou aleatória | Extrato paginado por cursor | trocar | genérico |
| Mediator | Sala de chat | Câmara de compensação entre participantes | trocar | genérico |
| Memento | Histórico de um editor de texto | Histórico de uma simulação de empréstimo | trocar | genérico |
| Observer | Mudança de estoque avisa e-mail e painel | Pix recebido avisa push, webhook e conciliação | trocar | genérico |
| State | Pedido de e-commerce | Ciclo de vida de uma cobrança Pix | trocar | genérico |
| Strategy | Cálculo de frete | Sistema de amortização (SAC ou Price) | trocar | genérico |
| Template Method | Importação de CSV e JSON | Processamento de retorno CNAB 240 e 400 | trocar | genérico |
| Visitor | Área e exportação de formas geométricas | Imposto e informe de rendimentos por tipo de ativo | trocar | genérico |
| Null Object | `NullLogger` | `NoFeePolicy` para contas isentas | trocar | genérico |

### 3.2 Creational

#### Abstract Factory

- **Hoje (TypeScript):** `GUIFactory` cria `Button` e `Checkbox` com a aparência do sistema operacional.
- **Cenário proposto:** a fintech troca arquivos de cobrança com vários bancos parceiros, e cada banco tem seu layout CNAB. A fábrica do banco é escolhida uma vez e entrega um gerador de remessa e um leitor de retorno que combinam entre si.
- **Mapeamento:** `AbstractFactory` → `CnabFactory`; `ConcreteFactory` → `BankACnabFactory`, `BankBCnabFactory`; `AbstractProduct` → `RemessaWriter`, `RetornoParser`; `Client` → `BillingBatchService`.
- **Prosa a alinhar:** a Descrição cita "componentes de UI no estilo Windows ou Mac" e os Problemas citam "um botão de um tema com uma caixa de diálogo de outro". O equivalente é gerar a remessa no layout de um banco e ler o retorno no layout de outro.

#### Builder

- **Hoje (Java):** `HttpRequest.Builder` com URL obrigatória e cabeçalhos, timeout e corpo opcionais.
- **Cenário proposto:** uma cobrança Pix tem valor e chave do recebedor obrigatórios, e expiração, multa, juros, desconto e mensagem ao pagador opcionais. O builder valida as combinações (por exemplo, multa só com vencimento) e devolve um `PixCharge` imutável.
- **Mapeamento:** `Product` → `PixCharge`; `Builder` → `PixCharge.Builder`; `build()` valida e gera o `txid`.
- **Prosa a alinhar:** nada obrigatório. O "documento em HTML, Markdown ou PDF" da Descrição é ilustração genérica.

#### Factory Method

- **Hoje (TypeScript):** `NotificationService` com fluxo comum, e subclasses que criam `EmailNotifier` ou `SmsNotifier`.
- **Cenário proposto:** toda transferência segue o mesmo fluxo (validar saldo, criar a instrução, registrar no ledger), mas a instrução varia conforme o trilho. Cada subclasse decide qual `PaymentInstruction` criar.
- **Mapeamento:** `Creator` → `TransferProcessor` (método `process()` com o fluxo comum e `createInstruction()` abstrato); `ConcreteCreator` → `PixTransferProcessor`, `TedTransferProcessor`; `Product` → `PaymentInstruction`; `ConcreteProduct` → `PixInstruction`, `TedInstruction`.

#### Prototype

- **Hoje (TypeScript):** formas pré-configuradas clonadas ao serem arrastadas para a tela.
- **Cenário proposto:** o cliente salva pagamentos favoritos (aluguel, mesada). Para agendar um novo, o app clona o favorito e muda só a data e o valor, sem reconstruir dados do recebedor e descrição.
- **Mapeamento:** `Prototype` → `PaymentOrder` com `clone()`; `ConcretePrototype` → `PixPaymentOrder`, `BoletoPaymentOrder`; `PrototypeRegistry` → `FavoritePayments`.

#### Singleton

- **Hoje (Java):** `AppConfig` carregado uma vez de `app.properties`.
- **Cenário proposto:** o calendário de dias úteis e feriados bancários é carregado uma vez e consultado por todos os módulos que calculam vencimento, liquidação de TED e prazo de compensação de boleto.
- **Mapeamento:** `Singleton` → `BusinessCalendar` com `isBusinessDay(date)` e `nextBusinessDay(date)`.
- **Por que ajustar e não trocar:** o exemplo atual é técnico e correto. A mudança é só de assunto. Dados que mudam em produção (tarifas, limites) não servem de exemplo, porque um singleton com estado mutável é justamente o risco que o documento descreve.

#### Factory

- **Hoje (TypeScript):** `NotifierFactory.create(channel)` devolve e-mail, SMS ou push.
- **Cenário proposto:** no checkout, o comprador escolhe Pix, boleto ou cartão. A fábrica traduz essa escolha no `PaymentMethod` correto, e o restante do código só chama `charge()`.
- **Mapeamento:** fábrica → `PaymentMethodFactory.create(type)`; produto → `PaymentMethod`; produtos concretos → `PixPayment`, `BoletoPayment`, `CardPayment`.
- **Diagrama (redesenhar):** hoje usa `ShapeFactory`, `Shape`, `Circle` e `Square`. Trocar pelas classes acima.

#### Object Pool

- **Hoje (Python):** `ConnectionPool` de conexões com o banco de dados.
- **Cenário proposto:** toda mensagem enviada ao SPI precisa ser assinada em um HSM. Abrir uma sessão no HSM é caro e o equipamento aceita poucas sessões simultâneas, então elas ficam em um pool limitado.
- **Mapeamento:** `ObjectPool` → `HsmSessionPool` com `acquire()` e `release()`; `Reusable` → `HsmSession`; `Client` → `MessageSigner`.
- **Por que ajustar e não trocar:** pool de conexões é o exemplo canônico e a estrutura do código não muda. Se o HSM parecer exótico demais, a alternativa é manter o pool de conexões como está.

#### Telescoping Constructor

- **Hoje (Java):** `NutritionFacts` com porção obrigatória e calorias, gordura e sódio opcionais.
- **Cenário proposto:** um `Boleto` exige valor e vencimento. Multa, juros ao dia e desconto por antecipação são opcionais, com padrão zero.
- **Mapeamento:** construtores encadeados `Boleto(amount, dueDate)`, `Boleto(amount, dueDate, fine)`, `Boleto(amount, dueDate, fine, dailyInterest)`, `Boleto(amount, dueDate, fine, dailyInterest, discount)`.
- **Diagrama (redesenhar):** hoje mostra `NutritionFacts`. Trocar por `Boleto`.
- **Efeito colateral bom:** o exemplo passa a fazer par com o Builder (`PixCharge`), que resolve o mesmo problema. Vale citar isso nos Padrões relacionados.

### 3.3 Structural

#### Adapter

- **Hoje (TypeScript):** `PaymentGateway` em reais e o SDK `AcmePayClient` em centavos, com código de status.
- **Cenário proposto:** o mesmo, com vocabulário de Pix. A interface interna `PixGateway.send(key, amount)` trabalha com `Money`, e o SDK do parceiro de liquidação recebe centavos e devolve um código de status.
- **Mapeamento:** `Target` → `PixGateway`; `Adaptee` → `PartnerPixClient`; `Adapter` → `PartnerPixAdapter`.

#### Bridge

- **Hoje (TypeScript):** tipos de mensagem (alerta, lembrete) × canais (e-mail, SMS).
- **Cenário proposto:** tipos de cobrança (avulsa, recorrente) × trilhos de liquidação (Pix, boleto, cartão). Cada cobrança delega a liquidação a um trilho, o que evita classes como `RecurringPixCharge` e `OneTimeBoletoCharge`.
- **Mapeamento:** `Abstraction` → `Charge`; `RefinedAbstraction` → `OneTimeCharge`, `RecurringCharge`; `Implementor` → `SettlementRail`; `ConcreteImplementor` → `PixRail`, `BoletoRail`, `CardRail`.
- **Prosa a alinhar:** a Descrição cita `WindowsCircle`, `LinuxCircle` e "forma e plataforma de renderização".

#### Composite

- **Hoje (TypeScript):** arquivos e pastas com `getSize()`.
- **Cenário proposto:** uma carteira de investimentos contém ativos e subcarteiras (por exemplo, "Reserva" e "Aposentadoria"). O cliente pede o valor atual de qualquer nó sem saber se é um ativo ou uma carteira.
- **Mapeamento:** `Component` → `Holding` com `currentValue()`; `Leaf` → `Asset`; `Composite` → `Portfolio`.

#### Decorator

- **Hoje (TypeScript):** `EmailNotifier` decorado com SMS e Slack.
- **Cenário proposto:** o serviço de transferência básico só movimenta o dinheiro. Antifraude, limite noturno e trilha de auditoria são camadas empilhadas conforme o tipo de conta, sem uma subclasse para cada combinação.
- **Mapeamento:** `Component` → `TransferService`; `ConcreteComponent` → `BasicTransferService`; `Decorator` → `TransferDecorator`; `ConcreteDecorator` → `FraudCheckDecorator`, `NightLimitDecorator`, `AuditDecorator`.

#### Facade

- **Hoje (TypeScript):** `OrderFacade.placeOrder` coordena estoque, pagamento e entrega.
- **Cenário proposto:** enviar um Pix exige resolver a chave no DICT, passar pelo antifraude, debitar o ledger e enviar a mensagem ao SPI. `PixTransferFacade.send()` expõe uma única operação.
- **Mapeamento:** `Facade` → `PixTransferFacade`; subsistemas → `DictClient`, `FraudService`, `LedgerService`, `SpiClient`.

#### Flyweight

- **Hoje (Java):** `TreeType` (nome, cor, textura) compartilhado por um milhão de árvores.
- **Cenário proposto:** o extrato de cartões mantém milhões de lançamentos em memória para conciliação. Nome, MCC e logotipo do estabelecimento são compartilhados; valor, data e portador ficam em cada lançamento.
- **Mapeamento:** `Flyweight` → `MerchantInfo` (intrínseco); `FlyweightFactory` → `MerchantInfoFactory`; contexto extrínseco → `CardEntry` (valor, data, portador).

#### Proxy

- **Hoje (TypeScript):** `ImageProxy` carrega a imagem do disco só quando é exibida.
- **Cenário proposto:** a consulta ao bureau de crédito é lenta e cobrada por chamada. O proxy só consulta quando a análise realmente precisa do score e guarda o resultado para as chamadas seguintes.
- **Mapeamento:** `Subject` → `CreditBureau`; `RealSubject` → `RemoteCreditBureau`; `Proxy` → `CachingCreditBureauProxy`.

#### Private Class Data

- **Hoje (Java):** `Circle` guarda raio, cor e origem em `CircleData`, que só permite leitura.
- **Cenário proposto:** um `Card` recebe token do número, validade e nome do portador na emissão, e esses valores não podem mudar depois. Os dados ficam em `CardData`, e métodos como `isExpired()` só leem.
- **Mapeamento:** `MainClass` → `Card`; `DataClass` → `CardData`.

### 3.4 Behavioral

#### Chain of Responsibility

- **Hoje (TypeScript):** reembolso de despesas aprovado por líder, gerente ou diretoria conforme o valor.
- **Cenário proposto:** a mesma estrutura, para concessão de crédito. O analista aprova até R$ 5.000, o coordenador até R$ 50.000 e o comitê de crédito acima disso.
- **Mapeamento:** `Handler` → `CreditApprover`; `ConcreteHandler` → `Analyst`, `Coordinator`, `CreditCommittee`; `Request` → `CreditProposal`.

#### Command

- **Hoje (TypeScript):** `InsertTextCommand` com `undo()` sobre um `TextEditor`.
- **Cenário proposto:** cada movimentação no ledger é um comando com `execute()` e `undo()`. O histórico permite estornar a última operação, e os mesmos comandos servem para transferências agendadas.
- **Mapeamento:** `Command` → `LedgerCommand`; `ConcreteCommand` → `DebitCommand`, `CreditCommand`; `Receiver` → `Account`; `Invoker` → `LedgerHistory`.
- **Cuidado ao escrever:** em contabilidade o estorno é um lançamento novo, e não a remoção do original. O `undo()` deve gerar o lançamento inverso.

#### Interpreter

- **Hoje (TypeScript):** `cliente_vip AND (valor_alto OR primeira_compra)` avaliada contra um pedido.
- **Cenário proposto:** o antifraude avalia regras como `valor_alto AND (dispositivo_novo OR horario_noturno)` contra os dados de cada transação. A estrutura do código não muda.
- **Mapeamento:** `AbstractExpression` → `Expression`; `TerminalExpression` → `Variable`; `NonterminalExpression` → `And`, `Or`; `Context` → mapa com os sinais da transação.

#### Iterator

- **Hoje (TypeScript):** `Playlist` percorrida em ordem normal ou aleatória.
- **Cenário proposto:** o extrato de uma conta tem milhares de lançamentos e a API devolve páginas com cursor. O consumidor só chama `hasNext()` e `next()`, e o iterador busca a próxima página quando a atual acaba.
- **Mapeamento:** `Aggregate` → `Statement`; `Iterator` → `StatementIterator`; `ConcreteIterator` → `PagedStatementIterator`.
- **Diferença em relação ao atual:** hoje o exemplo mostra dois iteradores sobre a mesma coleção. Para manter esse ponto, dá para oferecer também um `ReverseStatementIterator` (do mais recente para o mais antigo).

#### Mediator

- **Hoje (TypeScript):** `ChatRoom` repassa mensagens entre usuários.
- **Cenário proposto:** os bancos participantes não enviam ordens de pagamento diretamente uns aos outros. A câmara de compensação recebe a ordem e a entrega ao banco de destino.
- **Mapeamento:** `Mediator` → `ClearingHouse`; `ConcreteMediator` → `InstantPaymentClearing`; `Colleague` → `ParticipantBank`.

#### Memento

- **Hoje (TypeScript):** `Editor` salva conteúdo e posição do cursor em `EditorMemento`.
- **Cenário proposto:** em uma simulação de empréstimo, o cliente altera valor, prazo e data do primeiro vencimento, e pode voltar às simulações anteriores.
- **Mapeamento:** `Originator` → `LoanSimulation`; `Memento` → `SimulationSnapshot` (valor, prazo, taxa); `Caretaker` → `SimulationHistory`.

#### Observer

- **Hoje (TypeScript):** `Inventory` avisa e-mail e painel quando o estoque muda.
- **Cenário proposto:** quando um Pix é creditado, o app precisa enviar um push, o lojista precisa receber um webhook e a conciliação precisa registrar o recebimento, sem que o serviço de recebimento conheça esses canais.
- **Mapeamento:** `Subject` → `PixReceiptService`; `Observer` → `PixReceivedListener`; `ConcreteObserver` → `PushNotifier`, `MerchantWebhook`, `ReconciliationRecorder`.

#### State

- **Hoje (TypeScript):** pedido em "aguardando pagamento", "pago" e "enviado", com `pay()` e `ship()`.
- **Cenário proposto:** uma cobrança Pix passa por "ativa", "paga", "expirada" e "devolvida". `pay()` só vale para a cobrança ativa e `refund()` só para a paga.
- **Mapeamento:** `Context` → `PixCharge`; `State` → `ChargeState`; `ConcreteState` → `Active`, `Paid`, `Expired`, `Refunded`.

#### Strategy

- **Hoje (TypeScript):** `ShippingStrategy` com frete padrão, expresso e retirada.
- **Cenário proposto:** o simulador de crédito calcula as parcelas pelo sistema de amortização escolhido: SAC (parcelas decrescentes) ou Price (parcelas fixas).
- **Mapeamento:** `Strategy` → `AmortizationStrategy` com `schedule(principal, rate, months)`; `ConcreteStrategy` → `SacAmortization`, `PriceAmortization`; `Context` → `LoanSimulator`.
- **Prosa a alinhar:** a Descrição cita "diferentes formas de calcular frete".

#### Template Method

- **Hoje (Java):** `DataImporter` com subclasses para CSV e JSON.
- **Cenário proposto:** o processamento de um arquivo de retorno bancário é sempre ler, converter em registros, validar e baixar os boletos pagos. Só a leitura e a conversão mudam entre CNAB 240 e CNAB 400.
- **Mapeamento:** `AbstractClass` → `RetornoProcessor` com `process(path)` final; `ConcreteClass` → `Cnab240Processor`, `Cnab400Processor`; hook → `beforeSettle(records)`.
- **Atenção à coerência:** o Abstract Factory também usa CNAB. Os dois exemplos se complementam (um cria a família, o outro define o fluxo), mas convém citar um no outro.

#### Visitor

- **Hoje (TypeScript):** `ShapeVisitor` calcula área e exporta JSON de `Circle` e `Rectangle`.
- **Cenário proposto:** a carteira tem tipos de ativo estáveis (`Cdb`, `Stock`, `FundShare`), e novas operações aparecem com frequência: calcular o imposto devido, gerar o informe de rendimentos. Cada operação é um visitante, e as classes dos ativos não mudam.
- **Mapeamento:** `Element` → `Asset` com `accept(visitor)`; `ConcreteElement` → `Cdb`, `Stock`, `FundShare`; `Visitor` → `AssetVisitor`; `ConcreteVisitor` → `TaxCalculator`, `IncomeReportExporter`.
- **Prosa a alinhar:** a Descrição cita `visitor.visitCircle(this)`.
- **Atenção à coerência:** o Composite também usa a carteira. O par Composite e Visitor é clássico e vale explicitar o vínculo.

#### Null Object

- **Hoje (TypeScript):** `NullLogger` no lugar de um logger opcional.
- **Cenário proposto:** o serviço de transferência aplica uma política de tarifa. Contas isentas recebem uma `NoFeePolicy`, que devolve zero, em vez de o serviço testar se existe política.
- **Mapeamento:** `AbstractObject` → `FeePolicy`; `RealObject` → `PerTransferFeePolicy`; `NullObject` → `NoFeePolicy`.
- **Prosa a alinhar:** o Quando usar cita "um `NullLogger` em testes". Pode ficar, porque continua sendo um uso real do padrão.

## 4. Patterns of Enterprise Application Architecture (`docs/design/poeaa`)

### Domain Logic

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Transaction Script | Script calcula total do pedido com desconto e grava | Script `payBoleto`: valida saldo, debita a conta e grava o pagamento. Diagrama: `PaymentScripts` | trocar | redesenhar |
| Domain Model | `Order` calcula total e impede cancelamento após envio | `CardInvoice` calcula o total e recusa lançamentos depois de fechada. Diagrama: `Customer`, `CardInvoice`, `InvoiceEntry`, `Merchant` | trocar | redesenhar |
| Table Module | Módulo `Orders` soma itens de um conjunto de registros | Módulo `Installments` calcula o saldo devedor a partir das parcelas carregadas. Diagrama: `InstallmentsModule`, `ContractsModule` | trocar | redesenhar |
| Service Layer | `OrderService` usado por REST e por consumidor de fila | `PixTransferService` usado pela API do app e pelo job de transferências agendadas | trocar | redesenhar |

### Data Source Architectural

Nos quatro, o diagrama usa `Person` (nome do livro) e o exemplo usa outra entidade. A proposta unifica.

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Table Data Gateway | `OrderGateway` sobre a tabela `orders`; diagrama com `PersonGateway` | `BoletoGateway` sobre a tabela `boletos`, usado pelos scripts de cobrança | trocar | redesenhar |
| Row Data Gateway | `CustomerGateway`, uma instância por linha; diagrama com `PersonGateway` | `PixKeyGateway`, uma instância por chave Pix cadastrada, e `PixKeyFinder` | trocar | redesenhar |
| Active Record | `Product` aplica desconto e se salva; diagrama com `Person` | `Card` com regras simples (`block()`, `isExpired()`) e `save()` | trocar | redesenhar |
| Data Mapper | `Employee` e tabela `employees` com colunas diferentes; diagrama com `Person` | `Account` com regras de saldo e a tabela legada `contas_correntes`; `AccountMapper` traduz | trocar | redesenhar |

### Object-Relational Behavioral

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Unit of Work | Transferência bancária altera duas contas e cria um lançamento | Já financeiro. Só alinhar os nomes: `Account` e `LedgerEntry` | ajustar | genérico |
| Identity Map | Cobrança e entrega buscam o mesmo `Customer` | Antifraude e verificação de limite carregam a mesma `Account` na mesma requisição e recebem a mesma instância | trocar | genérico |
| Lazy Load | `Customer` com pedidos carregados só na tela de histórico | `Account` com lançamentos carregados só quando o extrato é aberto | trocar | genérico |

### Object-Relational Structural

Os quatro padrões de herança devem usar a mesma hierarquia, como o livro faz com `Player`, para que a comparação entre eles continue direta. Proposta: `PaymentInstruction` com as subclasses `PixTransfer` e `TedTransfer`.

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Identity Field | `Customer` com `id` gerado pelo banco | `Account` com `id` gerado no `INSERT`. Diagrama: `Account`, `AccountTable` | ajustar | redesenhar |
| Inheritance Mappers | `Player`, `Footballer`, `Cricketer` | `AbstractPaymentInstructionMapper`, `PixTransferMapper`, `TedTransferMapper` | trocar | redesenhar |
| Foreign Key Mapping | `Order` pertence a `Customer`; diagrama com `ALBUM` e `TRACK` | `Card` pertence a `Account`, pela coluna `account_id`. Diagrama: `ACCOUNT`, `CARD` | trocar | redesenhar |
| Association Table Mapping | Funcionários e habilidades | Conta conjunta: `ACCOUNT`, `HOLDER` e a tabela de ligação `ACCOUNT_HOLDER` | trocar | redesenhar |
| Dependent Mapping | `Order` e `OrderLine`; diagrama com `Album` e `Track` | `LoanContract` e `Installment`: as parcelas só existem dentro do contrato. `LoanContractMapper` salva as duas | trocar | redesenhar |
| Embedded Value | `Employee` com `Address` embutido | `LedgerEntry` com `Money` embutido (`amount`, `currency` como colunas) | trocar | redesenhar |
| Serialized LOB | Hierarquia de departamentos de um cliente em JSON | `Consent` do Open Finance com a lista de permissões guardada em uma coluna JSON | trocar | redesenhar |
| Single Table Inheritance | Jogadores em uma tabela com discriminador | `payment_instructions` com a coluna `type` e colunas nulas por subclasse | trocar | redesenhar |
| Class Table Inheritance | `PLAYER`, `FOOTBALLER`, `CRICKETER` | `PAYMENT_INSTRUCTION`, `PIX_TRANSFER`, `TED_TRANSFER`, com a mesma chave primária | trocar | redesenhar |
| Concrete Table Inheritance | Uma tabela por classe concreta de jogador | `PIX_TRANSFER` e `TED_TRANSFER`, cada uma repetindo `id`, `amount` e `status` | trocar | redesenhar |

### Object-Relational Metadata Mapping

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Metadata Mapping | `Customer` mapeado por anotações JPA | `Account` mapeada por anotações JPA | ajustar | genérico |
| Query Object | Busca de pedidos por cliente e valor mínimo | Busca no extrato por período, tipo de lançamento e valor mínimo, com filtros opcionais | trocar | genérico |
| Repository | `OrderRepository` com Spring Data | `AccountRepository` (`findByHolderCpf`, `save`). Compartilhado com o DDD | trocar | redesenhar |

### Web Presentation

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Model View Controller | `Product` exibido em HTML e em JSON | O mesmo `Statement` exibido em HTML no internet banking e em JSON para o app | trocar | genérico |
| Page Controller | Página de perfil de usuário | Página de comprovante de Pix (`/receipts/{id}`) | trocar | genérico |
| Front Controller | Servlet que mapeia caminho para command; diagrama com `BookCommand` e `OrderCommand` | Mesmo exemplo. Diagrama: `TransferCommand`, `StatementCommand` | ajustar | redesenhar |
| Template View | Template lista pedidos do cliente | Template lista os lançamentos da fatura do cartão | trocar | genérico |
| Transform View | Lista de produtos em XML convertida por XSLT | Extrato em XML (ISO 20022, `camt.053`) convertido em tabela HTML por XSLT | trocar | genérico |
| Two Step View | Telas devolvem estrutura lógica; renderizador único aplica o estilo | Sem domínio hoje. Basta citar as telas de extrato e de fatura como exemplos | manter | genérico |
| Application Controller | Fluxo de pedido: endereço, pagamento, confirmação | Fluxo de abertura de conta: dados pessoais, documento, selfie, análise | trocar | genérico |

### Distribution

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Remote Facade | App exibe `Order` com itens em uma chamada | App exibe a fatura com seus lançamentos em uma chamada: `InvoiceRemoteFacade`, `InvoiceAssembler`, `InvoiceDTO` | trocar | redesenhar |
| Data Transfer Object | `OrderDTO` com cliente e itens | `AccountSummaryDTO` com saldo, limite e últimos lançamentos, montado por `AccountSummaryAssembler` | trocar | redesenhar |

### Offline Concurrency

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Optimistic Offline Lock | Dois atendentes editam o mesmo cadastro de cliente | Dois analistas alteram o limite de crédito do mesmo cliente; o segundo recebe conflito | ajustar | genérico |
| Pessimistic Offline Lock | Só um redator edita um contrato por vez | Só um analista trabalha em um dossiê de KYC ou em uma contestação por vez | trocar | genérico |
| Coarse-Grained Lock | `Order`, `OrderLine` e `Payment` compartilham a versão | `LoanContract`, `Installment` e `Collateral` compartilham a versão da raiz | trocar | redesenhar |
| Implicit Lock | Supertipo dos mappers adquire o bloqueio; diagrama com `CustomerMapper` | Mesmo exemplo. Diagrama: `AccountMapper` | ajustar | redesenhar |

### Session State

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Client Session State | JWT com usuário e papel | Exemplo técnico, sem domínio. Fica como está | manter | genérico |
| Server Session State | Carrinho de compras em Redis por 30 minutos | Rascunho de transferência (chave de destino, valor, etapa de confirmação) em Redis por 5 minutos | trocar | genérico |
| Database Session State | Cadastro de seguro em várias etapas | Proposta de crédito consignado em várias etapas, retomada de outro dispositivo | ajustar | genérico |

### Base

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Gateway | `ExchangeRateGateway` consulta cotação de moedas para uma loja | Já financeiro. Trocar "loja" por conta global e citar a taxa de câmbio de referência | ajustar | genérico |
| Service Stub | Checkout calcula imposto em serviço remoto; stub com alíquotas fixas | Análise de crédito consulta o bureau; nos testes, `CreditBureauStub` devolve scores fixos. Diagrama: `CreditBureau`, `RemoteCreditBureau`, `CreditBureauStub`, `CreditAnalysisService` | trocar | redesenhar |
| Record Set | Tela de pedidos com total calculado sobre as linhas | Tela de extrato com saldo do período calculado sobre as linhas | trocar | genérico |
| Mapper | Mapper entre cobrança e envio de e-mails | Já próximo. Módulo de faturas de cartão e módulo de notificações | ajustar | genérico |
| Layer Supertype | `Customer`, `Order` e `Product` herdam de `DomainObject` | `Account`, `Card` e `LedgerEntry` herdam de `DomainObject` | trocar | redesenhar |
| Separated Interface | Domínio busca taxa de câmbio; diagrama com `ReportSource` | Exemplo já financeiro. Diagrama: `ExchangeRateProvider` no domínio e `HttpExchangeRateProvider` na infraestrutura | ajustar | redesenhar |
| Registry | `PersonFinder` e `OrderService` | `AccountFinder` e `FeeTable` | trocar | redesenhar |
| Value Object | Período de hospedagem (`DateRange`) | `PixKey` (tipo e valor) que valida o próprio formato. Diagrama: `Account` possui `PixKey`. Compartilhado com o DDD | trocar | redesenhar |
| Money | Parcelamento de 100,00 em 3 vezes sem perder centavos | Já é o exemplo ideal | manter | manter |
| Special Case | `UnknownCustomer` em uma companhia de energia | `UnknownMerchant` para lançamentos de cartão sem estabelecimento identificado. Diagrama: `Merchant`, `KnownMerchant`, `UnknownMerchant`, `MerchantFinder` | trocar | redesenhar |
| Plugin | Gerador de identificadores em memória ou por sequência | Mesmo exemplo, gerando o `endToEndId` das transações | ajustar | genérico |

## 5. Domain-Driven Design (`docs/design/ddd`)

O catálogo tem 41 documentos próprios e 4 padrões compartilhados, que o `sidebars.ts` referencia com links `sidebar-shared` (★). Eles aparecem no catálogo dono do documento: Value Object e Repository (seção 4), Domain Event (seção 6.1) e Anti-Corruption Layer (seção 6.3).

### Putting the Model to Work

No repositório, a pasta deste grupo é `model-in-practice`.

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Bounded Context | Telecom: `Customer` em vendas, cobrança e suporte; diagrama fala em carrinho e pedidos | "Cliente" em Onboarding (proponente com documentos), Crédito (tomador com score e limite) e Cobrança (devedor com parcelas em atraso) | trocar | redesenhar |
| Ubiquitous Language | Logística: "consolidar cargas" e "janela de coleta" | O código tinha `refund()` para tudo. Os especialistas distinguem devolução (Pix), estorno (cartão) e contestação. Viram `PixReturn`, `Reversal` e `Chargeback` | trocar | genérico |
| Continuous Integration | Companhia aérea: `SeatHold` e `SeatRestriction` | Contexto de Cartões: "bloqueio" modelado por duas pessoas como bloqueio do cartão e como pré-autorização. Viram `CardBlock` e `AuthorizationHold` | trocar | genérico |
| Model-Driven Design | Seguros: `Policy`, `Coverage`, `CoveragePeriod` | Crédito: `LoanContract`, `Installment` e `GracePeriod` (carência), com a regra de carência dentro das classes | trocar | genérico |
| Hands-on Modelers | Arquiteta de uma fintech, contexto de Pagamentos, regra de estorno | Já é fintech | manter | genérico |
| Refactoring Toward Deeper Insight | Aluguel de equipamentos: multa por atraso e `GracePolicy` | Fatura em atraso: flags como `isPayroll` e `isRenegotiated` dão lugar a `LateFeePolicy` (multa, juros e dias de tolerância) | trocar | genérico |

### Building Blocks

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Layered Architecture | Sistema de pedidos: controlador, serviço, agregado, repositório | Transferência Pix: `TransferController`, `TransferAppService`, `Account`, `AccountRepository` | trocar | genérico |
| Entity | Cliente muda de endereço e continua o mesmo | Serve para um cliente de banco. Trocar endereço por e-mail e telefone é opcional | manter | manter |
| Domain Service | Transferência entre contas (`FundsTransferService`) | Já financeiro | manter | manter |
| Module | Pacotes `shipping` e `billing` | Pacotes `payments` (`PixTransfer`, `Boleto`) e `ledger` (`Account`, `LedgerEntry`) | trocar | redesenhar |
| Aggregate | `Order` protege o limite de itens | `CardAccount` (raiz) controla as `AuthorizationHold`: a soma das pré-autorizações não passa do limite disponível. Referência a `Customer` só por identidade | trocar | redesenhar |
| Factory | `OrderFactory` impede pedido sem itens ou de cliente bloqueado | `LoanContractFactory` entrega o contrato com o cronograma de parcelas e recusa cliente com restrição | trocar | redesenhar |

### Supple Design

Quatro documentos usam o exemplo das tintas do livro do Evans (`Paint`, `PigmentColor`) como um fio condutor. A troca só faz sentido em bloco. Proposta de fio condutor: `Account` e `Money`.

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Intention-Revealing Interfaces | `paint(Paint)` renomeado para `mixIn` | `Account.process(Money)`, que na verdade bloqueava saldo, renomeado para `placeHold(Money)`. Diagrama: `AccountBefore`, `AccountAfter` | trocar | redesenhar |
| Side-Effect-Free Functions | Mistura de pigmentos em `PigmentColor`; `Paint` só aplica | Cálculo de juros e rateio em `Money` (imutável); o comando `Account.credit` só aplica o resultado | trocar | redesenhar |
| Assertions | Pós-condição de `Paint.mixIn`: volume final é a soma | Pós-condição de `Account.debit`: saldo final é o inicial menos o valor. Invariante: o saldo não fica abaixo do limite | trocar | redesenhar |
| Standalone Classes | `PigmentColor` só conhece números | `Money` só conhece números e moeda; não referencia `Account` nem o ledger | trocar | redesenhar |
| Closure of Operations | `DateRange.intersect` devolve `DateRange` | `Money.plus(Money)` devolve `Money`; `DateRange` pode ficar como segundo exemplo (período de carência) | ajustar | redesenhar |
| Declarative Design | Especificações "fatura vencida" e "de alto valor" | Já financeiro | manter | manter |
| Drawing on Established Formalisms | Partida dobrada: `Account`, `Entry`, `Transaction` | Já financeiro. É a base do ledger do domínio de referência | manter | manter |
| Conceptual Contours | `Invoice` separa preço, imposto e frete | O cálculo da parcela separa juros, IOF e seguro, que mudam por motivos diferentes. Diagrama: `Interest`, `Iof`, `Insurance` | trocar | redesenhar |

### Context Mapping

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Context Map | Varejista: Vendas, Estoque, Faturamento, ERP legado, gateway de pagamento | Conta Digital, Cartões, Crédito, core bancário legado, bureau de crédito (terceiro) e a rede do Pix | trocar | redesenhar |
| Partnership | Catálogo e Busca lançam filtros juntos | Pix e Antifraude lançam juntos o limite noturno: nenhum dos dois entrega sem o outro | trocar | redesenhar |
| Shared Kernel | Cobrança e Assinaturas compartilham `Money`, Plano e Período | Conta Digital e Cartões compartilham `Money`, `Cpf` e o calendário de dias úteis | ajustar | redesenhar |
| Customer/Supplier Development | Entregas depende de Pedidos | Conciliação (downstream) precisa que Pagamentos (upstream) exponha o `endToEndId` e a data de liquidação | trocar | redesenhar |
| Conformist | Checkout adota o modelo da API de frete do transportador | O contexto de Pix adota o modelo de mensagens do arranjo (ISO 20022), definido pelo regulador, sem tradução | trocar | redesenhar |
| Open-host Service | API de Clientes para Marketing, Faturamento, Suporte e parceiros | API de Contas para o app, o internet banking, o backoffice e instituições parceiras de Open Finance | trocar | redesenhar |
| Published Language | Evento `OrderPlaced` em JSON Schema | Evento `PaymentSettled` v1 em JSON Schema, lido por Conciliação e por Notificações | trocar | redesenhar |
| Separate Ways | Fidelidade e Estoque sem integração | Cashback e Câmbio sem integração | trocar | redesenhar |
| Big Ball of Mud | Seguradora com legado de apólices; diagrama cita Pedidos e Clientes | Core bancário legado, cercado por uma Anticorruption Layer; novos contextos de Conta Digital e de Crédito | trocar | redesenhar |

### Distillation

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Core Domain | Logística: otimização de rotas | Fintech de crédito: o core é a decisão de crédito e a precificação por risco. Emissão de boletos, autenticação e contabilidade são comprados | trocar | genérico |
| Generic Subdomains | Seguradora usa provedor de pagamentos, identidade e mensageria | Mesmo raciocínio na fintech de crédito. No diagrama, o rótulo "Pagamentos" vira "Emissão de boletos" | ajustar | redesenhar |
| Domain Vision Statement | Visão do core de roteirização | Visão do core de decisão de crédito: aprovar em minutos, com perda esperada dentro do apetite de risco | trocar | genérico |
| Highlighted Core | Seguradora: `RiskProfile`, `PremiumCalculator`, `UnderwritingRule` | `CreditPolicy`, `RiskScore` e `PricingRule` listados no `CORE.md` | ajustar | genérico |
| Cohesive Mechanisms | Busca de menor caminho (`DijkstraPlanner`, `AStarPlanner`) | O cálculo do CET exige um método numérico. Fica atrás de `RateSolver` (`NewtonRateSolver`, `BisectionRateSolver`), e `LoanOfferService` só o invoca | trocar | redesenhar |
| Segregated Core | Frota: módulo `maintenance-core` | Módulo `credit-decision-core` (`CreditPolicy`, `RiskScore`, `LimitOffer`) separado de cadastro, relatórios regulatórios e integração com o bureau | trocar | genérico |
| Abstract Core | Seguros de automóvel e de vida: `Policy`, `Insurable` | Crédito pessoal e consignado: `CreditProduct` e `Contract` abstratos; os módulos `personal-loan` e `payroll-loan` os especializam | trocar | redesenhar |

### Large-Scale Structure

| Padrão | Hoje | Proposta fintech | Exemplo | Diagrama |
| --- | --- | --- | --- | --- |
| Evolving Order | Logística com quatro equipes | Equipes de Pix, Cartões, Crédito e Conciliação percebem dois níveis: políticas (limites, tarifas, risco) e operações (transferir, liquidar) | trocar | genérico |
| System Metaphor | Roteirização de pacotes como "correio pneumático" | Caso forçado (ver seção 7). Sugestão: manter | manter | genérico |
| Responsibility Layers | Transportadora: Potential, Operations, Policy | Potential (limites concedidos, produtos), Operations (transferências, lançamentos), Policy (tarifas, limites, regras antifraude) | trocar | genérico |
| Knowledge Level | Banco: `Account` e `AccountType` | Já financeiro | manter | manter |
| Pluggable Component Framework | Corretora de seguros: `ProductModule` com cotar, emitir, renovar | Plataforma de produtos financeiros: `ProductModule` com simular, contratar e liquidar, para crédito pessoal, consignado e CDB | ajustar | manter |

## 6. Demais catálogos: só os diagramas concretos

Estes catálogos não têm seção Exemplo. A lista traz apenas os documentos cujo diagrama usa um cenário concreto. Os demais diagramas são genéricos e não mudam.

### 6.1 Microservices Patterns (`docs/architecture/microservices`)

14 de 43 diagramas. O catálogo segue o exemplo de pedidos e restaurantes do microservices.io.

| Padrão | Diagrama hoje | Proposta fintech |
| --- | --- | --- |
| Microservice Architecture | Serviços e bancos de Pedidos e de Entregas | Serviços de Contas, de Pix e de Cartões, cada um com seu banco |
| Decompose by Business Capability | Loja online: Catálogo, Estoque, Pedidos, Entrega | Banco digital: Onboarding, Contas, Pagamentos, Crédito |
| Decompose by Subdomain | Core: Pedidos; Supporting: Entrega; Generic: Pagamentos | Core: Decisão de crédito; Supporting: Conciliação; Generic: Validação de identidade (produto de mercado) |
| Self-contained Service | Serviço de Pedidos com réplica local de restaurantes | Serviço de Pix com réplica local de limites do cliente; a liquidação termina por saga |
| Service per Team | Equipes de Pedidos, Catálogo e Entrega | Equipes de Pix, Cartões e Crédito |
| Database per Service | Serviços e bancos de pedidos e de clientes | Serviços e bancos de contas e de cartões |
| Shared Database | Tabelas de pedidos e de clientes; serviços de pedidos, clientes e pagamentos | Tabelas de contas e de cartões; serviços de contas, cartões e crédito |
| Command-side Replica | Provedor de restaurantes; comando `createOrder()` | Provedor de limites; serviço de transferências com `createTransfer()` |
| API Composition | "Consultar cliente com pedidos recentes" | "Consultar visão geral": saldo no serviço de contas e fatura aberta no serviço de cartões |
| Domain Event | Agregado Pedido emite `PedidoCriado`. Seção Exemplo: `OrderCreated` (Java) | Agregado Cobrança emite `CobrancaPaga`; consumidores: saga de conciliação e visão de extrato. Seção Exemplo: `PixCharge` registra `ChargePaid` |
| Domain-specific Protocol | Player e cliente de e-mail; HLS, SMTP e IMAP | Autorizador de cartões falando ISO 8583 com a bandeira |
| API Gateway | Serviços de produtos, preços, estoque e avaliações | Serviços de contas, Pix, cartões e investimentos; clientes: app, internet banking e parceiros de Open Finance |
| Server-side Page Fragment Composition | Fragmentos: detalhes do livro, avaliações, disponibilidade | Página inicial do internet banking: fragmentos de saldo, fatura e investimentos |
| Client-side UI Composition | Componentes ligados a serviços de produto e estoque | Tela inicial do app: componentes de saldo, cartão e ofertas de crédito |

### 6.2 Enterprise Integration Patterns (`docs/architecture/eip`)

7 de 56 diagramas. O catálogo segue o exemplo de pedidos de widgets e gadgets do livro.

| Padrão | Diagrama hoje | Proposta fintech |
| --- | --- | --- |
| Datatype Channel | Canal de pedidos e canal de faturas | Canal de transferências Pix e canal de boletos |
| Content-Based Router | Pedido roteado para o estoque de widgets ou de gadgets | Instrução de pagamento roteada pelo trilho: conector de Pix, de TED ou de boleto |
| Splitter | Pedido com itens vira uma mensagem por item | Lote de folha de pagamento vira uma mensagem por pagamento |
| Composed Message Processor | Pedido dividido, verificado em dois estoques e reagregado | Lote de pagamentos dividido, roteado por trilho e reagregado em "lote processado" com o status de cada item |
| Scatter-Gather | Cotação com três fornecedores; melhor resposta | Cotação de câmbio com três provedores de liquidez; melhor taxa |
| Normalizer | Parceiros A (CSV), B (XML) e C | Extratos em CNAB 240, OFX e `camt.053` normalizados para o formato comum da conciliação |
| Messaging Gateway | `obterScore(cliente)` | Já financeiro. Manter |

### 6.3 Cloud Design Patterns (`docs/architecture/cloud-design-patterns`)

6 de 44 diagramas, mais a seção Exemplo do Anti-Corruption Layer. Os cenários de drones e de voo e hotel vêm da fonte (Azure Architecture Center).

| Padrão | Diagrama hoje | Proposta fintech |
| --- | --- | --- |
| Choreography | Entrega por drones: ingestão, pacotes, agendador, entrega | Transferência Pix: "transferência solicitada" → antifraude publica "aprovada" → ledger publica "débito efetuado" → conector publica "liquidada" |
| Compensating Transaction | Reservar voo, reservar hotel; compensação cancela o voo | Debitar a conta de origem, enviar ao sistema de liquidação; se o envio falha, a compensação credita a conta de volta |
| Saga | Criar pedido, processar pagamento, reservar estoque | Contratação de empréstimo: criar contrato, reservar funding, desembolsar por Pix. Compensações: liberar funding e cancelar contrato |
| Backends for Frontends | Serviços de catálogo, pedidos e clientes | Serviços de contas, cartões e investimentos |
| Gateway Aggregation | Pedidos, entregas e perfil do cliente | Tela inicial: saldo, fatura aberta e posição de investimentos |
| Gateway Routing | `/busca`, `/carrinho`, `/pedidos`; canário do Checkout v2 | `/contas`, `/pix`, `/cartoes`; canário do Pix v2; extrato por região |
| Anti-Corruption Layer | Diagrama genérico. Seção Exemplo: contexto de Pedidos consulta clientes em um ERP legado (`CustomerDirectory`) | Seção Exemplo: contexto de Conta Digital consulta contas no core bancário legado, com campos crípticos e status numéricos, por meio de `AccountDirectory` |

### 6.4 Patterns of Distributed Systems (`docs/architecture/distributed-systems`)

Nenhum dos 29 diagramas é concreto. Nada a fazer.

### 6.5 AI Agent Design Patterns (`docs/ai/agent-patterns`)

7 de 15 diagramas. O catálogo reúne duas fontes: 2 dos 6 padrões do guia da Microsoft (Handoff e Magentic Orchestration) e 5 dos 9 do guia do Google Cloud.

| Padrão | Diagrama hoje | Proposta fintech |
| --- | --- | --- |
| Handoff Orchestration | Triagem passa para agente de infraestrutura ou financeiro | Atendimento do banco: triagem passa para o agente de cartões ou para o agente de Pix |
| Magentic Orchestration | Resposta a incidente: diagnóstico, infraestrutura, comunicação | Investigação de alerta de fraude: agente de transações, agente de cadastro e agente de comunicação; humano decide o bloqueio |
| Multi-agent Coordinator | Status do pedido, devolução, reembolso | Status de um Pix, contestação de compra no cartão, devolução de Pix |
| Multi-agent Hierarchical Task Decomposition | Coleta de dados, análise, redação do relatório | Análise de crédito de empresa: coleta de balanços, análise de risco, redação do parecer |
| Multi-agent Swarm | Agentes de mercado, engenharia e financeiro; especificação final | Comitê de crédito: agentes de risco, comercial e compliance; parecer final |
| Human-in-the-loop | Agente de anonimização, revisão externa, agente de liberação | Agente prepara a comunicação de operação suspeita; analista de PLD aprova; agente registra |
| Custom Logic | Verificador de compra, elegibilidade a reembolso, crédito na loja | Contestação de compra: verificador da transação, elegibilidade, crédito provisório na fatura ou negativa |

## 7. Casos forçados e pontos de atenção

### Decisões a confirmar na onda 0

Propostas como padrão para as próximas ondas. Qualquer uma pode ser revista na revisão do PR da onda 0, antes de a onda correspondente começar.

| Ponto | Decisão |
| --- | --- |
| Exemplo das tintas (DDD, Supple Design) | Trocar em bloco por `Account` e `Money`, nos quatro documentos, pelo mesmo subagente |
| Hierarquia `Player` (PoEAA) | Trocar em bloco por `PaymentInstruction`, `PixTransfer` e `TedTransfer`, nos quatro padrões de herança |
| Cenários que vêm da fonte (drones, voo e hotel, restaurantes, widgets) | Trocar, e dizer na legenda do diagrama que a fonte usa outro cenário |
| System Metaphor, Two Step View, Client Session State | Manter como estão |
| Singleton e Object Pool | Ajustar só o assunto (`BusinessCalendar`, `HsmSessionPool`), mantendo a estrutura do código |
| "Pagamentos" como subdomínio genérico | Trocar o rótulo e reler o texto ao redor |

### Pontos de atenção

- **Singleton e Object Pool.** São padrões de infraestrutura. O cenário financeiro proposto é só uma roupa nova para o mesmo código. Se a prioridade for clareza para quem está aprendendo o padrão, manter `AppConfig` e o pool de conexões é defensável.
- **System Metaphor (DDD).** O documento é sobre metáforas, e a do correio pneumático funciona justamente por ser de fora do domínio. Uma metáfora financeira para um sistema financeiro confunde. Sugestão: manter.
- **Two Step View e Client Session State (PoEAA).** Exemplos puramente técnicos, sem domínio. Não há o que trocar.
- **Exemplo das tintas (DDD, Supple Design).** É o exemplo do livro, reconhecível por quem leu. A troca por `Account` e `Money` funciona, mas tem que ser feita nos quatro documentos de uma vez. Trocar só um quebra o fio condutor.
- **Hierarquia `Player` (PoEAA).** Mesmo caso: os quatro padrões de herança precisam da mesma hierarquia nova.
- **Cenários da fonte.** Drones (Choreography), voo e hotel (Compensating Transaction), pedidos e restaurantes (microservices.io), widgets e gadgets (EIP) são os exemplos das fontes originais. Trocar afasta o documento da referência linkada. Vale uma frase na legenda do diagrama dizendo que a fonte usa outro cenário.
- **"Pagamentos" como subdomínio genérico.** Dois diagramas (Decompose by Subdomain e Generic Subdomains) tratam pagamentos como genérico. Em uma fintech de pagamentos isso é o core. A proposta troca o rótulo, mas o texto ao redor precisa ser relido.
- **Estorno não é desfazer.** No Command e em qualquer exemplo com ledger, a reversão é um lançamento novo. O código de exemplo deve refletir isso.
- **Excesso de Pix.** O Pix aparece em muitos cenários porque é o caso mais familiar. Nos padrões vizinhos do GoF, a proposta alterna entre Pix, boleto, cartão, crédito e investimentos para os exemplos não parecerem o mesmo. Ao escrever o código, manter essa variedade.
- **Regras e valores reais.** Alíquotas, limites e prazos mudam por regulação. Os exemplos devem usar valores ilustrativos e evitar afirmar regras como fato.

## 8. Plano de execução em ondas

As ondas 0 a 4 estão feitas e aguardam revisão nos PRs indicados. Até os PRs entrarem, a `main` continua com os exemplos da coluna "Hoje".

Cada onda é um PR aberto direto contra a `main`, a partir de uma `main` atualizada, sem empilhar PRs. Dentro de uma onda, há um subagente por grupo, e cada um toca só os arquivos do seu grupo, nas duas línguas. Validação, build e commits ficam com a sessão principal.

| Onda | Escopo | Subagentes | Modelo | Situação |
| --- | --- | --- | --- | --- |
| 0. Preparação | Decisões da seção 7, `DOMINIO-DE-REFERENCIA.md`, convenção no `CLAUDE.md`, padrão-piloto (Strategy) em pt-BR e inglês | nenhum | – | feita (PR #17) |
| 1. GoF | Seção Exemplo dos 27 restantes, 2 diagramas, prosa indicada | 3 (creational, structural, behavioral) | `sonnet` | feita (PR #18) |
| 2. PoEAA | Exemplo e diagrama dos 51 | 10, um por grupo | `sonnet` | feita (PR #19) |
| 3. DDD | Exemplo e diagrama dos 41 | 6, um por grupo | `sonnet` em Building Blocks e Supple Design; `opus` nos 4 grupos narrativos | feita (PR #20) |
| 4. Só diagramas | 33 diagramas e 2 exemplos de Microservices, EIP, Cloud e AI | 4, um por catálogo | `sonnet`; `haiku` no EIP | feita (PR #21) |
| 5. Revisão | Coerência entre catálogos e paridade entre pt-BR e inglês | 1 revisor por catálogo, somente leitura | `opus` | feita (correções nos PRs #18 a #21) |

Regras de execução:

- **Dependências.** A onda 0 vem antes de todas e a 5 depois de todas. As ondas 1 a 4 não se sobrepõem em arquivos e podem rodar em qualquer ordem.
- **Duas línguas no mesmo PR.** O subagente escreve o exemplo em pt-BR e, em seguida, a tradução fiel em inglês: mesmos blocos de código, mesmos links, mesmos títulos. No código, os identificadores são idênticos e só comentários e strings voltadas ao usuário são traduzidos. No Mermaid, traduzem-se rótulos, participantes, notas e comentários `%%`; ids de nó e sintaxe não mudam. Rótulos de `flowchart` com acento, parênteses ou pontuação vão entre aspas, e não entra HTML nos diagramas.
- **Padrões compartilhados.** O documento existe só no catálogo dono, e os outros catálogos apontam para ele pelo `sidebars.ts`. Value Object e Repository são editados na onda 2; Domain Event e Anti-Corruption Layer, na onda 4. O `sidebars.ts` e o `also_in` não mudam.
- **O que não muda.** Títulos, `pattern_slug`, grupos, tags, `sidebars.ts` e `src/data/catalogs.json`. As tabelas das páginas de catálogo (`index.md`) usam a primeira frase da Descrição e só precisam ser regeradas se a "prosa a alinhar" mexer nessa frase (candidatos: Abstract Factory, Bridge, Strategy e Visitor).
- **Brief de cada subagente.** O `DOMINIO-DE-REFERENCIA.md`, o Strategy como modelo, as regras de i18n do `CLAUDE.md`, as linhas da proposta referentes ao grupo e o critério de pronto: `catalog.py validate` do catálogo passando e a lista dos arquivos alterados nas duas árvores.
- **Ao fim de cada onda.** Rodar `validate` do catálogo e `npm run build`, que compila as duas línguas e falha em link quebrado. Abrir o PR com um commit por catálogo e conferir o deploy preview do Netlify.
- **Fora do commit.** A pasta `.claude/` (onde fica o `catalog.py`) é local e nunca entra em commit. Este documento e o `DOMINIO-DE-REFERENCIA.md` são versionados na raiz do repositório.

Comandos de verificação, a partir da raiz do repositório:

```bash
python3 -I .claude/skills/pattern-catalog/scripts/catalog.py validate coding/gof
```

```bash
npm run build
```

Só quando a primeira frase de alguma Descrição mudar:

```bash
python3 -I .claude/skills/pattern-catalog/scripts/catalog.py index coding/gof
```
