CREATE TABLE IF NOT EXISTS Sectors (
  Sector_ID int NOT NULL AUTO_INCREMENT,
  Sector_Name varchar(255) UNIQUE,
  PRIMARY KEY (Sector_ID)
);

CREATE TABLE IF NOT EXISTS Companies (
  Company_ID int NOT NULL AUTO_INCREMENT,
  Company_code varchar(10) NOT NULL UNIQUE,
  Company_name varchar(255) NOT NULL UNIQUE,
  Sector_ID int NOT NULL,
  PRIMARY KEY (Company_ID),
  FOREIGN KEY (Sector_ID) REFERENCES Sectors(Sector_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Historical_Prices (
  Company_ID int NOT NULL,
  Record_Time DATETIME NOT NULL,
  Price decimal(8, 4) NOT NULL,
  PRIMARY KEY (Company_ID, Record_Time),
  FOREIGN KEY (Company_ID) REFERENCES Companies(Company_ID) ON DELETE CASCADE
);
