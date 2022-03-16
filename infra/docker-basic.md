class: center, middle, blue

![Epitech](/infra/epitech.png)

---
class: center, middle, blue

# Docker

![Docker](/infra/docker-logo2.png)

---
class: middle

## Evolution des équipes

La gestion d'une application était souvent:

**Dev**: utilise dernier paquet à jour, nouvelle version de compilateur, ...

**QA**: teste les derniers bugfixs / releases des Dev via des cahiers de tests, non reproductibiltés de bugs

**SysAdmin**: demande de la stabilité, Centos avec support sur 10 ans, vieille version de compilateur / librairie

---
class: middle

## Evolution des équipes

La gestion d'une application a évolué vers:

**DevOps**: développe, teste & déploiement en production

**SRE**: vue globale de la prod pour débugger ou optimiser la production (configuration ou code)

---
class: middle

## Un peu d'historique

- Le on-premise: l'application est déployée sur la machine
- La virtualisation lourde: une machine complète est "émulée"
- La containerisation: un OS est simulé à partir du noyau courant
- Docker: une containerisation qui comprend le minimun pour faire fonctionner l'application (et uniquement elle)

???
- Dédié
- Virtualisation (Machine Complete)
- Container (LXC)
- Docker
- environnement figé

---
class: middle,smallpic,center

## Comparaison Virtu / Docker

![Virtu](/infra/docker-virtual-machines.png) / 
![Docker](/infra/docker-containers.png)


---
class: middle

## Docker

- Permet de containeriser une application et ses dépendances
- Image imutable, ne dépend pas de ce qu'il y a sur la machine: "identique" entre le dev et la prod
- Docker c'est le go (ou rust) d'un binaire: all inclusive

???
- Utilisation des cgroups / namespace / overlay filesystem

---
class: middle

## Demo time

???
- PHP 5 and PHP 7

---
class: middle

## Les commandes à savoir:

```
docker inspect
docker ps
docker images
docker build
```

---
class: middle

# Install Time

- Mac
- Linux
- Windows: WSL2

---
class: middle

## Hello World

```
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete 
Digest: sha256:4c5f3db4f8a54eb1e017c385f683a2de6e06f75be442dc32698c9bbe6c861edd
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
...
$ docker ps
[...]
$ docker ps -a
[...]
$ docker images
[...]
```

---
class: middle

## Registry

Les images dockers sont stockés dans une registry:
par défaut, docker va résoudre le nom d'une image en local
puis sur hub.docker.com

Le nom d'une image docker est `vendor/name:tag`

- `vendor` (ou autre registery que docker), ignorés sur les images "officielles"
- `name`: le nom de l'application ou de l'OS (mysql ou ubuntu)
- `tag`: la version de l'image, si absent, c'est le tag `latest` qui est utilisé

Une même image peut être tagger plusieurs fois:
- L'image nginx:1.20 est aussi taggé nginx:1.20.2 
- le tag 1.20 représente la dernière version stable de la branche 1.20
- alors que 1.20.2 représente spécifiquement cette version de bugfix.


---
class: middle

## Création de notre container Docker

Les instructions sont par défaut contenu dans le fichier Dockerfile dans le même répertoire

```
$ cat Dockerfile
FROM alpine
CMD ["echo", "Hello !"]
$ docker build -t myhelloworld .
...
Successfully tagged myhelloworld:latest
$ docker run myhelloworld
Hello !
```

???
le tag via `-t` qui permet de retrouver son image plutôt que par son ID
permet aussi l'annotation (`latest`, défaut ou une version)

---
class: middle

## Les layers

Si on fait un `docker inspect` sur le container alpine & myhelloworld,
on remarque que le champ `RootFS` utilise le même layer: nous n'avons au
final que modifié la commande lancé sur l'image alpine.

Ajoutons maintenant deux fichiers

```
$ cat Dockerfile
FROM alpine
RUN echo "I was here" > /fichier
COPY fichier2 /
CMD ["cat", "/fichier", "/fichier2"]
$ docker build -t myhelloworld .
...
Successfully tagged myhelloworld:latest
$ docker run myhelloworld
I was here
```

---
class: middle

Chaque opération qui modifie le système de fichier va rajouter la création d'un layer supplémentaire.

Chaque layer sera download ou upload indépendement, permettant ainsi la réutilisation du cache.

```
$ docker history <mon-image>
...
```

**conseil**

Pour la création de votre container, utiliser des petites étapes type RUN

Pour la finalisation de votre container, regrouper le plus possible vos étapes de RUN et effacer
les caches

---
class: middle

## Le context

Lors de la création d'un container docker, le context par défaut est le répertoire courant:

chaque fois qu'un fichier va être modifié, le context changera.

**note** seul les fichiers d'un contexte peuvent être copié dans l'image.

**conseil**

Pensez à configurer `.dockerignore` pour ignorer des fichiers qui ne seront pas utilisé dans l'image docker.

---
class: middle

## Workshop

