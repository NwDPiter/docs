# Significado Erro init
---
## 🔎 O que está acontecendo

- O comando executado foi:
    
    ```bash
    sudo kubeadm init --config=kubeadm-config.yaml --upload-certs
    ```
    
- O sistema detectou problemas nos **pré-checks (preflight)**:
    - **Portas ocupadas**: 10259 (kube-scheduler), 10257 (kube-controller-manager) e 10250 (kubelet) já estão em uso.
    - **Arquivos de manifesto já existentes**: `/etc/kubernetes/manifests/kube-apiserver.yaml`, `kube-controller-manager.yaml`, `kube-scheduler.yaml` e `etcd.yaml`.
    - Isso indica que há **resquícios de uma instalação anterior** do Kubernetes no servidor.

## ⚠️ Causa provável

Você está tentando rodar o `kubeadm init` em um nó que **já possui componentes do plano de controle ativos ou parcialmente configurados**.

Ou seja, o cluster não foi resetado corretamente antes da nova inicialização.

## 🛠️ Como interpretar

- O Kubernetes não permite iniciar um novo cluster se já houver processos rodando nas portas críticas ou arquivos de configuração ativos.
- É necessário **resetar o ambiente** antes de tentar novamente.

## ✅ Caminho típico de correção

1. Executar `kubeadm reset -f` para limpar a configuração anterior.
2. Remover os arquivos residuais em `/etc/kubernetes/manifests/` e diretórios como `/var/lib/etcd` e `/var/lib/kubelet`. 

```yaml
sudo kubeadm reset -f && sudo rm -rf /etc/kubernetes/manifests/ /var/lib/etcd /var/lib/kubelet
```

1. Garantir que as portas 10250, 10257 e 10259 estejam livres (matando processos que as ocupam).
2. Migrar o arquivo de configuração para a versão suportada (v1beta4, já que v1beta3 está obsoleta).
3. Tentar novamente o `kubeadm init`.