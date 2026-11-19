---
title: Process Containment
pattern_slug: process-containment
category: Security
tags:
  - Security
source: https://k8spatterns.com/
sidebar_label: "Process Containment"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/security/process-containment.mdx';

# Process Containment

## Descrição

O padrão Process Containment aplica o princípio do menor privilégio a cada contêiner, restringindo o processo apenas às permissões de que ele realmente precisa para rodar. Mesmo com análise estática de código, varredura de imagens e de dependências, nenhuma verificação garante a ausência total de vulnerabilidades, então a configuração do Kubernetes funciona como mais uma linha de defesa: se um invasor comprometer a aplicação, ele continua preso dentro da fronteira definida para o processo.

Essas restrições são declaradas no `securityContext` do Pod (vale para todos os contêineres e volumes) e do contêiner (vale só para ele, e prevalece em caso de conflito). As medidas mais comuns são rodar com um usuário não root (`runAsNonRoot`, `runAsUser`), impedir a escalada de privilégios (`allowPrivilegeEscalation: false`), evitar contêineres `privileged`, descartar todas as capabilities do Linux e devolver só as necessárias, e montar o sistema de arquivos raiz como somente leitura. Perfis de `seccompProfile` e `seLinuxOptions` limitam ainda mais as chamadas de sistema e o acesso a objetos.

Como configurar isso Pod a Pod é sujeito a erro humano, o administrador do cluster impõe padrões mínimos por namespace com Pod Security Standards (perfis Privileged, Baseline e Restricted, cumulativos) e o controlador Pod Security Admission, que age por labels no namespace em três modos: `warn`, `audit` e `enforce`.

## Problemas que resolve

- Um invasor que explora uma falha na aplicação e tenta assumir o controle do nó ou do cluster
- Contêineres que rodam como root por padrão, ou que obtêm privilégios de root por escalada
- Conjunto padrão de capabilities do runtime, mais generoso do que a maioria dos processos precisa
- Escrita no sistema de arquivos do contêiner para adulterar configuração ou instalar executáveis
- Configurações de segurança inconsistentes entre equipes, dependentes de quem escreve cada manifesto

## Quando usar

- Em praticamente toda carga de trabalho em produção, como configuração padrão
- Quando a aplicação é stateless, não escreve em disco local e não precisa de privilégios especiais
- Para impor um nível mínimo de segurança em todos os Pods de um namespace de forma centralizada
- Ao conteinerizar aplicações legadas, definindo um usuário não root explícito na imagem

## Quando evitar

- Para contêineres de infraestrutura que exigem acesso amplo ao nó (sistemas de build, plugins de rede ou de armazenamento): eles precisam de perfis mais permissivos, restritos a namespaces confiáveis
- Ao forçar `runAsUser` sem conferir a propriedade dos arquivos da imagem, o que causa falhas de permissão em runtime
- Como substituto de varredura de imagens, revisão de código e controle de acesso: é uma camada adicional, não a única

## Trade-offs

| Ganho | Custo / Risco |
| --- | --- |
| Menor superfície de ataque e contenção de processos comprometidos | Aplicações legadas podem não funcionar sem ajustes (root, escrita em disco, portas baixas) |
| Padrão de segurança aplicado de forma uniforme por namespace | Perfil Restricted tem custo de adoção e exige revisar manifestos existentes |
| Reforça a imutabilidade do contêiner (sistema de arquivos somente leitura) | Aplicações que gravam arquivos temporários precisam de volumes dedicados |
| Falhas de configuração aparecem cedo, com `warn` e `audit` | Descobrir as capabilities realmente necessárias dá trabalho |

- **Adoção gradual:** comece com `warn` e `audit` para ver o impacto antes de ativar `enforce`.
- **Descartar tudo e devolver o necessário:** parta de nenhuma capability e adicione uma a uma; uma alternativa é usar uma porta acima de 1024 em vez de `NET_BIND_SERVICE`.
- **Tarefas como root:** se for preciso ajustar permissões de arquivos, faça isso em um init container de curta duração e mantenha o contêiner da aplicação sem root.
- **Mudança à esquerda:** rode em desenvolvimento com os mesmos padrões de segurança de produção para evitar surpresas tardias.

## Diagrama

<Diagram />

O namespace declara o padrão de segurança exigido; o controlador admite apenas Pods em conformidade, e cada Pod admitido roda com o mínimo de privilégios, sem alcançar o nó.

## Exemplo

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: fintech
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
---
apiVersion: v1
kind: Pod
metadata:
  name: pix-service
  namespace: fintech
  labels:
    app: pix-service
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: pix-service
      image: registry.fintech.example/pix-service:1.4.2
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
      volumeMounts:
        - name: tmp
          mountPath: /tmp
  volumes:
    - name: tmp
      emptyDir: {}
```

O namespace rejeita Pods fora do perfil Baseline e avisa sobre os que não atendem ao Restricted. O Pod roda sem root, sem escalada de privilégios, sem capabilities e com o sistema de arquivos raiz somente leitura, usando um `emptyDir` apenas para arquivos temporários.

## Padrões relacionados

- [Network Segmentation](/architecture/kubernetes-patterns/security/network-segmentation) — complementa a contenção do processo limitando também o que ele alcança pela rede
- [Access Control](/architecture/kubernetes-patterns/security/access-control) — restringe o que o Pod pode fazer na API do Kubernetes, enquanto este padrão restringe o que ele faz no nó
- [Stateless Service](/architecture/kubernetes-patterns/behavioral/stateless-service) — aplicações sem estado local são as que melhor funcionam com sistema de arquivos somente leitura
- [Init Container](/architecture/kubernetes-patterns/structural/init-container) — permite concentrar tarefas que exigem root em uma etapa curta antes do contêiner da aplicação
- [Image Builder](/architecture/kubernetes-patterns/advanced/image-builder) — builds de imagem costumam precisar de mais privilégios e merecem isolamento próprio
- [Gatekeeper](/architecture/cloud-design-patterns/security-and-access/gatekeeper) — também coloca uma camada de validação entre o invasor e o recurso protegido

## Referência

- [Kubernetes Patterns, capítulo 23: Process Containment](https://k8spatterns.com/)
- [Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [Pod Security Admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/)
