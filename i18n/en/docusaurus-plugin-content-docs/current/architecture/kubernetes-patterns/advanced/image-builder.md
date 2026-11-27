---
title: Image Builder
pattern_slug: image-builder
category: Advanced
tags:
  - Operational Excellence
  - Security
source: https://k8spatterns.com/
sidebar_label: "Image Builder"
mdx:
  format: mdx
---

import Diagram from '@site/docs/_diagrams/architecture/kubernetes-patterns/advanced/image-builder.mdx';

# Image Builder

## Description

The Image Builder pattern builds container images inside the Kubernetes cluster itself, using the platform's scheduler and resources to run the builds instead of an external build system. The classic approach builds the image outside the cluster, pushes it to the registry and only then references the image in Deployments; here, build and runtime happen in the same place.

The gains come from unifying the infrastructure: a single cluster reduces maintenance cost and simplifies capacity planning, and the Kubernetes scheduler is well suited to finding free resources for build jobs. In addition, since the cluster knows both the build and the deployment, it can react automatically: if a base image with a vulnerability is fixed, all the images that depend on it can be rebuilt and the applications redeployed without intervention.

The tooling ecosystem is broad and overlapping, and falls into two categories. **Container image builders** only create the image, without handling the redeploy, and run without root privileges:

- **Dockerfile-based:** Buildah and Podman, Kaniko (designed to run as a build container in an unprivileged Pod) and BuildKit, which has a low-level build format and frontends other than the Dockerfile.
- **Multilanguage:** Cloud Native Buildpacks detect the project type and follow an opinionated flow (detect, build, export); in the cluster, they are used through `pack`, CI steps or kpack, which expresses the concepts as CRDs. OpenShift's Source-to-Image follows the same idea.
- **Specialized:** Jib (Java), ko (Go) and Apko assemble the image layers directly, without running arbitrary commands, which makes them fast and rootless.

**Build orchestrators** sit one level above: they trigger a builder and take care of the rest, such as updating the deployment descriptors with the new image. They are CI and CD platforms such as Tekton, Argo CD and Flux, plus kbld (which builds and replaces the image references in the YAMLs), the OpenShift build subsystem and a plain Kubernetes Job wrapping a build Pod. In a **build Pod**, init containers run fetching the code, building and pushing to the registry in sequence, and a final step can update the Deployment, triggering a rollout.

**OpenShift Build** is one of the oldest and most mature ways of building images in the cluster. A `BuildConfig` defines the strategy (Source-to-Image, Docker, pipeline or custom) and the sources (Git, Dockerfile, image, Secret or binary). `ImageStreams` emit events when an image changes, and triggers such as `imageChange` rebuild or redeploy in a chain. This enables chained builds: one stage compiles and a second assembles a lean runtime image. The downside is that it works only on the OpenShift distribution.

Because the tooling landscape changes fast and projects can be discontinued, confirm that the chosen tool is still maintained before adopting it.

## Problems it solves

- Duplicated infrastructure: one cluster to run applications and another CI system to build the images
- Separate capacity planning and inefficient scheduling of build jobs on dedicated machines
- Distance between build and deployment, which makes it hard to rebuild and redeploy automatically when a base image changes
- Dependence on a privileged container daemon to assemble images

## When to use

- When company policy allows concentrating build and runtime in the same cluster
- When you want to rebuild and redeploy applications automatically when a base image is fixed
- When a cluster with capacity and scaling already exists and can absorb the build jobs
- When the team can run builds without root privileges and isolate them from production workloads

## When to avoid

- When the security policy requires strong isolation between the build and production environments
- When a managed build service or the current CI already works, with no extra operational cost
- When builds are heavy and can compete for resources with critical workloads, without namespaces, quotas or dedicated nodes to isolate them
- When the team cannot maintain the build tooling inside the platform

## Trade-offs

