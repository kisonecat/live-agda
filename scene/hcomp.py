import math
import cairo

square_alpha = 0
terms = ['','','','']
terms_alpha = [0,0,0,0]
arrows_alpha = 0
i_alpha = 0
j_alpha = 0

def render(cr, width, height, t, line, word, text, row, column):
    global square_alpha, terms, arrows_alpha, i_alpha, j_alpha
    
    x = width * 0.75
    r = width * 0.08
    y = width - x + 2*r
    sr = r/15

    previous_lines = text[:row]
    previous_lines = '\n'.join(previous_lines).split('\n\n')[-1]

    following_lines = text[row:]
    following_lines = '\n'.join(following_lines).split('\n\n')[0]
    paragraph = previous_lines + '\n' + following_lines
            
    if line[1:6] == ' i j ':
        arrows_alpha = (arrows_alpha + 0.6)/2
    else:
        arrows_alpha = (arrows_alpha + 0)/2
        
    if ('hcomp' in line or 'hcomp' in previous_lines) and not 'filler' in line and not 'refl≡p' in paragraph:
        square_alpha = (square_alpha + 1)/2
    else:
        square_alpha = (square_alpha + 0)/2

    words = line.split(' ')
    if 'hcomp' in previous_lines:
        j = -1
        if 'i = i0' in line and column >= 14:
            j = 0
        if 'i = i1' in line:
            j = 1 
        if 'p i' in line:
            j = 2
        if word == 'hcomp':
            j = 3
            
        for i in range(len(terms_alpha)):
            if i == j:
                terms_alpha[i] = (terms_alpha[i] + 0.5)/2
            else:
                terms_alpha[i] = (terms_alpha[i] + 0)/2
    else:
        for i in range(len(terms_alpha)):
            terms_alpha[i] = (terms_alpha[i] + 0)/2

    for l in paragraph.split('\n'):
        if '(i = i0)' in l:
            terms[0] = l.split(' → ')[-1]
        if '(i = i1)' in l:
            terms[1] = l.split(' → ')[-1].replace(' j','')
        if '(p i)' in paragraph:
            terms[2] = 'p'

    terms[3] = ''
    if word == 'hcomp':
        terms[3] = 'hcomp'
        
    cr.set_source_rgba(38/255, 139/255, 210/255, square_alpha) 
    cr.set_operator(cairo.Operator.OVER)
    cr.set_line_width(sr)
    cr.move_to(x-r,y-r)
    cr.line_to(x-r, y+r)
    cr.line_to(x+r,y+r)
    cr.line_to(x+r, y-r)
    #cr.close_path()
    cr.stroke()

    cr.set_line_width(2*sr)

    cr.set_source_rgba(38/255, 139/255, 210/255, 2*terms_alpha[0]*square_alpha) 
    cr.set_operator(cairo.Operator.ADD)
    cr.move_to(x-r,y+r)
    cr.line_to(x-r, y-r)
    cr.close_path()
    cr.stroke()

    cr.set_source_rgba(38/255, 139/255, 210/255, 2*terms_alpha[1]*square_alpha) 
    cr.set_operator(cairo.Operator.ADD)
    cr.move_to(x+r,y+r)
    cr.line_to(x+r, y-r)
    cr.close_path()
    cr.stroke()

    cr.set_source_rgba(38/255, 139/255, 210/255, 2*terms_alpha[2] *square_alpha)
    cr.set_operator(cairo.Operator.ADD)
    cr.move_to(x-r,y+r)
    cr.line_to(x+r, y+r)
    cr.close_path()
    cr.stroke()

    cr.set_source_rgba(38/255, 139/255, 210/255, 2*terms_alpha[3]*square_alpha) 
    cr.set_operator(cairo.Operator.ADD)
    cr.move_to(x-r,y-r)
    cr.line_to(x+r, y-r)
    cr.close_path()
    cr.stroke()
    
    cr.select_font_face("DejaVu Sans Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(height/24)

    if len(terms) >= 1:
        extents = cr.text_extents(terms[0])
        cr.set_source_rgba(1.1*38/255, 1.1*139/255, 1.1*210/255, square_alpha * (0.5 + terms_alpha[0]))
        cr.move_to(x - r - extents.x_advance - 2*sr, y)
        cr.show_text(terms[0])

    if len(terms) >= 2:
        cr.set_source_rgba(1.1*38/255, 1.1*139/255, 1.1*210/255, square_alpha * (0.5 + terms_alpha[1]))
        cr.move_to(x+r + 2*sr, y)
        cr.show_text(terms[1])

    if len(terms) >= 3:
        cr.set_source_rgba(1.1*38/255, 1.1*139/255, 1.1*210/255, square_alpha * (0.5 + terms_alpha[2]))
        extents = cr.text_extents(terms[2])
        cr.move_to(x - extents.x_advance / 2, y+r+2*sr+height/24)
        cr.show_text(terms[2])

    if len(terms) >= 4:
        cr.set_source_rgba(1.1*38/255, 1.1*139/255, 1.1*210/255, square_alpha * terms_alpha[3] * 1.0 / 0.5)
        extents = cr.text_extents(terms[3])
        cr.move_to(x - extents.x_advance / 2, y-r-3*sr)
        cr.show_text(terms[3])

    cr.set_source_rgba(203/255, 75/255, 22/255, arrows_alpha)

    ax = x - r * 1.5 
    ay = y + r * 1.5
    d = r / 2.1
    head = d / 5
    
    cr.set_source_rgba(203/255, 75/255, 22/255, square_alpha * (i_alpha + arrows_alpha))

    cr.set_line_width(sr)
    cr.move_to(ax,ay)
    cr.line_to(ax+d,ay)
    cr.move_to(ax+d-head,ay+head)
    cr.line_to(ax+d,ay)
    cr.line_to(ax+d-head,ay-head)
    cr.stroke()

    cr.move_to(ax+d/2, ay+height/24+head)
    cr.show_text('i')

    cr.set_source_rgba(203/255, 75/255, 22/255, square_alpha * (j_alpha + arrows_alpha))

    cr.set_line_width(sr)
    cr.move_to(ax,ay)
    cr.line_to(ax,ay-d)
    cr.move_to(ax-head,ay-d+head)
    cr.line_to(ax,ay-d)
    cr.line_to(ax+head,ay-d+head)
    cr.stroke()
    
    cr.move_to(ax - height/24, ay-d/2)
    cr.show_text('j')
