import function as f
import debug
from colors import *
from gridfunc import *
import vania
import vanib
import ui

CELL = 50
SIZE = 90
LEN  = CELL * SIZE
TRUECELL = CELL
TRUELEN  = LEN

mouseIn = False
tmouse  = [0, 0]
offset  = [-2220, -2220]
rescale = 1.0
gridVal = 0

configs = [True, True]

def config(flip):
    configs[flip] = not configs[flip]

def step():
    # Called every frame (and when needed)
    #  Updates important variables like mouse position
    global TRUECELL
    global TRUELEN
    global tmouse
    global gridVal
    global mouseIn
    
    TRUECELL = CELL * rescale
    TRUELEN  = LEN * rescale
    tmouse = list(real_to_trans((mouseX, mouseY)))
    
    gridVal = snap_to_all(tmouse)[1]
    
    mouseIn = ui.mouseInside()

def pan():
    # Pan canvas by mouse movement
    offset[0] -= pmouseX - mouseX
    offset[1] -= pmouseY - mouseY
    bindPan() 

def zoom(amount):
    # Zoom canvas by certain scale
    global rescale
    
    offset[0] -= mouseX
    offset[1] -= mouseY
    delta = 1.05 if amount < 0 else (1/1.05 if amount > 0 else 1)
    rd = rescale * delta
    if rd <= 1.7 and rd >= 0.195:
        rescale *= delta
        offset[0] *= delta
        offset[1] *= delta
    offset[0] += mouseX
    offset[1] += mouseY 
    
    bindPan()
    
def bindPan():
    # Bind pan within reasonable range
    
    step()
    if offset[0] > 20: offset[0] = 20
    if offset[1] > 80: offset[1] = 80
    # 0.9 > 4050(TL) - 880 = 3170(x)
    #     > 4050(TL) - 630 = 3420(y)
    # 0.8 > 3600(TL) - 880 = 2720(x)
    #     > 3600(TL) - 630 = 2970(y)
    if offset[0] < -(TRUELEN - 880): offset[0] = -(TRUELEN - 880)
    if offset[1] < -(TRUELEN - 630): offset[1] = -(TRUELEN - 630)

def drawGrid():
    noFill()
    stroke(COLORS['UILINE'])
    strokeWeight(map(rescale, 0.5, 1.5, 2, 1))

    translate(offset[0], offset[1])
    scale(rescale)
    
    if configs[0]:
        for x in range(0, LEN + 1, CELL):
            x_ = trans_to_real((x, 0))[0]
            if x_ < 0 or x_ > width: continue
            line(x, 0, x, LEN)
        for y in range(0, LEN + 1, CELL):
            y_ = trans_to_real((0, y))[1]
            if y_ < 0 or y_ > height: continue
            line(0, y, LEN, y)
    
    cell = snap_to_grid(tmouse)
    
    if mouseIn:
        if not f.drawing and not f.deleting:
            noStroke()
            fill(COLORS['CLHIGH'])
            if f.checkTool("MOVE") and f.grabbing:
                r = vania.rooms[f.grabbed]
                rx = grid.tmouse[0] - (r.size[0] / 2)
                ry = grid.tmouse[1] - (r.size[1] / 2)
                pos = snap_to_grid((rx, ry), aprox=True)
                if not vania.roomIn(pos, r.size, r.id):
                    rect(pos[0] + 3, pos[1] + 3, r.size[0] - 5, r.size[1] - 6)
                
            elif f.checkTool(("BRUSH", "DELETE", "MARK", "PAINT")) and not vania.roomAt(tmouse):
                if f.checkTool("DELETE"): fill(COLORS['CLHDEL'])
                rect(cell[0] + 3, cell[1] + 3, CELL - 6, CELL - 6)
            elif f.checkTool("LINK"):
                edge = snap_to_edge(tmouse)
                rectMode(CENTER)
                fill(COLORS['CLHTRS'])
                rect(edge[0], edge[1], 10 - (CELL) * edge[2], 10 + (CELL) * (edge[2] - 1))
                rectMode(CORNER)
                
        else:
            noStroke()
            fill(COLORS['CLHIGH'] if f.drawing else COLORS['CLHDEL'])
            r = f.getDrawSpan()
            rect(r[0] + 3, r[1] + 3, r[2] - 6, r[3] - 6)
        
    rectMode(CORNER)
    debug.indicator()
