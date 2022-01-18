class: center, middle, inverse

# Reverse Proxy

---

## Un proxy ?

Un proxy est un intermédiare entre le client et le serveur d'une resource.

---
class: pic,middle,center

![Proxy](/infra/1280px-Proxy_concept_en.svg.png)

---
class: middle


**quelques cas d'utilisation :**

- Être anonyme
- Partager un cache
- Permet de maitriser l'accès de resource externe d'une entreprise à Internet

???

- On n'est pas anonyme pour le service proxy
- Le cache peut parfois contenir des infos personnelles

---
class: middle,center

## Reverse proxy

Un reverse proxy permet à l'inverse de concentrer l'accès à une resource interne.

---
class: pic,center,middle

![Reverse Proxy](/infra/Reverse_proxy_h2g2bob.svg.png)

---
class: middle

**Intérêt:**

- Séparer la partie accessible depuis Internet avec le service lui-même
    - un point d'accès unique
    - permet d'ajouter des règles de sécurités
- Permettre la séparation entre plusieurs service pour le même domaine
- Permet de mettre en cache du contenu statique 
- Déléguer la partie TLS au reverse proxy

???

- Attention au contenu statique mais souvent plus simple car on maitrise le site

---
class: middle

## Apache HTTP

Historiquement le premier projet de la fondation Apache, lorsqu'on parle 
du serveur apache, il faudrait parler du server httpd d'Apache. 

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

## Configuration nouveau site

Site statique

```bash
$ cat <<EOF >/etc/apache2/sites-available/example.conf
<VirtualHost *:80>
  ServerName example.vcap.me
  DocumentRoot /var/www/html
</VirtualHost>
EOF
$ a2ensite example.conf
Enabling site exemple.
$ systemctl reload apache2
```

???
*.vcap.me redirige tout les sous domaines vers 127.0.0.1 qui est une addresse locale à tout les ordinateurs

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

Apache HTTP veut contacter le service web sur 127.0.0.1:8000

Lançons un service

---
class: middle

### DNS

Le DNS:
- associe une IP (l'adresse logique) au nom de domaine

```shell
$ ping -c1 perdu.com
PING perdu.com (208.97.177.124) 56(84) bytes of data.
```

---
class: middle

---

???

---
class: middle

**A REECRIRE**

GET test.com/ => Reverse Proxy => Service 1

GET test.com/static => Reverse Proxy => Service 2

GET admin.test.com => Reverse Proxy => Service 3

Avec un seul serveur exposé sur Internet, il est possible d'attaquer plusieurs services en interne.

Comme il n'est plus possible d'avoir une IP par nom de domaine, la version 1.1 de la norme HTTP à introduit l'entête Host.

Lorsqu'un serveur HTTP reçoit une requête, il analyse le champ `Host` pour savoir où envoyer la requête.


### Apache httpd

### Exemples

Un site web qui est fourni par Apache directement

```
<VirtualHost *:80>
    DocumentRoot /www/test.com/
    ServerName test.com 

    # Autres directives ici
</VirtualHost>
```

Un site web en mode reverse-proxy

```
<VirtualHost *:80>
    ServerName autre.com
    ProxyPass http://127.0.0.1:8000
</VirtualHost>
```

### Démarrage rapide

Sur Debian/Ubuntu:

```
$ apt install apache2
$ a2enmod proxy_http
```

Création de votre fichier de configuration dans `/etc/apache2/sites-availables`

```
$ cat <<EOF >/etc/apache2/sites-availables/test.com.conf
<VirtualHost>
    ProxyPass http://127.0.0.1:8000
    ServerName test.com
</VirtualHost>
EOF
```
puis activation du site
```
$ a2ensite test.com.conf
$ systemctl reload apache2
$ apache2 -M
```


Sur Centos 8

```
$ yum install httpd
$ httpd -M
```

Après chaque modif de conf, il est recommandé de faire une vérification avant de relancer Apache pour éviter d'avoir une interruption 
```
$ apache2 -t
```


### Test Rapide

#### Lancement du service en lui-même
Lancement d'un service HTTP lambda
```
$ python -m http.server 8080
```
ou si vous avez déjà un projet Laravel
```
$ php artisan serve --port=8080
```

#### Création de la configuration Apache

```
<VirtualHost *:80>
    ServerName autre.com
    ProxyPass http://127.0.0.1:8000
</VirtualHost>
```

```
$ systemctl reload apache2
```

#### Test en ligne de commande

```
$ curl -H "Host: autre.com" http://127.0.0.1:8000
...
```
à tester vs
```
$ curl http://127.0.0.1:8000
```
