-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `cliniquepasteur`
--

-- --------------------------------------------------------

--
-- Structure de la table `etatinclusion`
--

DROP TABLE IF EXISTS `etatinclusion`;
CREATE TABLE IF NOT EXISTS `etatinclusion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `libelleEtat` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `etatinclusion`
--

INSERT INTO `etatinclusion` (`id`, `libelleEtat`) VALUES
(1, 'Inclus'),
(2, 'En cours'),
(3, 'Terminé'),
(4, 'Exclu');

-- --------------------------------------------------------

--
-- Structure de la table `etudes`
--

DROP TABLE IF EXISTS `etudes`;
CREATE TABLE IF NOT EXISTS `etudes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomEtu` varchar(100) NOT NULL,
  `descEtude` text,
  `idProtocole` int DEFAULT NULL,
  `idQuestion` int DEFAULT NULL, 
  `idOrganisme` int DEFAULT NULL,
  `dateDebEtu` date DEFAULT NULL,
  `dateFinEtu` date DEFAULT NULL,
  `idChirResp` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idProtocole` (`idProtocole`),
  KEY `idQuestion` (`idQuestion`),
  KEY `idOrganisme` (`idOrganisme`),
  KEY `idChirResp` (`idChirResp`)
) ENGINE=InnoDB  AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `etudes`
--

INSERT INTO `etudes` (`id`, `nomEtu`, `descEtude`, `idProtocole`, `idQuestion`, `idOrganisme`, `dateDebEtu`, `dateFinEtu`, `idChirResp`) VALUES
(1, 'Étude Cancer Poumon 2020', 'Suivi de patients atteints de cancer du poumon', 2, NULL, 1, '2020-01-01', '2024-12-31', 1),
(2, 'Étude Cirrhose Lyon', 'Ancien essai (non utilisé car hors cancer, conservé pour cohérence historique)', 1, NULL, 2, '2019-05-15', '2023-12-31', 2),
(3, 'Essai Chirurgie Cancer Rectum', 'Évaluation des résultats post-opératoires en chirurgie rectum', 2, NULL, 1, '2022-01-01', '2026-12-31', 4),
(4, 'Protocole RecaRe', 'Essai multicentrique sur la prise en charge du cancer rectum : chirurgie + radiochimiothérapie', 2, NULL, 2, '2023-01-01', '2027-12-31', 4),
(5, 'Étude Cancer Sein', 'Essai clinique sur traitements innovants cancer du sein', 2, NULL, 3, '2021-01-01', '2025-12-31', 5);

-- --------------------------------------------------------

--
-- Structure de la table `inclusions`
--

DROP TABLE IF EXISTS `inclusions`;
CREATE TABLE IF NOT EXISTS `inclusions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idPatient` int DEFAULT NULL,
  `dateInclusion` date DEFAULT NULL,
  `idEtude` int DEFAULT NULL,
  `idEtat` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_patient_etude` (`idPatient`,`idEtude`),
  KEY `idEtude` (`idEtude`),
  KEY `idEtat` (`idEtat`)
) ENGINE=InnoDB  AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `inclusions`
--

INSERT INTO `inclusions` (`id`, `idPatient`, `dateInclusion`, `idEtude`, `idEtat`) VALUES
(1, 1, '2020-03-01', 1, 1),
(2, 4, '2022-08-01', 3, 1),
(3, 4, '2023-02-01', 4, 1),
(4, 5, '2023-04-01', 4, 1),
(5, 6, '2023-06-15', 4, 2),
(6, 7, '2021-03-20', 5, 1);

-- --------------------------------------------------------

--
-- Structure de la table `maladies`
--

DROP TABLE IF EXISTS `maladies`;
CREATE TABLE IF NOT EXISTS `maladies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomMaladie` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `maladies`
--

INSERT INTO `maladies` (`id`, `nomMaladie`) VALUES
(1, 'Cancer du poumon'),
(2, 'Cancer du foie'),
(3, 'Cancer du rectum'),
(4, 'Cancer du rein'),
(5, 'Cancer du sein');

-- --------------------------------------------------------

--
-- Structure de la table `personnels`
--

DROP TABLE IF EXISTS `personnels`;
CREATE TABLE IF NOT EXISTS `personnels` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomPersonnels` varchar(100) DEFAULT NULL,
  `prenomPersonnels` varchar(100) DEFAULT NULL,
  `idSpecialite` int DEFAULT NULL,
  `idService` int DEFAULT NULL,
  `idRole` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idSpecialite` (`idSpecialite`),
  KEY `idService` (`idService`),
  KEY `idRole` (`idRole`)
) ENGINE=InnoDB  AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `personnels`
--

INSERT INTO `personnels` (`id`, `nomPersonnels`, `prenomPersonnels`, `idSpecialite`, `idService`, `idRole`) VALUES
(1, 'Durand', 'Paul', 1, 1, 1),
(2, 'Bernard', 'Sophie', 2, 2, 2),
(3, 'Garcia', 'Elena', 3, 3, 2),
(4, 'Lefevre', 'Antoine', 4, 4, 4),
(5, 'Marchand', 'Isabelle', 5, 5, 5);

-- --------------------------------------------------------

--
-- Structure de la table `organes`
--

DROP TABLE IF EXISTS `organes`;
CREATE TABLE IF NOT EXISTS `organes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomOrgane` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `organes`
--

INSERT INTO `organes` (`id`, `nomOrgane`) VALUES
(1, 'Poumon'),
(2, 'Foie'),
(3, 'Rectum'),
(4, 'Rein'),
(5, 'Sein');

-- --------------------------------------------------------

--
-- Structure de la table `organismes`
--

DROP TABLE IF EXISTS `organismes`;
CREATE TABLE IF NOT EXISTS `organismes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomOrg` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `organismes`
--

INSERT INTO `organismes` (`id`, `nomOrg`) VALUES
(1, 'Institut Pasteur'),
(2, 'CHU Lyon'),
(3, 'INSERM');

-- --------------------------------------------------------

--
-- Structure de la table `patients`
--

DROP TABLE IF EXISTS `patients`;
CREATE TABLE IF NOT EXISTS `patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomPat` varchar(100) DEFAULT NULL,
  `prenomPat` varchar(100) DEFAULT NULL,
  `dateNaisPat` date DEFAULT NULL,
  `sexe` char(1) DEFAULT NULL,
  `numDossierClinique` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numDossierClinique` (`numDossierClinique`)
) ENGINE=InnoDB  AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `patients`
--

