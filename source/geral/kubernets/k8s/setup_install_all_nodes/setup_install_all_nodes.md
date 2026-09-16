# 1 - Instalação padrão em todos os nodes

0. Depedências

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget vim git jq apt-transport-https ca-certificates gnupg lsb-release
```

1. Desativação do swap

```bash
sudo swapoff -a
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

2. Ativar configurações do kernel para melhor funcionamento

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Configurações de rede para o K8s
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```

3. Instalação do Runtime (Containerd) [sistema que dá suporte à execução]

```bash
# Adicionar chave GPG do Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Adicionar repositório
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update && sudo apt install -y containerd.io
```

4. Definindo o **systemd**  como o runtime de contêiner conversa com o kernel para controlar recursos.

```bash
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml > /dev/null
sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
sudo systemctl restart containerd && sudo systemctl enable containerd
```

5. Instalando Kubeadm, Kubectl e Kubelet

::: {important} Verifique as versões utilizadas no servidor, master1:
```bash
kubectl get nodes -owide
```
:::

Caso precise consultar a versão: [Install and Set Up kubectl on Linux | Kubernetes](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

```bash
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.36/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.36/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update && sudo apt-cache madison kubectl kubeadm kubelet
sudo apt install -y kubelet kubeadm kubectl

# OU VERSÂO DEFINIDA
# Veja com: "sudo apt-cache madison kubectl kubeadm kubelet"
# sudo apt install -y kubelet=1.35.4-1.1 kubeadm=1.35.4-1.1 kubectl=1.35.4-1.1

# Trava as versões para não att em um upgrade
sudo apt-mark hold kubelet kubeadm kubectl
```

::: {note} Caso queira destravar as versões:
```bash
sudo apt-mark unhold kubelet kubeadm kubectl
```
:::
---

## **APENAS EM MASTERS**

6. **Pré-validar a instalação (Apenas em master)**

```bash
sudo kubeadm init phase preflight
```

Resposta esperada:

![Prefligth-k8s](/geral/imgs/k8s-preflight.png)
