from pyfpdf import FPDF

class PostIt(object):
    def __init__(self, title, description, assignee = '', priority = 0, points  = 0):
        self.title = title
        self.description = description
        self.assignee = assignee 
        self.priority = priority
        self.points = points 

    @classmethod
    def load_post(klass, form):
        ids = [int(k.replace('title','')) for k in form if k.startswith('title')]
        ids.sort()
        postits = []
        for i in ids:
            i = str(i)
            title = form['title' + i]
            description = form['description' + i]
            assignee = form['assignee' + i]
            priority = form['priority' + i]
            priority = int(priority) if priority.isdigit() else 0
            points = form['points' + i]
            points = int(points) if points.isdigit() else 0
            p = klass(title, description, assignee, priority, points)
            postits.append(p)
        return postits

    @staticmethod
    def make_pdf(postits):
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font('Arial','B',16)
        for i,p in enumerate(postits):
            pdf.cell(40,10 + (i * 20), str(p))
        return pdf.output(dest='S')

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
 
