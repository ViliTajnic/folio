from flask import Flask, render_template, request, redirect
import csv
import os
import json
from datetime import datetime

app = Flask(__name__)

COUNTER_FILE = 'visit_counts.json'
TRACKED_PAGES = ['work.html', 'oci-autonomous-terraform.html', 'sqlcl-connection-manager.html']

def increment_visit(page_name):
    counts = {}
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            counts = json.load(f)
    counts[page_name] = counts.get(page_name, 0) + 1
    counts['_last_updated'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counts, f, indent=2)

# Root route → serves index.html
@app.route('/')
def home():
    return render_template('index.html')

# Dynamic route → serves any HTML page from /templates
@app.route('/<string:page_name>')
def render_static_page(page_name):
    if page_name in TRACKED_PAGES:
        increment_visit(page_name)
    return render_template(page_name)

# Write form data to a CSV file
def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as db:
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        writer = csv.writer(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([email, subject, message])

# Handle form submission
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()
            write_to_csv(form_data)
            return redirect('/thankyou.html')
        except Exception as e:
            return f"An error occurred while saving your data: {e}", 500
    else:
        return 'Form submission method not allowed', 405

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
