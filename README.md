![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/rauanisanfelice/easy-park.svg)
![GitHub top language](https://img.shields.io/github/languages/top/rauanisanfelice/easy-park.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/rauanisanfelice/easy-park.svg)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/rauanisanfelice/easy-park)
![GitHub contributors](https://img.shields.io/github/contributors/rauanisanfelice/easy-park.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/rauanisanfelice/easy-park.svg)

![GitHub stars](https://img.shields.io/github/stars/rauanisanfelice/easy-park.svg?style=social)
![GitHub followers](https://img.shields.io/github/followers/rauanisanfelice.svg?style=social)
![GitHub forks](https://img.shields.io/github/forks/rauanisanfelice/easy-park.svg?style=social)

# Easy Park

Projeto de Estacionamento Rotativo

# Instruções

1. Ambiente Python;
2. Instalando dependências;
3. Criando arquivo .env;
4. Inicialização dos container;
    1. Configurando o pgAdmin;
    2. Migrando o BD;
    3. Insert inicial;
5. Iniciar o servidor.

## Ambiente Python;

```
virtualenv -p python3 env
source env/bin/activate
```

## Instalando dependências:

```
pip3 install -r requirements.txt
```

### Criando arquivo .env;

Copie o conteúdo do arquivo .env-example e crie um novo arquivo .env, cole o conteúdo e altere as variáveis.

### Inicialização dos container;

```
docker-compose up -d
```

#### Configurando o pgAdmin;

Acesse o link:

[pgAdmin](http://localhost:80)

Realize o login:
>User: admin  
>Pass: admin

Clique em: Create >> Server

Conecte no Banco com os seguintes parametros:  

Name: #nome desejado#  
>Host: easy-park-postgre
>Port: 5432  
>DB  : postgres  
>User: admin  
>Pass: docker123

#### Migrando o BD;

```
python manage.py migrate
```

#### Insert inicial;

Copie o conteúdo do arquivo abaixo e realize um insert no Banco.
> database > inser.sql


### Iniciar o servidor

```
python manage.py runserver 8000 --noreload
```

[Site](http://localhost:8000)