INSERT INTO `patients` (`id`, `nomPat`, `prenomPat`, `dateNaisPat`, `sexe`, `numDossierClinique`) VALUES
(2, 'Dupont', 'Jean', '1970-05-12', 'M', 'DCL-0001'),
(3, 'Martin', 'Claire', '1982-08-23', 'F', 'DCL-0002'),
(4, 'Lopez', 'Maria', '1965-11-03', 'F', 'DCL-0003'),
(5, 'Rousseau', 'Camille', '1975-09-14', 'F', 'DCL-0004'),
(6, 'Petit', 'Nicolas', '1980-02-25', 'M', 'DCL-0005'),
(7, 'Fabre', 'Elise', '1968-07-09', 'F', 'DCL-0006'),
(8, 'Durand', 'Sophie', '1977-04-19', 'F', 'DCL-0007');

-- --------------------------------------------------------

--
-- Structure de la table `patientsmaladies`
--

DROP TABLE IF EXISTS `patientsmaladies`;
CREATE TABLE IF NOT EXISTS `patientsmaladies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idPatient` int DEFAULT NULL,
  `idMaladie` int DEFAULT NULL,
  `dateDiagnostic` date DEFAULT NULL,
  `idStade` int DEFAULT NULL,
  `idOrgane` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_patient_maladie` (`idPatient`,`idMaladie`, `dateDiagnostic`),
  KEY `idPatient` (`idPatient`),
  KEY `idMaladie` (`idMaladie`),
  KEY `idStade` (`idStade`),
  KEY `idOrgane` (`idOrgane`)
) ENGINE=InnoDB  AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `patientsmaladies`
--

INSERT INTO `patientsmaladies` (`id`, `idPatient`, `idMaladie`, `dateDiagnostic`, `idStade`, `idOrgane`) VALUES
(1, 1, 1, '2020-02-15', 2, 1),
(2, 2, 2, '2018-06-10', 3, 2),
(3, 3, 4, '2019-12-20', 4, 4),
(4, 4, 3, '2022-07-10', 2, 3),
(5, 5, 3, '2023-03-12', 3, 3),
(6, 6, 3, '2023-05-22', 2, 3),
(7, 7, 5, '2021-09-01', 1, 5);

-- --------------------------------------------------------

--
-- Structure de la table `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `libelleRole` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `roles`
--

INSERT INTO `roles` (`id`, `libelleRole`) VALUES
(1, 'Chef de service'),
(2, 'Médecin référent'),
(3, 'Attaché de recherche clinique'),
(4, 'Chirurgien digestif'),
(5, 'Oncologue mammaire');

-- --------------------------------------------------------

--
-- Structure de la table `services`
--

DROP TABLE IF EXISTS `services`;
CREATE TABLE IF NOT EXISTS `services` (
  `id` int NOT NULL AUTO_INCREMENT,
  `libelleServ` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `services`
--

INSERT INTO `services` (`id`, `libelleServ`) VALUES
(1, 'Service Oncologie'),
(2, 'Service Hépato'),
(3, 'Service Néphrologie'),
(4, 'Service Chirurgie Digestive'),
(5, 'Service Sénologie');

-- --------------------------------------------------------

--
-- Structure de la table `specialites`
--

DROP TABLE IF EXISTS `specialites`;
CREATE TABLE IF NOT EXISTS `specialites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `libelleSpec` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `specialites`
--

INSERT INTO `specialites` (`id`, `libelleSpec`) VALUES
(1, 'Oncologie'),
(2, 'Hépato-gastroentérologie'),
(3, 'Néphrologie'),
(4, 'Chirurgie digestive'),
(5, 'Oncologie mammaire');

-- --------------------------------------------------------

--
-- Structure de la table `stades`
--

DROP TABLE IF EXISTS `stades`;
CREATE TABLE IF NOT EXISTS `stades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nomStade` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `stades`
--

INSERT INTO `stades` (`id`, `nomStade`) VALUES
(1, 'I'),
(2, 'II'),
(3, 'III'),
(4, 'IV');

-- --------------------------------------------------------

--
-- Structure de la table `protocole`
--

DROP TABLE IF EXISTS `protocole`;
CREATE TABLE IF NOT EXISTS `protocole` (
  `id` int NOT NULL AUTO_INCREMENT,
  `libelleProtocole` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `protocole`
--

INSERT INTO `protocole` (`id`, `libelleProtocole`) VALUES
(1, 'Étude observationnelle'),
(2, 'Essai clinique randomisé'),
(3, 'Étude prospective');


-- -------------------------------------------------------

--
-- Structure de la table `questionnaire`
--

DROP TABLE IF EXISTS `questionnaire`;
CREATE TABLE IF NOT EXISTS `questionnaire` (
  `id` int NOT NULL AUTO_INCREMENT,
  `libelleQuestion` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `questionnaire`
--

INSERT INTO `questionnaire` (`id`, `libelleQuestion`) VALUES
(1, 'QLQ-C30'),
(2, 'QLQ-CR29'),
(3, 'TAILORx') ;



COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
