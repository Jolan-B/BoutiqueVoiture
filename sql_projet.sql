DROP TABLE IF EXISTS Voiture;
DROP TABLE IF EXISTS Categorie;

CREATE TABLE Categorie(
   idCategorie INT AUTO_INCREMENT,
   nomCategorie VARCHAR(50),
   catalogueCategorie INT,
   photoCategorie VARCHAR(50),
   PRIMARY KEY(idCategorie)
);

CREATE TABLE Voiture(
   idVoiture INT AUTO_INCREMENT,
   nomVoiture VARCHAR(50),
   dateLancementVoiture DATE,
   prixVoiture DECIMAL(15,2),
   puissanceVoiture INT,
   photoVoiture VARCHAR(50),
   id_categorie INT NOT NULL,
   PRIMARY KEY(idVoiture),
   FOREIGN KEY(id_categorie) REFERENCES Categorie(idCategorie)
);

INSERT INTO Categorie (idCategorie , nomCategorie, catalogueCategorie, photoCategorie) VALUES
(NULL, 'Berline',1,'logo_berline.png'),
(NULL, 'Break',1,'logo_break.png'),
(NULL, 'SUV',1,'logo_suv.png'),
(NULL, 'Monospace',2,'logo_monospace.png'),
(NULL, 'Utilitaire',3,'logo_utilitaire.png'),
(NULL, 'Citadine',1,'logo_citadine.png'),
(NULL, 'Autre',3,'logo_autre.png');

INSERT INTO Voiture (idVoiture,nomVoiture, dateLancementVoiture, prixVoiture, id_categorie, puissanceVoiture, photoVoiture) VALUES
(NULL,'Renault Clio 3','2010-1-1',5000,1,4,'clio3.jpg'),
(NULL, 'BMW Serie 6 Gran Coupe', '2012-01-09', 118400,1,34,'bmws6.jpg'),
(NULL, 'Mercedes Classe S', '2014-09-15', 181000,1, 50,'mercedesclasseS.jpg'),
(NULL,'Audi RS6', '2013-11-07', 120600,2,64,'audiRS6.jpg'),
(NULL,'Porsche Panamera', '2013-04-25', 123965, 2, 35,'porschePanamera.jpg'),
(NULL,'Range Rover Evoque', '2014-03-10', 50700, 3, 19,'rrEvoque.jpg'),
(NULL,'Citroen C4 Picasso', '2013-06-04', 31150, 4, 8,'c4Picasso.jpg'),
(NULL,'Ford S-Max', '2012-08-28', 38450, 4, 8,'sMax.jpg'),
(NULL,'Fiat Ducato', '2009-07-02', 24575, 5, 9,'fiatDucato.jpg'),
(NULL,'Renault Kangoo', '2008-05-31', 19750, 5, 7,'kangoo.jpg'),
(NULL,'Opel Adam', '2009-12-15', 18900, 6, 8,'opelAdam.jpg'),
(NULL,'Citroen DS3', '2010-02-17', 19490, 6, 9,'DS3.jpg'),
(NULL,'Dodge RAM 1500 V8 HEMI', '2015-03-26', 55800, 7, 30,'DodgeRAM.jpg');