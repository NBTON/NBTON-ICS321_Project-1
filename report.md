# Horse Racing Database System - Project Report

## Table Schema Adjustments

### Changes Made from Original Schema

The original schema has been enhanced with several improvements to meet the project requirements:

#### 1. Stable Table
**Original:**
```sql
stableId varchar(15) not null, 
stableName varchar(30), 
location varchar(30), 
colors varchar(20), 
primary key (stableId)
```

**Adjusted:** No changes made to this table structure. The implementation maintains the original specification.

#### 2. Horse Table
**Original:**
```sql
horseId varchar(15) not null, 
horseName varchar(15) not null, 
age int,  
gender char, 
registration integer not null, 
stableId varchar(30) not null, 
foreign key(stableId) references Stable(stableId), 
primary key(horseId)
```

**Adjusted:** No changes made to this table structure. Foreign key constraint remains as specified.

#### 3. Owner Table
**Original:**
```sql
ownerId varchar(15) not null, 
lname varchar(15), 
fname varchar(15), 
primary key(ownerId)
```

**Adjusted:** No changes made to this table structure.

#### 4. Owns Table (Many-to-Many Relationship)
**Original:**
```sql
ownerId varchar(15) not null, 
horseId varchar(15) not null, 
primary key(ownerId, horseId), 
foreign key(ownerId) references Owner(ownerId), 
foreign key(horseId) references Horse(horseId)
```

**Adjusted:** No changes made to this table structure. The junction table is properly implemented.

#### 5. Trainer Table
**Original:**
```sql
trainerId varchar(15) not null, 
lname varchar(30), 
fname varchar(30),  
stableId varchar(30), 
primary key(trainerId), 
foreign key(stableId) references Stable(stableId)
```

**Adjusted:** No changes made to this table structure.

#### 6. Track Table
**Original:**
```sql
trackName varchar(30) not null, 
location varchar(30), 
length integer, 
primary key(trackName)
```

**Adjusted:** No changes made to this table structure.

#### 7. Race Table
**Original:**
```sql
raceId varchar(15) not null, 
raceName varchar(30), 
trackName varchar(30), 
raceDate date, 
raceTime time, 
primary key(raceId), 
foreign key (trackName) references Track(trackName)
```

**Adjusted:** No changes made to this table structure.

#### 8. RaceResults Table
**Original:**
```sql
raceId varchar(15) not null, 
horseId varchar(15) not null, 
results varchar(15), 
prize float(10,2), 
primary key (raceId, horseId), 
foreign key(raceId) references Race(raceId), 
foreign key(horseId) references Horse(horseId)
```

**Adjusted:** No changes made to this table structure.

#### 9. NEW: old_info Table (Added for Trigger Requirement)

**New Table Created:**
```sql
CREATE TABLE old_info (
    horseId VARCHAR(15),
    horseName VARCHAR(15),
    age INT,
    gender CHAR,
    registration INTEGER,
    stableId VARCHAR(30),
    deletedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** This table was added to satisfy the requirement for implementing a trigger that copies horse information whenever a horse is deleted from the database.

## Functions Implementation

### Admin Functions

#### Function 1: Add a new race with the results of the race
**Implementation Location:** `admin_gui.py` - `save_race()` method (lines 366-415)

**Implementation Details:**
- **Query Used:**
```sql
INSERT INTO Race (raceName, trackName, raceDate, raceTime) 
VALUES (%s, %s, %s, %s)

INSERT INTO RaceResults (raceId, horseId, results, prize) 
VALUES (%s, %s, %s, %s)
```

**How it works:**
1. User enters race details (name, track, date, time)
2. Adds race results for multiple horses
3. System inserts race first, then retrieves the auto-generated race ID
4. Inserts each race result with the race ID
5. All operations use transaction handling for data integrity

#### Function 2: Delete an owner and all the related information from the database
**Implementation Location:** `admin_gui.py` - `delete_owner()` method (lines 417-440)
**Stored Procedure:** `procedures_triggers.sql` - `DeleteOwner` procedure (lines 4-24)

**Implementation Details:**
- **Stored Procedure Query:**
```sql
CREATE PROCEDURE DeleteOwner(IN owner_to_delete VARCHAR(15))
BEGIN
    START TRANSACTION;
    DELETE FROM Owns WHERE ownerId = owner_to_delete;
    DELETE FROM Owner WHERE ownerId = owner_to_delete;
    COMMIT;
