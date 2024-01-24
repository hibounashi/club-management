-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 24 jan. 2024 à 14:44
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `club_management`
--

-- --------------------------------------------------------

--
-- Structure de la table `club_event`
--

CREATE TABLE `club_event` (
  `id_event` int(11) NOT NULL,
  `eventName` varchar(50) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `club_event`
--

INSERT INTO `club_event` (`id_event`, `eventName`, `description`) VALUES
(1, 'Event A', 'This is the description for Event A.'),
(2, 'Event B', 'This is the description for Event B.'),
(3, 'Event C', 'This is the description for Event C.'),
(4, 'Event D', 'This is the description for Event D.'),
(5, 'Event E', 'This is the description for Event E.');

-- --------------------------------------------------------

--
-- Structure de la table `departement`
--

CREATE TABLE `departement` (
  `departementID` int(11) NOT NULL,
  `departementName` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `departement`
--

INSERT INTO `departement` (`departementID`, `departementName`) VALUES
(1, 'IT Department'),
(2, 'Marketing Department'),
(3, 'Finance Department'),
(4, 'Human Resources Department'),
(5, 'Research and Development Department');

-- --------------------------------------------------------

--
-- Structure de la table `manager`
--

CREATE TABLE `manager` (
  `managerID` int(11) NOT NULL,
  `managerName` varchar(50) DEFAULT NULL,
  `number_events` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `manager`
--

INSERT INTO `manager` (`managerID`, `managerName`, `number_events`) VALUES
(1, 'ymym', 5),
(2, 'Manager 2', 8),
(3, 'Manager 3', 3),
(4, 'Manager 4', 6),
(5, 'Manager 5', 4);

-- --------------------------------------------------------

--
-- Structure de la table `managermember`
--

CREATE TABLE `managermember` (
  `managerID` int(11) NOT NULL,
  `memberID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `member`
--

CREATE TABLE `member` (
  `memberID` int(11) NOT NULL,
  `fname` varchar(60) DEFAULT NULL,
  `lname` varchar(60) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` enum('Male','Female') DEFAULT NULL,
  `discord` varchar(60) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `school_year` varchar(60) DEFAULT NULL,
  `university` varchar(80) DEFAULT NULL,
  `skills` varchar(255) DEFAULT NULL,
  `departement` enum('logistics','development','relax','communication','design') DEFAULT NULL,
  `role` enum('Member','Manager') DEFAULT NULL,
  `managerID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `member`
--

INSERT INTO `member` (`memberID`, `fname`, `lname`, `dob`, `gender`, `discord`, `email`, `password`, `school_year`, `university`, `skills`, `departement`, `role`, `managerID`) VALUES
(1, 'hiab', 'nehili', '2003-06-10', '', '#hiba', '1hiba2nehili@gmail.com', 'hiba', '1CS', 'ESTIN', 'hdejkzediojfk', 'logistics', 'Manager', 1),
(2, 'anfal', 'yara', '0000-00-00', '', 'anfalllll', 'doku@gmail.com', 'hiba', 'ESTIN', 'ESTIN', 'walou', 'relax', NULL, NULL),
(3, 'kaoutar', 'nehili', '0000-00-00', '', 'ihdk', 'JIJK0@IKL.TFYUI', 'hiba', '1CS', 'estin', 'notihng', 'communication', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `participate`
--

CREATE TABLE `participate` (
  `participate_id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `id_event` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `participate`
--

INSERT INTO `participate` (`participate_id`, `member_id`, `id_event`) VALUES
(1, 1, 1);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `club_event`
--
ALTER TABLE `club_event`
  ADD PRIMARY KEY (`id_event`);

--
-- Index pour la table `departement`
--
ALTER TABLE `departement`
  ADD PRIMARY KEY (`departementID`);

--
-- Index pour la table `manager`
--
ALTER TABLE `manager`
  ADD PRIMARY KEY (`managerID`);

--
-- Index pour la table `managermember`
--
ALTER TABLE `managermember`
  ADD PRIMARY KEY (`managerID`,`memberID`),
  ADD KEY `memberID` (`memberID`);

--
-- Index pour la table `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`memberID`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fk_manager` (`managerID`);

--
-- Index pour la table `participate`
--
ALTER TABLE `participate`
  ADD PRIMARY KEY (`participate_id`),
  ADD KEY `member_id` (`member_id`),
  ADD KEY `id_event` (`id_event`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `club_event`
--
ALTER TABLE `club_event`
  MODIFY `id_event` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `departement`
--
ALTER TABLE `departement`
  MODIFY `departementID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `manager`
--
ALTER TABLE `manager`
  MODIFY `managerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `member`
--
ALTER TABLE `member`
  MODIFY `memberID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `participate`
--
ALTER TABLE `participate`
  MODIFY `participate_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `managermember`
--
ALTER TABLE `managermember`
  ADD CONSTRAINT `managermember_ibfk_1` FOREIGN KEY (`managerID`) REFERENCES `manager` (`managerID`),
  ADD CONSTRAINT `managermember_ibfk_2` FOREIGN KEY (`memberID`) REFERENCES `member` (`memberID`);

--
-- Contraintes pour la table `member`
--
ALTER TABLE `member`
  ADD CONSTRAINT `fk_manager` FOREIGN KEY (`managerID`) REFERENCES `manager` (`managerID`);

--
-- Contraintes pour la table `participate`
--
ALTER TABLE `participate`
  ADD CONSTRAINT `participate_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`memberID`),
  ADD CONSTRAINT `participate_ibfk_2` FOREIGN KEY (`id_event`) REFERENCES `club_event` (`id_event`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
