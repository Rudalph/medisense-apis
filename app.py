# app.py
from flask import Flask, render_template
from data_processor import process_sample_data

app = Flask(__name__)

@app.route('/')
def index():
    # Get data from data_processor
    data = process_sample_data()
    # Pass the data to the template
    return render_template('index.html', 
                         average_age=round(data['average_age'], 1),
                         total_records=data['total_records'],
                         cities=data['cities'])

if __name__ == '__main__':
    app.run(debug=True)

# data_processor.py remains the same as before