# Add ou Del Workers

## Add Workers

1. Em qualquer master execute:
```sh
kubeadm token create --print-join-command
```

2. Pegue  a saída e execute no worker

```sh
kubeadm join 192.168.1.100:6443 --token xxx --discovery-token-ca-cert-hash sha256:xxx
```

---

## Removendo worker do cluster:

1. Trava o nó para não receber mais pods
```sh
kubectl cordon <nome-do-node>
```
2. Drenar os pods:
```sh
kubectl drain <nome-do-worker> --ignore-daemonsets --delete-emptydir-data
```

3. Deletar o nó
```sh
kubectl delete node <nome-do-node>
```
---

## Limpando worker
1. Limpa o worker
```sh
sudo kubeadm reset
```

2. Remover config da CNI:
```sh
sudo rm -rf /etc/cni/net.d
sudo rm -rf /var/lib/cni/
```

3. Remover configs locais
```sh
sudo rm -rf /var/lib/kubelet/*
sudo rm -rf /etc/kubernetes/
sudo rm -rf ~/.kube
```

4. Resetar regras do iptables
```sh
sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
```

5. Resetar serviços
```sh
sudo systemctl restart kubelet
sudo systemctl restart containerd
```
