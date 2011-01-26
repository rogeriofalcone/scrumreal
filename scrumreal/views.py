from flask import render_template, url_for, Response, request

from pyfpdf import FPDF

from app import app
from scrumreal.utils import PostIt

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/postit', methods=['POST'])
def postit():
    postits = PostIt.load_post(request.form)
    pdf_postits = PostIt.make_pdf(postits, ref=request.form['ref'])
    response = Response(response=pdf_postits, mimetype="application/pdf")
    response.headers['Content-Disposition'] = 'filename=postits.pdf'
    return response


@app.route('/about')
def about():
    return render_template('about.html')

