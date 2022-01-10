# Reverse Proxy

## Un proxy ?

Un proxy est un intermédiare entre le client et le serveur d'une resource.

Plus cas d'utilisation

- Être Anonyme*
- Partager un cache
- Permet de maitriser l'accès de resource externe d'une entreprise à Internet*

![Proxy](1280px-Proxy_concept_en.svg.png)

## Un reverse proxy

Un reverse proxy permet à l'inverse de concentrer l'accès à une resource interne.

**GRAPH**

- Séparer la partie accessible depuis Internet avec le service lui-même, permet d'ajouter des règles de sécurités, ...
- Permettre la séparation entre plusieurs service d'après le même Hostname
- Permet de mettre en cache du contenu statique 
- Déléguer la partie TLS au reverse proxy

### DNS

Un DNS est l'association IP (le protocole Internet) au nom de domaine.
Pour plein de raison, l'IP associé à un nom de domaine est gardé en cache par tout les serveurs intermédiaires.

***à supprimer ou simplifier***:

Le site www.perdu.com est associé à l'IP 208.97.177.124, c'est un enregistrement de type A (on pourrait dire bas niveau), avec très souvent un temps de cache de 24h.
A chaque enregistrement de type A, il est possible d'ajouter des enregistrement de type CNAME.

### Questionnaire

**A REECRIRE**

GET test.com/ => Reverse Proxy => Service 1

GET test.com/static => Reverse Proxy => Service 2

GET admin.test.com => Reverse Proxy => Service 3

Avec un seul serveur exposé sur Internet, il est possible d'attaquer plusieurs services en interne.

Comme il n'est plus possible d'avoir une IP par nom de domaine, la version 1.1 de la norme HTTP à introduit l'entête Host.

Lorsqu'un serveur HTTP reçoit une requête, il analyse le champ `Host` pour savoir où envoyer la requête.


### Apache httpd

Historiquement le premier projet de la fondation Apache, lorsqu'on parle 
du serveur apache, il faudrait parler du server httpd d'Apache. 

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
