import grid
import gridfunc
import function as f
from colors import *
import debug
import vanib

ID = 0
lID = 0
rooms = []
links = []

def step():
    global ID
    global lID
    global rooms
    global links
    
    nc = 0
    for r in rooms:
        if r is None:
            nc += 1
            continue
        r.hovered = False
        r.endangered = False
        if f.posin(grid.tmouse, r.pos, r.size):
            if f.checkTool(("MOVE", "MARK")):
                r.hovered = True
            if f.checkTool("DELETE"):
                r.endangered = True
            if f.checkTool("PAINT") and grid.gridVal == 0:
                r.hovered = True
        if f.deleting:
            delSpan = f.getDrawSpan()
            if gridfunc.overlap((delSpan[0], delSpan[1]), (delSpan[2], delSpan[3]), r.pos, r.size):
                r.endangered = True 
    if nc == len(rooms):
        rooms = []
        ID = 0
    nc = 0
    for l in links:
        if l is None:
            nc += 1
            continue
        l.hovered = False
        l.endangered = False
        m = gridfunc.snap_to_edge(grid.tmouse)
        la = linkAt(m)
        if not la is None and la.id == l.id:
            if f.checkTool("LINK"):
                l.hovered = True
            if f.checkTool("PAINT") and grid.gridVal == 1 and l.state != 2:
                l.hovered = True
        if f.deleting:
            delSpan = f.getDrawSpan()
            if gridfunc.overlap((delSpan[0], delSpan[1]), (delSpan[2], delSpan[3]), (l.pos[0], l.pos[1]), (grid.CELL, grid.CELL)):
                l.endangered = True 
            if gridfunc.overlap((delSpan[0], delSpan[1]), (delSpan[2], delSpan[3]), (l.pos[2], l.pos[3]), (grid.CELL, grid.CELL)):
                l.endangered = True 
    if nc == len(links):
        links = []
        lID = 0

def roomAt(pos):
    # Takes in trans coordinates
    for r in rooms:
        if r is None: continue
        if f.posin(pos, r.pos, r.size):
            return r
    return None

def roomIn(pos, s, skip=-1):
    # Takes in trans position and size
    results = []
    for r in rooms:
        if r is None: continue
        if r.id == skip: continue
        if gridfunc.overlap(pos, s, r.pos, r.size) > 0: results.append(r)
    if len(results) > 0: return results
    return None

def linkAt(pos):
    for l in links:
        if l is None: continue
        if l.edge[0] == pos[0] and l.edge[1] == pos[1]: return l
    return None

def posInRoom(pos, r):
    o = 0
    if not r is None:
        o = gridfunc.overlap(pos, (2, 2), (r.pos[0] + 10, r.pos[1] + 10), (r.size[0] - 20, r.size[1] - 20))
    return o

def drawLinks():
    for l in links:
        if l is None: continue
        l.draw()

def drawRooms():
    top = -1
    for r in rooms:
        if r is None: continue
        if not r.grabbed: r.draw()
        else: top = r.id
    if top != -1:
        rooms[top].draw()

def drawLinkages():
    cellsChecked = {}
    for l in links:
        if l is None: continue
        cell = (l.pos[0], l.pos[1])
        if cell in cellsChecked.keys():
            cellsChecked[cell].append(l.id)
        else:
            cellsChecked[cell] = [l.id]
        cell = (l.pos[2], l.pos[3])
        if cell in cellsChecked.keys():
            cellsChecked[cell].append(l.id)
        else:
            cellsChecked[cell] = [l.id]

    noStroke()
    ch = (grid.CELL / 2)
    for cell in cellsChecked.keys():
        lk = cellsChecked[cell]
        if len(lk) % 2 == 0:
            edges = [-1, -1, -1, -1]
            for lid in lk:
                l = links[lid]
                if l.edge[0] < cell[0] + ch: edges[0] = lid
                if l.edge[1] < cell[1] + ch: edges[1] = lid
                if l.edge[0] > cell[0] + ch: edges[2] = lid
                if l.edge[1] > cell[1] + ch: edges[3] = lid
                
            corned = False
            rectMode(CENTER)
            if len(lk) == 2 and not (all(edges[x] != -1 for x in (0, 2)) and all(edges[x] != -1 for x in (1, 3))):
                corned = True
                fill(COLORS['CLFILL'])
                if all(x == -1 or links[x].state == 1 for x in edges): fill(COLORS['CLFADE'])
                rect(cell[0] + ch, cell[1] + ch, 15, 15)
                if edges[0] != -1:
                    rect(links[edges[0]].edge[0] + 10, links[edges[0]].edge[1], 20, 15)
                if edges[1] != -1:
                    rect(links[edges[1]].edge[0], links[edges[1]].edge[1] + 10, 15, 20)
                if edges[2] != -1:
                    rect(links[edges[2]].edge[0] - 10, links[edges[2]].edge[1], 20, 15)
                if edges[3] != -1:
                    rect(links[edges[3]].edge[0], links[edges[3]].edge[1] - 10, 15, 20)
                    
            if not corned:
                if not -1 in (edges[0], edges[1], edges[2], edges[3]):
                    fill(COLORS['CLFILL'])
                    if all(links[x].state == 1 for x in (edges[1], edges[3])): fill(COLORS['CLFADE'])
                    rect(links[edges[1]].edge[0], links[edges[1]].edge[1] + 10, 15, 20)
                    rect(links[edges[3]].edge[0], links[edges[3]].edge[1] - 10, 15, 20)
                    rect(cell[0] + ch, cell[1] + ch, 15, 15)
                    fill(COLORS['CLFILL'])
                    if all(links[x].state == 1 for x in (edges[0], edges[2])): fill(COLORS['CLFADE'])
                    rect(links[edges[0]].edge[0] + 8, links[edges[0]].edge[1], 16, 15)
                    rect(links[edges[2]].edge[0] - 8, links[edges[2]].edge[1], 16, 15)

