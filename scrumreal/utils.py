#-*- coding: utf-8 -*-

from pyfpdf import FPDF

class PostItReport(FPDF):
    def __init__(self, *args, **kwargs):
        self.postits = kwargs.pop('postits')
        super(PostItReport, self).__init__(*args, **kwargs)
        self.alias_nb_pages()
        self.show_postits()

    def show_postits(self):
        #FIXME maxlength nos texto
        per_line = 2
        per_page = 6
        for i,p in enumerate(self.postits):
            if not i % 6:
                self.add_page()
            c = i % per_page
            w,h = 102,74
            sep = (210 - 2 * w) / 3
            x = (c % per_line) * sep + sep +  ((c % per_line) * w)
            y = (c / per_line) * 10 + 10 + ((c / per_line) * h)
            #draw border
            self.rect(x,y,w,h)
            #draw title
            self.set_font('Arial','B',13)
            self.text(x+2,y+6, p.title)
            self.set_font('Arial','',11)
            #draw line separator title content
            self.line(x,y+8,x+w,y+8)
            self.set_xy(x+2,y+10);
            self.multi_cell(98,5, p.description)
    
            #draw line separator content footer
            footer_y = 10
            footer_text_y = (footer_y / 2.7)
            self.line(x,y+h-footer_y,x+w,y+h-footer_y)
            self.text(x + 1,y + h - footer_text_y, "as: %s" % p.assignee)
            #draw line separator assign priority
            priority_x = (w / 2) 
            self.line(x + priority_x,y+h-footer_y,x+priority_x,y+h)
            self.text(x + priority_x + 1,y + h - footer_text_y, "pr: %s" % p.priority)
            #draw line separator priority point 
            point_x = (w / 1.3) 
            self.line(x + point_x,y+h-footer_y,x+point_x,y+h)
            points = str(p.points) if p.points else ""
            self.text(x + point_x + 1,y + h - footer_text_y, "pt: %s" % points)

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
 
