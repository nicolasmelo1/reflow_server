# Reflow Server

## IMPORTANT
Como esse projeto utiliza o pypy3 por baixo dos panos e não o python, que por sua vez até o presente momento utiliza-se como base o python 3.6, existe um problema que qualquer erro no codigo ele aparece um erro de `cirular import` (você pode ler mais sobre ele [aqui](https://code.djangoproject.com/ticket/30500)). Para contornar isso devemos usar a flag `--noreload` em desenvolvimento. Essa flag impede que o Django faça o reload automatico quando algum arquivo é modificado o que é ruim para o desenvolvimento. Por isso foi criado um no app `core` [comando](https://docs.djangoproject.com/pt-br/3.0/howto/custom-management-commands/) que resolve esse problema.

Assim ao inves de utilizar do comando `manage.py runserver`

Você deve utilizar o comando `pypy3 manage.py run`, os parametros do runserver são definidos dentro do codigo python localizado no app `core/management/commands/run.py`

A dependência cryptography pode ter problemas na hora de instalar. Se você der os seguintes exports provavelmente vai funcionar tudo bem no momento da instalação:

export CPPFLAGS=-I/usr/local/opt/openssl/include 
export LDFLAGS=-L/usr/local/opt/openssl/lib    

SE O SEU PROGRAMA PRECISA CHAMAR OUTROS SERVIÇOS MUITO PROVAVELMENTE ELE É UM SERVIÇO.
## Configuration
O programa não conta com uma venv ja criada, você precisa criar isso na mão usando o arquivo `requirements.txt`.
Para isso use os seguintes comandos:
```    
$ python3 -m venv venv
```
+ __Mac ou Linux__
```  
$ source venv/bin/activate 
```
+ __Windows__
```
> \path\to\venv\Scripts\activate
```
```   
$ pip install -r requirements.txt
```

#### Obs
Se acontecer algum problema com o psycopg2 ou psycopg2cffi, cheque se você tem todos os [pré-requisitos](http://initd.org/psycopg/docs/install.html#prerequisites) da lib configurados no seu computador.
O sistema usa como dependência o `cryptography`, caso você tenha algum problema com essa lib, tente seguir os passos [daqui](https://cryptography.io/en/latest/installation/) de acordo com seu sistema operacional.

- __linux__ - Caso você esteja no linux, rode os seguintes comandos
```
$ sudo apt-get install postgresql
$ sudo apt-get install python-psycopg2
$ sudo apt-get install libpq-dev
```

## Initialization
Você pode rodar o programa dentro de um docker usando um banco de dados postgres ou usando o sqlite3

#### Docker
+ Instale o Docker **CE** por esse [link](https://www.docker.com/get-docker)
+ Rode os seguintes comandos:

```    
$ docker-compose run reflow-web python manage.py makemigrations
$ docker-compose run reflow-web python manage.py migrate
```
#### Sem Docker
+ Faça a seguinte modificação na variável estática DATABASES no arquivo `settings.py` na pasta **berkley**

```python 
DATABASES = {
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
## Running

### Docker

##### reflow-web
Você pode rodar sua aplicação através do terminal usando o seguinte comando
```
$ docker-compose run reflow-web python manage.py runserver
```
Sua aplicação poderá ser acessada em um dos seguintes endereços:
+ **localhost:8000**
+ **127.0.0.1:8000**

##### Database
Para acessar o banco de dados via terminal use o seguinte comando:
```
$ docker exec -it berkley_db_1 psql -U postgres
```
Para acessar através do Pycharm ou outro conector
(Pode deixar a senha vazia)
```
URL = jdbc:postgresql://localhost:5432/postgres
USER = postgres
```

## Templating (Não usamos mais templates, agora temos um front end em React, YEY)
Infelizmente, quando comecei a programar o aplicativo em questão, tinha um conhecimento de django bem básico
portanto iniciei colocando todos os templates de todos os apps na pasta templates no diretório principal.

Tentei ao maximo otimizar a estrutura para entregar, dentro dos Templates do Django uma estrutura que se assemelha
a frameworks de front-end como Vue ou React. (apesar de ter falhado miseravelmente)

Como ja estavamos muito avançados quando percebi o que havia feito, resolvi não e manter o que tinhamos. 
Então todos os templates estão na pasta `templates`
ela consiste da seguinte estrutura:
+ `index.html` -  Todas as aplicações chamam esse arquivo, ele renderiza os demais, como se fosse um codigo feito em react ou vue
+ `content.html` - Funciona como o __router__ da aplicação, quando renderizamos o template passamos para o template __OBRIGATORIAMENTE__ uma variavel
chamada `app`. essa variavel é usada como Titulo da pagina em alguns casos e para o router identificar qual app renderizar
+ `header.html` - Header da nossa aplicação
+ `footer.html` - Footer da nossa aplicação
+ `script.html` - Scripts que ficam no head da aplicação, são compartilhados por todos os apps
+ `style.html` - Estilização básica que fica no header da aplicação
+ `utils` - pasta com helpers que podem ser usados por apps ou sub-apps

#### Estrutura de Pastas
A estrutura das pastas segue a seguinte ordem `<nome-do-app-django>/<sub-app>`

__`<nome-do-app-django>`__: recebe o mesmo nome que o nome do app no django, assim, fica mais facil se achar no projeto e nos templates

__`<sub-app>`__: Dentro do app notification no django por exemplo trabalhamos tanto com a configuração das notificações 
tanto com as notificações propriamente ditas, isso são dois sub-apps distintos.

Dentro dos sub-apps temos a seguinte estrutura:
+ `content.html` - como se fosse a tag <template> do Vue, ela é usada para definir quais componentes se renderiza
+ `scripts.html` - container com todos os scripts registrados para uso da pagina
+ `style.html` - container com todos os styles registrados para uso da pagina
+ `scripts` - pasta com todos os scripts usados pelo sub-app
+ `components` - é possivel separar o content em partes menores, coloque esses pequenos componentes nessa pasta
+ `styles` - pasta com todos os styles registrados para o sub-app


#### Important
TODOS OS ARQUIVOS DEVEM SER .html para inclui-los no html usando a função builtin do django chamada `{% includes %}`

Pensei em criar arquivos static para o js e css, porém não quis mexer na pasta static no diretorio principal, uma vez que la 
contem arquivos static usados pela aplicação no geral.


#### Improvements
Acredito que o principal espaço para melhoria é separar de uma vez por todas o front-end dessa aplicação.
ainda que eu ache importante seguirmos o guideline da aplicação, não acho necessário perdermos MUITO tempo
arrumando essa estrutura com algo que provavelmente irá mudar.
 
Diria que o primeiro passo, pode ser mover essa estrutura, como está para um codigo a parte.


## Data Dump
O sistema para funcionar depende de alguns dados obrigatórios (geralmente com a flag _type no nome), você pode
encontrá-los na pasta `fixtures` com o nome `required_data.json`

Os temas por sua vez não são obrigatórios para o funcionamento do sistema em si
mas são utilizados para o cadastro de novos usuários, você pode
encontrá-los na pasta `fixtures` com o nome `theme_data.json`

#### Novos dumps
Podem ser feitos tanto via docker quanto pelo próprio terminal:

##### required_data.json
_Obs: Não precisa fazer dump dos objetos necessariamente na ordem_
+ __docker__
```
$ docker-compose run reflow_server pypy3 manage.py dumpdata data.FormType data.FieldType data.ConditionalType data.PeriodIntervalType data.NumberMaskType data.DateFormatType login.Profiles login.DataType login.CompanyType login.GroupType > fixtures/required_data.json
```
+ __terminal__
```
$ pypy3 manage.py dumpdata data.FormType data.FieldType data.ConditionalType data.PeriodIntervalType data.NumberMaskType data.DateFormatType login.Profiles login.DataType login.CompanyType login.GroupType > fixtures/required_data.json
```

##### theme_data.json
_IMPORTANTE: Precisa fazer dump dos objetos NECESSARIAMENTE na ordem_
+ __docker__
```
$ docker-compose run reflow_server pypy3 manage.py dumpdata configuration.Theme configuration.ThemeForm configuration.ThemeField configuration.ThemeFieldOptions configuration.ThemeListingTotalForField configuration.ThemeKanbanCard configuration.ThemeKanbanCardField configuration.ThemeKanbanDimensionOrder configuration.ThemeNotificationConfiguration > fixtures/theme_data.json
```
+ __terminal__
```
$ pypy3 manage.py dumpdata configuration.Theme configuration.ThemeForm configuration.ThemeField configuration.ThemeFieldOptions configuration.ThemeListingTotalForField configuration.ThemeKanbanCard configuration.ThemeKanbanCardField configuration.ThemeKanbanDimensionOrder configuration.ThemeNotificationConfiguration > fixtures/theme_data.json
```

#### Carregar dados
_IMPORTANTE: O load PRECISA NECESSARIAMENTE ser em ordem_

Para carregar os dados em seu ambiente de desenvolvimento:
+ __docker__
```
$ docker-compose run reflow-web pypy3 manage.py loaddata fixtures/required_data.json
$ docker-compose run reflow-web pypy3 manage.py loaddata fixtures/theme_data.json
```
+ __terminal__
```
$ pypy3 manage.py loaddata fixtures/required_data.json
$ pypy3 manage.py loaddata fixtures/theme_data.json
```
