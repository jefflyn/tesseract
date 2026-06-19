"""
DAO for contract table with automatic deleted=0 filtering
Supports both MySQL and SQLite databases
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Integer, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base
from zillion.db.multi_db import get_session, get_scoped_session

Base = declarative_base()


class ContractModel(Base):
    """SQLAlchemy model for contract table"""
    __tablename__ = 'contract'

    symbol = Column(String(4), nullable=False)
    code = Column(String(8), primary_key=True, nullable=False)
    main = Column(Integer, default=1)
    limit = Column(Integer, default=None)
    low = Column(DECIMAL(10, 2), nullable=False)
    high = Column(DECIMAL(10, 2), nullable=False)
    low_time = Column(String(20), default=None)
    high_time = Column(String(20), default=None)
    h_low = Column(DECIMAL(10, 2), default=None)
    h_high = Column(DECIMAL(10, 2), default=None)
    h_low_time = Column(String(20), default=None)
    h_high_time = Column(String(20), default=None)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False, default=datetime.now)
    deleted = Column(Integer, default=0)

    def __repr__(self):
        return f"<Contract(symbol={self.symbol}, code={self.code}, main={self.main})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'symbol': self.symbol,
            'code': self.code,
            'main': self.main,
            'limit': self.limit,
            'low': float(self.low) if self.low else 0.0,
            'high': float(self.high) if self.high else 0.0,
            'low_time': self.low_time,
            'high_time': self.high_time,
            'h_low': float(self.h_low) if self.h_low else None,
            'h_high': float(self.h_high) if self.h_high else None,
            'h_low_time': self.h_low_time,
            'h_high_time': self.h_high_time,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None,
            'deleted': self.deleted
        }


class ContractDAO:
    """
    DAO for contract table

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

    def get_all_contracts(self) -> List[ContractModel]:
        """
        Get all contract records where deleted=0

        Returns:
            List of ContractModel objects
        """
        session = self._get_session()
        return session.query(ContractModel).filter(ContractModel.deleted == 0).all()

    def get_all_contracts_as_map(self) -> dict[str, ContractModel]:
        """
        Get all contract records where deleted=0 and return as a dictionary keyed by code

        Returns:
            Dictionary mapping code to ContractModel objects
        """
        session = self._get_session()
        results = session.query(ContractModel).filter(ContractModel.deleted == 0).all()
        return {record.code: record for record in results}

    def get_all_contracts_as_df(self):
        """
        Get all contract records where deleted=0 and return as a DataFrame

        Returns:
            pandas DataFrame containing all contract records
        """
        session = self._get_session()
        results = session.query(ContractModel).filter(ContractModel.deleted == 0).all()

        import pandas as pd
        if not results:
            return pd.DataFrame()

        data = [{
            'symbol': r.symbol,
            'code': r.code,
            'main': r.main,
            'limit': r.limit,
            'low': float(r.low) if r.low else 0.0,
            'high': float(r.high) if r.high else 0.0,
            'low_time': r.low_time,
            'high_time': r.high_time,
            'h_low': float(r.h_low) if r.h_low else None,
            'h_high': float(r.h_high) if r.h_high else None,
            'h_low_time': r.h_low_time,
            'h_high_time': r.h_high_time,
            'create_time': r.create_time.strftime('%Y-%m-%d %H:%M:%S') if r.create_time else None,
            'update_time': r.update_time.strftime('%Y-%m-%d %H:%M:%S') if r.update_time else None,
            'deleted': r.deleted
        } for r in results]

        return pd.DataFrame(data)


    def get_contract_by_code(self, code: str) -> Optional[ContractModel]:
        """
        Get a single contract record by code where deleted=0

        Args:
            code: Contract code to search for

        Returns:
            ContractModel object or None
        """
        session = self._get_session()
        return session.query(ContractModel).filter(
            ContractModel.code == code,
            ContractModel.deleted == 0
        ).first()

    def get_contracts_by_symbol(self, symbol: str) -> List[ContractModel]:
        """
        Get all contracts by symbol where deleted=0

        Args:
            symbol: Symbol to filter by

        Returns:
            List of ContractModel objects
        """
        session = self._get_session()
        return session.query(ContractModel).filter(
            ContractModel.symbol == symbol,
            ContractModel.deleted == 0
        ).all()

    def get_main_contracts(self) -> List[ContractModel]:
        """
        Get all main contracts (main=1, deleted=0)

        Returns:
            List of ContractModel objects
        """
        session = self._get_session()
        return session.query(ContractModel).filter(
            ContractModel.deleted == 0,
            ContractModel.main == 1
        ).all()

    def get_contracts_by_conditions(
        self,
        symbol: Optional[str] = None,
        main: Optional[int] = None
    ) -> List[ContractModel]:
        """
        Query contract records with flexible conditions (always filters deleted=0)

        Args:
            symbol: Filter by symbol
            main: Filter by main contract flag (0=no, 1=yes)

        Returns:
            List of ContractModel objects matching the conditions
        """
        session = self._get_session()
        query = session.query(ContractModel).filter(ContractModel.deleted == 0)

        if symbol is not None:
            query = query.filter(ContractModel.symbol == symbol)

        if main is not None:
            query = query.filter(ContractModel.main == main)

        return query.all()

    def count_by_conditions(
        self,
        symbol: Optional[str] = None,
        main: Optional[int] = None
    ) -> int:
        """
        Count records matching the given conditions (always filters deleted=0)

        Args:
            symbol: Filter by symbol
            main: Filter by main contract flag

        Returns:
            Count of matching records
        """
        session = self._get_session()
        query = session.query(ContractModel).filter(ContractModel.deleted == 0)

        if symbol is not None:
            query = query.filter(ContractModel.symbol == symbol)

        if main is not None:
            query = query.filter(ContractModel.main == main)

        return query.count()

    def exists(self, code: str) -> bool:
        """
        Check if a contract record exists (only checks non-deleted records)

        Args:
            code: Contract code to check

        Returns:
            True if exists and not deleted, False otherwise
        """
        session = self._get_session()
        count = session.query(ContractModel).filter(
            ContractModel.code == code,
            ContractModel.deleted == 0
        ).count()
        return count > 0

    def get_lowest_price_contract(self, symbol: str) -> Optional[ContractModel]:
        """
        Get contract with lowest price for a symbol (deleted=0)

        Args:
            symbol: Symbol to search

        Returns:
            ContractModel with lowest price or None
        """
        session = self._get_session()
        return session.query(ContractModel).filter(
            ContractModel.symbol == symbol,
            ContractModel.deleted == 0
        ).order_by(ContractModel.low.asc()).first()

    def get_highest_price_contract(self, symbol: str) -> Optional[ContractModel]:
        """
        Get contract with highest price for a symbol (deleted=0)

        Args:
            symbol: Symbol to search

        Returns:
            ContractModel with highest price or None
        """
        session = self._get_session()
        return session.query(ContractModel).filter(
            ContractModel.symbol == symbol,
            ContractModel.deleted == 0
        ).order_by(ContractModel.high.desc()).first()

    # ==================== Insert/Update/Delete Methods ====================

    def insert_contract(self, contract_data: dict) -> bool:
        """
        Insert a new contract record (automatically sets deleted=0)

        Args:
            contract_data: Dictionary containing contract record data

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            # Ensure deleted is set to 0 and timestamps are set
            if 'deleted' not in contract_data:
                contract_data['deleted'] = 0

            if 'create_time' not in contract_data:
                contract_data['create_time'] = datetime.now()

            if 'update_time' not in contract_data:
                contract_data['update_time'] = datetime.now()

            contract = ContractModel(**contract_data)
            session.add(contract)
            session.commit()
            return True
        except Exception as e:
            print(f"Insert error: {e}")
            session.rollback()
            return False

    def insert_many(self, contracts_list: List[dict]) -> int:
        """
        Insert multiple contract records

        Args:
            contracts_list: List of dictionaries containing contract record data

        Returns:
            Number of successfully inserted records
        """
        session = self._get_session()
        count = 0
        try:
            now = datetime.now()
            for contract_data in contracts_list:
                if 'deleted' not in contract_data:
                    contract_data['deleted'] = 0
                if 'create_time' not in contract_data:
                    contract_data['create_time'] = now
                if 'update_time' not in contract_data:
                    contract_data['update_time'] = now

                contract = ContractModel(**contract_data)
                session.add(contract)
                count += 1
            session.commit()
            return count
        except Exception as e:
            print(f"Batch insert error: {e}")
            session.rollback()
            return 0

    def update_contract(self, code: str, updates: dict) -> bool:
        """
        Update an existing contract record

        Args:
            code: Contract code to update
            updates: Dictionary of fields to update

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            contract = session.query(ContractModel).filter(
                ContractModel.code == code,
                ContractModel.deleted == 0
            ).first()

            if contract:
                # Auto-update update_time
                updates['update_time'] = datetime.now()

                for key, value in updates.items():
                    if hasattr(contract, key) and key not in ['code', 'create_time']:
                        setattr(contract, key, value)
                session.commit()
                return True
            return False
        except Exception as e:
            print(f"Update error: {e}")
            session.rollback()
            return False

    def update_contract_prices(
        self,
        code: str,
        low: Optional[float] = None,
        high: Optional[float] = None,
        low_time: Optional[str] = None,
        high_time: Optional[str] = None
    ) -> bool:
        """
        Update contract price information

        Args:
            code: Contract code
            low: New low price
            high: New high price
            low_time: Time when low price occurred
            high_time: Time when high price occurred

        Returns:
            True if successful, False otherwise
        """
        updates = {}
        if low is not None:
            updates['low'] = low
        if high is not None:
            updates['high'] = high
        if low_time is not None:
            updates['low_time'] = low_time
        if high_time is not None:
            updates['high_time'] = high_time

        return self.update_contract(code, updates)

    def delete_contract(self, code: str, soft_delete: bool = True) -> bool:
        """
        Delete a contract record (soft delete by default)

        Args:
            code: Contract code to delete
            soft_delete: If True, set deleted=1; if False, actually delete

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            contract = session.query(ContractModel).filter(
                ContractModel.code == code
            ).first()

            if contract:
                if soft_delete:
                    contract.deleted = 1
                    contract.update_time = datetime.now()
                    session.commit()
                else:
                    session.delete(contract)
                    session.commit()
                return True
            return False
        except Exception as e:
            print(f"Delete error: {e}")
            session.rollback()
            return False

    def restore_contract(self, code: str) -> bool:
        """
        Restore a soft-deleted record (set deleted=0)

        Args:
            code: Contract code to restore

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            contract = session.query(ContractModel).filter(
                ContractModel.code == code,
                ContractModel.deleted == 1
            ).first()

            if contract:
                contract.deleted = 0
                contract.update_time = datetime.now()
                session.flush()
                return True
            return False
        except Exception as e:
            print(f"Restore error: {e}")
            session.rollback()
            return False

    def set_main_contract(self, symbol: str, code: str) -> bool:
        """
        Set a contract as the main contract for its symbol
        (Unsets other main contracts for the same symbol)

        Args:
            symbol: Symbol
            code: Contract code to set as main

        Returns:
            True if successful, False otherwise
        """
        session = self._get_session()
        try:
            # First, unset all main contracts for this symbol
            session.query(ContractModel).filter(
                ContractModel.symbol == symbol,
                ContractModel.main == 1,
                ContractModel.deleted == 0
            ).update({'main': 0, 'update_time': datetime.now()})

            # Then set the specified contract as main
            contract = session.query(ContractModel).filter(
                ContractModel.code == code,
                ContractModel.deleted == 0
            ).first()

            if contract:
                contract.main = 1
                contract.update_time = datetime.now()
                session.flush()
                return True
            return False
        except Exception as e:
            print(f"Set main contract error: {e}")
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

