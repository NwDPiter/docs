# troubleshooting

- Pc não ligou
    
    Instale e use o tcpdump caso não tenha para validar se o pacote chega na máquina.
    
    ```bash
    sudo apt install tcpdump -y
    sudo tcpdump -i <SUA_PLACA> port 9 or port 7
    ```
    
    Se o pacote chegar durante o teste o problema é no HARDWARE/BIOS