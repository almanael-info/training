class: center, middle, inverse

# Reverse Proxy

---
class: middle

## Un proxy ?

Un proxy est un intermédiaire entre le client et le serveur d'une resource.

En français, un serveur mandataire

---
class: pic,middle,center

![Proxy](infra/1280px-Proxy_concept_en.svg.png)

---
class: middle


**quelques cas d'utilisation :**

- Être anonyme
- Partager un cache
- Permet de maitriser l'accès de resource externe d'une entreprise à internet

???
- On n'est pas anonyme pour le service proxy
- Le cache peut parfois contenir des infos personnelles

---
class: middle,center

## Reverse proxy

Un reverse proxy permet à l'inverse d'imposer le passage à un serveur pour l'accès à une resource interne

---
class: pic,center,middle

![Reverse Proxy](infra/Reverse_proxy_h2g2bob.svg.png)

---
class: middle

## Intérêt:

- Séparer la partie accessible depuis Internet avec le service lui-même
    - un point d'accès unique
    - permet d'ajouter des règles de sécurités
- Permettre la séparation entre plusieurs service pour le même domaine
- Permet de mettre en cache du contenu statique
- Déléguer la partie TLS au reverse proxy

???

- Attention au contenu statique mais souvent plus simple car on maitrise le site
- Mise à jour des certificats sans faire d'interruption de service

---
class: middle,pic

## Apache HTTP

![Apache](infra/apache.png)


Historiquement le premier projet de la fondation Apache, lorsqu'on parle
du serveur apache, il faudrait parler du server http d'Apache.

???

Couteau suisse avec la possibilité d'ajouter plein de modules

---
class: middle

## Installation

```bash
$ apt update
$ apt install -y apache2
$ curl -I http://localhost/
HTTP/1.1 200 OK
...
```

???

Pour ubuntu 20.04

---
class: middle

## Configuration d'un nouveau site

Un site statique

```bash
# on désactive la conf par défaut
$ a2dissite 000-default
$ cat <<EOF >/etc/apache2/sites-available/example.conf
<VirtualHost *:80>
  DocumentRoot /var/www/html
</VirtualHost>
EOF
$ a2ensite example.conf
Enabling site exemple.
$ systemctl reload apache2
```

???

---
class: middle

## Configuration reverse-proxy

```bash
$ a2enmod proxy_http # à ne faire qu'une fois
# éditer le fichier /etc/apache2/sites-available/example.conf
# remplace DocumentRoot /var/www/html
# par ProxyPass / http://127.0.0.1:8000/
$ systemctl restart apache2
```

Quel va être le résultat ?

???

Attention: on a rajoute un nouveau module d'où le restart au lieu de reload

---
class: middle

## 503 Service unavailable

```bash
$ curl -I http://127.0.0.1
HTTP/1.1 503 Service Unavailable
```

Apache HTTP veut contacter le service web sur 127.0.0.1:8000
mais aucun service n'est accessible.

Lançons notre service
```bash
$ php artisan serve --port 8000
```

Et...

???

- `apt install -y php php-cli php-zip php-dom unzip`
- `wget https://getcomposer.org/installer`
- `php installer`
- `php composer.phar create-project laravel/laravel hello-world`
- `php artisan serve --port=8000`

---
class: middle

## 200 OK

```bash
$ curl -I http://127.0.0.1
HTTP/1.1 200 OK
...
```

# ✌️

???

---
class: middle

## DNS

