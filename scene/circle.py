import math
import cairo

loop_alpha = 0
base_alpha = 0

def render(cr, width, height, t, line, word):
    global base_alpha, loop_alpha

    x = width * 0.80
    r = width * 0.10
    y = width - x
    sr = r/10
        
    if line.startswith('f '):
        if word == 'base':
            base_alpha = (base_alpha + 1)/2
        else:
            base_alpha = (base_alpha + 0.7)/2
        
        if word == 'loop':
            loop_alpha = (loop_alpha + 1)/2
        else:
            loop_alpha = (loop_alpha + 0.7)/2
    else:
        loop_alpha = (loop_alpha + 0)/2
        base_alpha = (base_alpha + 0)/2

    cr.set_source_rgba(38/255, 139/255, 210/255, loop_alpha)
    cr.set_operator(cairo.Operator.OVER)
    cr.set_line_width(sr)
    cr.move_to(x+r,y)
    cr.arc(x, y, r, 0, 2*math.pi)
    cr.stroke()

    cr.set_source_rgba(38/255, 139/255, 210/255, base_alpha)
    cr.set_operator(cairo.Operator.OVER)
    cr.set_line_width(1)
    cr.move_to(x+r,y+r)
    cr.arc(x, y+r, 2*sr, 0, 2*math.pi)
    cr.fill()
     