END;
```

**How it works:**
1. User selects owner from listbox
2. Calls stored procedure `DeleteOwner`
3. Procedure deletes all relationships from `Owns` table first
4. Then deletes the owner from `Owner` table
5. Uses transaction to ensure atomicity
6. Includes error handling with rollback capability

#### Function 3: Given the horse ID, move the horse from one stable to another
**Implementation Location:** `admin_gui.py` - `move_horse()` method (lines 470-493)

**Implementation Details:**
- **Query Used:**
```sql
UPDATE Horse SET stableId = %s WHERE horseId = %s
```

**How it works:**
1. User enters horse ID
2. System retrieves current horse information and stable
3. User selects new stable from dropdown
4. Updates the horse's `stableId` in the database
5. Displays confirmation of successful move

#### Function 4: Approve a new trainer to join a stable
**Implementation Location:** `admin_gui.py` - `approve_trainer()` method (lines 495-525)

**Implementation Details:**
- **Query Used:**
```sql
INSERT INTO Trainer (trainerId, fname, lname, stableId) 
VALUES (%s, %s, %s, %s)
```

**How it works:**
1. User enters trainer first and last name
2. Selects stable from dropdown
3. System generates unique trainer ID using hash function
4. Inserts new trainer record into database
5. Displays success message with generated trainer ID

### Guest Functions

#### Function 1: Browse the names and ages of horses and the names of their trainer that are owned by people given their last name as input
**Implementation Location:** `guest_gui.py` - `search_horses_by_owner()` method (lines 241-279)

**Implementation Details:**
- **Query Used:**
```sql
SELECT DISTINCT h.horseName, h.age, h.gender, 
       CONCAT(t.fname, ' ', t.lname) as trainer_name
FROM Horse h
JOIN Owns o ON h.horseId = o.horseId
JOIN Owner owner ON o.ownerId = owner.ownerId
LEFT JOIN Trainer t ON h.stableId = t.stableId
WHERE owner.lname LIKE %s
ORDER BY h.horseName
```

**How it works:**
1. User enters owner last name
2. System searches using LIKE pattern matching
3. Joins Horse, Owns, Owner, and Trainer tables
4. Displays results in formatted table with columns: Horse Name, Age, Gender, Trainer
5. Handles case where horse has no assigned trainer

#### Function 2: Browse the first and last names of trainers who have trained winners (i.e., horses who have won first place)
**Implementation Location:** `guest_gui.py` - `search_winning_trainers()` method (lines 281-319)

**Implementation Details:**
- **Query Used:**
```sql
SELECT DISTINCT CONCAT(t.fname, ' ', t.lname) as trainer_name,
       h.horseName as horse_name,
       r.raceName,
       tr.trackName,
       r.raceDate,
       rr.prize
FROM Trainer t
JOIN Horse h ON h.stableId = t.stableId
JOIN RaceResults rr ON h.horseId = rr.horseId AND rr.results = 'first'
JOIN Race r ON rr.raceId = r.raceId
JOIN Track tr ON r.trackName = tr.trackName
ORDER BY r.raceDate DESC
```

**How it works:**
1. Searches for trainers whose horses have `results = 'first'` in race results
2. Joins Trainer, Horse, RaceResults, Race, and Track tables
3. Displays comprehensive information including trainer details, winning horse, race details, track, date, and prize money
4. Results sorted by race date (newest first)

#### Function 3: Browse the first and last name of the trainer and the total amount of winnings in terms of prize money for each trainer
**Implementation Location:** `guest_gui.py` - `search_trainer_winnings()` method (lines 321-355)

**Implementation Details:**
- **Query Used:**
```sql
SELECT CONCAT(t.fname, ' ', t.lname) as trainer_name,
       IFNULL(SUM(rr.prize), 0) as total_winnings,
       COUNT(CASE WHEN rr.results = 'first' THEN 1 END) as num_wins,
       s.stableName
FROM Trainer t
LEFT JOIN Horse h ON h.stableId = t.stableId
LEFT JOIN RaceResults rr ON h.horseId = rr.horseId
LEFT JOIN Stable s ON t.stableId = s.stableId
GROUP BY t.trainerId, t.fname, t.lname, s.stableName
ORDER BY total_winnings DESC
```

**How it works:**
1. Calculates total prize money won by each trainer's horses
2. Counts number of first-place wins for each trainer
3. Includes stable information for each trainer
4. Uses LEFT JOIN to include trainers with no wins (showing $0.00)
5. Results sorted by total winnings (highest first)
6. Handles NULL values using IFNULL function

#### Function 4: List the tracks and the count of races held on the track and the total number of horses participating in races on the track
**Implementation Location:** `guest_gui.py` - `search_track_stats()` method (lines 357-392)

**Implementation Details:**
- **Query Used:**
```sql
SELECT tr.trackName,
       tr.location,
       tr.length,
       COUNT(DISTINCT r.raceId) as num_races,
       COUNT(DISTINCT rr.horseId) as total_horses
