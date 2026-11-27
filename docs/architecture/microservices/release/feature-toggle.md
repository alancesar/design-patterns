---
title: Feature Toggle
pattern_slug: feature-toggle
category: Release
tags:
  - Operational Excellence
  - Reliability
source: https://martinfowler.com/articles/feature-toggles.html
sidebar_label: "Feature Toggle"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/microservices/release/feature-toggle.mdx';

# Feature Toggle

## Descrição

Feature Toggle, também chamado de Feature Flag, envolve uma funcionalidade em uma condição que pode ser ligada ou desligada em tempo de execução, sem um novo deploy. O código novo vai para produção desligado, e a decisão de ativá-lo, para todos ou para um grupo de usuários, passa a ser uma mudança de configuração. Assim, implantar uma versão e lançar uma funcionalidade deixam de ser o mesmo evento.

Pete Hodgson classifica os toggles pelo propósito e pela duração: *release toggles* escondem trabalho incompleto e duram dias ou semanas; *experiment toggles* sustentam testes A/B; *ops toggles* funcionam como *kill switch* para desligar uma funcionalidade problemática; e *permissioning toggles* liberam recursos para grupos específicos de clientes. A decisão costuma ficar em um ponto único, que consulta um repositório de configuração e avalia regras como lista de contas liberadas ou porcentagem de usuários.

## Problemas que resolve

- Deploy acoplado ao lançamento, que obriga a decidir no momento do deploy se a funcionalidade já deve aparecer.
- Branches longos para esconder trabalho incompleto, com merges difíceis no fim.
- Falta de um jeito rápido de desligar uma funcionalidade com problema sem reverter o deploy.
- Lançamento para todos de uma vez, sem testar com um grupo pequeno de clientes.

## Quando usar

- Integração contínua com funcionalidades ainda incompletas no tronco principal.
- Lançamentos graduais por funcionalidade, por grupo de clientes ou por porcentagem.
- Testes A/B e experimentos de produto.
- *Kill switch* para funcionalidades de risco, como uma nova forma de pagamento.

## Quando evitar

- Mudanças pequenas e de baixo risco, em que o toggle só acrescenta complexidade.
- Como substituto permanente de configuração ou de regras de permissão, sem prazo para remoção.
- Mudanças de esquema ou de infraestrutura que não podem ser desligadas por uma condição no código.

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Deploy independente do lançamento | Toggles esquecidos viram dívida técnica |
| Desligamento imediato, sem novo deploy | Combinações de toggles multiplicam os caminhos a testar |
| Lançamento gradual por cliente ou porcentagem | A configuração vira parte crítica da produção |
| Experimentos A/B com o mesmo código | Lógica condicional espalhada dificulta a leitura |

- **Remoção planejada:** todo release toggle deve nascer com prazo e responsável pela remoção. Algumas equipes limitam quantos toggles ativos cada serviço pode ter.
- **Decisão em um ponto:** centralize a avaliação em um serviço ou biblioteca e passe a decisão adiante, em vez de espalhar `if` pelo código.
- **Testes:** teste os dois estados de cada toggle que vai a produção, e não todas as combinações possíveis.
- **Atribuição estável:** em liberações por porcentagem, use um hash do identificador do cliente para que a mesma conta sempre caia no mesmo grupo.

## Diagrama

<Diagram />

O mesmo artefato roda em produção com os dois caminhos. A configuração decide qual deles cada conta vê.

## Exemplo

A conta digital da fintech vai lançar o Pix parcelado. O código já está em produção, mas o checkout só mostra a nova opção para as contas que o toggle `pix-installments` libera: uma lista de contas internas e 30% das demais, escolhidas por um hash estável do identificador. Se algo der errado, a equipe desliga o toggle e todos voltam a ver só o Pix à vista.

<Tabs groupId="lang" queryString>
<TabItem value="java" label="Java">

```java
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

record Toggle(boolean enabled, int rolloutPercent, Set<String> allowlist) {}

class FeatureToggles {
    private final Map<String, Toggle> toggles = new HashMap<>();

    void define(String name, Toggle toggle) {
        toggles.put(name, toggle);
    }

    boolean isEnabled(String name, String accountId) {
        Toggle t = toggles.get(name);
        if (t == null || !t.enabled()) {
            return false; // toggle desconhecido ou desligado: comportamento atual
        }
        if (t.allowlist().contains(accountId)) {
            return true;
        }
        return bucket(name + ":" + accountId) < t.rolloutPercent();
    }

    // FNV-1a de 32 bits: a mesma conta cai sempre no mesmo grupo (0 a 99)
    static int bucket(String key) {
        int hash = 0x811c9dc5;
        for (byte b : key.getBytes(StandardCharsets.UTF_8)) {
            hash ^= (b & 0xff);
            hash *= 0x01000193;
        }
        return (int) (Integer.toUnsignedLong(hash) % 100);
    }
}

class PixCheckout {
    private final FeatureToggles toggles;

    PixCheckout(FeatureToggles toggles) {
        this.toggles = toggles;
    }

    List<String> paymentOptions(String accountId) {
        if (toggles.isEnabled("pix-installments", accountId)) {
            return List.of("pix", "pix-installments");
        }
        return List.of("pix");
    }
}

public class FeatureToggleDemo {
    public static void main(String[] args) {
        FeatureToggles toggles = new FeatureToggles();
        toggles.define("pix-installments", new Toggle(true, 30, Set.of("acc-001")));
        PixCheckout checkout = new PixCheckout(toggles);

        for (String id : List.of("acc-001", "acc-002", "acc-003", "acc-004", "acc-005")) {
            System.out.println(id + ": " + String.join(", ", checkout.paymentOptions(id)));
        }

        // kill switch: desliga a funcionalidade sem novo deploy
        toggles.define("pix-installments", new Toggle(false, 30, Set.of("acc-001")));
        System.out.println("acc-001: " + String.join(", ", checkout.paymentOptions("acc-001")));
    }
}

// acc-001: pix, pix-installments
// acc-002: pix
// acc-003: pix
// acc-004: pix, pix-installments
// acc-005: pix
// acc-001: pix
```

