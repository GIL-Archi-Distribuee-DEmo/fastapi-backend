from confluent_kafka import Consumer
from prisma import Prisma
import json

KAFKA_BROKER = "kafka-service:9092"
TOPIC_UPDATE_FOURNISSEUR = "update_fournisseur"
TOPIC_DELETE_FOURNISSEUR = "delete_fournisseur" 

consumer = Consumer({
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "produits_service",
    "auto.offset.reset": "earliest"
})

consumer.subscribe([TOPIC_UPDATE_FOURNISSEUR, TOPIC_DELETE_FOURNISSEUR])

db = Prisma()

async def delete_produits(fournisseur_id):
    await db.connect()
    await db.produits.delete_many(where={"fournisseur_id": fournisseur_id})
    await db.disconnect()

async def update_produits(fournisseur_id):
    # Ici, on pourrait mettre à jour les produits si nécessaire (ex: en changeant des métadonnées)
    print(f"Les produits du fournisseur {fournisseur_id} pourraient être mis à jour ici.")

print("En attente des événements Kafka...")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Erreur Kafka : {msg.error()}")
        continue

    event_data = json.loads(msg.value().decode("utf-8"))
    print(f"Message reçu de Kafka : {event_data}")

    if msg.topic() == TOPIC_DELETE_FOURNISSEUR:
        print(f"Suppression des produits liés au fournisseur {event_data['id']}")
        import asyncio
        asyncio.run(delete_produits(event_data["id"]))

    elif msg.topic() == TOPIC_UPDATE_FOURNISSEUR:
        print(f"Mise à jour des produits liés au fournisseur {event_data['id']}")
        import asyncio
        asyncio.run(update_produits(event_data["id"]))
