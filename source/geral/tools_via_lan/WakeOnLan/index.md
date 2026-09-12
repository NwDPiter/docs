# WakeOnLan

```{toctree}
:maxdepth: 2
:hidden:

troubleshooting/index
```

::::{grid} 3
:::{grid-item-card} 🔍 (Troubleshooting)
:link: troubleshooting/index
:link-type: doc
:shadow: sm

Em caso de erro
:::
::::


1. No linux é preciso instalar o ***ethtool**, pois por padrão as placa vem com a opção “wol” desativada*

```bash
sudo apt update && sudo apt install ethtool -y
```

2. Valide como está a configuração do “wol”:

```bash
sudo ethtool eno1 | grep Wake-on
```

3. Deve aparecer algo como isso:

```bash
Supports Wake-on: pumbg   |
	Wake-on: g        | Ativado
			  |

	--- ou ---       ---
						  
Supports Wake-on: pumbg   |    
	Wake-on: d        | Desativado  
			  |
```							

Caso esteja como “d”, ative o modo ”wol” :

```bash
sudo ethtool -s eno1 wol g
```

4. Após ativar,edite as permissões e o arquivo de rede com:

```bash
sudo chmod 600 /etc/netplan/*.yaml && sudo nano /etc/netplan/01-netcfg.yaml
```

5. Adicione esse conteúdo:

```bash
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    eno1:
      wakeonlan: true
```

6. Aplique as configurações:

```bash
sudo netplan apply
```

7. Antes de testar, vamos para a BIOS configurar o que precisamos

```bash
Reiniciar por PME : HABILITADO # Permite a placa de rede acordar a máquina

Função EUP: DESABILITADO # Permite a placa não desligar totalmente, ter a energia mínima, para não escutar o pacote chegando 
```

8. Após essa config na BIOS, deixe o pc desligado e … TESTE:

```bash
wakeonlan -i <REDE_DO_PC> -p 7 ou 8 <MAC_DO_PC>
```

::: {note}
- <REDE_DO_PC>  -> O padrão é 255.255.255.255 você deve modifcar com base na rede do pc, use:(ip -br a)

- 7 ou 8 -> É preciso validar em qual vai funcionar

- MAC_DO_PC -> Use(ip a) para descobrir o mac 
:::