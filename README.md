# Scrum Real

Este é um projeto com objetivos didáticos que eu criei para estudar [Flask](http://flask.pocoo.org) e a integração com o
Google App Engine([GAE](http://code.google.com/appengine/))

### Por que usar?

Basicamente o uso é motivado quando a equipe só tem homem da letra feia e que não escreve faz muito tempo, então como
já temos prática em digitar essa app irá facilitar seu trabalho. :D

### Como funciona?

Basta você ir criando as tarefas, que no caso são representados por postits, e preencher os campos, caso queira gerar
o gráfico burndown também, basta preencher os pontos nas tarefas e dizer o intervalo do seu sprint e o gráfico será
adicionado ao final do arquivo.


### Executando localmente

Se você quiser executar o projeto localmente, seja para contribuir ou porque você estava sem internet quando precisou,
basta seguir os seguintes passos:

Faça download do [SDK do GAE para Python](http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python)

Faça um clone do repositório

    git clone git://github.com/fabiocerqueira/scrumreal.git

Execute o servidor de desenvolvimento do GAE

    /caminho/do/google_appengine/dev_appserver.py /caminho/do/scrumreal

Geralmente eu crio um link simbólico do arquivo `dev_appserver.py` e `appcfg.py` na pasta do projeto
    
    ./dev_appserver.py .