| Benefit | Cost / Risk |
| --- | --- |
| A single infrastructure to build and run, with lower maintenance cost | Builds run in the same cluster as production workloads, widening the attack surface |
| Uses the Kubernetes scheduler to allocate build jobs | Heavy builds can compete for resources with critical services |
| Automatic rebuild and redeploy when the base image changes | Dependence on specific tools, some evolving fast or discontinued |
| Daemonless, rootless builds reduce the risk of container escape | Builds tend to be slower, without layer and dependency caching |

- **No privileges:** prefer daemonless, rootless builders; avoid mounting the host daemon socket in the build container. Some, such as Kaniko, still run as UID 0 inside an unprivileged Pod, which clusters that forbid root in containers do not accept.
- **Isolation:** use namespaces, ResourceQuotas, [Predictable Demands](/architecture/kubernetes-patterns/foundational/predictable-demands) and dedicated nodes so that builds do not affect services.
- **Lean image:** separate the build environment from the runtime (multistage or chained builds, or Buildpacks, which use a separate runtime image) so compilers do not reach production; Source-to-Image, by default, leaves the build environment in the final image.
- **Cache:** a dependency repository internal to the cluster reduces build time.
- **Credentials:** access to the registry and the code repository should use Secrets with minimal permissions, and the build Pod should be able to change only the Deployment it needs to update.
- **Changing tools:** check the current status of each tool before adopting it.
- **The build Pod is didactic:** in production, use an orchestrator (Tekton, Argo CD, Flux or OpenShift Build) instead of manual steps.

## Diagram

<Diagram />

The build runs as a Job in the cluster itself; the published image feeds the Deployment, and the update of a base image triggers a new build.

## Example

This Job (`batch/v1`) builds the `pix-service` image inside the cluster. An init container fetches the code at tag `v1.4.2`, and Kaniko, which needs neither a daemon nor privileges in the Pod, assembles the image from the Dockerfile and pushes it to the registry using the credentials of a `kubernetes.io/dockerconfigjson` Secret. The repository and registry names and the tool image versions are illustrative. The original Kaniko repository was archived in June 2025, after the book was published; for real use, check for a maintained fork or prefer another daemonless builder such as Buildah.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: build-pix-service-1-4-2
  namespace: fintech
spec:
  backoffLimit: 0
  ttlSecondsAfterFinished: 3600
  template:
    spec:
      restartPolicy: Never
      securityContext:
        fsGroup: 65533 # lets git-sync write to the shared volume
      initContainers:
        - name: fetch-source
          image: registry.k8s.io/git-sync/git-sync:v4.2.1
          args:
            - --repo=https://git.fintech.example/payments/pix-service.git
            - --ref=v1.4.2
            - --depth=1
            - --root=/workspace
            - --link=src
            - --one-time
          volumeMounts:
            - name: workspace
              mountPath: /workspace
      containers:
        - name: build
          image: gcr.io/kaniko-project/executor:v1.23.2
          args:
            - --context=dir:///workspace/src
            - --destination=registry.fintech.example/pix-service:1.4.2
          securityContext:
            privileged: false # the build needs no privileges in the Pod
          volumeMounts:
            - name: workspace
              mountPath: /workspace
            - name: registry-creds
              mountPath: /kaniko/.docker
      volumes:
        - name: workspace
          emptyDir: {}
        - name: registry-creds
          secret:
            secretName: registry-creds
            items:
              - key: .dockerconfigjson
                path: config.json
```

## Related patterns

- [Declarative Deployment](/architecture/kubernetes-patterns/foundational/declarative-deployment) — deploys the image produced by the build, with a controlled update strategy
- [Batch Job](/architecture/kubernetes-patterns/behavioral/batch-job) — a build is a finite workload, run to completion
- [Init Container](/architecture/kubernetes-patterns/structural/init-container) — build steps can run in sequence as init containers of a Pod
- [Immutable Configuration](/architecture/kubernetes-patterns/configuration/immutable-configuration) — versioned, immutable images make the build result reproducible
- [Operator](/architecture/kubernetes-patterns/advanced/operator) — in-cluster build tools are often implemented as Operators with their own CRDs

## Reference

- [Kubernetes Patterns, chapter 30: Image Builder](https://k8spatterns.com/)
