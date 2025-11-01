-- Schéma MySQL pour l'application de gestion de bibliothèque

DROP DATABASE IF EXISTS gestion_bibliotheque;
CREATE DATABASE gestion_bibliotheque CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE gestion_bibliotheque;

-- Table utilisateurs (comptes login)
CREATE TABLE users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash CHAR(64) NOT NULL, -- SHA256
    email VARCHAR(255),
    role ENUM('admin','member') NOT NULL DEFAULT 'member',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table membres (profils)
CREATE TABLE members (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NULL,
    nom VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telephone VARCHAR(50),
    adresse TEXT,
    date_inscription DATE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Auteurs
CREATE TABLE authors (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    nationalite VARCHAR(100),
    biographie TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Emplacements
CREATE TABLE locations (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(100) NOT NULL UNIQUE,
    section VARCHAR(100),
    etage INT,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Livres
CREATE TABLE books (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(500) NOT NULL,
    author_id INT UNSIGNED,
    isbn VARCHAR(50) UNIQUE,
    annee INT,
    categorie VARCHAR(100),
    quantite INT NOT NULL DEFAULT 1,
    location_id INT UNSIGNED NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE SET NULL,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Réservations
CREATE TABLE reservations (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    member_id INT UNSIGNED NOT NULL,
    book_id INT UNSIGNED NOT NULL,
    date_debut DATE NOT NULL,
    duree_jours INT NOT NULL,
    statut ENUM('En attente','Approuvé','Refusé','Annulé') NOT NULL DEFAULT 'En attente',
    date_reservation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Messages / messagerie (texte, image, audio)
CREATE TABLE messages (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sender_user_id INT UNSIGNED NOT NULL,
    recipient_user_id INT UNSIGNED NULL, -- NULL = public/admin
    texte TEXT,
    image LONGBLOB,   -- stocke image en binaire (optionnel)
    audio LONGBLOB,   -- stocke audio en binaire (optionnel)
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX (sender_user_id),
    INDEX (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Exemple: créer un admin (mot de passe : admin123) stocké en SHA256
INSERT INTO users (username, password_hash, email, role)
VALUES ('admin', SHA2('admin123',256), 'admin@example.com', 'admin');

-- Optionnel: index utiles
CREATE INDEX idx_books_titre ON books(titre);
CREATE INDEX idx_members_nom ON members(nom);