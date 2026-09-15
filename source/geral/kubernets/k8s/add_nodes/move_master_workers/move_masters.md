# Add ou Del Master no cluster


## Add Master

### 1 - Gerar token no master1

```bash
kubeadm token create --print-join-command --certificate-key $(kubeadm init phase upload-certs --upload-certs | tail -1)
```

### 2 - Nos outros masters, executar

::: {important}
Usar o ip do KUBE-VIP (192.168.1.100:6443) pode mudar de acordo com a rede
:::

```bash
sudo kubeadm join 192.168.1.100:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash> --control-plane --certificate-key <key>
```

### 3 - Configurar kubectl nos novos masters

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

---

## Del Master

### Resetando um master (Demora um pouco)

1. Reset do kubeadm
```bash
sudo kubeadm reset -f
```

2. Remover diretórios de configuração
```bash
sudo rm -rf /etc/kubernetes/
sudo rm -rf /var/lib/etcd/
sudo rm -rf /var/lib/kubelet/
```

3. Remover configurações do kube-vip (se existirem)
```bash
kubectl delete daemonset -n kube-system kube-vip-ds 2>/dev/null
kubectl delete configmap -n kube-system kubevip 2>/dev/null
```

4. Limpar o kubeconfig local
```bash
rm -rf ~/.kube/
```

5. Reiniciar o kubelet
```bash
sudo systemctl restart kubelet
```

6. Verificar se o reset foi completo:

```bash
sudo kubeadm reset phase cleanup-node
​```

 

1. Remover configurações restantes do Calico (se houver)
```bash
sudo rm -rf /var/lib/calico/
sudo rm -rf /etc/cni/net.d/
```

# 2. Limpar iptables (regras de rede)
sudo iptables -F
sudo iptables -t nat -F
sudo iptables -t mangle -F
sudo iptables -X

# 3. Limpar IPVS (se usado)
sudo ipvsadm -C 2>/dev/null

# 4. Remover interfaces de rede virtuais (se existirem)
sudo ip link delete cni0 2>/dev/null
sudo ip link delete flannel.1 2>/dev/null

# 5. Parar e limpar o kubelet completamente
sudo systemctl stop kubelet
sudo rm -rf /var/lib/kubelet/
sudo rm -rf /var/lib/kube-proxy

# 6. Remover arquivos de configuração do containerd (opcional)
sudo rm -rf /var/lib/rancher/

# 1. Reiniciar o containerd
sudo systemctl restart containerd

# 2. Reiniciar o kubelet
sudo systemctl restart kubelet

# 3. Verificar se os serviços estão rodando
sudo systemctl status containerd --no-pager
sudo systemctl status kubelet --no-pager

# 7. Remover todos os containers parados (Exited)
sudo crictl rm -a

# 8. Verificar se não há mais containers
sudo crictl ps -a
​
