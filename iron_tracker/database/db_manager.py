import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """Manages SQLite database operations for iron level tracking."""
    
    def __init__(self, db_path: str = "iron_tracker.db"):
        self.db_path = db_path
        self.connection = None
    
    def init_db(self) -> None:
        """Initialize the database and create tables if they don't exist."""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self._create_tables()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
    
    def _create_tables(self) -> None:
        """Create database tables."""
        cursor = self.connection.cursor()
        
        # Iron readings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iron_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reading_date DATE NOT NULL,
                reading_time TIME NOT NULL,
                iron_level REAL NOT NULL,
                unit TEXT DEFAULT 'μg/dL',
                notes TEXT,
                test_type TEXT DEFAULT 'Serum Iron',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User profile table for reference ranges
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                gender TEXT CHECK(gender IN ('male', 'female', 'other')),
                normal_range_min REAL DEFAULT 60,
                normal_range_max REAL DEFAULT 170,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert default profile if none exists
        cursor.execute("SELECT COUNT(*) FROM user_profile")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO user_profile (age, gender, normal_range_min, normal_range_max)
                VALUES (30, 'other', 60, 170)
            """)
        
        self.connection.commit()
    
    def add_reading(self, iron_level: float, reading_date: date = None, 
                   reading_time: str = None, notes: str = "", test_type: str = "Serum Iron") -> bool:
        """Add a new iron level reading."""
        try:
            if reading_date is None:
                reading_date = date.today()
            if reading_time is None:
                reading_time = datetime.now().strftime("%H:%M")
            
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO iron_readings (reading_date, reading_time, iron_level, notes, test_type)
                VALUES (?, ?, ?, ?, ?)
            """, (reading_date, reading_time, iron_level, notes, test_type))
            
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding reading: {e}")
            return False
    
    def get_all_readings(self) -> List[Dict]:
        """Get all iron level readings."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM iron_readings 
                ORDER BY reading_date DESC, reading_time DESC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching readings: {e}")
            return []
    
    def get_recent_readings(self, limit: int = 10) -> List[Dict]:
        """Get the most recent iron level readings."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM iron_readings 
                ORDER BY reading_date DESC, reading_time DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching recent readings: {e}")
            return []
    
    def get_readings_by_date_range(self, start_date: date, end_date: date) -> List[Dict]:
        """Get readings within a specific date range."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT * FROM iron_readings 
                WHERE reading_date BETWEEN ? AND ?
                ORDER BY reading_date ASC, reading_time ASC
            """, (start_date, end_date))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching readings by date range: {e}")
            return []
    
    def delete_reading(self, reading_id: int) -> bool:
        """Delete a specific reading."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM iron_readings WHERE id = ?", (reading_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting reading: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """Get statistical information about iron readings."""
        try:
            cursor = self.connection.cursor()
            
            # Basic statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_readings,
                    AVG(iron_level) as average_level,
                    MIN(iron_level) as min_level,
                    MAX(iron_level) as max_level,
                    MIN(reading_date) as first_reading_date,
                    MAX(reading_date) as last_reading_date
                FROM iron_readings
            """)
            stats = dict(cursor.fetchone())
            
            # Get normal range from user profile
            cursor.execute("SELECT normal_range_min, normal_range_max FROM user_profile LIMIT 1")
            profile = cursor.fetchone()
            if profile:
                stats['normal_range_min'] = profile['normal_range_min']
                stats['normal_range_max'] = profile['normal_range_max']
                
                # Count readings in different ranges
                cursor.execute("""
                    SELECT 
                        SUM(CASE WHEN iron_level < ? THEN 1 ELSE 0 END) as low_readings,
                        SUM(CASE WHEN iron_level BETWEEN ? AND ? THEN 1 ELSE 0 END) as normal_readings,
                        SUM(CASE WHEN iron_level > ? THEN 1 ELSE 0 END) as high_readings
                    FROM iron_readings
                """, (profile['normal_range_min'], profile['normal_range_min'], 
                     profile['normal_range_max'], profile['normal_range_max']))
                
                range_stats = dict(cursor.fetchone())
                stats.update(range_stats)
            
            return stats
        except sqlite3.Error as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def update_user_profile(self, age: int = None, gender: str = None, 
                           normal_range_min: float = None, normal_range_max: float = None) -> bool:
        """Update user profile information."""
        try:
            cursor = self.connection.cursor()
            
            # Build dynamic UPDATE query
            updates = []
            values = []
            
            if age is not None:
                updates.append("age = ?")
                values.append(age)
            if gender is not None:
                updates.append("gender = ?")
                values.append(gender)
            if normal_range_min is not None:
                updates.append("normal_range_min = ?")
                values.append(normal_range_min)
            if normal_range_max is not None:
                updates.append("normal_range_max = ?")
                values.append(normal_range_max)
            
            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                query = f"UPDATE user_profile SET {', '.join(updates)} WHERE id = 1"
                cursor.execute(query, values)
                self.connection.commit()
                return True
            
            return False
        except sqlite3.Error as e:
            print(f"Error updating user profile: {e}")
            return False
    
    def get_user_profile(self) -> Dict:
        """Get user profile information."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM user_profile LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else {}
        except sqlite3.Error as e:
            print(f"Error getting user profile: {e}")
            return {}
    
    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None