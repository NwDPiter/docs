# Tecnologias utilizadas

### 1º - Github Actions -> Automação

### 2º - Docker         -> Virtualizador de nível de SO

### 3º - Portainer      -> Gerencinamento de containers


# 1º Github Actions

GitHub Actions é uma ferramenta de automação de fluxo de trabalho integrada ao GitHub, que permite aos desenvolvedores automatizar processos como compilação, teste e implantação de software diretamente nos repositórios GitHub.

## Como está sendo utilizando?

O INBCM está dividido em 3 repositórios (**inbcm-backend**, **inbcm-admin-frontend** e **inbcm-public-frontend**) e em cada um deles há uma actios que fica em "/.github/workflows/Nome_action.yml" no qual contém o conteúdo abaixo:

    name: Publish Docker image     | Nome da action

    -------------------------------| 
    on:                            | 
    workflow_dispatch:             | Esse bloco permite que o código seja executado de duas 
    pull_request:                  | maneiras, (workflow_dispatch) permite o manual na aba
        branches:                  | actions do github e (pull_request) permite o automático
        - main                     | no qual definimos as branches que fara a ativação dessa
        - development              | actions quando um pull_request fechado.
        types: [closed]            |   
    -------------------------------|

    -------------------------------------------------|
    jobs:                                            | Aqui é onde começa os trabalhos fazemos
    push_to_registry:                                | uma verificação para saber so o pr foi 
        name: Push Docker image to Registry          | fechado com um merge, caso sim, vai ini
        if: github.event.pull_request.merged == true | ciar essa action, além de escolher qual
        runs-on: ubuntu-latest                       | SO vai rodar essa action (ubuntu).
    -------------------------------------------------|

    ----------------------------------|
        steps:                        | Esse bloco faz um git clone do projeto para dentro da
        - name: Check out the repo    | VM que escolhemos, no caso ubuntu, existe windows e
            uses: actions/checkout@v3 | mac ,mas ficamos com a atual.
    ----------------------------------|

    ------------------------------------------------------------------------|
        - name: Set Docker repository name for main branch                  |
            if: github.ref == 'refs/heads/main'                             |
            run: echo "DOCKER_REPOSITORY=inbcm-backend-main" >> $GITHUB_ENV |Aqui verifica qual
                                                                            |branch alvo do marge
                                                                            |pois a imagem será
        - name: Set Docker repository name for development branch           |enviada para um 
            if: github.ref == 'refs/heads/development'                      |dockerhub específico
            run: echo "DOCKER_REPOSITORY=inbcm-backend" >> $GITHUB_ENV      |
    ------------------------------------------------------------------------|

    -------------------------------------------------|
        - name: Log in to Docker Registry            |
            uses: docker/login-action@v3             | Aqui ocorre o login, no qual foi
            with:                                    | definido nas secrets as variáveis
            username: ${{ secrets.DOCKER_USERNAME }} | de login e senha para o dockerhub
            password: ${{ secrets.DOCKER_PASSWORD }} |
    -------------------------------------------------|

    ------------------------------------------|
        - name: Build and push Docker image   |Por fim o deploy, aqui e gerado uma imagem 
            uses: docker/build-push-action@v6 |a partir do Dockerfile que está no repositório
            with:                             |e feito o push para o dockerhub.
            context: .                        |
            file: ./Dockerfile                |_______________________________________
            push: true                                                               |
            tags: ${{ secrets.DOCKER_USERNAME }}/${{ env.DOCKER_REPOSITORY }}:latest |
    ---------------------------------------------------------------------------------|


# 2º Docker

Docker é uma plataforma de software que permite criar, testar e implantar aplicações rapidamente em ambientes isolados, chamados de containers.

## Como está sendo utilizando?

Em nossos repositórios há 3 Dockerfiles dois identicos para o front-end e um apenas para o back-end

