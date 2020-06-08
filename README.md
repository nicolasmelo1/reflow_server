# Reflow Server

## IMPORTANT
Como esse projeto utiliza o pypy3 por baixo dos panos e não o python, que por sua vez até o presente momento utiliza-se como base o python 3.6, existe um problema que qualquer erro no codigo ele aparece um erro de `cirular import` (você pode ler mais sobre ele [aqui](https://code.djangoproject.com/ticket/30500)). Para contornar isso devemos usar a flag `--noreload` em desenvolvimento. Essa flag impede que o Django faça o reload automatico quando algum arquivo é modificado o que é ruim para o desenvolvimento. Por isso foi criado um no app `core` [comando](https://docs.djangoproject.com/pt-br/3.0/howto/custom-management-commands/) que resolve esse problema.

Assim ao inves de utilizar do comando `manage.py runserver`

Você deve utilizar o comando `pypy3 manage.py run`, os parametros do runserver são definidos dentro do codigo python localizado no app `core/management/commands/run.py`

A dependência cryptography pode ter problemas na hora de instalar. Se você der os seguintes exports provavelmente vai funcionar tudo bem no momento da instalação:

export CPPFLAGS=-I/usr/local/opt/openssl/include 
export LDFLAGS=-L/usr/local/opt/openssl/lib    

SE O SEU PROGRAMA PRECISA CHAMAR OUTROS SERVIÇOS MUITO PROVAVELMENTE ELE É UM SERVIÇO.

## Configuração
__IMPORTANTE__: Não pule essa etapa, mesmo se você estiver utilizando containers docker para desenvolver.

Nós utilizamos o [pypy3](https://www.pypy.org/)(Não confundir com o [PyPi](https://pypi.org/)(Onde se baixa as libs com o comando `pip install`)) no projeto ao invés do python devido a sua performance até 4x superior. Como esse projeto é um projeto, como você pode perceber, monolito, que exige muita performance para gerenciar todos os requests a uma boa velocidade. 

Talvez você não conheça o **pypy3**, de maneira resumida ele é um compilador just-in-time (JIT) python feito em python! Incrivel né?
Ou seja, de maneira resumida como ele é um compilador python feito usando o próprio python você não deve ter problema escrevendo grande parte do seu código python e portando para o **pypy3**. O grande problema que existe com ele é com libs que criam interfaces com código escrito em C como o caso do psycopg2. Você pode ver se o **pypy3** é compativel com a lib que você quer usar [aqui](https://bitbucket.org/pypy/compatibility/wiki/Home)(obviamente eles não checam todas as libs disponiveis, apenas aquelas criticas.)


#### Instalando o pypy
__IMPORTANTE__: O pypy oferece suporte para o python 2.7, mas não utilizamos o python 2.7, utilizamos python 3.x na Reflow, portanto garanta que você não tem a versão compativel com o python 2.7 e sim compativel com o python 3.x.

Você pode seguir a [documentação](https://www.pypy.org/download.html#python-3-6-compatible-pypy3-6-v7-3-1). Baixe um dos arquivos dependendo do seu sistema operacional descomprima e instale em sua máquina.

Caso você esteja em um ambiente _linux_ você pode tentar baixar usando o comando `apt-get`. 
No _windows_ você pode baixar utilizando o [chocolatey](https://chocolatey.org/packages/python.pypy).
No _macos_ você pode baixar utilizando o [homebrew](https://formulae.brew.sh/formula/pypy3#default).

Só verifique após a instalação se você tem a versão mais recente instalada usando o comando `pypy3 --version`


#### Instalando as bibliotecas
__IMPORTANTE__: Evite a todo custo desenvolver fora de um _Ambiente Virtual_, você com certeza vai precisar baixar novas libs e vai precisar gerar novos arquivos `requirements.txt`, trabalhar dentro de um ambiente virtual garante que trabalhemos todos em um ambiente controlado :).

Com o __pypy3__ funcionando em sua máquina, é o momento de criar um _Ambiente Virtual_ para você começar a desenvolver.
O nosso código não conta com uma __venv__ ja criada, então precisamos criar do 0 uma nova. Mas utilizamos estamos utilizando o __pypy3__ e agora? Você cria e acessa seus ambientes virtuais no pypy da mesma maneira que você o faz, vamos lá?

Comece digitando os seguintes comandos:
```    
$ pypy3 -m venv venv
```
Vamos la, `pypy3` é utilizado para rodar qualquer programa python com o compilador pypy que você instalou.
`-m venv` representa que você está tentando criar um novo _virtual environment_. 
O ultimo `venv` é o nome do seu _ambiente virtual_ ou seja, você pode ter mais de um _ambiente virutal_ na sua máquina, nesse caso damos o nome de `venv`.

Agora vamos ativar a `venv` na nossa máquina (Você precisa seguir esses comandos sempre que você ativar seu terminal):
+ __Mac ou Linux__
```  
$ source venv/bin/activate 
```
+ __Windows__
```
> venv/Scripts/activate
```

Saindo da sua venv
```
$ deactivate
```

Com a venv instalada em seu computador, rode o seguinte comando para instalar as dependências do projeto.
```   
$ pip install -r requirements.txt
```

__OBSERVAÇÃO E ATENÇÃO__
Algumas dependências podem causar problemas no momento da instalação, mas não tem porque se desesperar.
Se acontecer algum problema com o `psycopg2` ou `psycopg2cffi`, cheque se você tem todos os [pré-requisitos](http://initd.org/psycopg/docs/install.html#prerequisites) da lib configurados no seu computador.
O sistema usa como dependência o `cryptography`, que pode causar alguns problemas durante a instalação, caso você tenha algum problema com essa lib, tente seguir os passos de acordo com a [documentação de instalação](https://cryptography.io/en/latest/installation/)


## INICIALIZAR
Se você não quiser ficar fazendo toda vez o processo acima, na hora que for inicializar o projeto, nós por conveniência colocamos ele dentro de containers docker.

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

## Estilo do código
Nossa aplicação está toda dentro da pasta `reflow_server`, dentro dessa pasta você irá encontrar novas pastas, cada uma dessas pastas é uma [aplicação Django](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-the-polls-app). A ideia do nosso código é utilizarmos a metodologia de microsserviços e tentar aplicá-la, da melhor maneira possivel, ao Django. Ou seja, cada aplicação deve ser na medida do possivel independente uma da outra (com excessão da aplicação `core`, falaremos dela mais pra frente) compartilhando pouco código entre elas (com excessão dos `services`).

### Estrutura dos apps
+ __views__ - Se você sabe django, acreditamos que você entenda o que são as [views](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#write-your-first-view). As views funcionam como controllers (caso você venha do padrão MVC) no django, portanto, nesse projeto é necessário que as views contenham o MINIMO de lógica possivel, geralmente, elas recebem um request, processam e mandam a resposta, NÃO COLOQUE REGRA DE NEGÓCIO ou MUITA LÓGICA NAS VIEWS, caso necessário crie um `service`. Por padrão do Django as views ficam todas em um unico arquivo, mas para melhorar a legibilidade você pode separá-las em varios arquivos dentro da pasta `views` (Por padrão suas views devem ser importadas pelo caminho `reflow_server.<seu_app>.views`, ou seja, importe elas no arquivo `__init__.py` da pasta `views`)

+ __urls__ - São as urls do seu app. Por padrão no ROOT do projeto, você também vai encontrar um arquivo `urls.py`, esse arquivo no root define a url para cada app django. Dentro do seu arquivo `urls.py` no seu app, você pode utilizar `includes` para incluir urls separando-as por contextos especificos do seu código. Por exemplo, aquelas urls que cuidam das configurações, aquelas urls que servem para se conectar com apps externos, etc.
+ __tests__ - Onde devem ficar todos os testes do seu app, novamente, o ideal é que vc pense em cada app isoladamente, teste apenas seu app.
+ __serializers__ - Definido de acordo com [Django Rest Framework](https://www.django-rest-framework.org/tutorial/1-serialization/), por padrão nosso deixe nesse arquivo apenas os Serializers que você importa em suas `views` ou `externals`, relações, ou ForeignKeys, você pode deixar no arquivo `relations`
+ __relations__ - Varios models podem se relacionar com outros models com ForeignKeys, você pode definir as relações em seus models e criar [relações em seus serializers](https://www.django-rest-framework.org/api-guide/relations/) de uma maneira facil e rapida utilizando o Rest Framework. Geralmente as relações possuem pouca ou nenhuma lógica, não salvamos nenhum dado diretamente nas relações, no máximo, realizamos filtros para filtrar os dados que queremos, mas além disso nenhuma, por isso, suas relações dos serializers devem ficar no arquivo `relations.py`
+ __externals__ - Criado e definido por nós na reflow, não existe por padrão no Django. Um external é uma classe que é utilizada para se comunicar com um app externo dessa aplicação, para criar a classe você deve importar a classe `External` definida no app `core`, essa classe expõe alguns metodos, comuns para suas chamadas api como `.post()`, `.get()`, `.delete()` e `.put()`, sendo cada um desses metodos podendo ser acessados pelo `self.` dentro do seu método. Cada método do external funciona meio que como uma view, porém do lado oposto (ao invés de receber dados ele envia dados)
+ __utils__ - Pode causar confusão com `services`, então vou começar explicando porque existe `utils` e `services` e qual a diferença entre ambos. Um `utils` é uma função ou classe que faz qualquer ação que pode ser feita em um app FORA da reflow, ou seja, não é algo que precisa ser utilizado ESPECIFICAMENTE dentro da reflow, pode ser portado para outras aplicações, se você criar um novo projeto django, muito provavelmente você poderá pegar um arquivo ou função da pasta `utils` e utilizar no seu projeto pessoal, por exemplo o `RunAsyncFunction` do caminho `reflow_server.core.utils.asynchronous`.
+ __services__ - TODA A REGRA DE NEGOCIO DA NOSSA APLICAÇÃO, isso é muito importante que você entenda, toda a regra de negócio é escrita dentro dos services. Se você chama 1 service não relacionado a sua view ou serializer, muito provavelmente seu código deve ser separado em um service. (esse exemplo é muito claro ao salvar as notification_configurations que devemos chamar o pre_notification_service, ambos não são relacionados, portanto separamos o código dentro do service de notification_configurations). Com services conseguimos garantir a testabilidade do código, a legibilidade e a facilidade de se separar "só código", de códigos que efetivamente fazem algo na aplicação. A maioria do seu desenvolvimento acontecerá dentro de services. Você NÃO deve relacionar o código do seu service de NENHUMA maneira a `serializers` uma vez que ainda que os serializers mudem, isso não irá afetar o código do seu service.

### Como saber se eu devo criar um novo app ou não?
Um microsserviço, diferente de como muitas pessoas pensam, não devem resolver uma coisa SUPER especifica do seu código, obviamente um microsserviço pode crescer e não ficar mais tão pequeno. O grande problema, que causa muita confusão, não é o que é "micro" e sim o que é "serviço". Nesse ponto acreditamos que um "serviço" não faz necessariamente uma coisa muito pequena, temos serviços relativamente grandes e complexos, como o __formulary__ por exemplo. E isso volta na nossa pergunta, como saber se o que estou criando é um novo serviço ou não?

1 - Verifique os `models`. Como falado anteriormente, queremos pouco ou nenhum compartilhamento de codigo entre as aplicações, o ideal é que seu serviço de `dashboard`, seja o mais independente possivel de outros serviços, um bom passo é fazer uma modelagem que faça sentido com os dados que você mais vai utilizar dentro do seu app.
2 - Pense em regras de negócio. O que esse app quer resolver? É só uma interface pra uma api? (Talvez não precise ser um serviço separado). É um serviço com regras de negócio que será reaproveitado em outras partes do código? (Provavelmente é um serviço) Tem grandes chances de crescer no futuro? (Provavelmente é um serviço)
3 - Um exemplo: tinhamos um serviço chamado `visualization` que cuidava primordialmente da visualização dos dados em `Kanban` ou `Listagem`, porém queremos no futuro, criar mais visualizações e melhorar as visualizações de `kanban` e `listagem`, o código não possuia praticamente nenhuma correlação entre si. Então fez sentido separar em serviços menores.
4 - Outro exemplo: `formulary` talvez seja nosso maior serviço, porém não é de se espantar uma vez que basicamente nosso sistema inteiro é guiado a partir dos formulários de um usuário e de uma companhia. Faz sentido separar entre os serviços de `data` (para puxar e inserir dados), `formulary` (que contém todas as infos de construção do formulário).
No momento, acreditamos que não porque é uma coisa só e ambas as coisas se complementam. No futuro talvez possamos separar. (O seu serviço vai crescer e não tem problema algum nisso)

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
