import logging
from flask import Flask, jsonify
from models import TranslationProduct, get_db_session, init_db
from update_database import update_database

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database tables once at startup
init_db()

@app.route('/langops-dashboard/products', methods=['GET'])
def get_products():
    logger.info("Fetching products...")
    session = get_db_session()
    try:
        products = session.query(TranslationProduct).all()
        return jsonify([p.to_dict() for p in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        logger.info("Fetch complete.")
        session.close()

@app.route('/langops-dashboard/refresh', methods=['POST'])
def refresh():
    """Endpoint for Google Sheets to trigger a data update"""
    logger.info("Refreshing database...")
    try:
        update_database()
        return jsonify({'status': 'success', 'message': 'Sync completed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        logger.info("Refresh complete.")

if __name__ == '__main__':
    # Used for local development only
    app.run(host="0.0.0.0", port=5000, debug=True)