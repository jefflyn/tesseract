"""
SQLite Database Initialization Script for Futures Database
"""
import sqlite3
import os


def init_futures_db(db_path='future.db'):
    """
    Initialize the futures database with all required tables

    Args:
        db_path: Path to the SQLite database file
    """
    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Connect to SQLite database (creates file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Table: basic (F12基本信息)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS basic (
            symbol      VARCHAR(4)    NOT NULL,
            name        VARCHAR(16)   NOT NULL,
            type        VARCHAR(8)    DEFAULT '',
            amount      INTEGER       DEFAULT 0,
            unit        VARCHAR(4)    DEFAULT '',
            step        DECIMAL(6,2)  DEFAULT 0.00,
            profit      INTEGER       DEFAULT 0,
            exchange    VARCHAR(16)   DEFAULT '',
            night       INTEGER       DEFAULT 1,
            deleted     INTEGER       DEFAULT 0,
            PRIMARY KEY (symbol)
        )
    ''')

    # Table: contract (合约信息)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contract (
            symbol        VARCHAR(4)    NOT NULL,
            code          VARCHAR(8)    NOT NULL,
            main          INTEGER       DEFAULT 0,
            "limit"       INTEGER       DEFAULT NULL,
            low           DECIMAL(10,2) NOT NULL,
            high          DECIMAL(10,2) NOT NULL,
            low_time      VARCHAR(20)   DEFAULT NULL,
            high_time     VARCHAR(20)   DEFAULT NULL,
            h_low         DECIMAL(10,2) DEFAULT NULL,
            h_high        DECIMAL(10,2) DEFAULT NULL,
            h_low_time    VARCHAR(20)   DEFAULT NULL,
            h_high_time   VARCHAR(20)   DEFAULT NULL,
            create_time   DATETIME      NOT NULL,
            update_time   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
            deleted       INTEGER       DEFAULT 0,
            PRIMARY KEY (code),
            CONSTRAINT uidx_contract_symbol_code UNIQUE (symbol, code)
        )
    ''')

    # Table: trade_daily (每日行情)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trade_daily (
            id            INTEGER       PRIMARY KEY AUTOINCREMENT,
            symbol        VARCHAR(6)    NOT NULL,
            trade_date    VARCHAR(10)   NOT NULL,
            code          VARCHAR(10)   DEFAULT NULL,
            open          DECIMAL(10,2) DEFAULT NULL,
            high          DECIMAL(10,2) DEFAULT NULL,
            low           DECIMAL(10,2) DEFAULT NULL,
            close         DECIMAL(10,2) DEFAULT NULL,
            settle        DECIMAL(10,2) DEFAULT NULL,
            pre_close     DECIMAL(10,2) DEFAULT NULL,
            pre_settle    DECIMAL(10,2) DEFAULT NULL,
            close_change  DECIMAL(10,2) DEFAULT NULL,
            settle_change DECIMAL(10,2) DEFAULT NULL,
            deal_vol      INTEGER       DEFAULT NULL,
            hold_vol      INTEGER       DEFAULT NULL,
            create_time   DATETIME      NOT NULL,
            CONSTRAINT uidx_future_daily_trade_date_contract_code UNIQUE (trade_date, code)
        )
    ''')

    # Create indexes for better query performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_future_daily_code 
        ON trade_daily (symbol)
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_future_daily_code_date 
        ON trade_daily (code, trade_date)
    ''')

    # Commit changes and close connection
    conn.commit()

    print(f"Database initialized successfully at: {db_path}")
    print(f"Tables created:")
    print(f"  - basic (F12基本信息)")
    print(f"  - contract (合约信息)")
    print(f"  - trade_daily (每日行情)")

    cursor.close()
    conn.close()

    return True


if __name__ == '__main__':
    # Initialize database in the default location
    init_futures_db('data/future.db')