Cloner ce répertoire http://github.com/Cristy94/markdown-blog.git et le déployer dans un container

**conseil**
- regarder les dépendances du projet
- faites pas à pas
- partir d'une image dont vous maitrisez l'OS
- utiliser apache comme serveur web

???
Docker build context
Layer

---
class: middle

##  Exemple

```
$ cat Dockerfile
FROM ubuntu:20.04

ENV TZ="Europe/Paris"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -yy apache2 php libapache2-mod-php tzdata && \
    apt clean && \
    a2enmod rewrite
COPY . /var/www/html/
CMD  [ "apachectl", "-D", "FOREGROUND"]
```

---
class: middle

## Les Volumes

Permettre à un docker d'utiliser des données locales à la machine
(persistance base de donnée, page web à servir, ...)

---
class: middle

Volume nommé
```
$ docker volume create mydata
mydata
$ docker volume inspect mydata
[
    {
        "CreatedAt": "2022-03-15T15:12:57+01:00",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/mydata/_data",
        "Name": "mydata",
        "Options": {},
        "Scope": "local"
    }
]
$ docker run -v mydata:/inside-container -it alpine 
```

---
class: middle

Point de montage sur un docker

```
$ docker run -it -v $HOME:/my-home alpine
/ # ls
bin      home     mnt      proc     sbin     tmp
dev      lib      my-home  root     srv      usr
etc      media    opt      run      sys      var
```

**⚠** 
- un volume nommé sera crée automiquement (absence de / comme suffix)
- un répertoire sera crée automatiquement s'il n'existe pas

---
class: middle

## Exposer des ports

`EXPOSE` indique à Docker et à l'utilisateur que l'appli écoutera sur ce(s) port(s)

=>
Par défaut Docker utilise une interface réseau virtuelle (bridge sous linux)
Chaque instance aura une IP attaché à ce réseau virtuelle.

=>
Il est possible d'exposer un port d'un docker sur l'interface de votre PC

???
Attention
certains exemples sur Internet abuse de ce mécanisme et vous pourrez rencontrer
des problèmes (port déjà utilisé ou port < 1024 donc inutilisable par un utilisateur non root)

---
class: middle

## Sécurité

Isolation != Sécurité

- Ne pas exposer `/var/run/docker.sock` dans un container
- Limiter les resources
- Utiliser des images officiels
- Utiliser des tags sur les version majeures (php:8 par ex)
- Rebuilder ses images après des alertes de sécurité sur les dépendences (image ou paquet)
- Embarqué seulement ce qui est nécessaire
- Ne pas lancer le process en root
- Scanner ses images

---
class: middle

## Conseil

- Avoir un seul process au sein d'un container
- Avoir le process principal avec le PID 1
(lancé par le CMD)

=> si le PID 1 s'arrête, le container s'arrête
(comme sous linux)

---
class: center, middle, blue

# Docker Compose

![DockerCompose](/infra/docker-compose-logo.png)

???
Permet d'orchestrer une application multi container


---
class: middle

## Exemple

Application Laravel:
- code php
- base de donnée
- memcache / redis pour le cache

---
class: middle

```
$ cat docker-compose.yml
version: '3.8'

services:
  helloworld:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
  mysql:
    image: "mysql:8"
    environment:
      - MYSQL_DATABASE=reppop
      - MYSQL_USER=reppop
      - MYSQL_PASSWORD=reppop
      - MYSQL_ROOT_PASSWORD=secret
```

---
class: middle

## Run

```
# crée le réseaun construit / récupère les images, démarre tout
$ docker-compose up

# détruit le réseau
$ docker-compose down
```


---
class: middle

## Le réseau

Un réseau est crée de manière automatique et un DNS
est crée automatiquement:

L'application se connectera à mysql via le DNS mysql
(l'entrée `mysql:` dans le fichier `docker-compose.yml`)

l'information `ports` permet d'indiquer que l'image `helloworld` expose le port 8000.

Les IPs peuvent être figés (attention aux ranges !)

---
class: middle

## Dépendences entre services

Dans l'exemple précédent, l'application peut tomber en erreur car
l'application va démarrer en même temps que mysql.

```
version: "3.9"
services:
  web:
    build: .
    depends_on:
      - db
      - redis
  redis:
    image: redis
  db:
    image: postgres
```

**note** le timeout par défaut sur les services peut être trop court parfois

---
class: middle

## Workshop

Déployons votre application Laravel dans Docker Compose

---
class: middle

## Attention

- Pas de secret dans le docker-compose.yml !
- La syntaxe docker-compose 3 est compatible docker swarm (plusieurs machines)

---
class: middle

## Entracte : Apache HTTP / Reverse Proxy

Boring stuff...

---
class: middle

## Notre premier déployement

- Création d'un compte gratuit sur https://hub.docker.com
- Push de vos images sur votre compte
- Me communiquer un nom pour que je puisse renseigner un DNS
- Se connecter sur dockerworkshop.murlock.org avec votre user
- Editons ensemble le fichier de conf d'apache !