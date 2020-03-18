import csv
import os
from datetime import datetime
from flask import Flask, render_template, request

# When we run from command line, __name__ is "__main__"
app = Flask(__name__)

# Decorator to call this hello_word() when "/" is entered in a browser.
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()  # email = request.form['email']
    
            # Email the info to a tech support
            # OR, log to a csv file with date and time.
            # OR, send to customer support app.
            # OR, save to customer support database.
            store_contact_info(data)  # saving to a csv file.
    
            return render_template('contact_thankyou.html', email=data['email'], subject=data['subject'])
    
            # NOTE: You could do the following but you won't be able to pass
            # the form data to the template.
            # return redirect('/contact_thankyou.html')
        except:
            return "Unable to save the contact information to database."
    else:
        return "🤔😢Something went wrong!"


def store_contact_info(data_dict):
    """
    Adds the given parameters along with the current date and time to a CSV file
    for the webmaster to check periodically and respond to our website visitors
    who have requested information via our website's contact page.

    :param data_dict: A dictionary containing the email, subject, and message
    from our website's contact page.
    :return: None
    """

    CSV_FILE = "contacts_query.csv"
    COMMA = ","
    date_time = datetime.now()  # contains date & time components as a tuple

    entry = [date_time.strftime("%m/%d/%Y"), date_time.strftime("%H:%M:%S")]
    entry.extend([data_dict[k] for k in data_dict.keys()])

    # Check if file exists. If not, create the csv file with the header line.
    if not os.path.isfile(CSV_FILE):
        header = ["Date", "Time", "Email Address", "Email Subject", "Email Body"]
        with open(CSV_FILE, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
    
    with open(CSV_FILE, "a") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(entry)

# end store_contact_info():

