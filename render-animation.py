#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p "python3.withPackages(ps:[ps.scipy ps.numpy ps.pycairo ps.tqdm ps.tinycss2])"

import os
import re
import math
import sys
import subprocess
import cairo
import tqdm
import numpy as np
from scipy.ndimage import gaussian_filter

from parser import parse

import tinycss2
import tinycss2.color3

################################################################
print('Parse styles.css...')

f = open("styles.css", "rb")

colors = {}

rules = tinycss2.parse_stylesheet_bytes(f.read())

for rule in rules[0]:
    if rule.type == 'qualified-rule':
        kind = None
        for x in rule.prelude:
            if x.type == 'ident':
                kind = x.value

        color_next = False
        for x in rule.content:
            if color_next:
                if x.type == 'hash':
                    colors[kind] = tinycss2.color3.parse_color(x)
                    color_next = False
                if x.type == 'ident':
                    colors[kind] = tinycss2.color3.parse_color(x)
                    color_next = False
                
            if x.type == 'ident':
                if x.value == 'color':
                    color_next = True

current_colors = {}
for k in colors:
    current_colors[k] = {
        'r': colors[k].red,
        'g': colors[k].green,
        'b': colors[k].blue
        }
                         

################################################################
print('Reading timestamps...')
stamps = []

for file in os.listdir("."):
    if file.endswith('.agda'):
        t = re.sub("[^0-9]", "", file)
        if len(t) > 0:
            stamps.append(int(t))
    if file.endswith('.txt'):
        t = re.sub("[^0-9]", "", file)
        if len(t) > 0:
            stamps.append(int(t))

stamps = list(set(sorted(stamps)))
            
################################################################            
print('Computing cursor position...')
rows = {}
columns = {}
lines = []
point = 0
for s in tqdm.tqdm(sorted(stamps)):
    infile = "board{:d}.agda".format(s)
    if os.path.isfile(infile):
        f = open(infile, "r")
        lines = f.readlines()
        f.close()

    if os.path.isfile("point{:d}.txt".format(s)):
        g = open("point{:d}.txt".format(s), "r")
        point = int(g.readlines()[0])
        g.close()

    count = 0
    row = 1
    for line in lines:
        if count + len(line) >= point:
            rows[s] = row
            columns[s] = point - count
            break
        row = row + 1
        count = count + len(line)

