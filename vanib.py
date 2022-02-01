import grid
import gridfunc
import function as f
from colors import *
import vania
import debug

ID = 0
decals = []
mID = 0
marks = []

SIGNS = []

def setup():
    SIGNS.append(loadShape("assets/signage/x.svg"))
    SIGNS.append(loadShape("assets/signage/o.svg"))
    SIGNS.append(loadShape("assets/signage/q.svg"))
    SIGNS.append(loadShape("assets/signage/dot1.svg"))
    SIGNS.append(loadShape("assets/signage/dot2.svg"))
    SIGNS.append(loadShape("assets/signage/dot3.svg"))
    SIGNS.append(loadShape("assets/signage/dot4.svg"))
    SIGNS.append(loadShape("assets/signage/arrowUP.svg"))
    SIGNS.append(loadShape("assets/signage/arrowRIGHT.svg"))
    SIGNS.append(loadShape("assets/signage/arrowDOWN.svg"))
    SIGNS.append(loadShape("assets/signage/arrowLEFT.svg"))
    SIGNS.append(loadShape("assets/signage/stairsLEFT.svg"))
    SIGNS.append(loadShape("assets/signage/stairsRIGHT.svg"))
    SIGNS.append(loadShape("assets/signage/chest.svg"))
    
    for s in SIGNS:
        s.disableStyle()

def step():
    global ID
    global mID
    global decals
    global marks
    
    nc = 0
    for d in decals:
        if d is None:
            nc += 1
            continue
        c = d.check()
        if not c:
            nc += 1
            continue
        d.getCell()
    if nc == len(decals):
        ID = 0
        decals = []
    nc = 0
    for m in marks:
        if m is None:
            nc += 1
            continue
        c = m.check()
        #print(c)
        if not c:
            nc += 1
            continue
        m.getCell()
    if nc == len(marks):
        mID = 0
        marks = []

def drawDecals(level, null=False):
    for d in decals:
        if d is None: continue
        if d.type == level and ((d.bind is None) == null):
            d.draw()
    if level == 0:
        for m in marks:
            if m is None: continue
            if (m.bind is None) == null: m.draw()

def decalAt(snap):
    pos = snap[0]
    type = snap[1]
    for d in decals:
        if d is None or d.type != type: continue
        if type == 1:
            if d.pos[0] == pos[0] and d.pos[1] == pos[1]: return d
        else:
            ch = grid.CELL / 2
            if f.posin((pos[0] + ch, pos[1] + ch), (d.pos[0] - ch, d.pos[1] - ch), (grid.CELL, grid.CELL)):
                return d
    if type == 0:
        for m in marks:
            if m is None: continue
            ch = grid.CELL / 2
            if f.posin((pos[0] + ch, pos[1] + ch), (m.pos[0] - ch, m.pos[1] - ch), (grid.CELL, grid.CELL)):
                return m
    return None

def deleteDecal(id, t=0):
    if t == 0: decals[id] = None
    else: marks[id] = None

