# 2 - Configurando o cluster

```{toctree}
:maxdepth: 2
:hidden:
explicacoes/kubevip
explicacoes/erro-init
```

---

## 🔧 FASE 1: PREPARAÇÃO DO SISTEMA

### **1.1 Configurar /etc/hosts em TODOS os nós**

```bash
# Em CADA máquina (masters e workers) Modifique o ip com base nas suas VMS
cat <<EOF | sudo tee -a /etc/hosts
# Kubernetes Cluster
192.168.1.100 k8s-vip k8s-kube-vip
192.168.1.107 k8s-master-1
192.168.1.112 k8s-master-2
192.168.1.12  k8s-master-3
192.168.1.105 k8s-worker-1
192.168.1.106 k8s-worker-2
EOF

# Validar hostname
hostname  # Deve ser k8s-master-1, k8s-master-2, etc.

# Validar IP
ip -4 addr show enp0s3 | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'
```

---

## 🚀 FASE 2: INICIALIZAR CLUSTER (SEM KUBE-VIP)

### **2.1 Criar arquivo kubeadm-config.yaml (SEM controlPlaneEndpoint)**

```yaml
cat << 'EOF' > kubeadm-config.yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 192.168.1.107  # IP deste master
  bindPort: 6443
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
kubernetesVersion: v1.35.4
# controlPlaneEndpoint: "192.168.1.100:6443"
apiServer:
  certSANs:
  - "192.168.1.100"  #|
  - "192.168.1.107"  #| Altere para o ip das suas VMs
  - "192.168.1.105"  #|
  - "k8s-kube-vip"
  - "k8s-master-1"
  - "k8s-master-2"
networking:
  serviceSubnet: "10.96.0.0/12"
  podSubnet: "192.168.0.0/16"
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
EOF
```

::::{grid} 3
:::{grid-item-card} 🔍 (Explicação do arquivo acima)
:link: explicacoes/kubevip
:link-type: doc
:shadow: sm
:columns: 5
:::
::::

### **2.2 Validar configuração**

```bash
# Testar com dry-run
sudo kubeadm init --config=kubeadm-config.yaml --dry-run

# Validar versões da API
grep "apiVersion" kubeadm-config.yaml
# Deve mostrar v1beta4 nas duas primeiras linhas (04/2026)
```

Para saber qual a versão de api é mais recente: Configuration APIs | Kubernetes

### **2.3 Inicializar cluster**

```bash
sudo kubeadm init --config=kubeadm-config.yaml --upload-certs
```

Se caso você usou o comando acima e aparecer algo como isso:

![Erro-init](/geral/imgs/erro-init.png)

::::{grid} 3
:::{grid-item-card} 🔍 (Significa do erro acima)
:link: explicacoes/erro-init
:link-type: doc
:shadow: sm
:columns: 5
:::
::::

### **2.4 Configurar kubectl**

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Verificar cluster
kubectl get nodes
```

# Kubernetes HA Core Stack

Calico + Helm + Kube-vip + Traefik,  longhorn, veleiro, Prometheus + Grafana,  loki + Grafana Alloy, ArgoCD, trivy + Falco 

---

1. Calico ~ Helm ~ kube-vip ~ Traefik

---

2. Longhorn

---

3. Velero

---

4. Prometheus + Grafana

---

5. Loki + Grafana Alloy

---

6. ArgoCD

---

7. Trivy + Falco

# Kubernetes Small Stack

Calico + Helm + Kube-vip(DaemonSet), + Traefik, NFS Provisioner OU Longhorn (2 réplicas), Prometheus + Grafana, ArgoCD, Trivy

1. Calico ~ Helm ~ kube-vip ~ Traefik

---

(OPCIONAL) Longhorn  ou **Storage**: NFS provisioner simples (PVCs atendidos por exportação NFS)

---

2. Prometheus + Grafana

---

3. ArgoCD

---

4. Trivy

---