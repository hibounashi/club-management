CREATE DATABASE IF NOT EXISTS club_management;
USE DATABASE club_management;

CREATE TABLE Member (
    memberID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    fname VARCHAR(60),
    lname VARCHAR(60),
    dob DATE,
    gender ENUM('Male', 'Female'),
    discord VARCHAR(60),
    email VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    school_year VARCHAR(60),
    university VARCHAR(80),
    skills VARCHAR(255),
    departement ENUM('logistics', 'development', 'relax', 'communication', 'design'),
    role ENUM('Member', 'Manager'),
    managerID INT,
    FOREIGN KEY (managerID) REFERENCES Manager(managerID)
);

CREATE TABLE Manager (
    managerID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    managerName VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    phone VARCHAR(20),
    number_events INT
);

CREATE TABLE ManagerMember (
    managerID INT,
    memberID INT,
    PRIMARY KEY (managerID, memberID),
    FOREIGN KEY (managerID) REFERENCES Manager(managerID),
    FOREIGN KEY (memberID) REFERENCES Member(memberID)
);

CREATE TABLE event (
    id_event INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    eventName VARCHAR(50),
    description VARCHAR(255)
);

CREATE TABLE departement(
    departementID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    departementName VARCHAR(50)
);

CREATE TABLE participate (
    participate_id INT PRIMARY KEY,
    member_id INT,
    event_id INT,
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

INSERT INTO departement (departementName) VALUES ('logistics');
INSERT INTO departement (departementName) VALUES ('development');
INSERT INTO departement (departementName) VALUES ('relax');
INSERT INTO departement (departementName) VALUES ('communication');
INSERT INTO departement (departementName) VALUES ('design');

INSERT INTO Manager (managerID, managerName, number_events) VALUES
(1, 'ymym', 5),
(2, 'Manager 2', 8),
(3, 'Manager 3', 3),
(4, 'Manager 4', 6),
(5, 'Manager 5', 4);

INSERT INTO Member (memberID, fname, lname, dob, gender, discord, email, password, school_year, university, skills, departement, role, managerID) VALUES
(11, 'hiba', 'neh', '2024-01-31', '', '#mimi', 'h_nehili@estin.dz', 'hiba', '1CS', 'ESTIN', 'notihng', 12, NULL, NULL),
(12, 'manel', 'drz', '2024-01-08', '', '#manar', 'manel@gamil.com', 'hiba', '1CS', 'ESTIN', 'html css js', 12, NULL, NULL),
(13, 'houda', 'btn', '2024-01-16', '', '#housi', 'houda@admin.com', 'hiba', '1CS', 'ESTIN', 'html css js', 12, NULL, NULL),
(16, 'yasmine', 'maroua', '2024-01-18', '', '#yesmine', 'yesmine@gmail.com', 'hiba', '1CS', 'ESTIN', 'css js', 12, NULL, NULL);

INSERT INTO participate (participate_id, member_id, event_id) VALUES
(2, 11, 6),
(26, 11, 6),
(27, 11, 7),
(28, 11, 8),
(29, 12, 6),
(30, 13, 6),
(31, 13, 9),
(32, 13, 6),
(33, 13, 10),
(37, 16, 10);

SELECT departementID FROM Departement WHERE departementName = %s;
SELECT * FROM Member WHERE email = %s AND password = %s;
SELECT * FROM Member WHERE memberID = %s;
SELECT COUNT(*) AS user_count FROM Member;
SELECT COUNT(*) AS event_count FROM club_event;
SELECT COUNT(*) AS dep_count FROM departement;
SELECT COUNT(DISTINCT m.memberID) AS event_members_count FROM club_event c JOIN participate p ON p.id_event = c.id_event JOIN member m ON m.memberID = p.member_id;
SELECT id_event FROM club_event WHERE eventName = %s;
INSERT INTO club_event (eventName) VALUES (%s);
INSERT INTO participate (member_id, id_event) VALUES (%s, %s);
SELECT * FROM Member WHERE memberID = %s;
UPDATE Member SET email = %s, discord = %s, skills = %s, departement = (SELECT departementID FROM Departement WHERE departementName = %s) WHERE memberID = %s;
DELETE FROM Member WHERE memberID = %s;
SELECT id_event, eventName FROM club_event;
SELECT member.fname, member.lname FROM participate JOIN member ON participate.member_id = member.memberID WHERE participate.id_event = %s;
INSERT INTO Member (fname, lname, email, gender, discord, dob, password, school_year, university, skills, confirmpassword) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
SELECT * FROM Member WHERE email = %s AND password = %s;
SELECT COUNT(*) AS user_count FROM Member;
INSERT INTO Member (fname, lname, dob, gender, discord, email, password, school_year, university, skills, departement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT departementID FROM Departement WHERE departementName = %s));
SELECT COUNT(DISTINCT m.memberID) AS event_members_count FROM club_event c JOIN participate p ON p.id_event = c.id_event JOIN member m ON m.memberID = p.member_id;
