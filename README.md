# Horse Racing Database System (ICS321 Project #1)

## Project Overview
This is a complete Horse Racing Database System implementation for the ICS321 course. The system provides a simple GUI interface using Python with Tkinter to manage and query a MySQL database containing horse racing information.

## Features Implemented

### Admin Functions
- **Add New Race with Results**: Create races and add multiple horse results with prize money
- **Delete Owner**: Remove an owner and all related information using a stored procedure
- **Move Horse**: Transfer horses between stables
- **Approve Trainer**: Add new trainers and assign them to stables

### Guest Functions
- **Browse Horses by Owner**: Search horses by owner last name with trainer information
- **Winning Trainers**: View trainers who have trained first-place winners
- **Trainer Winnings**: See total prize money and wins for each trainer (sorted by winnings)
- **Track Statistics**: Display tracks with race counts and total participating horses

### Database Implementation
- **Schema**: Complete horse racing database with proper relationships
- **Sample Data**: 26 horses, 20 owners, 8 trainers, 6 stables, 9 tracks, 36 races with results
- **Stored Procedures**: DeleteOwner procedure for cascading deletions
- **Triggers**: Automatic backup of horse information before deletion

## Database Schema
The database follows the original ICS321 specification with the following tables:
- **Stable**: Stable information (ID, name, location, colors)
- **Horse**: Horse details (ID, name, age, gender, registration, stable)
- **Owner**: Owner information (ID, first name, last name)
- **Owns**: Many-to-many relationship between owners and horses
- **Trainer**: Trainer details (ID, name, assigned stable)
- **Track**: Racing track information (name, location, length)
- **Race**: Race details (ID, name, track, date, time)
- **RaceResults**: Race results (race ID, horse ID, position, prize money)
- **old_info**: Backup table for deleted horse information

## Technologies Used
- **Backend**: Python with MySQL connector
- **GUI**: Tkinter (built-in Python library)
- **Database**: MySQL Server
- **Architecture**: MVC pattern with separate modules

## Setup Instructions

### Prerequisites
1. Python 3.x installed
2. MySQL Server running on localhost
3. MySQL user: `root` with password: `Asd11011`

### Installation
1. Install required Python packages:
   ```bash
   pip install mysql-connector-python
   ```

2. Run the database setup script:
   ```bash
   python setup_database.py
   ```

3. Launch the main application:
   ```bash
   python main.py
   ```

## Usage

### First Time Setup
1. Run `setup_database.py` to create the "Horses" database and populate it with sample data
2. The setup will create all tables, relationships, and sample data automatically

### Using the Application
1. **Main Menu**: Choose between Admin Access or Guest Access
2. **Database Connection**: Use "Test Database Connection" to verify connectivity
3. **Admin Panel**: Access administrative functions through tabbed interface
4. **Guest Panel**: Browse and search through the database with various queries

## Key Features

### Admin Panel
- **Add Race Tab**: Add new races with multiple participants and results
- **Delete Owner Tab**: Remove owners using stored procedure (cascades to Owns table)
- **Move Horse Tab**: Transfer horses between stables with validation
- **Approve Trainer Tab**: Add new trainers and assign to stables

### Guest Panel
- **Horses by Owner**: Search by owner last name (case-insensitive)
- **Winning Trainers**: View trainers with first-place victories
- **Trainer Winnings**: Sorted list of trainer performance
- **Track Statistics**: Comprehensive track usage statistics

## Database Functions

### Stored Procedures
- `DeleteOwner(owner_to_delete)`: Safely deletes an owner and all related horse ownership records

### Triggers
- `horse_delete_trigger`: Automatically copies horse information to `old_info` table before deletion

## Sample Data Included
- **6 Stables**: From various Middle Eastern locations
- **26 Horses**: With diverse names and characteristics
- **20 Owners**: With Arabic names and multiple horse holdings
- **8 Trainers**: Assigned to different stables
- **9 Tracks**: Including famous racing venues
- **36 Races**: With complete result data
- **Race Results**: Detailed positioning and prize money

## Project Structure
```
├── main.py              # Main application entry point
├── database.py          # Database connectivity module
├── admin_gui.py         # Administrative interface
├── guest_gui.py         # Guest browsing interface
├── setup_database.py    # Database setup script
├── database_schema.sql  # Complete database schema
├── sample_data.sql      # Sample data insertion
├── procedures_triggers.sql # Stored procedures and triggers
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Error Handling
- Comprehensive error handling throughout the application
- User-friendly error messages with GUI notifications
- Database connection validation and recovery
- Input validation for all user inputs

## Security Features
- Parameterized SQL queries to prevent SQL injection
- Input validation and sanitization
- Connection security with proper credentials

## Performance Considerations
- Efficient database queries with proper JOINs
- GUI responsiveness through proper threading
- Optimized queries for large datasets

## Compliance with Requirements
✅ Simple UI using Python (Tkinter)
✅ MySQL database (no SQLite)
✅ Admin and Guest user types
✅ All required functions implemented
✅ Stored procedures and triggers
✅ Proper database relationships and constraints
✅ Sample data matching specification

## Future Enhancements
- User authentication system
- Advanced reporting features
- Data export capabilities
- Enhanced validation and error handling
- Performance optimization for large datasets

## Course Information
- **Course**: ICS321 - Database Systems
- **Project**: #1 Horse Racing Database System
- **Due Date**: October 18, 2025
- **Professor**: [Instructor Name]