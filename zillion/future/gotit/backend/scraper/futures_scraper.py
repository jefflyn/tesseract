"""
Data Scraper using akshare
"""
import akshare as ak
import pandas as pd
from datetime import datetime
from dao.database import db_manager
from typing import List, Dict
import time


class FuturesScraper:
    def __init__(self):
        self.db = db_manager

    def fetch_basic_info(self) -> List[Dict]:
        """Fetch all futures basic information from Sina"""
        try:
            df = ak.futures_display_main_sina()

            basics = []
            for _, row in df.iterrows():
                symbol = str(row['代码'])
                basic = {
                    'symbol': symbol[:4] if len(symbol) >= 4 else symbol,
                    'name': row['名称'],
                    'type': '',
                    'amount': 0,
                    'unit': '',
                    'step': 0.00,
                    'profit': 0,
                    'limit': -1,
                    'exchange': row['交易所'] if '交易所' in row.index else '',
                    'night': -1,
                    'deleted': 0,
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                basics.append(basic)

            self._save_basics(basics)
            return basics

        except Exception as e:
            print(f"Error fetching basic info: {e}")
            raise

    def _save_basics(self, basics: List[Dict]):
        """Save basic info to database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        for basic in basics:
            cursor.execute('''
                INSERT OR REPLACE INTO basic 
                (symbol, name, type, amount, unit, step, profit, limit, exchange, night, deleted, update_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                basic['symbol'], basic['name'], basic['type'], basic['amount'],
                basic['unit'], basic['step'], basic['profit'], basic['limit'],
                basic['exchange'], basic['night'], basic['deleted'], basic['update_time']
            ))

        conn.commit()
        conn.close()

    def fetch_main_contracts(self) -> List[Dict]:
        """Fetch current main contracts"""
        try:
            df = ak.futures_main_sina()

            contracts = []
            for _, row in df.iterrows():
                code = str(row['代码'])
                contract = {
                    'symbol': code[:4] if len(code) >= 4 else code,
                    'code': code,
                    'ts_code': f"{code}.SHF",
                    'main': 1,
                    'limit': None,
                    'low': float(row['最低']) if '最低' in row.index and pd.notna(row['最低']) else 0.0,
                    'high': float(row['最高']) if '最高' in row.index and pd.notna(row['最高']) else 0.0,
                    'low_time': None,
                    'high_time': None,
                    'h_low': None,
                    'h_high': None,
                    'h_low_time': None,
                    'h_high_time': None,
                    'selected': 0,
                    'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'deleted': 0
                }
                contracts.append(contract)

            self._save_contracts(contracts)
            return contracts

        except Exception as e:
            print(f"Error fetching main contracts: {e}")
            raise

    def _save_contracts(self, contracts: List[Dict]):
        """Save contracts to database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        for contract in contracts:
            cursor.execute('''
                INSERT OR REPLACE INTO contract 
                (symbol, code, ts_code, main, limit, low, high, low_time, high_time,
                 h_low, h_high, h_low_time, h_high_time, selected, create_time, update_time, deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                contract['symbol'], contract['code'], contract['ts_code'], contract['main'],
                contract['limit'], contract['low'], contract['high'], contract['low_time'],
                contract['high_time'], contract['h_low'], contract['h_high'],
                contract['h_low_time'], contract['h_high_time'], contract['selected'],
                contract['create_time'], contract['update_time'], contract['deleted']
            ))

        conn.commit()
        conn.close()

    def fetch_daily_data(self, symbol: str, start_date: str = None) -> List[Dict]:
        """Fetch daily trade data for a specific contract"""
        try:
            if start_date is None:
                start_date = "20200101"

            df = ak.futures_zh_daily_sina(symbol=symbol, start_date=start_date)

            daily_data = []
            for _, row in df.iterrows():
                data = {
                    'symbol': symbol[:6],
                    'trade_date': str(row['date']) if 'date' in row.index else None,
                    'code': symbol,
                    'open': float(row['open']) if 'open' in row.index and pd.notna(row['open']) else None,
                    'high': float(row['high']) if 'high' in row.index and pd.notna(row['high']) else None,
                    'low': float(row['low']) if 'low' in row.index and pd.notna(row['low']) else None,
                    'close': float(row['close']) if 'close' in row.index and pd.notna(row['close']) else None,
                    'settle': None,
                    'pre_close': None,
                    'pre_settle': None,
                    'close_change': None,
                    'settle_change': None,
                    'deal_vol': int(row['volume']) if 'volume' in row.index and pd.notna(row['volume']) else None,
                    'hold_vol': None,
                    'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                daily_data.append(data)

            self._save_daily_data(daily_data)
            return daily_data

        except Exception as e:
            print(f"Error fetching daily data for {symbol}: {e}")
            raise

    def _save_daily_data(self, daily_data: List[Dict]):
        """Save daily data to database"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        for data in daily_data:
            cursor.execute('''
                INSERT OR REPLACE INTO trade_daily 
                (symbol, trade_date, code, open, high, low, close, settle, pre_close,
                 pre_settle, close_change, settle_change, deal_vol, hold_vol, create_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['symbol'], data['trade_date'], data['code'], data['open'],
                data['high'], data['low'], data['close'], data['settle'],
                data['pre_close'], data['pre_settle'], data['close_change'],
                data['settle_change'], data['deal_vol'], data['hold_vol'],
                data['create_time']
            ))

        conn.commit()
        conn.close()

    def fetch_all_main_contracts_daily(self):
        """Fetch daily data for all main contracts"""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT DISTINCT code FROM contract WHERE main = 1 AND deleted = 0')
        contracts = [row['code'] for row in cursor.fetchall()]
        conn.close()

        results = []
        for contract in contracts:
            try:
                data = self.fetch_daily_data(contract)
                results.append({'contract': contract, 'records': len(data)})
                print(f"✓ Updated {contract}: {len(data)} records")
                time.sleep(1)  # Be respectful to the API
            except Exception as e:
                print(f"✗ Failed to fetch data for {contract}: {e}")
                results.append({'contract': contract, 'error': str(e)})

        return results
