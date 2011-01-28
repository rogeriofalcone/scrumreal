from flask import render_template, url_for, Response, request
from pyfpdf import FPDF

from app import app
from scrumreal.utils import PostIt

from datetime import datetime,timedelta

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/postit', methods=['POST'])
def postit():
    if request.form['from'] and request.form['to']:
        date_from = datetime.strptime(request.form['from'], "%m/%d/%Y")
        date_to = datetime.strptime(request.form['to'], "%m/%d/%Y")
        date_diff = date_to - date_from 
        days = date_diff.days + 1
    else:
        days = 0
    postits = PostIt.load_post(request.form)
    pdf_postits = PostIt.make_pdf(postits, ref=request.form['ref'], days=days)
    response = Response(response=pdf_postits, mimetype="application/pdf")
    response.headers['Content-Disposition'] = 'filename=postits.pdf'
    return response


@app.route('/about')
def about():
    return render_template('about.html')

