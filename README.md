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
$ docker exec -it reflow_db psql -U postgres
```
Para acessar através do Pycharm ou outro conector
(Pode deixar a senha vazia)
```
URL = jdbc:postgresql://localhost:5432/reflow
USER = postgres
```

## Estilo do código
Nossa aplicação está toda dentro da pasta `reflow_server`, dentro dessa pasta você irá encontrar novas pastas, cada uma dessas pastas é uma [aplicação Django](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-the-polls-app). A ideia do nosso código é utilizarmos a metodologia de Domain Driven Design e tentar aplicá-la, da melhor maneira possivel, ao Django. Ou seja, cada aplicação deve ser na medida do possivel independente uma da outra (com excessão da aplicação `core`, falaremos dela mais pra frente) compartilhando pouco ou, preferencialmente, nenhum código entre elas (com excessão dos `services` e `models` APENAS). Um problema que isso pode acarretar é gerar código muito parecido um com o outro, uma vez que não se compartilha código entre os apps. Isso pode ser resolvido importando algum código de algum app no app `core`, que tem como finalidade compartilhar funcionalidades especificas entre os apps. Sempre que você tiver um código em um app e desejar usar ele em outros apps, você deve importar essa classe ou função em algum dos arquivos no aplicativo `core` e deve importá-la dentro de seus apps, diretamente do `core`. 

Obs.: `services` e `models` podem ser importados diretamente de cada app Django.

### Estrutura dos apps
+ __views__ - Se você sabe django, acreditamos que você entenda o que são as [views](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#write-your-first-view). As views funcionam como controllers (caso você venha do padrão MVC) no django. Portanto, nesse projeto é necessário que as views contenham o MINIMO de lógica possivel, geralmente, elas recebem um request, processam e mandam a resposta para o client. NÃO COLOQUE REGRA DE NEGÓCIO ou MUITA LÓGICA NAS VIEWS, caso necessário crie um `service`. Por padrão do Django as views ficam todas em um unico arquivo, mas para melhorar a legibilidade você pode separá-las em varios arquivos dentro da pasta `views` (Por padrão suas views devem ser importadas pelo caminho `reflow_server.<seu_app>.views`, ou seja, importe elas no arquivo `__init__.py` da pasta `views`)
+ __urls__ - São as urls do seu app. Por padrão no ROOT do projeto, você também vai encontrar um arquivo `urls.py`, esse arquivo no root define a url para cada app django. Dentro do seu arquivo `urls.py` no seu app, você pode utilizar `includes` para incluir urls separando-as por contextos especificos do seu código. Por exemplo, aquelas urls que cuidam das configurações, aquelas urls que servem para se conectar com apps externos, etc.
+ __tests__ - Onde devem ficar todos os testes do seu app, novamente, o ideal é que vc pense em cada app isoladamente, teste apenas seu app.
+ __serializers__ - Definido de acordo com [Django Rest Framework](https://www.django-rest-framework.org/tutorial/1-serialization/), por padrão nosso deixe nesse arquivo apenas os Serializers que você importa em suas `views` ou `externals`, relações, ou ForeignKeys, você pode deixar no arquivo `relations`
+ __relations__ - Varios models podem se relacionar com outros models com ForeignKeys, você pode definir as relações em seus models e criar [relações em seus serializers](https://www.django-rest-framework.org/api-guide/relations/) de uma maneira facil e rapida utilizando o Rest Framework. Geralmente as relações possuem pouca ou nenhuma lógica, não salvamos nenhum dado diretamente nas relações, no máximo, realizamos filtros para filtrar os dados que queremos, mas além disso nenhuma, por isso, suas relações dos serializers devem ficar no arquivo `relations.py`
+ __externals__ - Criado e definido por nós na reflow, não existe por padrão no Django. Um external é uma classe que é utilizada para se comunicar com um app externo dessa aplicação, para criar a classe você deve importar a classe `External` definida no app `core`, essa classe expõe alguns metodos, comuns para suas chamadas api como `.post()`, `.get()`, `.delete()` e `.put()`, sendo cada um desses metodos podendo ser acessados pelo `self.` dentro do seu método. Cada método do external funciona meio que como uma view, porém do lado oposto (ao invés de receber dados ele envia dados)
+ __utils__ - Pode causar confusão com `services`, então vou começar explicando porque existe `utils` e `services` e qual a diferença entre ambos. Um `utils` é uma função ou classe que faz qualquer ação que pode ser feita em um app FORA da reflow. Ou seja, não é algo que precisa ser utilizado ESPECIFICAMENTE dentro da reflow, pode ser portado para outras aplicações. Se você criar um novo projeto django, muito provavelmente você poderá pegar um arquivo ou função da pasta `utils` e utilizar no seu projeto pessoal. Por exemplo o `RunAsyncFunction` do caminho `reflow_server.core.utils.asynchronous`.
+ __services__ - TODA A REGRA DE NEGOCIO DA NOSSA APLICAÇÃO, isso é muito importante que você entenda, toda a regra de negócio é escrita dentro dos services. Se você chama 1 service não relacionado a sua view ou serializer, muito provavelmente seu código deve ser separado em um service. (esse exemplo é muito claro ao salvar as notification_configurations que devemos chamar o pre_notification_service, ambos não são relacionados, portanto separamos o código dentro do service de notification_configurations). Com services conseguimos garantir a testabilidade do código, a legibilidade e a facilidade de se separar "só código", de códigos que efetivamente fazem algo na aplicação. A maioria do seu desenvolvimento acontecerá dentro de services. Você NÃO deve relacionar o código do seu service de NENHUMA maneira a `serializers` uma vez que ainda que os serializers mudem, isso não irá afetar o código do seu service.
+ __consumers__ - Por padrão os `consumers` são algo do [Django Channels](https://channels.readthedocs.io/en/latest/) porém na nossa aplicação realizamos uma pequena mudança em como os consumers funcionam, uma vez que no client, podemos ter apenas UM e apenas UM webservice conectado por vez. Com isso criamos um consumer Base no arquivo `consumers.py` no qual seus consumers devem por padrão importar dele. Isso acarreta uma pequena e simples diferença em nosso app onde os consumers viram classes simples que apenas importam de um Consumer pai. Os consumers, caso você não tenha entendido ainda funcionam para se comunicar em tempo real com nossos clientes e outras aplicações, sem a necessidade de apis. Conseguimos comunicar entre as aplicações através de eventos em tempo real. Leia mais sobre em `core/consumers.py`

##### Importante
__Vi que vocês criaram os arquivos `permissions` os arquivos `externals` e os arquivos `events`. Isso não me parece algo padrão do Django__

Realmente, os 3 tipos de arquivos citados foram criados por nós da Reflow e qual é o racional por trás desses arquivos? porque eles não estão na pasta 'utils'?
1 - A definição deles acontece no app `core`. Ou seja, se você criar um tipo de arquivo que será utilizado em um app, então ele deve ser criado na pasta `core`. 
2 - Esses arquivos contém funcionalidades criadas que podem ser extendidas e utilizados em cada app django individualmente e de maneira descentralizada. O `permissions` permite que cada app defina suas próprias regras de permissionamento, o `externals` permite que cada app defina e organize suas chamadas de apis externas, o `events` permite que cada app defina quais eventos se deseja "ouvir" de maneira explicita.

__"COMO ASSIM?"__ 
Imagina que eu quero criar uma nova funcionalidade, essa funcionalidade é despachar os eventos para os consumers através do ChannelLayer do django channels. Para isso pensei em criar um novo tipo de arquivo chamado 'dispatchers.py' que será meu despachador de eventos.

Primeira pergunta a se fazer: Isso é realmente algo que cada app precisa implementar só seu? É REALMENTE uma funcionalidade tão comum assim? Ou isso é mais uma função comum?
Se a resposta for não, provavelmente sua classe deva ser definida na pasta utils. Se será utilizado por todos os apps do server, deve ser criado na pasta `utils` do app `core`.
Caso a resposta for sim, você deve pensar em como deverá ser definido e utilizado essa nova funcionalidade dentro de cada app.
Lembre-se, cada app DEVE SER DESCENTRALIZADO.
Por exemplo, no caso dos serializers, quando você faz `from rest_framework import serializers` ao acessar a variavel `serializers` você terá acesso as classes Serializer, CharField, BooleanField, entre outros, para que você seja capaz de montar seu próprio serializer.
No caso dos `permissions` eu devo criar minhas classes de permissionamento dentro de cada app e defini-las no arquivo `settings.py`. Você percebe que dentro do arquivo `permissions.py` existe uma documentação concisa de como criar permissões dentro dos seus apps. O mesmo pode-se dizer para `events.py` na pasta `core`

Recomendo pensar em soluções onde o desenvolvedor não deva usar a classe diretamente, mas pelo contrário, possa usar uma string, assim como é por exemplo ao definir ForeignKeys nos models:
```python
# Aqui estou usando a classe `Field` diretamente, ao usar a classe diretamente posso ter problemas de
# importação circular, a ordem que os models são criados também pode causar problemas, para isso preferimos usar string.
field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True)

