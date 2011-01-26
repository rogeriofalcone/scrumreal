#-*- coding: utf-8 -*-

from pyfpdf import FPDF

class PostItReport(FPDF):
    def __init__(self, *args, **kwargs):
        self.postits = kwargs.pop('postits')
        super(PostItReport, self).__init__(*args, **kwargs)
        self.alias_nb_pages()
        self.show_postits()

    def show_postits(self):
        #FIXME problema de encoding
        #FIXME maxlength nos texto
        per_line = 2
        per_page = 6
        for i,p in enumerate(self.postits):
            if not i % 6:
                self.add_page()
            c = i % per_page
            w,h = 102, 76 
            x = (c % per_line) * 2 + 2 +  ((c % per_line) * w)
            y = (c / per_line) * 10 + 10 + ((c / per_line) * h)
            #draw border
            self.rect(x,y,w,h)
            #draw title
            self.set_font('Arial','B',13)
            self.text(x+2,y+6, p.title)
            self.set_font('Arial','',12)
            #draw line separator title content
            self.line(x,y+8,x+w,y+8)
            self.set_xy(x+2,y+10);
            self.multi_cell(98,5, p.description)
    
            #draw line separator content footer
            self.line(x,y+h-10,x+w,y+h-10)
            self.text(x + 1,y + h - 4, "assignee: %s" % p.assignee)
            #draw line separator assign priority
            priority_x = 48
            self.line(x + priority_x,y+h-10,x+priority_x,y+h)
            self.text(x + priority_x + 1,y + h - 4, "priority: %s" % p.priority)
            #draw line separator priority point 
            point_x = 78
            self.line(x + point_x,y+h-10,x+point_x,y+h)
            self.text(x + point_x + 1,y + h - 4, "points:")
            if p.points:
                self.text(x + point_x + 14,y + h - 4, str(p.points))

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.cell(0,10,'scrumreal.appspot.com - Page '+str(self.page_no())+'/{nb}',0,0,'C')


class PostIt(object):
    def __init__(self, title, description, assignee = '', priority = '', points  = 0):
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
            points = form['points' + i]
            points = int(points) if points.isdigit() else 0
            p = klass(title, description, assignee, priority, points)
            postits.append(p)
        return postits

    @staticmethod
    def make_pdf(postits):
        pdf=PostItReport(postits = postits)
        return pdf.output(dest='S')

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
 
