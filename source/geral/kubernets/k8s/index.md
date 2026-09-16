# Cluster k8s

```{toctree}
:maxdepth: 2
:hidden:
setup_install_all_nodes/setup_install_all_nodes
stack_cluster/setup_cluster
add_nodes/move_nodes
```

::::{grid} 3
:::{grid-item-card} 🔍 (Instalação padrão e todos os nós)
:link: setup_install_all_nodes/setup_install_all_nodes
:link-type: doc
:shadow: sm
:columns: 7
:::
::::
---
::::{grid} 3
:::{grid-item-card} 🔍 (Configurando stack do Cluster)
:link: stack_cluster/setup_cluster
:link-type: doc
:shadow: sm
:columns: 7
:::
::::
---
::::{grid} 3
:::{grid-item-card} 🔍 (Adição de Node?)
:link: add_nodes/move_nodes
:link-type: doc
:shadow: sm
:columns: 4
:::
::::
---

:::: {note} 
EXPLICAÇÕES (Seguir aqui é opcional):
::::

**📌 PAPEL DE CADA UM**

| **Componente** | **Função** | **Onde roda** | **O que faz** |
| --- | --- | --- | --- |
| **kubeadm** | 🏗️ **Instalador/Configurador** | Sua máquina (onde vc executa comandos) | Cria e configura o cluster |
| **kubelet** | ⚙️ **Executor** | Em TODOS os nós (masters e workers) | Roda os containers/pods |
| **kubectl** | 🎮 **Controlador** | Sua máquina (CLI de administração) | Envia comandos para o cluster |

**Fase 1: Criação do Cluster (kubeadm → kubelet)**

```bash
[Você executando comandos]
         │
         ▼
    ┌─────────┐
    │ kubeadm │  ← "Vou criar um cluster!"
    └────┬────┘
         │
         │ 1. Gera certificados
         │ 2. Cria arquivos de configuração
         │ 3. Coloca manifests em /etc/kubernetes/manifests/
         ▼
    ┌─────────┐
    │ kubelet │  ← "Detectei novos manifests!"
    └────┬────┘
         │
         │ 4. Cria os containers (API server, etcd, scheduler, controller)
         ▼
    ┌─────────┐
    │ Cluster │  ← Cluster funcionando!
    └─────────┘
```

**Fase 2: Cluster Rodando (kubectl → API Server → kubelet)**

```bash
[Você administrando]
         │
    ┌────▼────┐
    │ kubectl │  ← "kubectl get pods"
    └────┬────┘
         │
         │ 1. Envia comando para a API
         ▼
    ┌───────────┐
    │ API Server│  ← "Verificando permissões..."
    └─────┬─────┘
          │
          │ 2. Consulta scheduler, controller
          ▼
    ┌──────────┐
    │ Scheduler│  ← "Este pod deve ir para node2"
    └─────┬────┘
          │
          │ 3. Ordena a criação
          ▼
    ┌──────────┐
    │ kubelet  │  ← "Recebi ordem! Vou criar o container"
    │ (node2)  │
    └─────┬────┘
          │
          │ 4. Cria o pod
          ▼
    ┌──────────┐
    │  Pod     │  ← Rodando!
    │ (node2)  │
    └──────────┘
```

* **📊 ANALOGIA PARA ENTENDER**

Imagine um **restaurante**:

| **Componente** | **Analogia** | **Explicação** |
| --- | --- | --- |
| **kubeadm** | 🏗️ **Engenheiro de obra** | Projeta e constrói a cozinha (o cluster) |
| **kubelet** | 👨‍🍳 **Cozinheiro** | Executa o trabalho real (faz os pratos/pods) |
| **kubectl** | 📋 **Gerente** | Dá as ordens ("faça 10 pratos de macarrão") |
| **API Server** | 📞 **Atendente** | Recebe os pedidos do gerente |
| **Cluster** | 🍽️ **Restaurante** | Onde tudo acontece |

**🔍 DEPENDÊNCIAS ENTRE ELES**

```bash
kubeadm:
  - NÃO depende de kubelet ou kubectl para funcionar
  - PRECISA de containerd/docker para puxar imagens
  - Chama o kubelet para iniciar os componentes

kubelet:
  - DEPENDE de: containerd/docker (para rodar containers)
  - É chamado pelo kubeadm durante init
  - Responde às ordens da API Server (via kubectl)

kubectl:
  - DEPENDE de: API Server funcionando
  - Só funciona DEPOIS que o cluster está rodando
  - Comunica-se com o cluster via arquivo kubeconfig
```

* ***🎯 RESUMO SIMPLES**

| **Componente** | **"O quê?"** | **"Para quê?"** |
| --- | --- | --- |
| **kubeadm** | Instalador | Cria/configura o cluster (só usado no início) |
| **kubelet** | Motor | Roda os containers (sempre ativo em cada nó) |
| **kubectl** | Controle remoto | Administra o cluster (comandos do dia a dia) |