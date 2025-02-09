from fastapi import FastAPI, HTTPException
from prisma import Prisma
from confluent_kafka import Producer
import json

app = FastAPI()
db_fournisseurs = Prisma()
KAFKA_BROKER = "kafka-service:9092"
TOPIC_UPDATE_FOURNISSEUR = "update_fournisseur"
TOPIC_DELETE_FOURNISSEUR = "delete_fournisseur"

producer = Producer({"bootstrap.servers": KAFKA_BROKER})

@app.on_event("startup")
async def startup():
    await db_fournisseurs.connect()

@app.on_event("shutdown")
async def shutdown():
    await db_fournisseurs.disconnect()

def send_kafka_message(topic, message):
    producer.produce(topic, value=json.dumps(message))
    producer.flush()
#Endpoint pour récupérer tous les fournisseurs
@app.get("/fournisseurs")
async def get_fournisseurs():
    return await db_fournisseurs.fournisseurs.find_many()

#Endpoint pour récupérer un fournisseur par ID
@app.get("/fournisseurs/{fournisseur_id}")
async def get_fournisseur(fournisseur_id: int):
    fournisseur = await db_fournisseurs.fournisseurs.find_unique(where={"id": fournisseur_id})
    if not fournisseur:
        raise HTTPException(status_code=404, detail="Fournisseur non trouvé")
    return fournisseur

#Endpoint pour créer un fournisseur
@app.post("/fournisseurs")
async def create_fournisseur(nom: str, contact: str, email: str, adresse: str = None):
    return await db_fournisseurs.fournisseurs.create(
        data={"nom": nom, "contact": contact, "email": email, "adresse": adresse}
    )

#Endpoint pour mettre à jour un fournisseur
@app.put("/fournisseurs/{fournisseur_id}")
async def update_fournisseur(fournisseur_id: int, nom: str = None, contact: str = None, email: str = None, adresse: str = None):
    fournisseur = await db_fournisseurs.fournisseurs.update(
        where={"id": fournisseur_id},
        data={k: v for k, v in {"nom": nom, "contact": contact, "email": email, "adresse": adresse}.items() if v is not None}
    )
    if not fournisseur:
        raise HTTPException(status_code=404, detail="Fournisseur non trouvé")

    # Envoyer un message Kafka
    send_kafka_message(TOPIC_UPDATE_FOURNISSEUR, {"id": fournisseur.id})

    return fournisseur

#Supprimer un fournisseur et publier l'événement Kafka
@app.delete("/fournisseurs/{fournisseur_id}")
async def delete_fournisseur(fournisseur_id: int):
    fournisseur = await db_fournisseurs.fournisseurs.find_unique(where={"id": fournisseur_id})
    if not fournisseur:
        raise HTTPException(status_code=404, detail="Fournisseur non trouvé")

    await db_fournisseurs.fournisseurs.delete(where={"id": fournisseur_id})

    # Envoyer un message Kafka pour supprimer tous les produits liés
    send_kafka_message(TOPIC_DELETE_FOURNISSEUR, {"id": fournisseur_id})

    return {"message": "Fournisseur supprimé avec succès"}
