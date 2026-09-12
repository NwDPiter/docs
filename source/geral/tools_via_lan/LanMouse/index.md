# LanMouse
## Documentação Técnica: KVM via Software com Lan Mouse (Pop!_OS / Ubuntu)

Esta documentação descreve a arquitetura, instalação, fluxo de comunicação e configuração persistente para compartilhamento de teclado e mouse entre um nó emissor (**Pop!_OS**) e um nó receptor (**Ubuntu**) na mesma rede local.

## 1. Arquitetura e Fluxo de Comunicação

O **Lan Mouse** opera em um modelo cliente-servidor para tráfego UDP criptografado via **DTLS** (Datagram Transport Layer Security).

  
```
[ Pop!_OS (Emissor / Sender) ]  --- UDP 4242 (DTLS) --->  [ Ubuntu (Receptor / Receiver) ]
 (Mouse & Teclado Físicos)                                 (Emulação libei/X11/uinput)
```

- **Pop!_OS (Emissor):** Monitora as bordas da tela via portal do ambiente gráfico (COSMIC/Wayland). Ao atingir o limite configurado, captura os eventos de entrada físicos (`enable_capture = true`) e os envia via rede.
    
      
    
- **Ubuntu (Receptor):** Escuta na porta `4242/UDP` e injeta os eventos recebidos diretamente na sessão de usuário (`enable_emulation = true`).
    

## 2. Dependências do Sistema

Para compilar ou executar o binário do Lan Mouse em distribuições baseadas em Debian/Ubuntu, os seguintes pacotes são obrigatórios:

  
- **`libei-dev`**: Biblioteca de emulação de entrada (_Emulated Input_) do ecossistema Wayland/GNOME.  
      
    
- **`libxkbcommon-dev`**: Processa e traduz layouts de teclado e mapas de teclas (_keymaps_).
    
    
- **`libglib2.0-0`**: Biblioteca base de suporte a _event loops_ e abstrações do sistema.
    

**Comando de Instalação (em ambas as máquinas):**

```bash
sudo apt update
sudo apt install -y libei-dev libxkbcommon-dev libglib2.0-0
```

## 3. Instalação do Executável

Colocar o binário no diretório `/usr/local/bin` garante conformidade com o FHS (_Filesystem Hierarchy Standard_) e disponibiliza o comando no `PATH` do sistema sem sobrescrever o gerenciador de pacotes (`apt`).

```bash
cd ~/Downloads
chmod +x lan-mouse-linux-x86_64
sudo mv lan-mouse-linux-x86_64 /usr/local/bin/lan-mouse
```

## 4. Configuração da Rede e Firewall

O serviço de escuta do Lan Mouse opera por padrão na porta **`4242/UDP`**.

**Abertura no Firewall (UFW):**

```bash
sudo ufw allow 4242/udp
```

**Verificação de Escuta:**

```bash
sudo ss -tulnp | grep lan-mouse
# Retorno esperado: UNCONN 0 0 0.0.0.0:4242
```

## 5. Configuração via interface

### 5.1. Máquina Emissora (Pop!_OS)

Abra a interface do Lan-mouse e clique em "+ Add" e adicione o ip da máquina alvo e seleciona em qual posição a tela do outro pc vai ficar, após adicionar e ativar a opção de conexão, vá para a próxima config

#### 5.2. Máquina Receptora (Ubuntu/popos)

Ná máquina distino deixe o lan-mouse aberto e volte para o popos mova o mouser para a borda da tela e espere aparecer na tela do ubuntu um pedido de autorização, quando aparecer de um nome, autorize e pronto. Deve funcinar.

## 6. Automação e Persistência via Systemd (Serviço de Usuário)

Para que o daemon do Lan Mouse inicie automaticamente no Boot sem depender da interface gráfica, configure um serviço Systemd de usuário em ambas as máquinas.

### 6.1. Criar a Unidade de Serviço

Arquivo: `~/.config/systemd/user/lan-mouse.service`

```ini
[Unit]
Description=Lan Mouse Daemon
After=graphical-session.target

[Service]
ExecStart=/usr/local/bin/lan-mouse daemon
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=graphical-session.target
```

### 6.2. Ativar e Iniciar o Serviço

Execute os comandos em ambos os sistemas:

```bash
systemctl --user daemon-reload
systemctl --user enable --now lan-mouse.service
```

**Verificação do Status:**

```bash
systemctl --user status lan-mouse.service
```

## 7. Troubleshooting e Diagnóstico Rápido

- **Erro `emulation is disabled on target device`:** O arquivo `config.toml` do receptor está com `enable_emulation = false`.     
    
- **Erro `no active client at this position`:** O array `ips` na chave `[[clients]]` da máquina emissora está vazio ou desconectado.      
    
- **Erro de D-Bus / Backend no Wayland:** Executar no receptor indicando o backend suportado:
    
      
    - GNOME/Wayland: `lan-mouse --emulation-backend libei`
        
          
        
    - Sessão X11: `lan-mouse --emulation-backend x11`
        
          
        
    - Acesso Kernel direto: `lan-mouse --emulation-backend uinput` (requer grupo `input` no usuário).