Le DNS associe une IP (l'adresse logique) au nom de domaine

```shell
$ ping -c1 perdu.com
PING perdu.com (208.97.177.124) 56(84) bytes of data.
```
Mais seulement 4 milliards de périphériques (*)


???

- grosso modo hein, bascule vers IPv6 mais c'est lent
- demander qu'est-ce qu'un périphérique: box internet, smartphone, console, ordi, serveur, router, point wifi, badgeuse, ...
- Une IP est l'adresse d'un immeuble, le port est le numéro d'appartement

---
class: middle

## DNS

L'idée: partager une IP avec plusieurs nom de domaine

```shell
$ nslookup -q=a gitlock.me
Name:	gitlock.me
Address: 91.121.155.34
$ nslookup -q=a murlock.org
Name:	murlock.org
Address: 91.121.155.34
```

Mais ce n'est pas le même contenu !
Une idée ?

???

nslookup permet de interroger les différents enregistrements lié
à un nom de domain
(mail, ...)
HTTP 1.1 ! (1999)


---
class: middle

## Test en local

Dans l'exemple, on va utiliser `vcap.me` qui redirige tout les sous domaines
vers l'IP local à l'ordinateur (127.0.0.1)

*note* il est possible d'utiliser `/etc/hosts`

???

Home sweet Home

---
class: middle

## Virtual Host 1


- Editons le fichier `/etc/apache2/sites-available/example.conf`
- Ajoutons les lignes
- `ServerName example.vcap.me`
- `ServerAlias exemple.vcap.me`

???

Permet d'avoir une seule configuration pour plusieurs domaines

---
class: middle

## Virtual Host 2

```bash
$ cat <<EOF >/etc/apache2/sites-availables/perdu.conf`
<VirtualHost *:80>
    ProxyPass 127.0.0.1:8001
    ServerName perdu.vcap.me
</VirtualHost>
EOF
$ systemctl reload apache2
```

???

Note: on utilise ici un autre port pour la destination

---
class: middle

## Résultat

---
class: middle, center

# Les pièges

[!Proxy](infra/error_proxy.png)


---
class: middle

### Mauvais site

Utiliser une IP ou un nom de domaine qui est résolu sur la même IP.

`perdu.vcap.me` & `example.vcap.me` mais `toto.vcap.me` sera aussi résolu

Avoir un VirtualHost par défaut qui sera nommé 000-default par example avec une page d'erreur statique

---
class: middle

![Proxy](infra/logs.jpg)

Regarder les logs du service ET du reverse-proxy
(configuration pas aligné par exemple)

---
class: middle

## Vérifier sa configuration Apache

```bash
$ apache2ctl -t
Syntax OK
```

---
class: middle

## Les headers

Certaines entêtes sont généralement présente pour un reverse proxy

```
# l'IP du client
X-Forwarded-For: 127.0.0.1
# le nom de domaine reçu par Apache
X-Forwarded-Host: example.vcap.me
# le nom de domaine résolu par Apache
X-Forwarded-Server: example.vcap.me
```

---
class: middle, center

# ANNEXE

---
class: middle

## HTTP/1.1

Le nom de domaine de la requête est envoyé au serveur,
permettant ainsi à celui ci de savoir quel Virtual Host
utilisé
```bash
$ curl -vIs http://toto.vcap.me
HEAD / HTTP/1.1
Host: toto.vcap.me
...
```

---
class: middle

## Network can't lie

Utiliser les outils comme wireshark (outil graphique)
ou ngrep ou tcpdump

```bash
$ sudo ngrep -d any port 80
```
ou
```bash
$ sudo ngrep -d any port 8000
```

port 80: entre Internet et le reverse proxy
port 8000:  entre le reverse proxy et le service

???

---
class: middle

## Reverse Proxy et le path

Il est possible d'avoir un service différent exposé sur un même
VirtualHost avec Location

```
<VirtualHost>
  ServerName location.vcap.me
  ProxyPass 127.0.0.1:8000
  <Location /private>
    ProxyPass 127.0.0.1:9000
  </Location>
  <Location /image>
    # static here
  </Location>
</VirtualHost>
```

---
class: middle

## DNS

Les types d'enregistrement DNS

```bash
A     IPv4
AAAA  IPv6
MX    Serveur de mail
CNAME (sous)-Domaine qui pointe vers un autre nom de domaine
TXT   Ajoute des propriétés à un nom de domaine
```

???

CNAME => les enregistrements CNAME associé à un type A vont partager le même cache

TXT => certains sites vous demande d'un ajouter pour prouver que vous en êtes propriétaires

---
class: middle

## TLS

Prérequis:
- avoir un nom de domaine
- un serveur accessible depuis Internet via le domaine
- un VirtualHost configuré avec www.domain.org & domain.org
Installation
```bash
$ apt  install -y certbot python3-certbot-apache
[...]
$ certbot --apache


---
class: middle, center

# QUESTIONS


---
class: middle

**References**

- Certbot: https://urlz.fr/hbLg
- Apache HTTP: https://urlz.fr/hbLh
- DNS: https://urlz.fr/hbLj
- Wireshark: https://urlz.fr/hbLl
