# Explicação do kubeadm-config.yaml

---

## 📌 Principais seções e o que dá para configurar

```yaml
# 11 - Criar configuração do kubeadm (COM controlPlaneEndpoint)
cat <<EOF > kubeadm-config.yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
localAPIEndpoint:
advertiseAddress: 192.168.1.107 # IP do master que inicial o cluster
bindPort: 6443
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: v1.35.0 # Versão do k8s instalada
controlPlaneEndpoint: "192.168.1.100:6443"  # IP do kube-vip que foi escolhido
apiServer:
certSANs:         # Altere os ips desse campo com base na sua rede
- "192.168.1.100" # IP dO KUBE-VIP
- "192.168.1.10"  # IP da VM Master 
- "192.168.1.11"  # IP da VM Master
- "192.168.1.12"  # IP da VM Master 
- "k8s-kube-vip"
- "k8s-master-1"
- "k8s-master-2"
- "k8s-master-3"
networking:
serviceSubnet: "10.96.0.0/12"
podSubnet: "192.168.0.0/16"
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
EOF
```

### 1. **InitConfiguration**

- **`localAPIEndpoint.advertiseAddress`** → IP do nó master que está inicializando.
- **`localAPIEndpoint.bindPort`** → porta onde o kube-apiserver vai escutar (normalmente 6443).
👉 Essa parte define como o nó master se apresenta para o cluster.

---

### 2. **ClusterConfiguration**

- **`kubernetesVersion`** → versão do Kubernetes que será instalada.
- **`controlPlaneEndpoint`** → IP ou hostname do *load balancer* ou do nó master principal, usado como ponto de entrada para o cluster.
- **`apiServer.certSANs`** → lista de IPs e hostnames válidos para o certificado TLS do API Server (inclui masters e, se houver, o load balancer).
- **`networking.serviceSubnet`** → faixa de IPs usada para os serviços internos do Kubernetes.
- **`networking.podSubnet`** → faixa de IPs usada para os pods.
👉 Aqui você define a topologia da rede e como os certificados vão validar os acessos.

---

### 3. **KubeletConfiguration**

- **`cgroupDriver`** → driver de gerenciamento de grupos de controle (geralmente `systemd` ou `cgroupfs`).
👉 Isso garante compatibilidade entre kubelet e container runtime.

---

## 🔧 Outras opções que podem ser configuradas

Além do que você mostrou, esse arquivo pode incluir:

- **`apiServer.extraArgs`** → parâmetros adicionais para o kube-apiserver.
- **`controllerManager.extraArgs`** → parâmetros extras para o kube-controller-manager.
- **`scheduler.extraArgs`** → parâmetros extras para o kube-scheduler.
- **`etcd.local`** → configuração do etcd embutido (ou remoto, se for externo).
- **`imageRepository`** → repositório de imagens do Kubernetes (útil em ambientes sem acesso à internet).
- **`dns.type`** → tipo de DNS (CoreDNS é o padrão).
- **`featureGates`** → ativar ou desativar recursos experimentais.
- **`apiServer.timeoutForControlPlane`** → tempo limite para operações do control plane.

---

## 📌 Resumindo

Esse arquivo é o **coração da configuração inicial do cluster**.

- Define **como os masters se comunicam** (`advertiseAddress`, `controlPlaneEndpoint`).
- Configura **rede de pods e serviços** (`serviceSubnet`, `podSubnet`).
- Ajusta **certificados** (`certSANs`).
- Permite **customizar componentes** (apiServer, controllerManager, scheduler, etcd).

---