def deleteRoom(id):
    rooms[id] = None

def deleteLink(id):
    links[id] = None

class Link():
    def __init__(self, cell, edge):
        global lID
        
        for l in links:
            if l is None: continue
            if l.edge[0] == edge[0] and l.edge[1] == edge[1]:
                l.advance()
                return None
        
        self.id = lID
        lID += 1
        links.append(self)
        
        self.cell = cell
        self.edge = edge
        self.state = 0
        
        self.hovered = False
        self.endangered = False
        
        grid = gridfunc.trans_to_grid(cell)
        xo = (-1 if edge[3] == 0 else 1) if edge[2] == 0 else 0
        yo = (-1 if edge[3] == 1 else 1) if edge[2] == 1 else 0
        ocell = gridfunc.grid_to_trans((grid[0] + xo, grid[1] + yo))
                               
        self.pos = (min(cell[0], ocell[0]), min(cell[1], ocell[1]), max(cell[0], ocell[0]), max(cell[1], ocell[1]))
        
    def advance(self):
        self.state += 1
        if self.state > 2: self.state = 0
        
    def isShort(self):
        ch = grid.CELL / 2
        return roomAt((self.pos[0] + ch, self.pos[1] + ch)) and roomAt((self.pos[2] + ch, self.pos[3] + ch))
        
    def draw(self):
        actual = gridfunc.trans_to_real(self.edge)
        if actual[0] + grid.TRUECELL < 0 or actual[0] > width or actual[1] + grid.TRUECELL < 0 or actual[1] > height:
            return
        
        noStroke()
        
        if grid.configs[1] and self.state == 2:
            fill(COLORS['SHADOW'])
            self.drawSelf(10, grid.CELL - 10, 5)
        
        fill([COLORS['CLFADE'], COLORS['CLFILL']][abs(self.state - 1)])
        if self.hovered:
            fill([COLORS['CLHFAD'], COLORS['CLHFIL']][abs(self.state - 1)])
        if self.endangered:
            fill(COLORS['CLHFDL'])
        if self.state != 2: self.drawSelf()
        else: self.drawSelf(20, h_=grid.CELL - 10)
        
        if debug.showId:
            fill(255)
            text(self.id, self.edge[0], self.edge[1])
        
    def drawSelf(self, w_=20, h_=15, off=0):
        w = w_ if self.edge[2] == 0 else h_
        h = h_ if self.edge[2] == 0 else w_
        rectMode(CENTER)
        rect(self.edge[0] + off, self.edge[1] + off, w, h)
        rectMode(CORNER)

class Room():
    def __init__(self, rec):
        global ID
        
        self.id = ID
        ID += 1
        rooms.append(self)
        
        self.pos = (rec[0], rec[1])
        self.size = (rec[2], rec[3])

        self.grabbed = False
        self.hovered = False
        self.endangered = False

        self.crush()
        
    def grab(self):
        self.grabbed = True
        
    def drop(self):
        self.grabbed = False
        
        mx = grid.tmouse[0] - (self.size[0] / 2)
        my = grid.tmouse[1] - (self.size[1] / 2)
        newpos = gridfunc.snap_to_grid((mx, my), aprox=True)
        
        if not roomIn(newpos, self.size, self.id):
            self.pos = newpos
            self.crush()
        
    def crush(self):
        for l in links:
            if l is None: continue
            o = posInRoom(l.edge, self)
            if o != 0:
                deleteLink(l.id)
        for d in vanib.decals:
            if d is None: continue
            if not d.bind is None: continue
            o = posInRoom(d.pos, self)
            if o != 0:
                vanib.deleteDecal(d.id, 0)
        for m in vanib.marks:
            if m is None: continue
            if not m.bind is None: continue
            o = posInRoom(m.pos, self)
            if o != 0:
                vanib.deleteDecal(m.id, 1)
            
    def draw(self):
        actual = gridfunc.trans_to_real(self.pos)
        scaled = (self.size[0] * grid.rescale, self.size[1] * grid.rescale)
        if actual[0] + scaled[0] < 0 or actual[0] > width or actual[1] + scaled[1] < 0 or actual[1] > height:
            return
        
        noStroke()
        
        shade = 5
        x = self.pos[0]
        y = self.pos[1]
        fil = COLORS['CLFILL']
        if self.hovered and not f.checkTool(("PAINT", "MARK")):
            fil = COLORS['CLHFIL']
        if self.grabbed:
            shade = 15
            fil = COLORS['CLHFIL']
            x = grid.tmouse[0] - (self.size[0] / 2)
            y = grid.tmouse[1] - (self.size[1] / 2)
        if self.endangered:
            fil = COLORS['CLHFDL']
            
        if grid.configs[1]:
            push()
            translate(shade, shade)
            fill(COLORS['SHADOW'])
            self.drawSelf(x, y)
            pop()
        fill(fil)
        self.drawSelf(x, y)
        if self.hovered and f.checkTool(("PAINT", "MARK")):
            self.drawHover()
        
    def drawSelf(self, x, y):
        rect(x + 5, y + 5, self.size[0] - 10, self.size[1] - 10)
        
    def drawHover(self):
        cell = gridfunc.snap_to_grid(grid.tmouse)
        rectMode(CORNER)
        fill(COLORS['CLHFIL'])
        rect(cell[0] + 5, cell[1] + 5, grid.CELL - 10, grid.CELL - 10)
