"""
Script to properly create stored procedures and triggers
This handles the DELIMITER issue when creating procedures
"""

import mysql.connector
from mysql.connector import Error

def create_procedures():
    """Create stored procedures with proper delimiter handling"""
    try:
        # Connect to MySQL
        print("Connecting to MySQL server...")
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Asd11011",
            database="Horses"
        )
        
        if connection.is_connected():
            print("Connected to Horses database successfully!")
            
            cursor = connection.cursor()
            
            # Drop existing procedure if it exists
            print("Dropping existing procedure if it exists...")
            try:
                cursor.execute("DROP PROCEDURE IF EXISTS DeleteOwner")
                connection.commit()
                print("Existing procedure dropped.")
            except Error as e:
                print(f"Note: {e}")
            
            # Create DeleteOwner procedure
            print("Creating DeleteOwner procedure...")
            delete_owner_proc = """
CREATE PROCEDURE DeleteOwner(IN owner_to_delete VARCHAR(15))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    DELETE FROM Owns WHERE ownerId = owner_to_delete;
    
    DELETE FROM Owner WHERE ownerId = owner_to_delete;
    
    COMMIT;
END
"""
            cursor.execute(delete_owner_proc)
            connection.commit()
            print("DeleteOwner procedure created successfully!")
            
            # Drop existing trigger if it exists
            print("Dropping existing trigger if it exists...")
            try:
                cursor.execute("DROP TRIGGER IF EXISTS horse_delete_trigger")
                connection.commit()
                print("Existing trigger dropped.")
            except Error as e:
                print(f"Note: {e}")
            
            # Create horse_delete_trigger
            print("Creating horse_delete_trigger...")
            horse_trigger = """
CREATE TRIGGER horse_delete_trigger
    BEFORE DELETE ON Horse
    FOR EACH ROW
BEGIN
    INSERT INTO old_info (horseId, horseName, age, gender, registration, stableId)
    VALUES (OLD.horseId, OLD.horseName, OLD.age, OLD.gender, OLD.registration, OLD.stableId);
END
"""
            cursor.execute(horse_trigger)
            connection.commit()
            print("horse_delete_trigger created successfully!")
            
            # Verify procedure was created
            cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'Horses'")
            procedures = cursor.fetchall()
            print(f"\nProcedures in database: {[proc[1] for proc in procedures]}")
            
            # Verify trigger was created
            cursor.execute("SHOW TRIGGERS FROM Horses")
            triggers = cursor.fetchall()
            print(f"Triggers in database: {[trigger[0] for trigger in triggers]}")
            
            cursor.close()
            connection.close()
            
            print("\n✓ All procedures and triggers created successfully!")
            return True
            
    except Error as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    create_procedures()
