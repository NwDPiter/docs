# Como usar o SOCKS via ssh
O SOCKS (especialmente a versão SOCKS5) no SSH é um recurso que transforma sua conexão segura em um servidor proxy dinâmico, permitindo rotear todo o tráfego de aplicativos (como navegadores) através de um servidor remoto.

:::{toctree}
:maxdepth: 2
:hidden:

SOCKS-Mine/index
:::


::::{grid} 3
:::{grid-item-card} 🔍 (Explicação Gamer (Mine))
:link: SOCKS-Mine/index
:link-type: doc
:shadow: sm
:::
::::

1. Primeiro passo e entender os parâmetros do comando:

```bash
ssh -D 1080 -N -f user@alvo
```
* **`-D 1080`**: Transforma a máquina local em um servidor de **Proxy SOCKS** na porta **1080**. Todo tráfego configurado para usar esse proxy será redirecionado de forma segura através do servidor remoto.
* **`-N`**: Diz para **não executar comandos** remotamente. Serve apenas para abrir o túnel e economizar recursos.
* **`-f`**: Envia o SSH para rodar em **segundo plano (background)**. Libera o terminal atual imediatamente para uso.