- Dockerfile front-end

        ----------------------------|
        FROM node:20-slim AS base   | Nesse bloco escolhemos nossa imagem e um apelido para que
        ENV PNPM_HOME="/pnpm"       | seja reutilizada mais a frente, criamos 2 ENV um para o 
        ENV PATH="$PNPM_HOME:$PATH" | diretório do pnpm e o outro e com caminho que faz a execução
        RUN corepack enable         | do pnpm, além de rodar um comando para ativar o corepack.
        ----------------------------|

        -----------------------------------------------------------------------------------|Aqui reutilizamos nossa imagem e colocamos outro apelido para ser usada depois
        FROM base AS build                                                                 |Copiamos o que tem no diretório atual par dentro de "/usr/src/app" do container 
        COPY . /usr/src/app                                                                |Informamos o diretório de trabalho do container ou seja, pode manipular arquivos 
        WORKDIR /usr/src/app                                                               |e entre outro lá dentro, rodamos um comando que vai gerar um cache temporário de 
        RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile   |todos os módulos usados na aplicação que vai ser usado jájá e rodamos o comando
        RUN pnpm build                                                                     |para compilar o código
        -----------------------------------------------------------------------------------|

        ---------------------------------------|
        FROM devforth/spa-to-http              | Aqui escolhemos uma imagem adquada para nosso ambiente
        COPY --from=build /usr/src/app/dist .  | Copiamos o conteúdo do cache temporário que foi criado 
        ---------------------------------------| na imagem anterior apelidada de "build" para nosso container

- Dockerfile back-end

        -----------------------------|
        FROM node:20-slim AS base    |
        ENV PNPM_HOME="/pnpm"        |Esse bloco segue um padrão parecido 
        ENV PATH="$PNPM_HOME:$PATH"  |do front-end a diferença e que ele
        RUN corepack enable          |já indica o diretório de trabalho e
        COPY . /app                  |copia o conteúdo local para lá.
        WORKDIR /app                 |
        -----------------------------|

        ----------------------------------------------------------------------------------------|
        FROM base AS prod-deps                                                                  |
        RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile |Aqui também segue o padrão do front-end
                                                                                                |criamos uma cache com o conteúdo necessário
        FROM base AS build                                                                      |para rodar a aplicação e apilidamos para 
        RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile        |ser utilizados mais a frente.
        RUN pnpm run build                                                                      |
        ----------------------------------------------------------------------------------------|    

        -----------------------------------------------------------|
        FROM base                                                  |Nesse último bloco copiamos
        COPY --from=prod-deps /app/node_modules /app/node_modules  |todos os conteúdo que foram 
        COPY --from=prod-deps /app/package.json /app/package.json  |gerandos em cache na etapa 
        COPY --from=build /app/dist /app/dist                      |anterior para a imagem final
        EXPOSE 3000                                                |libera a porta necessária da 
        CMD [ "pnpm", "start" ]                                    |aplicação e iniciamos.
        -----------------------------------------------------------|


### Exemplo do passo a passo de como gera uma imagem usando docker (Método manual):

OBS: Supondo que você já tenha o docker em sua máquina, caso não, segue o site oficial para instalação:

https://docs.docker.com/engine/install/  (Aqui vai encontra a instalção tanto da GUI como CLI do docker)

1º Precisamos de um arquivo Dockerfile, vamos usar algo simples:

1.1 Aqui escolhemos um SO que vai ser utilzado no container.

    FROM alpine:latest          

1.2 O comando abaixo informa ao container o que ele deve fazer,no caso, escrever "hello" na tela.

    CMD ["echo","Hello"]

1.3 Logo seu Dockerfile deve ter esse conteúdo.

    FROM alpine:latest
    CMD ["echo","Hello"]     

2º Agora que temos nosso Dockerfile vamos buildar/gerar uma imagem.

![Docker_build](/imagens/Docker_build.png)

3º Após criarmos a imagem podemos verificar se realmete foi criada usando:

- docker ps

vai aparecer uma lista de imagens é nela deve ter aque acabamos de criar

4º Para rodar essa imagem usamos:

- docker run exemplo/hello

e ela vai executar o que foi escrito no Dockerfile.


# 3º Portainer

