# Gerenciando_volumes_lógicos

- Piramide de analise
	- pvs -> Diz o volume total entregue para a vm gerenciar
	- vgs -> Mosta o tamanho do grupo de volume existente
	- lvs  -> Informa os volumes lógicos que estão montados

---
  [ Disco 1 ]   [ Disco 2 ]  --> Camada Física (pvs)
      \             /
    [  Grupo de Volumes  ]  --> Espaço (vgs) - Espaço do grupo de volume
     /      |       \
  [/]     [/var]   [/home]   --> Camada Lógica (lvs) - Onde os vgs montados estão localizados

---
📋 O Fluxo Correto (Do Disco Físico até a Pasta)

1. Mexer na partição física

```bash
sudo cfdisk /dev/sda
```

_Garante que o "pedaço de metal virtual" mudou de tamanho._

2. Avisar o LVM que o disco cresceu (O que faltou no seu fluxo)

Logo após sair do cfdisk, você obrigatoriamente precisa rodar o `pvresize` para o LVM enxergar o espaço livre. _(No seu caso atual, lembre-se que a partição é a `sda5`)_:

```bash
sudo pvresize /dev/sda5
```

_Esse comando injeta os Gigabytes novos no "pool" do LVM._

3. Expandir a "gaveta" (Volume Lógico)

Agora que o LVM tem espaço livre para gastar, você expande o volume que quiser usando o `-L +Tamanho`:

```bash
sudo lvextend -L +30G /dev/VM-113-vg/NOME_DO_LV
```

::: {important}
Recomendo aumentar aos poucos os volumes e não adicionar tudo de vez.
:::

4. Atualizar o Sistema de Arquivos

Por fim, você faz o Linux enxergar o espaço dentro da pasta:

```bash
sudo resize2fs /dev/VM-113-vg/NOME_DO_LV
```

---

::: {note}
O caminho do espaço é sempre de fora para dentro:

1. `cfdisk` (Aumenta a partição) ➡️
2. `pvresize` (Aumenta o LVM) ➡️
3. `lvextend` (Aumenta o Volume Lógico) ➡️
4. `resize2fs` (Aumenta o Sistema de Arquivos).
:::