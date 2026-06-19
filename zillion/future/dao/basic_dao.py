"""
DAO for basic table with automatic deleted=0 filtering
Supports both MySQL and SQLite databases
"""
from typing import List, Optional
from sqlalchemy import Column, String, Integer, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from zillion.db.multi_db import get_session, get_scoped_session

Base = declarative_base()


class BasicModel(Base):
    """SQLAlchemy model for basic table"""
    __tablename__ = 'basic'

    symbol = Column(String(4), primary_key=True, nullable=False)
    name = Column(String(16), nullable=False)
    type = Column(String(8), default='')
    amount = Column(Integer, default=0)
    unit = Column(String(4), default='')
    step = Column(DECIMAL(6, 2), default=0.00)
    profit = Column(Integer, default=0)
    exchange = Column(String(16), default='')
    night = Column(Integer, default=1)
    deleted = Column(Integer, default=0)

    def __repr__(self):
        return f"<Basic(symbol={self.symbol}, name={self.name}, night={self.night})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'symbol': self.symbol,
            'name': self.name,
            'type': self.type,
            'amount': self.amount,
            'unit': self.unit,
            'step': float(self.step) if self.step else 0.0,
            'profit': self.profit,
            'exchange': self.exchange,
            'night': self.night,
            'deleted': self.deleted
        }