FROM Track tr
LEFT JOIN Race r ON tr.trackName = r.trackName
LEFT JOIN RaceResults rr ON r.raceId = rr.raceId
GROUP BY tr.trackName, tr.location, tr.length
ORDER BY tr.trackName
```

**How it works:**
1. Provides comprehensive statistics for each track
2. Counts distinct races held on each track
3. Counts total number of unique horses that participated in races on each track
4. Includes track location and length information
5. Uses DISTINCT to avoid counting same horse in multiple races on same track
6. Results sorted alphabetically by track name

## Additional Requirements Implementation

### Additional Requirement 1: Use appropriate API(s) wherever needed
**Implementation Location:** `database.py` - DatabaseManager class (lines 12-158)

**API Implementation:**
- **MySQL Connector API:** Uses `mysql-connector-python` library for database connectivity
- **tkinter API:** Uses Python's built-in tkinter for GUI components
- **DatabaseManager Methods:**
  - `get_connection()`: Establishes MySQL connection
  - `execute_query()`: Handles all SQL query operations
  - `execute_procedure()`: Executes stored procedures
  - `test_connection()`: Validates database connectivity
  - `setup_database()`: Automates database initialization

### Additional Requirement 2: Using Procedural SQL

#### i. Stored Procedure to Delete an Owner
**Implementation Location:** `procedures_triggers.sql` - Lines 4-24

**Complete Implementation:**
```sql
CREATE PROCEDURE DeleteOwner(IN owner_to_delete VARCHAR(15))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Delete all Owns relationships for this owner
    DELETE FROM Owns WHERE ownerId = owner_to_delete;
    
    -- Delete the owner from Owner table
    DELETE FROM Owner WHERE ownerId = owner_to_delete;
    
    -- Commit the transaction
    COMMIT;
END;
```

**Features:**
- **Error Handling:** Includes exception handler with rollback capability
- **Transaction Management:** Uses START TRANSACTION and COMMIT for data integrity
- **Parameter Passing:** Accepts owner ID as input parameter
- **Referential Integrity:** Deletes relationships first, then owner record

#### ii. Trigger to Copy Horse Information
**Implementation Location:** `procedures_triggers.sql` - Lines 27-34

**Complete Implementation:**
```sql
CREATE TRIGGER horse_delete_trigger
    BEFORE DELETE ON Horse
    FOR EACH ROW
BEGIN
    -- Insert the horse information into old_info table before deletion
    INSERT INTO old_info (horseId, horseName, age, gender, registration, stableId)
    VALUES (OLD.horseId, OLD.horseName, OLD.age, OLD.gender, OLD.registration, OLD.stableId);
END;
```

**Features:**
- **Trigger Type:** BEFORE DELETE trigger on Horse table
- **Data Preservation:** Copies all horse information to old_info table
- **Automatic Execution:** Trigger fires automatically before any horse deletion
- **Audit Trail:** Includes timestamp of deletion via DEFAULT CURRENT_TIMESTAMP
- **Complete Data:** Captures all original horse fields using OLD keyword

## Technology Stack

### Core Technologies

#### Database System
- **MySQL Server:** Primary database management system
- **Database Name:** Horses (configured via MCP server)

#### Programming Languages
- **Python 3.x:** Primary programming language for application logic
- **SQL:** Structured Query Language for database operations
- **SQL Procedural Language:** For stored procedures and triggers

#### GUI Framework
- **tkinter:** Python's standard GUI toolkit
  - **ttk:** Themed tkinter widgets for modern appearance
  - **Custom styling:** Blue/dark theme with proper color schemes
  - **Tabbed interfaces:** Uses ttk.Notebook for organized functionality

#### Database Connectivity
- **mysql-connector-python:** Official MySQL connector for Python
  - **Version:** >=8.0.33 (specified in requirements.txt)
  - **Features:** 
    - Connection pooling
    - Prepared statements
    - Stored procedure execution
    - Transaction management
    - Dictionary cursor support

#### Application Architecture
- **Object-Oriented Design:** Classes for different components
- **Modular Structure:** Separate files for different functionalities
- **Database Abstraction:** DatabaseManager class for connection handling
- **GUI Separation:** Admin and Guest interfaces in separate modules

#### File Structure
- **`main.py`:** Main application entry point and user selection
- **`database.py`:** Database connection and management
- **`admin_gui.py`:** Administrative functions and interfaces
- **`guest_gui.py`:** Guest browsing and search functions
- **`database_schema.sql`:** Complete database schema definition
- **`sample_data.sql`:** Sample data for testing and demonstration
- **`procedures_triggers.sql`:** Stored procedures and triggers
- **`requirements.txt`:** Python dependencies

#### Development Features
- **Error Handling:** Comprehensive exception handling throughout
- **User Feedback:** Message boxes for success/error states
- **Data Validation:** Input validation for all user entries
- **Transaction Safety:** Database operations use proper transaction handling
- **Clean Code:** Well-documented with docstrings and comments

## Summary

This Horse Racing Database System successfully implements all required functionality using a modern Python GUI application with MySQL backend. The system provides both administrative and guest interfaces, implements all required functions with appropriate SQL queries, and includes advanced features like stored procedures and triggers. The technology stack provides a robust, scalable, and user-friendly solution for managing horse racing data.