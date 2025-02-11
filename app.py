from flask import Flask, request, jsonify, send_file
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

# BELOW ROUTES ARE OF PRESCRIPTION ANALYZER
 
from prescription_Analyzer.prescription import prescription
@app.route('/brand', methods=['POST'])
def get_brand_details():
    return prescription()

from prescription_Analyzer.pharmacy_location import pharmacy_location
@app.route('/find_medical_facilities', methods=['POST'])
def find_facilities():
    return pharmacy_location()

@app.route('/get_map', methods=['GET'])
def get_map():
    return send_file("medical_facilities_map.html")





# BELOW ROUTES ARE OF CHAT BOT

from bot.bot import chat_bot
@app.route('/bot', methods=['POST'])
def ask_question():
    return chat_bot()





# BELOW ARE THE ROUTES FOR LIVE WELL MONITOR

from live_monitor.recommendations import recommendations
@app.route('/genai', methods=['POST'])
def generate_recommendations():
    return recommendations() 





# BELOW ARE THE ROUTES OF ANALYSIS

from analyze.upload import upload
@app.route('/upload_to_pinata', methods=['POST'])
def upload_file():
    return upload()

from analyze.fetch_ipfs_files import fetch_ipfs_files
@app.route('/get-ipfs-files', methods=['GET'])
def get_ipfs_files():
    return fetch_ipfs_files()

from analyze.tabular_summary import tabular_summary
@app.route('/get_summary_analysis', methods=['POST'])
def extraction():
    return tabular_summary()





# ANALYSIS SIDEBAR ROUTES

from analyze_advance.overview import overview
@app.route('/overview', methods=['GET'])
def get_overview():
    return overview()

from analyze_advance.reco import reco
@app.route('/reco', methods=['GET'])
def get_reco():
    return reco()

from analyze_advance.parameters import parameters
@app.route('/indivisual', methods=['GET'])
def get_indivisual():
    return parameters()





# BELOW ARE REPORT SIMPLIFIER ROUTES 

from Report.upload_report import upload_report
@app.route('/upload', methods=['POST'])
def upload_medical_report():
    return upload_report()

from Report.save_folder import save_folder
@app.route('/savefolder', methods=['POST'])
def save_file_to_folder():
    return save_folder()

from Report.report_bot import report_bot
@app.route('/ask', methods=['POST'])
def ask_question_to_report():
    return report_bot()




if __name__ == '__main__':
    app.run(debug=True, port=5000)