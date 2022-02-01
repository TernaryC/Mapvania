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
        #print("check")
        c = None
        if not self.bind is None:
            if self.type == 0:
                if self.bind < len(vania.rooms):
                    c = vania.rooms[self.bind]
                else:
                    #print("nbn,0,b>")
                    return False
            else:
                if self.bind < len(vania.links):
                    c = vania.links[self.bind]
                    if c.state == 2:
                        deleteDecal(self.id, self.tid)
                        c = None
                else:
                    #print("nbn,1,b>")
                    return False
            if c is None: deleteDecal(self.id, self.tid)
            #print("c")
            return not c is None
        else:
            if self.type == 0:
                r = vania.roomAt((self.pos[0] + self.offset[0], self.pos[1] + self.offset[1]))
                if not r is None:
                    deleteDecal(self.id, self.tid)
                    #print("bn,0,nrn")
                    return False
            if self.type == 1:
                deleteDecal(self.id, self.tid)
                #print("bn,1")
                return False
            #print("bn")
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
            
SIGNS = []
            
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
        if not self.bind is None:
            r = vania.rooms[self.bind]
            if r.grabbed:
                p[0] = grid.tmouse[0] - (r.size[0] / 2)
                p[1] = grid.tmouse[1] - (r.size[1] / 2)
                p[0] += self.offset[0]
                p[1] += self.offset[1]
            
        imageMode(CENTER)
        if not self.bind is None: tint(eval('0xFF' + COLORS['CLMDEC'][1:]))
        else: tint(eval('0xFF' + COLORS['CLFILL'][1:]))
        image(SIGNS[self.sign], p[0], p[1], grid.CELL, grid.CELL)
        imageMode(CORNER)
        
        if debug.showId:
            fill(255, 0, 0)
            text(self.id, p[0] + 8, p[1] + 18)