class BasicDAO:
    """
    DAO for basic table

    All query methods automatically filter by deleted=0
    Supports both MySQL and SQLite databases
    """

    def __init__(self, db_name='future_sqlite'):
        """
        Initialize DAO with database name

        Args:
            db_name: Database configuration name (default: 'future_sqlite')
        """
        self.db_name = db_name
        self.session = None

    def _get_session(self):
        """Get current session or create scoped session"""
        if self.session is None:
            self.session = get_scoped_session(self.db_name)
        return self.session

    def set_session(self, session):
        """Set external session (for transaction management)"""
        self.session = session

    # ==================== Query Methods (all filter by deleted=0) ====================

    def get_all_basic(self) -> List[BasicModel]:
        """
        Get all basic records where deleted=0

        Returns:
            List of BasicModel objects
        """
        session = self._get_session()
        return session.query(BasicModel).all()

    def get_selected_basic_(self) -> List[BasicModel]:
        """
        Get all basic records where deleted=0

        Returns:
            List of BasicModel objects
        """
        session = self._get_session()
        return session.query(BasicModel).filter(BasicModel.deleted == 0).all()

    def get_all_basic_as_map(self) -> dict[str, BasicModel]:
        """
        Get all basic records where deleted=0 and return as a dictionary keyed by symbol

        Returns:
            Dictionary mapping symbol to BasicModel objects
        """
        session = self._get_session()
        results = session.query(BasicModel).filter(BasicModel.deleted == 0).all()
        return {record.symbol: record for record in results}


    def get_basic_by_symbol(self, symbol: str) -> Optional[BasicModel]:
        """
        Get a single basic record by symbol where deleted=0

        Args:
            symbol: Symbol to search for

        Returns:
            BasicModel object or None
        """
        session = self._get_session()
        return session.query(BasicModel).filter(
            BasicModel.symbol == symbol,
            BasicModel.deleted == 0
        ).first()

    def get_basics_by_conditions(
        self,
        symbol: Optional[str] = None,
        night: Optional[int] = None,
        type_filter: Optional[str] = None,
        exchange: Optional[str] = None
    ) -> List[BasicModel]:
        """
        Query basic records with flexible conditions (always filters deleted=0)

        Args:
            symbol: Filter by symbol (exact match for short symbols, prefix search for longer)
            night: Filter by night trading flag (0=no, 1=yes)
            type_filter: Filter by product type
            exchange: Filter by exchange

        Returns:
            List of BasicModel objects matching the conditions
        """
        session = self._get_session()
        query = session.query(BasicModel).filter(BasicModel.deleted == 0)

        if symbol is not None:
            if len(symbol) <= 2:
                # Exact match for short symbols
                query = query.filter(BasicModel.symbol == symbol)
            else:
                # Prefix search for longer symbols
                query = query.filter(BasicModel.symbol.like(f"{symbol}%"))

        if night is not None:
            query = query.filter(BasicModel.night == night)

        if type_filter is not None:
            query = query.filter(BasicModel.type == type_filter)

        if exchange is not None:
            query = query.filter(BasicModel.exchange == exchange)

        return query.all()

    def get_night_trading_basics(self) -> List[BasicModel]:
        """
        Get all basic records with night trading enabled (night=1, deleted=0)

        Returns:
            List of BasicModel objects
        """
        session = self._get_session()
        return session.query(BasicModel).filter(
            BasicModel.deleted == 0,
            BasicModel.night == 1
        ).all()

    def get_day_trading_basics(self) -> List[BasicModel]:
        """
        Get all basic records without night trading (night=0, deleted=0)

        Returns:
            List of BasicModel objects
        """
        session = self._get_session()
        return session.query(BasicModel).filter(
            BasicModel.deleted == 0,
            BasicModel.night == 0
        ).all()

    def get_basics_by_exchange(self, exchange: str) -> List[BasicModel]:
        """
        Get all basic records by exchange (deleted=0)

        Args:
            exchange: Exchange name (e.g., 'SHFE', 'DCE', 'ZZCE')

        Returns:
            List of BasicModel objects
        """
        session = self._get_session()
        return session.query(BasicModel).filter(
            BasicModel.deleted == 0,
            BasicModel.exchange == exchange
        ).all()

    def get_basics_by_type(self, type_filter: str) -> List[BasicModel]:
        """
        Get all basic records by type (deleted=0)

        Args:
            type_filter: Product type (e.g., '金属', '农产品', '化工')

        Returns:
            List of BasicModel objects
        """
        session = self._get_session()
        return session.query(BasicModel).filter(
            BasicModel.deleted == 0,
            BasicModel.type == type_filter
        ).all()

    def count_by_conditions(
        self,
        symbol: Optional[str] = None,
        night: Optional[int] = None,
        type_filter: Optional[str] = None,
        exchange: Optional[str] = None
    ) -> int:
        """
        Count records matching the given conditions (always filters deleted=0)

        Args:
            symbol: Filter by symbol
            night: Filter by night trading flag
            type_filter: Filter by product type
            exchange: Filter by exchange

        Returns:
            Count of matching records
        """
        session = self._get_session()
        query = session.query(BasicModel).filter(BasicModel.deleted == 0)

        if symbol is not None:
            query = query.filter(BasicModel.symbol == symbol)

        if night is not None:
            query = query.filter(BasicModel.night == night)

        if type_filter is not None:
            query = query.filter(BasicModel.type == type_filter)

        if exchange is not None:
            query = query.filter(BasicModel.exchange == exchange)

        return query.count()

    def exists(self, symbol: str) -> bool:
        """
        Check if a basic record exists (only checks non-deleted records)

        Args:
            symbol: Symbol to check

        Returns:
            True if exists and not deleted, False otherwise
        """
        session = self._get_session()
        count = session.query(BasicModel).filter(
            BasicModel.symbol == symbol,
            BasicModel.deleted == 0
        ).count()
        return count > 0

    # ==================== Insert/Update/Delete Methods ====================

    def insert_basic(self, basic_data: dict) -> bool:
        """
        Insert a new basic record (automatically sets deleted=0)

        Args:
            basic_data: Dictionary containing basic record data

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            # Ensure deleted is set to 0
            if 'deleted' not in basic_data:
                basic_data['deleted'] = 0

            basic = BasicModel(**basic_data)
            session.add(basic)
            session.flush()
            return True
        except Exception as e:
            print(f"Insert error: {e}")
            session.rollback()
            return False

    def insert_many(self, basics_list: List[dict]) -> int:
        """
        Insert multiple basic records

        Args:
            basics_list: List of dictionaries containing basic record data

        Returns:
            Number of successfully inserted records
        """
        session = self._get_session()
        count = 0
        try:
            for basic_data in basics_list:
                if 'deleted' not in basic_data:
                    basic_data['deleted'] = 0
                basic = BasicModel(**basic_data)
                session.add(basic)
                count += 1
            session.flush()
            return count
        except Exception as e:
            print(f"Batch insert error: {e}")
            session.rollback()
            return 0

    def update_basic(self, symbol: str, updates: dict) -> bool:
        """
        Update an existing basic record

        Args:
            symbol: Symbol to update
            updates: Dictionary of fields to update

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            basic = session.query(BasicModel).filter(
                BasicModel.symbol == symbol,
                BasicModel.deleted == 0
            ).first()

            if basic:
                for key, value in updates.items():
                    if hasattr(basic, key) and key != 'symbol':
                        setattr(basic, key, value)
                session.flush()
                return True
            return False
        except Exception as e:
            print(f"Update error: {e}")
            session.rollback()
            return False

    def delete_basic(self, symbol: str, soft_delete: bool = True) -> bool:
        """
        Delete a basic record (soft delete by default)

        Args:
            symbol: Symbol to delete
            soft_delete: If True, set deleted=1; if False, actually delete

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            basic = session.query(BasicModel).filter(
                BasicModel.symbol == symbol
            ).first()

            if basic:
                if soft_delete:
                    basic.deleted = 1
                    session.flush()
                else:
                    session.delete(basic)
                    session.flush()
                return True
            return False
        except Exception as e:
            print(f"Delete error: {e}")
            session.rollback()
            return False

    def restore_basic(self, symbol: str) -> bool:
        """
        Restore a soft-deleted record (set deleted=0)

        Args:
            symbol: Symbol to restore

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            basic = session.query(BasicModel).filter(
                BasicModel.symbol == symbol,
                BasicModel.deleted == 1
            ).first()

            if basic:
                basic.deleted = 0
                session.flush()
                return True
            return False
        except Exception as e:
            print(f"Restore error: {e}")
            session.rollback()
            return False

    def close(self):
        """Close the session"""
        if self.session is not None:
            if hasattr(self.session, 'remove'):
                self.session.remove()
            else:
                self.session.close()
            self.session = None