class Decal():
    def __init__(self, snap, bind, color=0):
        global ID
        
        self.id = ID
        ID += 1
        decals.append(self)
        self.tid = 0
        
        self.snap = snap
        self.pos  = list(snap[0])
        self.type = snap[1]  # 0 is cell, 1 is edge
        self.bind = bind
        
        self.state = 0
        self.color = color
        
        self.offset = [grid.CELL / 2, grid.CELL / 2]
        self.check()
        
        if self.type == 0:
            if not self.bind is None:
                self.offset[0] += self.pos[0] - vania.rooms[self.bind].pos[0]
                self.offset[1] += self.pos[1] - vania.rooms[self.bind].pos[1]
    
    def check(self):
        c = None
        if not self.bind is None:
            if self.type == 0:
                if self.bind < len(vania.rooms):
                    c = vania.rooms[self.bind]
                else:
                    return False
            else:
                if self.bind < len(vania.links):
                    c = vania.links[self.bind]
                    if not c is None:
                        if c.state == 2:
                            deleteDecal(self.id, self.tid)
                            c = None
                else:
                    return False
            if c is None: deleteDecal(self.id, self.tid)
            return not c is None
        else:
            if self.type == 0:
                r = vania.roomAt((self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]))
                if not r is None:
                    deleteDecal(self.id, self.tid)
                    return False
                bordering = 0
                for l in vania.links:
                    if l is None: continue
                    sp = gridfunc.snap_to_grid(self.pos)
                    if l.pos[0] == sp[0] and l.pos[1] == sp[1]:
                        bordering += 1
                        continue
                    if l.pos[2] == sp[0] and l.pos[3] == sp[1]:
                        bordering += 1
                if bordering > 0 and bordering % 2 == 0:
                    deleteDecal(self.id, self.tid)
                    return False
                    
            if self.type == 1:
                deleteDecal(self.id, self.tid)
                return False
            return True
    
    def getCell(self):
        if self.type == 1:
            if self.check() and not self.bind is None:
                self.pos = list(vania.links[self.bind].edge)
        else:
            if self.check():
                if not self.bind is None: 
                    self.pos = list(vania.rooms[self.bind].pos)
                else:
                    self.pos = list(self.snap[0])
                self.pos[0] += self.offset[0]
                self.pos[1] += self.offset[1] 
            
    def draw(self):
        actual = gridfunc.trans_to_real(self.pos)
        if actual[0] + grid.TRUECELL < 0 or actual[0] > width or actual[1] + grid.TRUECELL < 0 or actual[1] > height:
            return
        
        col = DECAL[self.color]
        p = self.pos
        if self.type == 0:
            if not self.bind is None:
                r = vania.rooms[self.bind]
                if r.grabbed:
                    p[0] = grid.tmouse[0] - (r.size[0] / 2)
                    p[1] = grid.tmouse[1] - (r.size[1] / 2)
                    p[0] += self.offset[0]
                    p[1] += self.offset[1]
                if r.endangered:
                    col = COLORS['CLMDEC']
        else:
            l = vania.links[self.bind]
            if l.endangered:
                col = COLORS['CLMDEC']
                
        noStroke()
        fill(col)
        if self.type == 0:
            s = 16
            if self.state == 1: s = 8
            quad(p[0] - s, p[1], p[0], p[1] - s, p[0] + s, p[1], p[0], p[1] + s)
        else:
            l = vania.links[self.bind]
            s = 10 if l.state == 0 or not l.isShort() else 5
            w = s if l.edge[2] == 0 else 15
            h = 15 if l.edge[2] == 0 else s
            rectMode(CENTER)
            rect(p[0], p[1], w, h)
            rectMode(CORNER)
            
class Mark(Decal):
    def __init__(self, pos, bind, start):
        global mID
        
        self.id = mID
        mID += 1
        marks.append(self)
        self.tid = 1
        
        self.snap = [pos]
        self.pos  = list(pos)
        self.type = 0
        self.bind = bind
        
        #print(self.pos, self.type, self.bind)        
        
        self.sign = 0 if start == 1 else len(SIGNS) - 1
        self.state = -1
        self.highlight = -1
        self.highmode = 0
        
        self.offset = [grid.CELL / 2, grid.CELL / 2]
        if not bind is None:
            self.offset[0] += self.pos[0] - vania.rooms[self.bind].pos[0]
            self.offset[1] += self.pos[1] - vania.rooms[self.bind].pos[1]
    
    def advance(self, dir):
        self.sign += dir
        if self.sign == -1 or self.sign == len(SIGNS): deleteDecal(self.id, self.tid)
    
    def draw(self):
        actual = gridfunc.trans_to_real(self.pos)
        if actual[0] + grid.TRUECELL < 0 or actual[0] > width or actual[1] + grid.TRUECELL < 0 or actual[1] > height:
            return
        
        p = self.pos
        if not self.bind is None and self.bind <= len(vania.rooms):
            r = vania.rooms[self.bind]
            if r.grabbed:
                p[0] = grid.tmouse[0] - (r.size[0] / 2)
                p[1] = grid.tmouse[1] - (r.size[1] / 2)
                p[0] += self.offset[0]
                p[1] += self.offset[1]
            
        cols = [-1, COLORS['CLFILL']]
        if self.highlight != -1: cols[0] = DECAL[self.highlight]
        if not self.bind is None: cols[1] = COLORS['CLMDEC']
        shapeMode(CENTER)
        if self.highlight != -1:
            noFill()
            strokeWeight(1) 
            stroke(cols[self.highmode])
            shape(SIGNS[self.sign], p[0], p[1], grid.CELL, grid.CELL)
        noStroke()
        fill(cols[abs(self.highmode - 1)])
        shape(SIGNS[self.sign], p[0], p[1], grid.CELL, grid.CELL)
        
        if debug.showId:
            fill(255, 0, 0)
            text(self.id, p[0] + 8, p[1] + 18)
