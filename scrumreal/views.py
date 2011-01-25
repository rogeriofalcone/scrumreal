from flask import render_template, url_for, Response
from pyfpdf import FPDF

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.cell(40,10,'Hello World!')
    response = Response(response=pdf.output(dest='S'), mimetype="application/pdf")
    response.headers['Content-Disposition'] = 'filename=postits.pdf'
    return response
