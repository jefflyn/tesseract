"""
Flask API Server
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper.futures_scraper import FuturesScraper
from dao.database import db_manager
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

scraper = FuturesScraper()


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


@app.route('/api/basics', methods=['GET'])
def get_basics():
    """Get all basic futures information"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM basic WHERE deleted = 0 ORDER BY symbol')
        basics = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({'data': basics, 'total': len(basics)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/basics/fetch', methods=['POST'])
def fetch_basics():
    """Fetch basic info from external source"""
    try:
        basics = scraper.fetch_basic_info()
        return jsonify({'message': 'Success', 'count': len(basics)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contracts', methods=['GET'])
def get_contracts():
    """Get contracts with optional filters"""
    try:
        selected_only = request.args.get('selected', 'false').lower() == 'true'

        conn = db_manager.get_connection()
        cursor = conn.cursor()

        if selected_only:
            cursor.execute('SELECT * FROM contract WHERE selected = 1 AND deleted = 0 ORDER BY symbol')
        else:
            cursor.execute('SELECT * FROM contract WHERE deleted = 0 ORDER BY symbol')

        contracts = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({'data': contracts, 'total': len(contracts)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contracts/fetch', methods=['POST'])
def fetch_contracts():
    """Fetch main contracts from external source"""
    try:
        contracts = scraper.fetch_main_contracts()
        return jsonify({'message': 'Success', 'count': len(contracts)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contracts/<code>/select', methods=['POST'])
def select_contract(code):
    """Select/deselect a contract"""
    try:
        data = request.json
        selected = data.get('selected', 1)

        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE contract SET selected = ?, update_time = ?
            WHERE code = ?
        ''', (selected, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/daily-data', methods=['GET'])
def get_daily_data():
    """Get daily trade data"""
    try:
        symbol = request.args.get('symbol')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', '100'))

        conn = db_manager.get_connection()
        cursor = conn.cursor()

        query = 'SELECT * FROM trade_daily WHERE 1=1'
        params = []

        if symbol:
            query += ' AND symbol = ?'
            params.append(symbol)

        if start_date:
            query += ' AND trade_date >= ?'
            params.append(start_date)

        if end_date:
            query += ' AND trade_date <= ?'
            params.append(end_date)

        query += ' ORDER BY trade_date DESC LIMIT ?'
        params.append(limit)

        cursor.execute(query, params)
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({'data': data, 'total': len(data)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/daily-data/fetch', methods=['POST'])
def fetch_daily_data():
    """Fetch daily data for a specific contract"""
    try:
        data = request.json
        symbol = data.get('symbol')

        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400

        records = scraper.fetch_daily_data(symbol)
        return jsonify({'message': 'Success', 'count': len(records)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/daily-data/update-all', methods=['POST'])
def update_all_daily_data():
    """Update daily data for all main contracts"""
    try:
        results = scraper.fetch_all_main_contracts_daily()
        return jsonify({'message': 'Update completed', 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('BACKEND_PORT', '5000'))
    app.run(host='0.0.0.0', port=port, debug=True)