def query_contracts_with_context(
    symbol: Optional[str] = None,
    main: Optional[int] = None,
    db_name: str = 'future_sqlite'
) -> List[dict]:
    """
    Query contracts using context manager (recommended for simple queries)

    Args:
        symbol: Filter by symbol
        main: Filter by main contract flag
        db_name: Database name

    Returns:
        List of dictionaries
    """
    results = []
    with get_session(db_name) as session:
        dao = ContractDAO(db_name)
        dao.set_session(session)

        contracts = dao.get_contracts_by_conditions(symbol=symbol, main=main)
        results = [contract.to_dict() for contract in contracts]

    return results


if __name__ == '__main__':
    # Example usage
    print("=" * 70)
    print("ContractDAO Examples")
    print("=" * 70)

    # Using DAO directly
    dao = ContractDAO('future_sqlite')

    try:
        # 1. Get all contracts (deleted=0)
        print("\n1. All contracts (deleted=0):")
        all_contracts = dao.get_all_contracts()
        print(f"   Count: {len(all_contracts)}")
        for contract in all_contracts[:5]:
            print(f"   - {contract.code}: {contract.symbol} (main={contract.main})")

        # 2. Get by code
        print("\n2. Get by code:")
        if all_contracts:
            first_code = all_contracts[0].code
            contract = dao.get_contract_by_code(first_code)
            if contract:
                print(f"   {contract.to_dict()}")
            else:
                print("   Not found")

        # 3. Get by symbol
        print("\n3. Get by symbol:")
        if all_contracts:
            first_symbol = all_contracts[0].symbol
            contracts = dao.get_contracts_by_symbol(first_symbol)
            print(f"   Symbol '{first_symbol}' has {len(contracts)} contracts")

        # 4. Main contracts
        print("\n4. Main contracts (main=1):")
        main_contracts = dao.get_main_contracts()
        print(f"   Count: {len(main_contracts)}")

        # 5. Flexible query
        print("\n5. Flexible queries:")
        filtered = dao.get_contracts_by_conditions(main=1)
        print(f"   Main contracts: {len(filtered)}")

        # 6. Count
        print("\n6. Count operations:")
        total = dao.count_by_conditions()
        print(f"   Total count: {total}")

        # 7. Check existence
        print("\n7. Check existence:")
        if all_contracts:
            exists = dao.exists(all_contracts[0].code)
            print(f"   Contract '{all_contracts[0].code}' exists: {exists}")

    finally:
        dao.close()

    # Using context manager (recommended)
    print("\n8. Using context manager:")
    results = query_contracts_with_context(main=1)
    print(f"   Results: {len(results)} records")