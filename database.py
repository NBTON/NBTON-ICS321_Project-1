"""
Database connectivity module for Horse Racing Database System
Handles MySQL connection and provides utility functions
"""

import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
import os

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.host = "127.0.0.1"
        self.database = "Horses"  # Match MCP configuration
        self.user = "root"
        self.password = "Asd11011"
        
    def get_connection(self):
        """Create and return database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                autocommit=True
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return None
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.get_connection()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            # Check if query is a SELECT statement
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return results
            else:
                # For INSERT, UPDATE, DELETE
                self.connection.commit()
                return cursor.rowcount
                
        except Error as e:
            print(f"Error executing query: {e}")
            messagebox.showerror("Database Error", f"Query execution failed: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def execute_procedure(self, procedure_name, params=None):
        """Execute a stored procedure"""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.get_connection()
            
            cursor = self.connection.cursor()
            cursor.callproc(procedure_name, params)
            
            # Get results if any
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            
            return results
                
        except Error as e:
            print(f"Error executing procedure: {e}")
            messagebox.showerror("Database Error", f"Procedure execution failed: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def test_connection(self):
        """Test database connection"""
        try:
            if self.get_connection():
                cursor = self.connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                cursor.close()
                return True
        except Error as e:
            print(f"Connection test failed: {e}")
            return False
    
    def setup_database(self):
        """Set up the database by running schema and sample data"""
        try:
            # First try to create the database (may fail if it already exists)
            try:
                temp_connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
                cursor = temp_connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS Horses")
                temp_connection.close()
            except Exception:
                pass  # Database might already exist or no permissions
            
            # Now connect to the database
            if not self.get_connection():
                return False
            
            # Read and execute schema file
            with open('database_schema.sql', 'r') as schema_file:
                schema_sql = schema_file.read()
            
            # Execute schema
            self.execute_query(schema_sql)
            
            # Read and execute sample data file
            with open('sample_data.sql', 'r') as data_file:
                data_sql = data_file.read()
            
            # Execute sample data
            self.execute_query(data_sql)
            
            # Read and execute procedures/triggers
            with open('procedures_triggers.sql', 'r') as proc_file:
                proc_sql = proc_file.read()
            
            # Execute procedures and triggers
            self.execute_query(proc_sql)
            
            messagebox.showinfo("Success", "Database setup completed successfully!")
            return True
            
        except Exception as e:
            print(f"Database setup failed: {e}")
            messagebox.showerror("Setup Error", f"Failed to setup database: {e}")
            return False

# Global database manager instance
db_manager = DatabaseManager()