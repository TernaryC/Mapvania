from colors import *
import function as f
import ui

title = "Popup"
message = "This is a popup."

popping = False

hovered = 0
active  = 0

centerx = 0
centery = 0
w = 450
h = 300
w2 = w / 2
h2 = h / 2
bx = centerx
by = centery + 80
weight = 0
offy = 0

def Pop(t, m, w=0):
    global popping
    global title
    global message
    global weight
    
    popping = True
    title = t
    message = m
    weight = w 
    
def Help():
    message = """Brush Tool: Click and drag to draw rooms. Right click to delete.
Pencil Tool: Click on edges to add hallways. Right click to delete.
                      Click again to toggle hallway type.
Keys Tool: Click to add colored indicators. Right click to delete.
                   Click again on large keys to change their size.
Move Tool: Click and drag to move rooms.
Delete Tool: Click and drag to delete rooms and hallways in an area.
Pan Tool: Click and drag to move the camera view.
Decal Tool: Click to add symbols. Click again to change symbol.
                     Right click to reverse.
"""
# 34-45 is the limit
    Pop("Mapvania v.1.0.0", message, 1)

def step():
    global centerx
    global centery
    global bx
    global by
    global hovered
    global active
    global popping
    
    centerx = width / 2
    centery = height / 2
    bx = centerx
    by = centery + 80
    
    if active and not f.mouseDown:
        popping = False
    
    hovered = 0
    if f.within(mouseX, mouseY, bx - 50, by - 25 + offy, bx + 50, by + 25 + offy):
        hovered = 1 
        
    active = False
    if hovered and f.mouseDown: active = True

def drawButton(x, y):
    rectMode(CENTER)
    rect(x, y, 100, 50)

def draw():
    global offy
    
    # Draw Popup
    rectMode(CENTER)
    fill(COLORS["SHADOW"])
    rect(centerx + 15, centery + 15, w, h)
    fill(COLORS["WHITE"])
    stroke(COLORS["UIGREY"])
    strokeWeight(6)
    rect(centerx, centery, w, h)
    noStroke()
    fill(COLORS["UIGREY"])
    rectMode(CORNER)
    rect(centerx - w2, centery - h2, w, 40)
    fill(COLORS["WHITE"])
    ui.setText(3)
    text(title, centerx - w2 + 5, centery - h2 + 30) 
    fill(COLORS["UIBACT"])
    offx = 0
    if weight == 0: ui.setText(4)
    else: 
        ui.setText(2)
        textAlign(LEFT, TOP)
        offx = -w2 + 20
    text(message, centerx + offx, centery - 50 - (45 * weight))
    
    off = 0.5 if hovered else 0
    if active: off = 3
    offy = 30 * weight
    fill(COLORS["SHADOW"])
    drawButton(bx + 6, by + 6 + offy)
    fill([COLORS['UIBUTT'], COLORS['UIHBUT']][hovered])
    drawButton(bx + off, by + off + offy)
    fill(COLORS['UIBACT'])
    ui.setText(1)
    textAlign(CENTER, CENTER)
    text("OK", bx + off, by + off + offy)
