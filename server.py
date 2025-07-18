from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

# Root route → serves index.html
@app.route('/')
def home():
    return render_template('index.html')

# Dynamic route → serves any HTML page from /templates
@app.route('/<string:page_name>')
def render_static_page(page_name):
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
