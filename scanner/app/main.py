import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import logging
from datetime import datetime
# Use absolute import for clarity when running directly
from utils.scanner import run_scan, VALID_SCAN_TYPES
from utils.scraper import process_scan_response

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure report directories exist
REPORTS_DIR = "reports"
ZAP_REPORTS_DIR = os.path.join(REPORTS_DIR, "zap")
NMAP_REPORTS_DIR = os.path.join(REPORTS_DIR, "nmap")

for directory in [REPORTS_DIR, ZAP_REPORTS_DIR, NMAP_REPORTS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

@app.route('/scan', methods=['POST'])
def scan():
    """Initiate a vulnerability scan"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    url = data.get('url')
    scan_type = data.get('scan_type')

    if not url or not scan_type:
        return jsonify({"error": "Missing 'url' or 'scan_type' in request"}), 400

    if scan_type not in VALID_SCAN_TYPES:
        return jsonify({"error": f"Invalid scan_type. Supported types: {', '.join(VALID_SCAN_TYPES)}"}), 400

    try:
        # Generate report ID upfront
        report_id = str(uuid.uuid4())

        # Define the report filename based on scan type
        if 'nmap' in scan_type:
            report_filename = f"{report_id}.xml"
            report_path = os.path.join(NMAP_REPORTS_DIR, report_filename)
        else:  # ZAP scan
            report_filename = f"{report_id}.html"
            report_path = os.path.join(ZAP_REPORTS_DIR, report_filename)

        # Run the scan with the report path directly
        report_content = run_scan(url, scan_type, report_dir=ZAP_REPORTS_DIR if 'zap' in scan_type else NMAP_REPORTS_DIR, report_filename=report_filename)

        # Save the report content for Nmap (ZAP saves via run_scan)
        if 'nmap' in scan_type:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)

        logger.info(f"Scan completed for URL: {url}, Scan Type: {scan_type}, Report ID: {report_id}")
        return jsonify({
            "message": "Scan completed",
            "report_id": report_id,
            "report_path": f"reports/{'zap' if 'zap' in scan_type else 'nmap'}/{report_filename}",
            "scan_type": scan_type
        }), 200

    except Exception as e:
        logger.error(f"Scan failed: {str(e)}")
        return jsonify({"error": f"Scan failed: {str(e)}"}), 500

@app.route('/scan-and-scrape', methods=['POST'])
def scan_and_scrape():
    """Initiate a vulnerability scan and scrape the report"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    url = data.get('url')
    scan_type = data.get('scan_type')

    if not url or not scan_type:
        return jsonify({"error": "Missing 'url' or 'scan_type' in request"}), 400

    if scan_type not in VALID_SCAN_TYPES:
        return jsonify({"error": f"Invalid scan_type. Supported types: {', '.join(VALID_SCAN_TYPES)}"}), 400

    try:
        # Generate report ID upfront
        report_id = str(uuid.uuid4())

        # Define the report filename based on scan type
        if 'nmap' in scan_type:
            report_filename = f"{report_id}.xml"
            report_path = os.path.join(NMAP_REPORTS_DIR, report_filename)
        else:  # ZAP scan
            report_filename = f"{report_id}.html"
            report_path = os.path.join(ZAP_REPORTS_DIR, report_filename)

        # Run the scan with the report directory and filename
        report_content = run_scan(url, scan_type, report_dir=ZAP_REPORTS_DIR if 'zap' in scan_type else NMAP_REPORTS_DIR, report_filename=report_filename)

        # Save the report content for Nmap (ZAP saves via run_scan)
        if 'nmap' in scan_type:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)

        # Prepare scan response for scraper
        scan_response = {
            "message": "Scan completed",
            "report_id": report_id,
            "report_path": f"reports/{'zap' if 'zap' in scan_type else 'nmap'}/{report_filename}",
            "scan_type": scan_type
        }

        # Scrape the report
        scraped_data = process_scan_response(scan_response)

        # Safeguard against None or non-dictionary responses
        if scraped_data is None or not isinstance(scraped_data, dict):
            logger.error(f"Invalid scraped data for Report ID: {report_id}, data: {scraped_data}")
            return jsonify({"error": "Failed to process scan data"}), 500

        if "error" in scraped_data:
            logger.error(f"Scraping failed for Report ID: {report_id}, error: {scraped_data['error']}")
            return jsonify({"error": scraped_data["error"]}), 500

        logger.info(f"Scan and scrape completed for URL: {url}, Scan Type: {scan_type}, Report ID: {report_id}")
        return jsonify(scraped_data), 200

    except Exception as e:
        logger.error(f"Scan and scrape failed: {str(e)}")
        return jsonify({"error": f"Scan and scrape failed: {str(e)}"}), 500

@app.route('/report/<report_id>', methods=['GET'])
def get_report(report_id):
    """Retrieve a scan report"""
    zap_report_path = os.path.join(ZAP_REPORTS_DIR, f"{report_id}.html")
    nmap_report_path = os.path.join(NMAP_REPORTS_DIR, f"{report_id}.xml")

    if os.path.exists(zap_report_path):
        return send_file(zap_report_path, mimetype='text/html')
    elif os.path.exists(nmap_report_path):
        return send_file(nmap_report_path, mimetype='application/xml')
    else:
        return jsonify({"error": "Report not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)