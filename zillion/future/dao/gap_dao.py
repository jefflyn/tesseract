"""
DAO for gap_tactics table
Supports both MySQL and SQLite databases
"""
from typing import List, Optional, Dict
from sqlalchemy import Column, String, Integer, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from zillion.db.multi_db import get_session, get_scoped_session

Base = declarative_base()


class GapTacticsModel(Base):
    """SQLAlchemy model for gap_tactics table"""
    __tablename__ = 'gap_tactics'

    symbol = Column(String(4), primary_key=True, nullable=False)
    name = Column(String(16), nullable=False)
    change = Column(DECIMAL(6, 2), default=0.5, nullable=False)
    up_tactic = Column(String(16))
    down_tactic = Column(String(16))
    gap_type = Column(String(16))
    industry = Column(String(8))
    action = Column(String(32))
    top10 = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<GapTactics(symbol={self.symbol}, name={self.name}, gap_type={self.gap_type})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'symbol': self.symbol,
            'name': self.name,
            'change': float(self.change) if self.change else 0.5,
            'up_tactic': self.up_tactic,
            'down_tactic': self.down_tactic,
            'gap_type': self.gap_type,
            'industry': self.industry,
            'action': self.action,
            'top10': self.top10
        }


class GapTacticsDAO:
    """
    DAO for gap_tactics table
    Provides methods to query gap tactics data
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

    # ==================== Query Methods ====================

    def get_all_gap_tactics_as_map(self) -> Dict[str, GapTacticsModel]:
        """
        Get all gap_tactics records and return as a dictionary keyed by symbol

        Returns:
            Dictionary mapping symbol to GapTacticsModel objects
        """
        session = self._get_session()
        results = session.query(GapTacticsModel).all()
        return {record.symbol: record for record in results}

    def close(self):
        """Close the session"""
        if self.session is not None:
            if hasattr(self.session, 'remove'):
                self.session.remove()
            else:
                self.session.close()
            self.session = None


if __name__ == '__main__':
    # Example usage
    print("=" * 60)
    print("GapTacticsDAO Example")
    print("=" * 60)

    dao = GapTacticsDAO('future_sqlite')

    try:
        # Get all gap tactics as map
        print("\nAll gap tactics:")
        gap_map = dao.get_all_gap_tactics_as_map()
        print(f"Count: {len(gap_map)}")

        for symbol, tactics in list(gap_map.items())[:5]:
            print(f"  - {symbol}: {tactics.name} (gap_type={tactics.gap_type}, action={tactics.action})")

    finally:
        dao.close()
