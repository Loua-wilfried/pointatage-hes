
-- Script de création de la base de données pour le système de pointage
-- À exécuter dans phpMyAdmin ou via ligne de commande MySQL

CREATE DATABASE IF NOT EXISTS pointatage_hes 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE pointatage_hes;

-- Vérification
SELECT 'Base de données pointatage_hes créée avec succès!' as message;
