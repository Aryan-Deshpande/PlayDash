# **`PLAYDASH`**
A web application for arranging outdoor sporting events that allows users to reserve turf. enables suppliers to receive data from the source of truth through external APIs.

## **FEATURES**
- Facilitates reservation system for outdoor sporting events
- External APIs for vendors to receive data from the source of truth
- View available turf for a given event. .

## **TECH STACK**
- Python / Flask
- PostgresSQL

<br>

## **INSTALLATION** 
```sh
git clone https://github.com/Aryan-Deshpande/PlayDash.git
```
Then move into the directory and run the following commands:
```sh
pip install -r requirements.txt
```

## **TESTING**
```sh
flask run --port=80 --host=localhost
```

## **HOSTING**

## **`Azure Kubernetes Service`**
![](https://media.discordapp.net/attachments/835750351621718030/1036720285744902235/k8saks1-1.jpg?width=1191&height=623)
- The K8s Cluster is segmented into services, deployment/pods and and nginx ingress controller.
- The FLASK backend application is containerized and accordingly service and deployment is created.

<br>

## **`Heroku Postgres`**
![](https://media.discordapp.net/attachments/835750351621718030/1036720212076142763/584815fdcef1014c0b5e497a.png)

- The database is hosted on Heroku Postgres.

<br>

# **`WORKFLOW`**

## **WORKFLOW OVERVIEW**
![](https://cdn.discordapp.com/attachments/835750351621718030/1036722209315635200/example.png)

