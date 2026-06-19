"""
Database Manager for Futures System
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseManager:
    def __init__(self, db_path: str = "futures.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create basic table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS basic (
                symbol VARCHAR(4) NOT NULL PRIMARY KEY,
                name VARCHAR(16) NOT NULL,
                type VARCHAR(8) DEFAULT '',
                amount INT DEFAULT 0,
                unit VARCHAR(4) DEFAULT '',
                step DECIMAL(6, 2) DEFAULT 0.00,
                profit INT DEFAULT 0,
                `limit` INT DEFAULT -1,
                exchange VARCHAR(16) DEFAULT '',
                night TINYINT DEFAULT -1,
                deleted TINYINT DEFAULT 0,
                update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create contract table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contract (
                symbol VARCHAR(4) NOT NULL,
                code VARCHAR(8) NOT NULL,
                ts_code VARCHAR(12) NOT NULL,
                main TINYINT DEFAULT 0,
                `limit` INT,
                low DECIMAL(10, 2) NOT NULL,
                high DECIMAL(10, 2) NOT NULL,
                low_time VARCHAR(20),
                high_time VARCHAR(20),
                h_low DECIMAL(10, 2),
                h_high DECIMAL(10, 2),
                h_low_time VARCHAR(20),
                h_high_time VARCHAR(20),
                selected TINYINT DEFAULT 0,
                create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                deleted TINYINT DEFAULT 0,
                PRIMARY KEY (code),
                UNIQUE (symbol, code),
                UNIQUE (symbol, ts_code)
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_contract_selected 
            ON contract (selected)
        ''')

        # Create trade_daily table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_daily (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol VARCHAR(6) NOT NULL,
                trade_date VARCHAR(10) NOT NULL,
                code VARCHAR(10),
                open DECIMAL(10, 2),
                high DECIMAL(10, 2),
                low DECIMAL(10, 2),
                close DECIMAL(10, 2),
                settle DECIMAL(10, 2),
                pre_close DECIMAL(10, 2),
                pre_settle DECIMAL(10, 2),
                close_change DECIMAL(10, 2),
                settle_change DECIMAL(10, 2),
                deal_vol INT,
                hold_vol INT,
                create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (trade_date, code)
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_future_daily_code 
            ON trade_daily (symbol)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_future_daily_code_date 
            ON trade_daily (code, trade_date)
        ''')

        conn.commit()
        conn.close()


db_manager = DatabaseManager()