</TabItem>
<TabItem value="python" label="Python">

```python
from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List


@dataclass(frozen=True)
class Toggle:
    enabled: bool
    rollout_percent: int
    allowlist: FrozenSet[str] = field(default_factory=frozenset)


class FeatureToggles:
    def __init__(self) -> None:
        self._toggles: Dict[str, Toggle] = {}

    def define(self, name: str, toggle: Toggle) -> None:
        self._toggles[name] = toggle

    def is_enabled(self, name: str, account_id: str) -> bool:
        t = self._toggles.get(name)
        if t is None or not t.enabled:
            return False  # toggle desconhecido ou desligado: comportamento atual
        if account_id in t.allowlist:
            return True
        return bucket(f"{name}:{account_id}") < t.rollout_percent


def bucket(key: str) -> int:
    # FNV-1a de 32 bits: a mesma conta cai sempre no mesmo grupo (0 a 99)
    h = 0x811C9DC5
    for b in key.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h % 100


class PixCheckout:
    def __init__(self, toggles: FeatureToggles) -> None:
        self._toggles = toggles

    def payment_options(self, account_id: str) -> List[str]:
        if self._toggles.is_enabled("pix-installments", account_id):
            return ["pix", "pix-installments"]
        return ["pix"]


toggles = FeatureToggles()
toggles.define("pix-installments", Toggle(True, 30, frozenset({"acc-001"})))
checkout = PixCheckout(toggles)

for account_id in ["acc-001", "acc-002", "acc-003", "acc-004", "acc-005"]:
    print(f"{account_id}: {', '.join(checkout.payment_options(account_id))}")

# kill switch: desliga a funcionalidade sem novo deploy
toggles.define("pix-installments", Toggle(False, 30, frozenset({"acc-001"})))
print(f"acc-001: {', '.join(checkout.payment_options('acc-001'))}")
# acc-001: pix, pix-installments
# acc-002: pix
# acc-003: pix
# acc-004: pix, pix-installments
# acc-005: pix
# acc-001: pix
```

</TabItem>
<TabItem value="go" label="Go">

```go
package main

import (
	"fmt"
	"hash/fnv"
	"strings"
)

type Toggle struct {
	Enabled        bool
	RolloutPercent uint32
	Allowlist      map[string]bool
}

type FeatureToggles struct {
	toggles map[string]Toggle
}

func NewFeatureToggles() *FeatureToggles {
	return &FeatureToggles{toggles: map[string]Toggle{}}
}

func (f *FeatureToggles) Define(name string, t Toggle) {
	f.toggles[name] = t
}

func (f *FeatureToggles) IsEnabled(name, accountID string) bool {
	t, ok := f.toggles[name]
	if !ok || !t.Enabled {
		return false // toggle desconhecido ou desligado: comportamento atual
	}
	if t.Allowlist[accountID] {
		return true
	}
	return bucket(name+":"+accountID) < t.RolloutPercent
}

// FNV-1a de 32 bits: a mesma conta cai sempre no mesmo grupo (0 a 99)
func bucket(key string) uint32 {
	h := fnv.New32a()
	h.Write([]byte(key))
	return h.Sum32() % 100
}

type PixCheckout struct {
	toggles *FeatureToggles
}

func (c PixCheckout) PaymentOptions(accountID string) []string {
	if c.toggles.IsEnabled("pix-installments", accountID) {
		return []string{"pix", "pix-installments"}
	}
	return []string{"pix"}
}

func main() {
	toggles := NewFeatureToggles()
	toggles.Define("pix-installments", Toggle{Enabled: true, RolloutPercent: 30, Allowlist: map[string]bool{"acc-001": true}})
	checkout := PixCheckout{toggles: toggles}

	for _, id := range []string{"acc-001", "acc-002", "acc-003", "acc-004", "acc-005"} {
		fmt.Printf("%s: %s\n", id, strings.Join(checkout.PaymentOptions(id), ", "))
	}

	// kill switch: desliga a funcionalidade sem novo deploy
	toggles.Define("pix-installments", Toggle{Enabled: false, RolloutPercent: 30, Allowlist: map[string]bool{"acc-001": true}})
	fmt.Printf("acc-001: %s\n", strings.Join(checkout.PaymentOptions("acc-001"), ", "))
}

// acc-001: pix, pix-installments
// acc-002: pix
// acc-003: pix
// acc-004: pix, pix-installments
// acc-005: pix
// acc-001: pix
```

</TabItem>
</Tabs>

## Padrões relacionados

- [Canary Release](/architecture/microservices/release/canary-release) — liberação gradual por versão do serviço, em vez de por funcionalidade.
- [Blue-Green Deployment](/architecture/microservices/release/blue-green-deployment) — troca de versão sem indisponibilidade; o toggle decide quando a funcionalidade aparece.
- [Externalized Configuration](/architecture/cloud-design-patterns/deployment-and-topology/external-configuration-store) — o repositório de onde os toggles são lidos em tempo de execução.
- [Log Deployments and Changes](/architecture/microservices/observability/log-deployments-and-changes) — registrar mudanças de toggle ajuda a correlacionar incidentes.
- [Strategy](/coding/gof/behavioral/strategy) — troca o comportamento por trás do toggle sem espalhar condicionais.

## Referência

- [Pete Hodgson — Feature Toggles (aka Feature Flags), martinfowler.com](https://martinfowler.com/articles/feature-toggles.html)
