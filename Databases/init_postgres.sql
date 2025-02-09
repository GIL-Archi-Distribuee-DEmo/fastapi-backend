-- Créer la table fournisseurs
CREATE TABLE IF NOT EXISTS fournisseurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    adresse TEXT,
    contact VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insérer des fournisseurs
INSERT INTO fournisseurs (nom, adresse, contact, email)
VALUES
    ('Fournisseur A', '123 Rue Principale, Paris', '0123456789', 'contact@fournisseurA.com'),
    ('Fournisseur B', '456 Avenue Centrale, Lyon', '0987654321', 'contact@fournisseurB.com'),
    ('Fournisseur C', '789 Boulevard Secondaire, Marseille', '0123456789', 'contact@fournisseurC.com'),
    ('Fournisseur D', '1011 Rue Tertiaire, Lille', '0987654321', 'contact@fournisseurD.com')
ON CONFLICT (email) DO NOTHING; -- Évite les doublons si le script est exécuté plusieurs fois