# se eu definir a classe Field antes ou depois de definir essa relação, simplesmente não tem problema. Ao mesmo tempo, problemas
# importação circular não existem uma vez que eu simplesmente não preciso importar nada
field = models.ForeignKey('formulary.Field', on_delete=models.CASCADE, null=True)

```

Enquanto externals são classes que eu chamo diretamente dentro do código, `permissions` e `events` devem ser definidas no arquivo settings.py. É importante pensar em uma maneira lógica e clara para se utilizar as apis.

TL.DR.: Só crie tipos de arquivos novos se eles realmente trouxerem alguma funcionalidade onde cada app deve definir o seu, assim como `views`, `urls`, `serializers` e outros. As views de um app são as views usadas especificamente pelo app, serializers são os serializers usados especificamente por um app, e assim por diante. Caso não seja o caso, ou ele é um service, ou ele é deve estar na pasta `utils`

### Como saber se eu devo criar um novo app ou não?
Um microsserviço, diferente de como muitas pessoas pensam, não devem resolver uma coisa SUPER especifica do seu código, obviamente um microsserviço pode crescer e não ficar mais tão pequeno. O grande problema, que causa muita confusão, não é o que é "micro" e sim o que é "serviço". Nesse ponto acreditamos que um "serviço" não faz necessariamente uma coisa muito pequena, temos apps/serviços relativamente grandes e complexos, como o __formulary__ por exemplo. E isso volta na nossa pergunta, como saber se o que estou criando é um novo app/serviço ou não?

1 - Verifique os `models`. Como falado anteriormente, queremos pouco ou nenhum compartilhamento de codigo entre as aplicações, o ideal é que seu app/serviço de `dashboard`, seja o mais independente possivel de outros apps/serviços, um bom passo é fazer uma modelagem de dados que faça sentido com os dados que você mais vai utilizar dentro do seu app.

2 - Pense em regras de negócio. O que esse app/serviço quer resolver? É só uma interface pra uma api? (Talvez não precise ser um serviço separado). É um app/serviço com regras de negócio que será reaproveitado em outras partes do código? (Provavelmente é um serviço) Tem grandes chances de crescer no futuro? (Provavelmente é um serviço)

3 - Um exemplo: tinhamos um serviço chamado `visualization` que cuidava primordialmente da visualização dos dados em `kanban` ou `listing`, porém queremos no futuro, criar mais visualizações e melhorar as visualizações de `kanban` e `listing`, o código de ambos não possuia praticamente nenhuma correlação entre si. Então fez sentido separar ambos em serviços/apps menores.

## Data Dump
O sistema para funcionar depende de alguns dados obrigatórios (geralmente com a flag `_type` no nome do banco de dados), você pode encontrá-los na pasta `fixtures` com o nome `required_data.json`

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
$ docker-compose run reflow_server pypy3 manage.py loaddata fixtures/required_data.json
$ docker-compose run reflow_server pypy3 manage.py loaddata fixtures/theme_data.json
```
+ __terminal__
```
$ pypy3 manage.py loaddata fixtures/required_data.json
$ pypy3 manage.py loaddata fixtures/theme_data.json
```