# ==================== Convenience Functions ====================

def query_basics_with_context(
    symbol: Optional[str] = None,
    night: Optional[int] = None,
    type_filter: Optional[str] = None,
    exchange: Optional[str] = None,
    db_name: str = 'future_sqlite'
) -> List[dict]:
    """
    Query basics using context manager (recommended for simple queries)

    Args:
        symbol: Filter by symbol
        night: Filter by night trading
        type_filter: Filter by product type
        exchange: Filter by exchange
        db_name: Database name

    Returns:
        List of dictionaries
    """
    results = []
    with get_session(db_name) as session:
        dao = BasicDAO(db_name)
        dao.set_session(session)

        basics = dao.get_basics_by_conditions(
            symbol=symbol,
            night=night,
            type_filter=type_filter,
            exchange=exchange
        )
        results = [basic.to_dict() for basic in basics]

    return results


if __name__ == '__main__':
    # Example usage
    print("=" * 60)
    print("BasicDAO Examples")
    print("=" * 60)

    # Using DAO directly
    dao = BasicDAO('future_sqlite')

    try:
        # 1. Get all basics (deleted=0)
        print("\n1. All basics (deleted=0):")
        all_basics = dao.get_all_basic()
        print(f"   Count: {len(all_basics)}")
        for basic in all_basics[:5]:
            print(f"   - {basic.symbol}: {basic.name} (night={basic.night})")

        # 2. Get by symbol
        print("\n2. Get by symbol 'A':")
        basic_a = dao.get_basic_by_symbol('A')
        if basic_a:
            print(f"   {basic_a.to_dict()}")
        else:
            print("   Not found")

        # 3. Night trading products
        print("\n3. Night trading products (night=1):")
        night_products = dao.get_night_trading_basics()
        print(f"   Count: {len(night_products)}")

        # 4. Day-only products
        print("\n4. Day-only products (night=0):")
        day_products = dao.get_day_trading_basics()
        print(f"   Count: {len(day_products)}")

        # 5. Flexible query
        print("\n5. Flexible queries:")
        filtered = dao.get_basics_by_conditions(night=1)
        print(f"   Night trading: {len(filtered)}")

        filtered = dao.get_basics_by_conditions(exchange='SHFE')
        print(f"   SHFE exchange: {len(filtered)}")

        # 6. Count
        print("\n6. Count operations:")
        total = dao.count_by_conditions()
        print(f"   Total count: {total}")

        night_count = dao.count_by_conditions(night=1)
        print(f"   Night trading count: {night_count}")

        # 7. Check existence
        print("\n7. Check existence:")
        exists = dao.exists('A')
        print(f"   Symbol 'A' exists: {exists}")

    finally:
        dao.close()

    # Using context manager (recommended)
    print("\n8. Using context manager:")
    results = query_basics_with_context(night=1)
    print(f"   Results: {len(results)} records")
