# Reverse Proxy

## Contexte

pourquoi un exposer un serveur web derrière un autre serveur web:

- limiter les risques (log4j !)
- permet une mise à jour d'un sous-ensemble de l'infra de manière transparente
- permet de faire de l'A/B testing, ... [X]

Les solutions les plus répandus

- Apache (plutôt historique, fait tout)
- Nginx (le concurrent mais version payante pour plus de fonctionnalité)
- Haproxy (Haute performance)

## Virtual host

Rappel: DNS

Le DNS permet d'associer une IP à un nom de domaine : 
- difficile d'avoir des IPV4 dédiés, et il y a du NAT caché côté opérateurs :( (lien vers le pb de pedo avec le NAT (SFR ?))
- IPv6 tout le monde n'est pas prêt 

Le virtual host permet de partager une IP pour plusiers nom de domaines

## Reverse proxy / Load balancer

Le reverse proxy permet de faire une requête venant d'internet vers le serveur final.
On peut ajouter la notion de backend pour faire de la distribution de requêtes vers plusieurs backends.

Le load balancer est aussi utiliser en interne

## Prérequis

Avoir des logs et des metrics, et si jamais vous avez plusieurs LB / Reverse proxy, il
est impératif d'avoir un txid qui va se propager entre le service initial et les différents services

Lien: opentracing, elastic search + kibana, loki + prometheus + grafana

## Cas d'usage

Exemple d'utilisation chez Scaleway:

### Mise à jour de X serveurs:

- "drain" du backend
- mise à jour du backend
- "réactivation" du backend, si pas possible après plusieurs secondes:
mise à jour stoppé: le devops doit intervenir pour identifier le pb

### Problème réseau

- le reverse proxy détecte que la sonde /status ne fonctionne plus après X échecs
- le backend en question est désactivé, i.e. mis hors flux.
- la sonde /status est testé régulierement

### A/B Testing

- Une partie des serveurs est mis à jour avec la nouvelle version
- On paramètre les backendend pour distribuer les requetes avec un ratio (80/20 par exemple)
- Soit c'était une mise à jour: on surveille le ratio de code success/erreur
- Soit c'était un test de site web à destination d'utilisateur et on va vérifier le retour d'engagement

## Exemple

Vous avez un service qui nécessite une version de PHP 6 mais votre serveur utilise déjà
une version de PHP 8.

Vos options:
- bazooka: prendre un nouveau serveur (coût)
- VM: (virtd ou ...) 
- container: déployer l'application dans Docker / Podman (pas forcément possible/simple 
suivant les dépendences)
- docker-compose: permet d'externaliser des services pour avoir chaque container qui ne fourni qu'un seul service
- LXC: réutilise l'option bazooka mais en utilisant la séparation légère (séparation des process, ...)

NOTE: 
- il est conseillé de passer vers Podman: ce dernier permet des containers d'être
lancé sans droit root !
- si vous créer vos propre container, vérifier ces différents points <lien>