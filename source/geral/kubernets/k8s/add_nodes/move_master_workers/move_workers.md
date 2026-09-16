# Add ou Del Masters


## Add Masters

1. Em qualquer master execute:

```bash
kubeadm token create --print-join-command
```

2. Pegue a saída e execute no worker

```bash
#EX:
kubeadm join 192.168.1.100:6443 --token xxx --discovery-token-ca-cert-hash sha256:xxx
```

## DEL MASTER

### Resetando um master (Demora um pouco)

```bash
# 1. Reset do kubeadm
sudo kubeadm reset -f

# 2. Remover diretórios de configuração
sudo rm -rf /etc/kubernetes/
sudo rm -rf /var/lib/etcd/
sudo rm -rf /var/lib/kubelet/

# 3. Remover configurações do kube-vip (se existirem)
kubectl delete daemonset -n kube-system kube-vip-ds 2>/dev/null
kubectl delete configmap -n kube-system kubevip 2>/dev/null

# 4. Limpar o kubeconfig local
rm -rf ~/.kube/

# 5. Reiniciar o kubelet
sudo systemctl restart kubelet

# 6. Verificar se o reset foi completo
sudo kubeadm reset phase cleanup-node
```

Limpeza