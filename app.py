import os
from flask import Flask, render_template, request
from data import GoogleSpread
from datetime import datetime

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/bc", methods=['GET', 'POST'])
def bodega_central():

    option_list = []
    if request.method == 'GET':
        google_spread = GoogleSpread(sheet="siscoin_data")
        option_list = google_spread.get_option_list()

    if request.method == 'POST':

        google_spread = GoogleSpread(sheet="siscoin_data", worksheet="Bodega Central")
        option_list = google_spread.get_option_list()

        now = datetime.now() # current date and time
        date_time = [now.strftime("%d/%m/%Y %H:%M:%S")]

        formheader = google_spread.process_form_header(request.form['formheaderdata'].split(","))
        formtable = google_spread.process_form_table(request.form['formtabledata'])

        for row in formtable:
            record = date_time + formheader + row
            google_spread.append(record)

    return render_template('form_bc.html', option_list=option_list)


@app.route("/bp", methods=['GET', 'POST'])
def bodega_periferica():

    option_list = []
    if request.method == 'GET':
        google_spread = GoogleSpread(sheet="siscoin_data")
        option_list = google_spread.get_option_list()

    if request.method == 'POST':

        google_spread = GoogleSpread(sheet="siscoin_data", worksheet="Bodega Periferica")
        option_list = google_spread.get_option_list()

        now = datetime.now() # current date and time
        date_time = [now.strftime("%d/%m/%Y %H:%M:%S")]

        formheader = google_spread.process_form_header(request.form['formheaderdata'].split(","))
        formtable = google_spread.process_form_table(request.form['formtabledata'])

        for row in formtable:
            record = date_time + formheader + row
            google_spread.append(record)

    return render_template('form_bp.html', option_list=option_list)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
