import math
import cairo

square_alpha = 0
terms = ['','','','']
terms_alpha = [0,0,0,0]
arrows_alpha = 0
i_alpha = 0
j_alpha = 0
face= [0,0,0,0,0,0]

def render(cr, width, height, t, line, word, text, row, column):
    global square_alpha, terms, arrows_alpha, i_alpha, j_alpha, face
    
    x = width * 0.75
    r = width * 0.08
    y = width - x + 2*r
    x = 2*r
    sr = r/15
    zy = -r / 3
    zx = 2 * r / 3

    vs = [ [ [ (x-r, y-r), (x+r, y-r) ],
             [ (x-r, y+r), (x+r, y+r) ] ],
           [ [ (x-r+zx, y-r+zy), (x+r+zx, y-r+zy) ],
             [ (x-r+zx, y+r+zy), (x+r+zx, y+r+zy) ] ],
         ]
    
    previous_lines = text[:row]
    previous_lines = '\n'.join(previous_lines).split('\n\n')[-1]
    following_lines = text[row:]
    following_lines = '\n'.join(following_lines).split('\n\n')[0]
    paragraph = previous_lines + '\n' + following_lines
            
    if 'refl≡p' in paragraph:
        square_alpha = (square_alpha + 1)/2
    else:
        square_alpha = (square_alpha + 0)/2

    cr.set_source_rgba(38/255, 139/255, 210/255, square_alpha*0.65)
    cr.set_operator(cairo.Operator.OVER)
    cr.set_line_width(sr)
    cr.move_to(*vs[1][0][0])
    cr.line_to(*vs[1][1][0])
    cr.line_to(*vs[1][1][1])
    cr.line_to(*vs[1][0][1])

    cr.line_to(*vs[0][0][1])
    cr.line_to(*vs[0][1][1])
    cr.line_to(*vs[0][1][0])
    cr.line_to(*vs[0][0][0])

    cr.line_to(*vs[1][0][0])
    cr.line_to(*vs[1][0][1])
    cr.line_to(*vs[1][1][1])
    cr.line_to(*vs[0][1][1])
    cr.line_to(*vs[0][0][1])
    cr.line_to(*vs[0][0][0])
    cr.line_to(*vs[0][1][0])
    cr.line_to(*vs[0][1][1])
    cr.line_to(*vs[0][0][1])
    cr.line_to(*vs[1][0][1])
    cr.line_to(*vs[0][0][1])
    cr.line_to(*vs[0][1][1])
    cr.line_to(*vs[0][1][0])
    cr.line_to(*vs[1][1][0])
    cr.close_path()
    
    cr.set_line_cap(cairo.LineCap.ROUND)
    cr.stroke()
    cr.set_line_cap(cairo.LineCap.BUTT)

    j = -1
    if '(filler i j)' in line:
        j = 3
    if 'i = i0' in line:
        j = 0
    if 'i = i1' in line:
        j = 1
    if 'j = i0' in line:
        j = 4
    if 'j = i1' in line:
        j = 5
    if (word == 'hcomp') or ('refl ≡ p' in line): 
        j = 2
    
    for i in range(6):
        if i == j:
            face[i] = (face[i] + 0.4)/2
        else:
            face[i] = (face[i] + 0)/2
        

    # left
    cr.set_source_rgba(38/255, 139/255, 210/255,square_alpha*face[0]) 
    cr.set_operator(cairo.Operator.ADD)
    cr.set_line_width(sr)
    cr.move_to(*vs[0][0][0])
    cr.line_to(*vs[1][0][0])
    cr.line_to(*vs[1][1][0])
    cr.line_to(*vs[0][1][0])
    cr.close_path()
    cr.fill()

    # right
    cr.set_source_rgba(38/255, 139/255, 210/255,square_alpha*face[1]) 
    cr.set_operator(cairo.Operator.ADD)
    cr.set_line_width(sr)
    cr.move_to(*vs[0][0][1])
    cr.line_to(*vs[1][0][1])
    cr.line_to(*vs[1][1][1])
    cr.line_to(*vs[0][1][1])
    cr.close_path()
    cr.fill()

    # front
    cr.set_source_rgba(38/255, 139/255, 210/255,square_alpha*face[2]) 
    cr.set_operator(cairo.Operator.ADD)
    cr.set_line_width(sr)
    cr.move_to(*vs[0][0][0])
    cr.line_to(*vs[1][0][0])
    cr.line_to(*vs[1][0][1])
    cr.line_to(*vs[0][0][1])
    cr.close_path()
    cr.fill()

    # back 
    cr.set_source_rgba(38/255, 139/255, 210/255, square_alpha*face[3])
    cr.set_operator(cairo.Operator.ADD)
    cr.set_line_width(sr)
    cr.move_to(*vs[0][1][0])
    cr.line_to(*vs[1][1][0])
    cr.line_to(*vs[1][1][1])
    cr.line_to(*vs[0][1][1])
    cr.close_path()
    cr.fill()

    # front 
    cr.set_source_rgba(38/255, 139/255, 210/255, square_alpha*face[4])
    cr.set_operator(cairo.Operator.ADD)
    cr.set_line_width(sr)
    cr.move_to(*vs[0][0][0])
    cr.line_to(*vs[0][1][0])
    cr.line_to(*vs[0][1][1])
    cr.line_to(*vs[0][0][1])
    cr.close_path()
    cr.fill()

    # top 
    cr.set_source_rgba(38/255, 139/255, 210/255, square_alpha*face[5])
    cr.set_operator(cairo.Operator.ADD)
    cr.set_line_width(sr)
    cr.move_to(*vs[1][0][0])
    cr.line_to(*vs[1][1][0])
    cr.line_to(*vs[1][1][1])
    cr.line_to(*vs[1][0][1])
    cr.close_path()
    cr.fill()

    return
