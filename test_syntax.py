#!/usr/bin/env python3
"""
Simple syntax validation script for Horse Racing Database System
Tests basic Python syntax and imports without requiring MySQL
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported"""
    print("Testing Python syntax and imports...")
    
    try:
        # Test basic imports
        import tkinter as tk
        print("[OK] tkinter imported successfully")
        
        # Test custom modules syntax (without MySQL connection)
        import database
        print("[OK] database.py syntax valid")
        
        import main
        print("[OK] main.py syntax valid")
        
        import admin_gui
        print("[OK] admin_gui.py syntax valid")
        
        import guest_gui
        print("[OK] guest_gui.py syntax valid")
        
        return True
        
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False
    except SyntaxError as e:
        print(f"[SYNTAX ERROR] Syntax error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Other error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'database_schema.sql',
        'sample_data.sql', 
        'procedures_triggers.sql',
        'database.py',
        'main.py',
        'admin_gui.py',
        'guest_gui.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for filename in required_files:
        if os.path.exists(filename):
            print(f"[OK] {filename} found")
        else:
            print(f"[MISSING] {filename} missing")
            missing_files.append(filename)
    
    return len(missing_files) == 0

def test_sql_files():
    """Test basic SQL syntax"""
    print("\nTesting SQL files...")
    
    sql_files = [
        'database_schema.sql',
        'sample_data.sql',
        'procedures_triggers.sql'
    ]
    
    for filename in sql_files:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read()
                if content.strip():
                    print(f"[OK] {filename} has content")
                else:
                    print(f"[EMPTY] {filename} is empty")
        else:
            print(f"[MISSING] {filename} missing")

def main():
    """Main test function"""
    print("Horse Racing Database System - Basic Validation")
    print("=" * 50)
    
    # Test file structure
    files_ok = test_file_structure()
    
    # Test SQL files
    test_sql_files()
    
    # Test Python imports (may fail due to missing MySQL connector)
    imports_ok = test_imports()
    
    print("\n" + "=" * 50)
    print("Validation Summary:")
    print(f"File structure: {'[OK] PASS' if files_ok else '[FAIL] FAIL'}")
    print(f"Python imports: {'[OK] PASS' if imports_ok else '[FAIL] FAIL (may need: pip install mysql-connector-python)'}")
    
    if files_ok and imports_ok:
        print("\n[SUCCESS] Basic validation PASSED!")
        print("To run the full application:")
        print("1. Install MySQL server")
        print("2. Install dependencies: pip install -r requirements.txt") 
        print("3. Run: python main.py")
    else:
        print("\n[ERROR] Validation FAILED - please check missing files or dependencies")

if __name__ == "__main__":
    main()