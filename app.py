import sys
import logging
from flask import Flask, jsonify
from wrappers import require_x_auth
from update_database import update_database
from models import TranslationProduct, get_db_session, init_db

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO, stream= sys.stdout)
logger = logging.getLogger(__name__)

# Initialize database tables once at startup
init_db()

@app.route('/products', methods=['GET'])
def get_products():
    logger.info("Fetching products...")
    session = get_db_session()
    try:
        products = session.query(TranslationProduct).all()
        logger.info("Fetch complete.")
        return jsonify([p.to_dict() for p in products]), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/refresh', methods=['POST'])
def refresh():
    """Endpoint for Google Sheets to trigger a data update"""
    logger.info("Refreshing database...")
    try:
        update_database()
        logger.info("Refresh complete.")
        return jsonify({'status': 'success', 'message': 'Sync completed'}), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'error': str(e)}), 500