Portainer é uma ferramenta de gerenciamento de containers que oferece uma interface gráfica de usuário (GUI), Ele simplifica o gerenciamento de containers, imagens, redes e volumes, permitindo que usuários interajam com esses recursos de maneira visual, em vez de usar apenas a linha de comando.

## Observações

- Atualmente o projetos está hospedado no servidor da UNB (Universidade de Brasília)
- O ambiente está sendo 

## Como está sendo utilizando?

Acessar portainer: https://portainer.tainacan.org

No portainer atualmente temos 4 stacks:

|        Stacks             | Branchs|                                 
|---------------------------|--------|
|inbcm                      |  main  |     
|homologacao_curadoria_ifrn |  main  |  
|inbcm-dev                  |  dev   |    
|dev_curadoria_ifrn         |  dev   |  

Ao clicar em uma delas vai abrir o gerenciador de stacks e lá temos essa duas opções

![Gerenciador_stack](imagens/Gerenciador_stack.png)

- Stack
    - Informa os container que estão rodando nessa stack
- Editor
    - Fazer edições em nossa stack

Cada stack tem um docker-compose que fica na aba "Editar" no qual é utilizado para subir o ambiente:

_**Docker-compose (inbcm-dev)**_

    version: "3.5"

    networks:
    ifrn_dev_internal_network:
    traefik_proxy:
        external: true

    volumes:
    mongo-data:
        driver: local
        driver_opts:
        type: nfs
        o: nfsvers=4,addr=10.10.10.100,rw
        device: ":/NFS_VOL/HDD/ifrn/mongodev"
    uploads-data:

    services:
    mongo:
        image: mongo
        volumes:
        - mongo-data:/data/db
        environment:
        MONGO_INITDB_ROOT_USERNAME: ${DB_USER}
        MONGO_INITDB_ROOT_PASSWORD: ${DB_PASS}
        MONGO_INITDB_DATABASE: ${DB_NAME}
        networks:
        - ifrn_dev_internal_network

    mongo-express:
        image: mongo-express
        environment:
        ME_CONFIG_BASICAUTH_USERNAME: ifrn.2024
        ME_CONFIG_BASICAUTH_PASSWORD: ifrn.2024
        ME_CONFIG_MONGODB_PORT: 27017
        ME_CONFIG_MONGODB_ADMINUSERNAME: ${DB_USER}
        ME_CONFIG_MONGODB_ADMINPASSWORD: ${DB_PASS}
        ME_CONFIG_MONGODB_SERVER: mongo
        depends_on:
        - mongo
        networks:
        - traefik_proxy
        - ifrn_dev_internal_network
        deploy:
        labels:
            - traefik.enable=true
            - traefik.docker.network=traefik_proxy
            - traefik.constraint-label=traefik-public
            - traefik.http.routers.dev-inbcm-mongoexpress-http.rule=Host(`mongoexpress.${DOMAIN}`)
            - traefik.http.routers.dev-inbcm-mongoexpress-http.entrypoints=http
            - traefik.http.routers.dev-inbcm-mongoexpress-http.middlewares=https-redirect
            - traefik.http.routers.dev-inbcm-mongoexpress-https.rule=Host(`mongoexpress.${DOMAIN}`)
            - traefik.http.routers.dev-inbcm-mongoexpress-https.entrypoints=https
            - traefik.http.routers.dev-inbcm-mongoexpress-https.tls=true
            - traefik.http.routers.dev-inbcm-mongoexpress-https.tls.certresolver=le
            - traefik.http.services.dev-inbcm-mongoexpress.loadbalancer.server.port=8081

    backend:
        image: thfields/inbcm-backend
        networks:
        - traefik_proxy
        - ifrn_dev_internal_network
        environment:
        DB_USER: ${DB_USER}
        DB_PASS: ${DB_PASS}
        DB_URL: mongodb://root:asdf1234@mongo:27017/INBCM?authSource=admin
        JWT_SECRET: ${JWT_SECRET}
        PUBLIC_SITE_URL: ${PUBLIC_SITE_URL}
        ADMIN_SITE_URL: ${ADMIN_SITE_URL}
        REGISTRY_USERNAME: ${REGISTRY_USERNAME}
        REGISTRY_PASSWORD: ${REGISTRY_PASSWORD}
        REGISTRY_URL: ${REGISTRY_URL}
        depends_on:
        - mongo
        deploy:
        labels:
            - traefik.enable=true
            - traefik.docker.network=traefik_proxy
            - traefik.constraint-label=traefik-public
            - traefik.http.routers.dev-inbcm-backend-http.rule=Host(`${DOMAIN}`) && PathPrefix(`/api`) || Host(`admin.${DOMAIN}`) && PathPrefix(`/api`)
            - traefik.http.routers.dev-inbcm-backend-http.entrypoints=http
            - traefik.http.routers.dev-inbcm-backend-http.middlewares=https-redirect
            - traefik.http.routers.dev-inbcm-backend-https.rule=Host(`${DOMAIN}`) && PathPrefix(`/api`) || Host(`admin.${DOMAIN}`) && PathPrefix(`/api`)
            - traefik.http.routers.dev-inbcm-backend-https.entrypoints=https
            - traefik.http.routers.dev-inbcm-backend-https.tls=true
            - traefik.http.routers.dev-inbcm-backend-https.tls.certresolver=le
            - traefik.http.services.dev-inbcm-backend.loadbalancer.server.port=3000
        volumes:
        - uploads-data:/uploads

    public:
        image: thfields/inbcm-public
        networks:
        - traefik_proxy
        - ifrn_dev_internal_network
        restart: always
        environment:
        REGISTRY_USERNAME: ${REGISTRY_USERNAME}
        REGISTRY_PASSWORD: ${REGISTRY_PASSWORD}
        REGISTRY_URL: ${REGISTRY_URL}
        depends_on:
        - backend
        - mongo
        deploy:
        labels:
            - traefik.enable=true
            - traefik.docker.network=traefik_proxy
            - traefik.constraint-label=traefik-public
            - traefik.http.routers.dev-inbcm-upload-http.rule=Host(`${DOMAIN}`)
            - traefik.http.routers.dev-inbcm-upload-http.entrypoints=http
            - traefik.http.routers.dev-inbcm-upload-http.middlewares=https-redirect
            - traefik.http.routers.dev-inbcm-upload-https.rule=Host(`${DOMAIN}`)
            - traefik.http.routers.dev-inbcm-upload-https.entrypoints=https
            - traefik.http.routers.dev-inbcm-upload-https.tls=true
            - traefik.http.routers.dev-inbcm-upload-https.tls.certresolver=le
            - traefik.http.services.dev-inbcm-upload.loadbalancer.server.port=8080

    admin:
        image: deploy164/inbcm-admin:latest 
        restart: always
        environment:
        REGISTRY_USERNAME: ${REGISTRY_USERNAME}
        REGISTRY_PASSWORD: ${REGISTRY_PASSWORD}
        REGISTRY_URL: ${REGISTRY_URL}
        depends_on:
        - backend
        - mongo
        networks:
        - traefik_proxy
        - ifrn_dev_internal_network
        deploy:
        labels:
            - traefik.enable=true
            - traefik.docker.network=traefik_proxy
            - traefik.constraint-label=traefik-public
            - traefik.http.routers.dev-inbcm-admin-http.rule=Host(`admin.${DOMAIN}`)
            - traefik.http.routers.dev-inbcm-admin-http.entrypoints=http
            - traefik.http.routers.dev-inbcm-admin-http.middlewares=https-redirect
            - traefik.http.routers.dev-inbcm-admin-https.rule=Host(`admin.${DOMAIN}`)
            - traefik.http.routers.dev-inbcm-admin-https.entrypoints=https
            - traefik.http.routers.dev-inbcm-admin-https.tls=true
            - traefik.http.routers.dev-inbcm-admin-https.tls.certresolver=le
            - traefik.http.services.dev-inbcm-admin.loadbalancer.server.port=8080


Temos os seguinte desenhos lógicos para melhor visualização da infra:

![Estrutura_lógica1](/imagens/Estrutura-1.png)
![Estrutura_lógica2](/imagens/Estrutura-2.png)

