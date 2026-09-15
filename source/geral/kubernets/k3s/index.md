# Cluster k3s

1. Instalação do Novo Control Plane (Master)

Vá para a máquina que será o seu Master e execute o script oficial de instalação. Sem passar parâmetros de banco de dados, ele assumirá a configuração padrão (SQLite), que é leve e perfeita para homologação.

```Bash
curl -sfL https://get.k3s.io | sh -
```

Aguarde alguns segundos e valide se o node master subiu com sucesso:

```Bash
sudo k3s kubectl get node
```

2. Extração do Token de Registro

Para que o worker consiga se autenticar e ingressar no cluster, você precisa do token seguro gerado pelo master. Ainda no Master, execute:

```Bash
sudo cat /var/lib/rancher/k3s/server/node-token
```

*Copie essa string longa. Você vai precisar dela no próximo passo.*

3. Ingresso do Data Plane (Worker)

Agora, acesse o terminal da sua **máquina Worker**. Substitua `<IP_DO_MASTER>` pelo endereço IP da rede local do seu master (ex: `172.16.0.X`) e `<TOKEN_COPIADO>` pela string do passo anterior:

```Bash
curl -sfL https://get.k3s.io | K3S_URL=https://<IP_DO_MASTER>:6443 K3S_TOKEN=<TOKEN_COPIADO> sh -
```

Aguarde alguns segundos e valide se o node subiu na vm Master:

```Bash
sudo k3s kubectl get node
```