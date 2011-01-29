#-*- coding: utf-8 -*-

from pyfpdf import FPDF

class PostItReport(FPDF):
    REFS = {'7644':(68,74),
           '7640':(102,74),}

    def __init__(self, *args, **kwargs):
        self.postits = kwargs.pop('postits')
        self.ref = kwargs.pop('ref')
        self.days = kwargs.pop('days')
        super(PostItReport, self).__init__(*args, **kwargs)
        self.alias_nb_pages()
        self.show_postits()
        self.show_burndown()

    def text_rotate(self, x, y, angle, text):
        self.rotate(angle, x, y)
        self.text(x, y, text)
        self.rotate(0)

    def show_postits(self):
        #FIXME maxlength nos texto
        per_line = 2
        per_page = 6
        for i,p in enumerate(self.postits):
            if not i % 6:
                self.add_page()
            c = i % per_page
            w,h = PostItReport.REFS.get(self.ref,(102,74))
            sep = (210 - 2 * w) / 3
            x = (c % per_line) * sep + sep +  ((c % per_line) * w)
            y = (c / per_line) * 10 + 10 + ((c / per_line) * h)
            #draw border
            self.rect(x,y,w,h)
            #draw title
            self.set_font('Arial','B',10)
            self.text(x+2,y+6, p.title)
            self.set_font('Arial','',10)
            #draw line separator title content
            self.line(x+2,y+8,x+w-2,y+8)
            self.set_xy(x+2,y+10);
            self.multi_cell(w - 6,5, p.description)
    
            #draw line separator content footer
            footer_y = 10
            footer_text_y = (footer_y / 1.5)
            self.line(x,y+h-footer_y,x+w,y+h-footer_y)
            self.set_font('Arial','B',10)
            self.text(x + 1,y + h - footer_text_y, "assignee")
            #draw line separator assign priority
            priority_x = (w / 2) 
            self.line(x + priority_x,y+h-footer_y,x+priority_x,y+h)
            self.text(x + priority_x + 1,y + h - footer_text_y, "priority")
            #draw line separator priority point 
            point_x = (w / 1.3) 
            self.line(x + point_x,y+h-footer_y,x+point_x,y+h)
            points = str(p.points) if p.points else ""
            self.text(x + point_x + 1,y + h - footer_text_y, "points")

            #dynamic data
            self.set_font('Arial','',10)
            self.text(x + priority_x + 1,y + h - footer_text_y + 5, p.priority)
            self.text(x + 1,y + h - footer_text_y + 5, p.assignee)
            self.text(x + point_x + 1,y + h - footer_text_y + 5, points)


    def show_burndown(self):
        w, h = 190, 273
        points = sum(p.points for p in self.postits)
        days = self.days
        if not (points and days):
            return

        self.add_page()
        self.set_font('Arial','',9)
        self.set_line_width(0.6)  

        self.line(10,10,10+w,10)
        self.rotate(270, 15+w, 5)
        self.text(15+w, 5, "Points")
        self.rotate(0)

        self.line(10,10,10,10+h)
        self.rotate(270, 9, 11+h)
        self.text(9, 11+h, "Days")
        self.rotate(0)

        self.set_line_width(0.1)  
        self.set_font('Arial','',8)

        # tics points
        interval_y = 5.0
        tics_y = points / interval_y
        space = 185 / tics_y 
        for i in range(1, int(tics_y)+1):
            x = 10 + (i * space)
            self.text_rotate(x - 1, 3, 270, str(i * int(interval_y)))
            self.line(x, 9, x, 11)
            
        #tics days
        tics_x = days
        space = 270. / tics_x 
        self.set_line_width(0.1)  
        self.set_font('Arial','',8)
        for i in range(1, int(tics_x)+1):
            y = 10 + (i * space)
            self.text(5, y+1, str(i))
            self.line(9, y, 11, y)

        self.line(195, 10,10, 280)


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
    def make_pdf(postits, ref, days):
        pdf=PostItReport(postits = postits, ref = ref, days=days)
        return pdf.output(dest='S')

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
 
