CREATE TABLE IF NOT EXISTS Company (
  Code varchar(10) NOT NULL,
  Name varchar(255) NOT NULL,
  Currency varchar(3),
  Sector_ID int,
  PRIMARY KEY (Code)
);

CREATE TABLE IF NOT EXISTS Sector (
  Sector_ID int NOT NULL,
  Sector_Name varchar(255),
  PRIMARY KEY (Sector_ID)
);

CREATE TABLE IF NOT EXISTS Company_Sectors (
  Code varchar(10) NOT NULL,
  Sector_ID int NOT NULL,
  PRIMARY KEY (Code, Sector_ID),
  FOREIGN KEY (Code) REFERENCES Company(Code) ON DELETE CASCADE,
  FOREIGN KEY (Sector_ID) REFERENCES Sector(Sector_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Historical_Price (
  Code varchar(10) NOT NULL,
  Record_Time DATETIME NOT NULL,
  Price double NOT NULL,
  PRIMARY KEY (Code, Record_Time),
  FOREIGN KEY (Code) REFERENCES Company(Code) ON DELETE CASCADE
);

INSERT INTO Company VALUES ('test','test','','0');
INSERT INTO Sector VALUES ('0','test');
INSERT INTO Company_Sectors VALUES ('test','0');
INSERT INTO Historical_Price VALUES ('test','2018-01-19 03:14:07',0);
