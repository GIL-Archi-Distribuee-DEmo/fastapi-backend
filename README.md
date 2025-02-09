# Projet : Architecture distribuée avec Kubernetes, Minikube, Docker et Kafka

## 📌 Description
Ce projet met en place une architecture distribuée basée sur **Kubernetes** et **Minikube**, avec **FastAPI**, **Prisma**, **PostgreSQL**, **MySQL** et **Kafka**.  
Il utilise des **services distincts** pour gérer les fournisseurs et les produits avec une **synchronisation via Kafka**.

---

## 🚀 Prérequis
Avant de commencer, assure-toi d'avoir installé les éléments suivants :

### 1️⃣ **Docker**
Docker est requis pour builder et exécuter les containers.
- 📌 **Installation Docker** : [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

### 2️⃣ **Kubernetes & Minikube**
Kubernetes orchestre les services, et Minikube permet de les exécuter en local.
- 📌 **Installation Minikube** : [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)
- 📌 **Installation kubectl** (CLI pour Kubernetes) : [https://kubernetes.io/docs/tasks/tools/](https://kubernetes.io/docs/tasks/tools/)

Vérifier que tout est bien installé :
```bash
docker --version
kubectl version --client
minikube version
```
## Configuration et déploiement du projet 
On doit maintenant créer les images docker, les mettre dans l'environnement de minikube et les apply dans kubernetes :
```bash
minikube start
eval $(minikube docker-env)
docker build -t fournisseurs-service -f Fournisseurs/Dockerfile Fournisseurs/
docker build -t produits-service -f Produits/Dockerfile Produits/
docker build --env-file .env -t mysql-db -f Databases/Dockerfile.Mysql Databases/
docker build --env-file .env -t postgres-db -f Databases/Dockerfile.Postgres Databases/


kubectl apply -f kubernetes/zookeeper.yaml
kubectl apply -f kubernetes/kafka.yaml
kubectl apply -f kubernetes/akhq.yaml
kubectl apply -f kubernetes/mysql.yaml
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/produits.yaml
kubectl apply -f kubernetes/fournisseurs.yaml
```
## Vérification du déploiement 
On peut maintenant vérifier si nos pods et services sont bel et bien déployé avec :
```bash
kubectl get pods
kubectl get services
```
Il faudra attendre un peut avant que les services sont tout en Running. Si après un cout moment de 2-3min est passé et il y'a encore des ERROR, vous pouvez consulter les logs du service avec :
```bash
kubectl logs -f nom-du-pod-xxxxx
```
## Lancement des tunnels :
Maintenant afin d'accéder de l'extérieur au services, on doit executer la commande suivante :
```bash
minikube tunnel
```
et maintenant on peut accéder à nos services via la external-ip.

## Test de l'API :
Fastapi donne accès à l'api avec un tool graphique et cela en entrant l'url suivante :
[external-ip:port/docs]

## 📌 Remarque sur les fichiers .env à créer
Les deux docker file des bases de données utilisent un .env file que vous allez configurer afin d'accéder à votre bdd. Et dans chaque service vous allez créer un .env file ou se trouve l'url de la base de donnée correspondante.

