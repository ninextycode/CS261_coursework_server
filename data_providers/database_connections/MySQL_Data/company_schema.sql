CREATE TABLE IF NOT EXISTS Company (
  Company_ID int NOT NULL,
  Code varchar(10) NOT NULL,
  Name varchar(255) NOT NULL,
  PRIMARY KEY (Company_ID),
);



CREATE TABLE IF NOT EXISTS Historical_Price (
  Company_ID int NOT NULL,
  Record_Time DATETIME NOT NULL,
  Price double NOT NULL,
  PRIMARY KEY (Company_ID, Record_Time),
  FOREIGN KEY (Company_ID) REFERENCES Company(Company_ID) ON DELETE CASCADE
);