################################################################            
SCALE = 6
imagesize = (1920//SCALE,1080//SCALE)

WIDTH = imagesize[0]
HEIGHT = imagesize[1]

cursor_x = math.nan
cursor_y = math.nan
current_row = math.nan

def render(surface, cr, frame, s, t, text, html, df):
    dpi = (400 / 72) * WIDTH / 1920
    
    cr.set_source_rgba(0.0, 0.0, 0.0, 0.5) # transparent black
    cr.rectangle(0, 0, imagesize[0], imagesize[1])
    cr.set_operator(cairo.Operator.SOURCE)
    cr.fill()
    
    global current_row
    global cursor_x
    global cursor_y

    if math.isnan(cursor_x):
        cursor_x = columns[s]
    else:
        cursor_x = (cursor_x + columns[s])/2.0
        
    if math.isnan(cursor_y):
        cursor_y = rows[s]
    else:
        cursor_y = (cursor_y + rows[s])/2.0        

    if math.isnan(current_row):
        current_row = rows[s]
    else:
        current_row = 0.9 * current_row + 0.1 * rows[s]
        
    margin = 7.086599 * dpi 
    bottom_margin = 2 * 7.70443 * dpi 
    bottom_margin = imagesize[1] / 2.0
    
    # cursor
    cr.select_font_face("DejaVu Sans Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    fontscale = 50 * WIDTH / 1920
    lineheight = fontscale
    cr.set_font_size(fontscale)

    extents = cr.text_extents("M")
    
    cr.set_source_rgba(1, 0.0, 0.0, 0.5)
    cr.set_operator(cairo.Operator.SOURCE)
    cr.rectangle(margin + (cursor_x - 1) * extents.x_advance,
                 imagesize[1] - bottom_margin - extents.height * 1.15 + (cursor_y - current_row) * lineheight,
                 extents.x_advance, extents.height * 1.30)
    cr.fill()    

    cr.set_operator(cairo.Operator.ADD)

    if html == None:
        for k in colors:                                                        
            current_colors[k]['r'] = 1  
            current_colors[k]['g'] = 1  
            current_colors[k]['b'] = 1  

        # text
        cr.set_source_rgba(1, 1, 1, 0.5) # gray

        lg1 = cairo.LinearGradient(0.0, 0.0, 0.0, imagesize[1])
        r = g = b = 1
        lg1.add_color_stop_rgba(0.0, r, g, b, 0.7)
        lg1.add_color_stop_rgba(0.1, r, g, b, 0.9)
        lg1.add_color_stop_rgba(0.5, r, g, b, 1)
        lg1.add_color_stop_rgba(0.9, r, g, b, 0.9)    
        lg1.add_color_stop_rgba(1.0, r, g, b, 0.7)

        cr.set_source(lg1)
        cr.set_operator(cairo.Operator.OVER)

        for r in range(len(text)):
            words = text[r]
            cr.move_to(margin,imagesize[1] - bottom_margin + (r - current_row + 1) * lineheight)
            cr.show_text(words)
    else:
        parsed = parse(html)

        grads = {}
        for k in colors:
            factor = 5
            current_colors[k]['r'] = (colors[k].red + factor*current_colors[k]['r']) / (factor + 1)
            current_colors[k]['g'] = (colors[k].green + factor*current_colors[k]['g']) / (factor + 1)
            current_colors[k]['b'] = (colors[k].blue + factor*current_colors[k]['b']) / (factor + 1)

            r = current_colors[k]['r']        
            g = current_colors[k]['g']
            b = current_colors[k]['b']

            grads[k] = cairo.LinearGradient(0.0, 0.0, 0.0, imagesize[1])
            grads[k].add_color_stop_rgba(0.0, r, g, b, 0.7)
            grads[k].add_color_stop_rgba(0.1, r, g, b, 0.9)
            grads[k].add_color_stop_rgba(0.5, r, g, b, 1)
            grads[k].add_color_stop_rgba(0.9, r, g, b, 0.9)    
            grads[k].add_color_stop_rgba(1.0, r, g, b, 0.7)

        for r in range(len(parsed)):
            blocks = parsed[r]
            c = margin 
            for block in blocks:
                kinds, text = block

                cr.set_source_rgba(1, 1, 1, 0.5) # gray

                for k in kinds:
                    if k in colors:
                        cr.set_source(grads[k])
                        cr.set_operator(cairo.Operator.OVER)

                cr.move_to(c,HEIGHT - bottom_margin + (r - current_row + 1) * lineheight)
                cr.show_text(text)
                extents = cr.text_extents(text)
                c = c + extents.x_advance 

            
loaded_html = 0
loaded_text = 0
text = []
html = []

start = min(stamps)
finish = max(stamps)
fps = 15
duration = int(fps * (finish - start) / 1000)

# thanks to
# https://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
FFMPEG_BIN = "/home/jim/.nix-profile/bin/ffmpeg"
command = [ FFMPEG_BIN,
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', ('%dx%d' % imagesize), # size of one frame
        '-pix_fmt', 'bgra',
        '-r', str(fps), # frames per secon
        '-i', '-', # The imput comes from a pipe
        '-an', # Tells FFMPEG not to expect any audio
        '-vcodec', 'libvpx-vp9',
        '-pix_fmt','yuva420p',
        '-crf','18',
        'rendered.webm' ]

ffmpeg = subprocess.Popen( command, stdin=subprocess.PIPE)

def clean(x):
     if x.startswith(' '):
         return '<a></a>' + x
     return x

print("Rendering frames...")
subset = 1000 
#for frame in tqdm.tqdm(range(subset,duration)):
for frame in tqdm.tqdm(range(subset,subset+300)):
#for frame in tqdm.tqdm(range(duration)):
    t = start + frame * 1000 / fps
    s = max([s for s in stamps if s <= t])

    if loaded_html != s:
        infile = "board{:d}.html".format(s)
        if os.path.isfile(infile):
            f = open(infile, "r")
            unsolved = ' <a id="23" class="Pragma">--allow-unsolved-metas</a>'
            html = [clean(x.rstrip("\n").replace(unsolved,'')) for x in f.readlines()]
            html = "\n".join(html)
            f.close()
            loaded_html = s        

    if loaded_text != s:
        infile = "board{:d}.agda".format(s)
        if os.path.isfile(infile):
            f = open(infile, "r")
            text = [x.rstrip("\n") for x in f.readlines()]
            f.close()
            loaded_text = s        

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, *imagesize)
    cr = cairo.Context(surface)
    df = 1.0 / fps
    if loaded_html == loaded_text:
        render(surface, cr, frame, s, t, text, html, df)
    else:
        render(surface, cr, frame, s, t, text, None, df)

    cr.select_font_face("DejaVu Sans Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(HEIGHT / 12)
    cr.set_source_rgba(1, 1, 1, 1)
    cr.move_to(0,HEIGHT/12)
    cr.show_text('%05d'%(frame))
        
    buf = surface.get_data()
    width = imagesize[0]
    height = imagesize[1]

    data = np.ndarray(shape=(height, width, 4),
                     dtype=np.uint8,
                     buffer=buf)

    #data = data.transpose( (2, 0, 1) )
    #data[3,::,::] = gaussian_filter(data[3,::,::], sigma=3)
    #data[3,::,::] = gaussian_filter(data[3,::,::], sigma=3)
    #data = data.transpose( (1, 2, 0) )
    #ffmpeg.stdin.write( surface.get_data() )
    ffmpeg.stdin.write( data )

ffmpeg.stdin.close()
ffmpeg.wait()
if ffmpeg.returncode !=0:
    print('ffmpeg failed')
