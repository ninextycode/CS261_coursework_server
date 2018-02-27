CREATE TABLE IF NOT EXISTS Sector (
  Sector_ID int NOT NULL,
  Sector_Name varchar(255),
  PRIMARY KEY (Sector_ID)
);

CREATE TABLE IF NOT EXISTS Company (
  Company_ID int NOT NULL,
  Code varchar(10) NOT NULL,
  Name varchar(255) NOT NULL,
  Currency varchar(3),
  Sector_ID int NOT NULL,
  PRIMARY KEY (Company_ID),
  FOREIGN KEY (Sector_ID) REFERENCES Sector(Sector_ID)
);



CREATE TABLE IF NOT EXISTS Historical_Price (
  Company_ID int NOT NULL,
  Record_Time DATETIME NOT NULL,
  Price double NOT NULL,
  PRIMARY KEY (Company_ID, Record_Time),
  FOREIGN KEY (Company_ID) REFERENCES Company(Company_ID) ON DELETE CASCADE
);

INSERT INTO Sector VALUES (0,"test_sect");
INSERT INTO Company VALUES (0, "tst","test_company","GBP",0);
INSERT INTO Historical_Price VALUES (0,"2018-01-19 03:14:07",0);
