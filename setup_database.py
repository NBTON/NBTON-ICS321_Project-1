"""
Database Setup Script for Horse Racing Database System
Creates the Horses database and sets up all tables with sample data
"""

import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
import re

def execute_sql_file(cursor, filename):
    """Execute SQL statements from a file"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Special handling for procedures_triggers.sql
    if 'procedures_triggers' in filename:
        # For procedures and triggers, we need special handling
        # Split by CREATE PROCEDURE or CREATE TRIGGER
        import re
        
        # Remove comments
        lines = []
        for line in content.split('\n'):
            line = re.sub(r'--.*', '', line).strip()
            if line:
                lines.append(line)
        content = ' '.join(lines)
        
        # Split by CREATE statements
        parts = re.split(r'(CREATE\s+(?:PROCEDURE|TRIGGER))', content, flags=re.IGNORECASE)
        
        statements = []
        for i in range(1, len(parts), 2):
            if i+1 < len(parts):
                # Combine CREATE keyword with the procedure/trigger definition
                stmt = parts[i] + parts[i+1]
                # Find the END; to properly terminate
                end_pos = stmt.find('END;')
                if end_pos != -1:
                    stmt = stmt[:end_pos+4]  # Include END;
                    statements.append(stmt.strip())
        
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except Error as e:
                    print(f"Error executing: {statement[:50]}... - {e}")
                    raise
    else:
        # Regular SQL file handling
        # Remove comments and split by semicolon
        statements = []
        for line in content.split('\n'):
            # Remove comments
            line = re.sub(r'--.*', '', line).strip()
            if line:
                statements.append(line)
        
        # Join and split by semicolon
        full_sql = ' '.join(statements)
        sql_statements = [stmt.strip() for stmt in full_sql.split(';') if stmt.strip()]
        
        for statement in sql_statements:
            if statement:
                try:
                    cursor.execute(statement)
                except Error as e:
                    print(f"Error executing: {statement[:50]}... - {e}")
                    raise

def create_database_and_setup():
    """Create database and setup all tables with data"""
    try:
        # Connect to MySQL server without specifying database
        print("Connecting to MySQL server...")
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Asd11011"
        )
        
        if connection.is_connected():
            print("Connected to MySQL server successfully!")
            
            cursor = connection.cursor()
            
            # Create database
            print("Creating 'Horses' database...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS Horses")
            connection.commit()
            print("Database 'Horses' created successfully!")
            
            # Switch to Horses database
            cursor.execute("USE Horses")
            
            # Execute schema
            print("Setting up database schema...")
            execute_sql_file(cursor, 'database_schema.sql')
            connection.commit()
            print("Schema created successfully!")
            
            # Execute sample data
            print("Inserting sample data...")
            execute_sql_file(cursor, 'sample_data.sql')
            connection.commit()
            print("Sample data inserted successfully!")
            
            # Execute procedures/triggers
            print("Setting up stored procedures and triggers...")
            execute_sql_file(cursor, 'procedures_triggers.sql')
            connection.commit()
            print("Procedures and triggers created successfully!")
            
            # Verify tables were created
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Created tables: {[table[0] for table in tables]}")
            
            cursor.close()
            connection.close()
            
            print("Database setup completed successfully!")
            return True
            
    except Error as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main function with GUI"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    if create_database_and_setup():
        messagebox.showinfo("Success", "Database setup completed successfully!\n\nYou can now run the main application.")
    else:
        messagebox.showerror("Error", "Database setup failed. Please check the console for details.")
    
    root.destroy()

if __name__ == "__main__":
    main()