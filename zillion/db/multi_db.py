"""
Multi-data source configuration and connection manager
Supports both MySQL and SQLite databases
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

# Database type constants
DB_TYPE_MYSQL = 'mysql'
DB_TYPE_SQLITE = 'sqlite'

# Database name constants
DB_FUTURE = 'future'
DB_STOCK = 'stock'
DB_APP = 'app'
DB_TEST = 'test'


class DatabaseConfig:
    """Database configuration manager"""

    def __init__(self):
        self.configs = {}
        self._load_configs()

    def _load_configs(self):
        """Load database configurations"""

        # MySQL configurations
        self.configs[DB_FUTURE] = {
            'type': DB_TYPE_MYSQL,
            'url': 'mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/future?charset=UTF8MB4',
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 10,
            'pool_recycle': 3600
        }

        self.configs[DB_STOCK] = {
            'type': DB_TYPE_MYSQL,
            'url': 'mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/stock?charset=UTF8MB4',
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 10,
            'pool_recycle': 3600
        }

        self.configs[DB_APP] = {
            'type': DB_TYPE_MYSQL,
            'url': 'mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/app?charset=UTF8MB4',
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 10,
            'pool_recycle': 3600
        }

        self.configs[DB_TEST] = {
            'type': DB_TYPE_MYSQL,
            'url': 'mysql+pymysql://linjingu:linjingu@127.0.0.1:3306/test?charset=UTF8MB4',
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 10,
            'pool_recycle': 3600
        }

        # SQLite configurations (for local development/testing)
        # File structure:
        #   zillion/db/multi_db.py (this file)
        #   zillion/db/data/future.db (database file)
        # Use absolute path based on this file's location
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.configs['future_sqlite'] = {
            'type': DB_TYPE_SQLITE,
            'url': f'sqlite:///{base_dir}/data/future.db',
            'echo': False
        }

        self.configs['stock_sqlite'] = {
            'type': DB_TYPE_SQLITE,
            'url': f'sqlite:///{os.path.dirname(base_dir)}/data/stock.db',
            'echo': False
        }

        self.configs['test_sqlite'] = {
            'type': DB_TYPE_SQLITE,
            'url': f'sqlite:///{base_dir}/data/test.db',
            'echo': False
        }

    def get_config(self, db_name):
        """Get database configuration by name"""
        if db_name not in self.configs:
            raise ValueError(f"Database '{db_name}' not configured")
        return self.configs[db_name]

    def add_config(self, db_name, config):
        """Add custom database configuration"""
        self.configs[db_name] = config


class ConnectionManager:
    """Manage database connections and sessions"""

    def __init__(self, config_manager=None):
        self.config_manager = config_manager or DatabaseConfig()
        self.engines = {}
        self.session_factories = {}

    def get_engine(self, db_name):
        """Get or create database engine"""
        if db_name not in self.engines:
            config = self.config_manager.get_config(db_name)
            db_type = config['type']

            if db_type == DB_TYPE_SQLITE:
                # SQLite specific configuration
                url = config['url']

                # Ensure directory exists for SQLite file
                if url.startswith('sqlite:///'):
                    db_path = url.replace('sqlite:///', '')
                    if not db_path.startswith(':memory:'):
                        db_dir = os.path.dirname(db_path)
                        if db_dir and not os.path.exists(db_dir):
                            os.makedirs(db_dir)

                self.engines[db_name] = create_engine(
                    url,
                    echo=config.get('echo', False),
                    connect_args={'check_same_thread': False}  # Allow multi-threading
                )
            else:
                # MySQL configuration
                self.engines[db_name] = create_engine(
                    config['url'],
                    echo=config.get('echo', False),
                    pool_size=config.get('pool_size', 5),
                    max_overflow=config.get('max_overflow', 10),
                    pool_timeout=config.get('pool_timeout', 30),
                    pool_recycle=config.get('pool_recycle', 3600)
                )

        return self.engines[db_name]

    def get_session_factory(self, db_name):
        """Get session factory for a database"""
        if db_name not in self.session_factories:
            engine = self.get_engine(db_name)
            self.session_factories[db_name] = sessionmaker(bind=engine)
        return self.session_factories[db_name]

    @contextmanager
    def get_session(self, db_name):
        """Get a database session (context manager)"""
        session_factory = self.get_session_factory(db_name)
        session = session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_scoped_session(self, db_name):
        """Get a scoped session (thread-local)"""
        session_factory = self.get_session_factory(db_name)
        return scoped_session(session_factory)

    def close_all(self):
        """Close all connections"""
        for session_factory in self.session_factories.values():
            if hasattr(session_factory, 'remove'):
                session_factory.remove()
        for engine in self.engines.values():
            engine.dispose()


# Global instances
db_config = DatabaseConfig()
connection_manager = ConnectionManager(db_config)


# Convenience functions
def get_engine(db_name):
    """Get database engine"""
    return connection_manager.get_engine(db_name)


def get_session(db_name):
    """Get database session (context manager)"""
    return connection_manager.get_session(db_name)


def get_scoped_session(db_name):
    """Get scoped session"""
    return connection_manager.get_scoped_session(db_name)

# ... existing code ...

def get_scoped_session(db_name):
    """Get scoped session"""
    return connection_manager.get_scoped_session(db_name)


def verify_tables(db_name='future_sqlite', required_tables=None):
    """
    Verify that required tables exist in the database

    Args:
        db_name: Database configuration name
        required_tables: List of table names to check

    Returns:
        Dictionary with table names and their existence status
    """
    if required_tables is None:
        required_tables = ['basic', 'contract', 'trade_daily']

    try:
        engine = get_engine(db_name)
        results = {}

        with engine.connect() as conn:
            for table in required_tables:
                # Check if table exists using SQLite system table
                result = conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table' AND name=:table_name"),
                    {"table_name": table}
                )
                exists = result.fetchone() is not None
                results[table] = exists

        return results
    except Exception as e:
        print(f"Error verifying tables: {e}")
        return {table: False for table in required_tables}


# ... existing code ...

if __name__ == '__main__':
    # Test MySQL connection
    print("Testing MySQL connection...")
    try:
        engine = get_engine(DB_FUTURE)
        print(f"MySQL Engine: {engine}")
    except Exception as e:
        print(f"MySQL connection failed: {e}")

    # Test SQLite connection
    print("\nTesting SQLite connection...")
    try:
        from sqlalchemy import text

        engine = get_engine('future_sqlite')
        print(f"SQLite Engine: {engine}")

        # Test session with proper text() wrapper
        with get_session('future_sqlite') as session:
            result = session.execute(text("SELECT 1"))
            print(f"SQLite query result: {result.fetchone()}")

        # Verify tables exist
        print("\nVerifying tables...")
        table_status = verify_tables('future_sqlite')
        for table, exists in table_status.items():
            status = "✓" if exists else "✗"
            print(f"  {status} {table}: {'exists' if exists else 'not found'}")

    except Exception as e:
        print(f"SQLite connection failed: {e}")



