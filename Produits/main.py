from fastapi import FastAPI, HTTPException
from prisma import Prisma
app = FastAPI()
db = Prisma()


@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

#Endpoint pour récupérer tous les produits
@app.get("/produits")
async def get_produits():
    return await db.produits.find_many()

#Endpoint pour récupérer un produit par ID
@app.get("/produits/{produit_id}")
async def get_produit(produit_id: int):
    produit = await db.produits.find_unique(where={"id": produit_id})
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit

#Endpoint pour créer un produit
@app.post("/produits")
async def create_produit(nom: str, categorie: str, prix: float, stock: int = 0):
    return await db.produits.create(
        data={"nom": nom, "categorie": categorie, "prix": prix, "stock": stock}
    )

#Endpoint pour mettre à jour un produit
@app.put("/produits/{produit_id}")
async def update_produit(produit_id: int, nom: str = None, categorie: str = None, prix: float = None, stock: int = None):
    produit = await db.produits.update(
        where={"id": produit_id},
        data={k: v for k, v in {"nom": nom, "categorie": categorie, "prix": prix, "stock": stock}.items() if v is not None}
    )
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit

#Endpoint pour supprimer un produit
@app.delete("/produits/{produit_id}")
async def delete_produit(produit_id: int):
    produit = await db.produits.delete(where={"id": produit_id})
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return {"message": "Produit supprimé avec succès"}
