-- Horse Racing Database Schema (ICS321 Project #1)
-- Drop tables if they exist to ensure clean setup
DROP TABLE IF EXISTS RaceResults;
DROP TABLE IF EXISTS Race;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Owns;
DROP TABLE IF EXISTS Horse;
DROP TABLE IF EXISTS Owner;
DROP TABLE IF EXISTS Stable;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS old_info;

-- Create Stable table
CREATE TABLE Stable (
    stableId VARCHAR(15) NOT null,
    stableName VARCHAR(30),
    location VARCHAR(30),
    colors VARCHAR(20),
    PRIMARY KEY (stableId)
);

-- Create Horse table
CREATE TABLE Horse (
    horseId VARCHAR(15) NOT null,
    horseName VARCHAR(15) NOT null,
    age INT,
    gender CHAR,
    registration INTEGER NOT null,
    stableId VARCHAR(30) NOT null,
    FOREIGN KEY(stableId) REFERENCES Stable(stableId),
    PRIMARY KEY(horseId)
);

-- Create Owner table
CREATE TABLE Owner (
    ownerId VARCHAR(15) NOT null,
    lname VARCHAR(15),
    fname VARCHAR(15),
    PRIMARY KEY(ownerId)
);

-- Create Owns table (many-to-many relationship)
CREATE TABLE Owns (
    ownerId VARCHAR(15) NOT null,
    horseId VARCHAR(15) NOT null,
    PRIMARY KEY(ownerId, horseId),
    FOREIGN KEY(ownerId) REFERENCES Owner(ownerId),
    FOREIGN KEY(horseId) REFERENCES Horse(horseId)
);

-- Create Trainer table
CREATE TABLE Trainer (
    trainerId VARCHAR(15) NOT null,
    lname VARCHAR(30),
    fname VARCHAR(30),
    stableId VARCHAR(30),
    PRIMARY KEY(trainerId),
    FOREIGN KEY(stableId) REFERENCES Stable(stableId)
);

-- Create Track table
CREATE TABLE Track (
    trackName VARCHAR(30) NOT null,
    location VARCHAR(30),
    length INTEGER,
    PRIMARY KEY(trackName)
);

-- Create Race table
CREATE TABLE Race (
    raceId VARCHAR(15) NOT null,
    raceName VARCHAR(30),
    trackName VARCHAR(30),
    raceDate DATE,
    raceTime TIME,
    PRIMARY KEY(raceId),
    FOREIGN KEY (trackName) REFERENCES Track(trackName)
);

-- Create RaceResults table
CREATE TABLE RaceResults (
    raceId VARCHAR(15) NOT null,
    horseId VARCHAR(15) NOT null,
    results VARCHAR(15),
    prize FLOAT(10,2),
    PRIMARY KEY (raceId, horseId),
    FOREIGN KEY(raceId) REFERENCES Race(raceId),
    FOREIGN KEY(horseId) REFERENCES Horse(horseId)
);

-- Create old_info table for trigger
CREATE TABLE old_info (
    horseId VARCHAR(15),
    horseName VARCHAR(15),
    age INT,
    gender CHAR,
    registration INTEGER,
    stableId VARCHAR(30),
    deletedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);