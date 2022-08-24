import math
import cairo

loop_alpha = {'p': 0, 'q':0}
base_alpha = {'p': 0, 'q':0}

def render(cr, width, height, t, line, word, matcher, direction):
    global base_alpha, loop_alpha

    x = width * 0.80
    r = width * 0.10
    y = width - x
    sr = r/10
        
    if line.startswith(matcher + ' i') or line.startswith(matcher + ' =') or line.startswith(matcher + ' :'):

        loop_alpha[matcher] = (loop_alpha[matcher] + 1)/2
        base_alpha[matcher] = (base_alpha[matcher] + 1)/2
    else:
        loop_alpha[matcher] = (loop_alpha[matcher] + 0)/2
        base_alpha[matcher] = (base_alpha[matcher] + 0)/2
        
    cr.set_source_rgba(38/255, 139/255, 210/255, loop_alpha[matcher])
    cr.set_operator(cairo.Operator.OVER)
    cr.set_line_width(sr)
    cr.move_to(x+r,y)
    cr.arc(x, y, r, 0, 2*math.pi)
    cr.stroke()

    cr.set_source_rgba(38/255, 139/255, 210/255, base_alpha[matcher])
    cr.set_operator(cairo.Operator.OVER)
    cr.set_line_width(1)
    cr.move_to(x+r,y+r)
    cr.arc(x, y+r, 2*sr, 0, 2*math.pi)
    cr.fill()

    cr.save()
    
    cr.set_source_rgba(203/255, 75/255, 22/255, base_alpha[matcher])
    cr.set_operator(cairo.Operator.OVER)
    cr.set_line_width(1)
    cr.translate(x, y)
    cr.rotate(direction * (-1) * ((t/20) % 360)*math.pi/180)
    cr.move_to(r,r)
    cr.arc(0, r, sr, 0, 2*math.pi)
    cr.fill()

    cr.restore()
