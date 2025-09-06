#!/usr/bin/env python3
"""
Database initialization script for Luminis AI Library Assistant
This script creates the database tables and populates them with sample data.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from database import create_tables, init_sample_data, engine
from sqlalchemy import text


def check_database_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Please check your database configuration:")
        print("1. Make sure MySQL is running")
        print("2. Check your DATABASE_URL in .env file")
        print("3. Ensure the database 'luminis_library' exists")
        print("\n📝 To create the database manually:")
        print("mysql -u root -p")
        print("CREATE DATABASE luminis_library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        return False


def main():
    """Main initialization function"""
    print("🚀 Initializing Luminis AI Library Database...")
    print("=" * 50)

    # Check database connection
    if not check_database_connection():
        return False

    try:
        # Create tables
        print("\n📋 Creating database tables...")
        create_tables()
        print("✅ Tables created successfully!")

        # Initialize sample data
        print("\n📚 Loading sample books...")
        init_sample_data()
        print("✅ Sample data loaded successfully!")

        print("\n🎉 Database initialization completed!")
        print("\n📖 Next steps:")
        print("1. Start the server: npm run start")
        print("2. Access the application: http://localhost:8000")
        print("3. The database is ready for use!")

        return True

    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
