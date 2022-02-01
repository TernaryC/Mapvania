import grid
import gridfunc
import vania
import vanib

shift = False 
ctrl  = False
alt   = False

mouseDown = False

tool = 0
decal = 0

drawing = False
drawStart = [0, 0]

grabbing = False
grabbed = -1

deleting = False

def within(x, y, x0, y0, x1, y1):
    return x > x0 and x <= x1 and y > y0 and y <= y1

def posin(pos0, pos1, s):
    return within(pos0[0], pos0[1], pos1[0], pos1[1], pos1[0] + s[0], pos1[1] + s[1])

def checkTool(c):
    l = ["BRUSH", "LINK", "PAINT", "MOVE", "DELETE", "PAN", "MARK"]
    if type(c) is not tuple:
        return tool == l.index(c)
    else: return any(tool == l.index(x) for x in c)

def setTool(t):
    global tool
    tool = t
    
def setColor(c):
    global decal
    decal = c
    
def disable():
    global drawing
    drawing = False
    
def getDrawSpan():
    return gridfunc.alignRect(drawStart, gridfunc.snap_to_grid(grid.tmouse))
    
def startRoom():
    global drawing
    global drawStart

    drawing = True
    drawStart = list(gridfunc.snap_to_grid(grid.tmouse))
    
def addRoom():
    global drawing
    drawing = False
    
    r = getDrawSpan()
    if not vania.roomIn((r[0], r[1]), (r[2], r[3])):
        vania.Room(r)
        
def addLink():
    cell = gridfunc.snap_to_grid(grid.tmouse)
    edge = gridfunc.snap_to_edge(grid.tmouse)
    
    r = vania.roomAt(grid.tmouse)
    o = vania.posInRoom(grid.tmouse, r)
    if o == 0:
        vania.Link(cell, edge)
        
def addDecal():
    snap = list(gridfunc.snap_to_all(grid.tmouse))
    id = None
    r = vania.roomAt(grid.tmouse)
    if snap[1] == 0:
        if not r is None: id = r.id
    else:
        o = vania.posInRoom(grid.tmouse, r)
        if o == 0:
            l = vania.linkAt(gridfunc.snap_to_edge(grid.tmouse))
            if not l is None: id = l.id
        if id is None and r is None:
            snap[0] = gridfunc.snap_to_grid(grid.tmouse)
            snap[1] = 0
    d = vanib.decalAt(snap)
    if d is None: vanib.Decal(snap, id, color=decal)
    elif d.tid == 0:
        if d.type == d.state == 0: d.state = 1
        else: vanib.deleteDecal(d.id)
    
        
def addMark(dir):
    cell = gridfunc.snap_to_grid(grid.tmouse)
    r = vania.roomAt(grid.tmouse)
    id = None
    if not r is None: id = r.id 
    d = vanib.decalAt((cell, 0))
    if d is None: vanib.Mark(cell, id, dir)
    elif d.tid == 1: d.advance(dir)
        
def deleteDecal():
    snap = gridfunc.snap_to_all(grid.tmouse)
    d = vanib.decalAt(snap)
    if not d is None: vanib.deleteDecal(d.id)
        
def deleteStart():
    global deleting
    global drawStart
    
    deleting = True
    drawStart = list(gridfunc.snap_to_grid(grid.tmouse))
        
def deleteRoom(all=False):
    global deleting
    deleting = False
    
    s = getDrawSpan()
    rooms = vania.roomIn((s[0], s[1]), (s[2], s[3]))
    if not rooms is None:
        for r in rooms: vania.deleteRoom(r.id)
    if all:
        for l in vania.links:
            if l is None: continue
            if gridfunc.overlap((l.pos[0], l.pos[1]), (10, 10), (s[0], s[1]), (s[2], s[3])) > 0:
                vania.deleteLink(l.id)
            if gridfunc.overlap((l.pos[2], l.pos[3]), (10, 10), (s[0], s[1]), (s[2], s[3])) > 0:
                vania.deleteLink(l.id)
        for d in vanib.decals:
            if d is None: continue
            if gridfunc.overlap(d.pos, (10, 10), (s[0], s[1]), (s[2], s[3])) > 0:
                vanib.deleteDecal(d.id, 0)
        for m in vanib.marks:
            if m is None: continue
            if gridfunc.overlap(d.pos, (10, 10), (s[0], s[1]), (s[2], s[3])) > 0:
                vanib.deleteDecal(d.id, 1)

def deleteLink():
    edge = gridfunc.snap_to_edge(grid.tmouse)
    l = vania.linkAt(edge)
    if not l is None: vania.deleteLink(l.id)

def moveRoom():
    global grabbed
    global grabbing
    
    r = vania.roomAt(grid.tmouse)
    if not r is None:
        grabbed = r.id
        grabbing = True
        r.grab()

def dropRoom():
    global grabbed
    global grabbing
    
    if grabbing:
        vania.rooms[grabbed].drop()
        grabbed = -1
        grabbing = False
