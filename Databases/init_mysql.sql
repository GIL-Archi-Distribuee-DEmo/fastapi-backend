-- Sélectionner la base de données à utiliser
USE produits_db;

-- Créer la table produits
CREATE TABLE IF NOT EXISTS produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    categorie VARCHAR(100),
    prix DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    fournisseur_id INT,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insérer des produits par défaut
INSERT INTO produits (nom, categorie, prix, stock, fournisseur_id)
VALUES
    ('Laptop HP', 'Informatique', 899.99, 10, 1),
    ('iPhone 13', 'Smartphones', 1099.99, 5, 2),
    ('TV Samsung 55"', 'Électronique', 649.99, 3, 3)
ON DUPLICATE KEY UPDATE nom=VALUES(nom);
