from colors import *
import function as f
import vanib
import filesys
import grid
from popup import Help

BC = 6

buttons = []
images = []
fonts = []

decalMenu = False

def loadFonts():
    fonts.append(loadFont("assets/Calibri.vlw"))
    fonts.append(loadFont("assets/Corbel-Bold.vlw"))

def loadImages():
    images.append((loadImage("assets/brush0.png"),   loadImage("assets/brush1.png")))
    images.append((loadImage("assets/pencil0.png"),  loadImage("assets/pencil1.png")))
    images.append((loadImage("assets/decal0.png"),   loadImage("assets/decal1.png")))
    images.append((loadImage("assets/move0.png"),    loadImage("assets/move1.png")))
    images.append((loadImage("assets/delete0.png"),  loadImage("assets/delete1.png")))
    images.append((loadImage("assets/pan0.png"),     loadImage("assets/pan1.png")))
    images.append((loadImage("assets/signage0.png"), loadImage("assets/signage1.png")))
    
    vanib.SIGNS.append(loadImage("assets/signX.png"))
    vanib.SIGNS.append(loadImage("assets/signO.png"))
    vanib.SIGNS.append(loadImage("assets/signQ.png"))
    vanib.SIGNS.append(loadImage("assets/sign1.png"))
    vanib.SIGNS.append(loadImage("assets/sign2.png"))
    vanib.SIGNS.append(loadImage("assets/sign3.png"))
    vanib.SIGNS.append(loadImage("assets/sign4.png"))
    vanib.SIGNS.append(loadImage("assets/signUP.png"))
    vanib.SIGNS.append(loadImage("assets/signLEFT.png"))
    vanib.SIGNS.append(loadImage("assets/signDOWN.png"))
    vanib.SIGNS.append(loadImage("assets/signRIGHT.png"))
    vanib.SIGNS.append(loadImage("assets/signSTAIRS0.png"))
    vanib.SIGNS.append(loadImage("assets/signSTAIRS1.png"))
    vanib.SIGNS.append(loadImage("assets/signCHEST.png"))

def setup():
    loadImages()
    loadFonts()
    # UI Buttons
    Button( 40, 40, 50, 50, tool=0)
    Button(100, 40, 50, 50, tool=1)
    Button(160, 40, 50, 50, tool=2)
    Button(220, 40, 50, 50, tool=3)
    Button(280, 40, 50, 50, tool=4)
    Button(340, 40, 50, 50, tool=5)
    Button(400, 40, 50, 50, tool=6)
    
    # Color Buttons
    Button( 45, 105, 30, 30, color=0)
    Button( 85, 105, 30, 30, color=1)
    Button(125, 105, 30, 30, color=2)
    Button(165, 105, 30, 30, color=3)
    Button(205, 105, 30, 30, color=4)
    Button(245, 105, 30, 30, color=5)
    Button(285, 105, 30, 30, color=6)
    
    # UI Buttons
    Button(486, 40, 50, 50, txt="NEW")
    Button(586, 40, 50, 50, txt="SAVE")
    Button(692, 40, 50, 50, txt="LOAD")
    Button(850, 40, 50, 50, txt=" ? ")
    Button(785, 28, 20, 20, txt="g01")
    Button(785, 53, 20, 20, txt="g02")

def draw():
    noStroke()
    push()
    translate(10, 10)
    fill(COLORS['SHADOW'])
    drawBorder()
    pop()
    fill(COLORS['UIGREY'])
    drawBorder()
    if decalMenu: drawDrop()
    drawScroll()
    drawButtons()
    
def drawBorder():
    rect(20, 0, width-20, 80)
    rect(0, 0, 20, height)
    rect(width, 0, -20, height)
    rect(20, height, width-20, -20)

dropW = 292
dropH = 55

def drawDrop():
    fill(COLORS['SHADOW'])
    rect(30, 90, dropW - 4, dropH - 4)
    fill(COLORS['UIBUTT'])
    rect(20, 80, dropW, dropH)
    fill(COLORS['SHADO2'])
    rect(20, 80, dropW, 6)
    rect(20, 86, 6, dropH - 6)
    
def drawScroll():
    sizex = map(grid.TRUELEN, grid.LEN * 1.7, grid.LEN * 0.195, 10, width - 40)
    sizey = map(grid.TRUELEN, grid.LEN * 1.7, grid.LEN * 0.195, 10, height - 100)
    scrollx = map(grid.offset[0], 20, -(grid.TRUELEN - 880), 20 + (sizex / 2), width - 20 - (sizex / 2))
    scrolly = map(grid.offset[1], 80, -(grid.TRUELEN - 630), 80 + (sizey / 2), height - 20 - (sizey / 2))
    rectMode(CENTER)
    fill(COLORS['UIBUTT'])
    #rect(scrollx, 80, sizex, 10)
    rect(scrollx, height - 20, sizex, 10)
    rect(20, scrolly, 10, sizey)
    rect(width - 20, scrolly, 10, sizey)
    rectMode(CORNER)
    
def step():
    for b in buttons:
        if len(b.txt) != 0 or decalMenu or b.id < BC + 1: b.update()
    
def drawButtons():
    for b in buttons:
        if len(b.txt) != 0 or decalMenu or b.id < BC + 1:
            b.draw()
    for b in buttons:
        if b.tool != -1:
            b.drawTooltip()
    
def mouseInside():
    o = f.within(mouseX, mouseY, 20, 80, width-20, width-20)
    d = True if not decalMenu else not f.within(mouseX, mouseY, 20, 80, dropW + 20, dropH + 80)
    return o and d
    
tooltips = ["Brush Tool", "Pencil Tool", "Keys Tool", "Move Tool", "Delete Tool", "Pan Tool", "Decal Tool"]
    
def setText(t):
    if t == 0:
        textFont(fonts[0], 12)
        textAlign(LEFT, BOTTOM)
    if t == 1:
        textFont(fonts[1], 31)
        textAlign(LEFT, CENTER)
    if t == 2:
        textFont(fonts[0], 15)
        textAlign(LEFT, CENTER)
    if t == 3:
        textFont(fonts[1], 21)
        textAlign(LEFT, BOTTOM)
    if t == 4:
        textFont(fonts[0], 31)
        textAlign(CENTER, TOP)
    
class Button():
    def __init__(self, x, y, w, h, tool=-1, color=-1, txt=""):
        self.id = int(len(buttons))
        buttons.append(self)
            
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.hovered = 0
        self.hoverTime = 0
        self.active = 0
        
        self.tool = tool
        self.color = color
        self.txt = txt
        
        self.tip = [0, 0]
        
        self.img = self.id if self.id < len(images) else -1
        
    def update(self):
        self.checkHover()
        self.tip = [mouseX, mouseY]
        setText(1)
        if len(self.txt) > 0 and self.txt[0] != "g":
            self.w = textWidth(self.txt) + 20
        
    def checkHover(self):
        self.hovered = 0
        hw = self.w / 2
        hh = self.h / 2
        if f.within(mouseX, mouseY, self.x - hw, self.y - hh, self.x + hw, self.y + hh):
            self.hovered = 1 
            
        if self.hovered == 1:
            self.hoverTime += 1
        else: self.hoverTime = 0
        
    def activate(self):
        self.active = 1
        if self.tool != -1:  f.setTool(self.tool)
        if self.color != -1: f.setColor(self.color)
        if len(self.txt) == 0:
            for b in buttons:
                if len(b.txt) != 0: continue
                if b.id == self.id: continue
                if self.tool  != -1 and b.id > BC: continue
                if self.color != -1 and b.id < BC + 1: continue
                b.disable()
        else:
            if self.txt == "NEW":  filesys.New()
            if self.txt == "SAVE": filesys.Save()
            if self.txt == "OPEN": filesys.Open()
            if "?" in self.txt:    Help()
            if self.txt[0] == "g":
                if self.txt[1:] == "01": grid.config(0)
                if self.txt[1:] == "02": grid.config(1)
            self.disable()
        
    def disable(self):
        self.active = 0
        
    def draw(self):
        noStroke()
        
        fill(COLORS['SHADOW'])
        self.drawSelf((6, 6))
        
        if self.color == -1:
            fill([COLORS['UIBUTT'], COLORS['UIHBUT'], COLORS['UIBACT'], COLORS['UIHACT']][self.hovered + 2 * (self.active)])
        else:
            fill([UIDEC[self.color], DECAL[self.color]][self.active or self.hovered])
            
        off = 0.5 if self.hovered else 0
        if off != 0 and f.mouseDown: off = 3
        self.drawSelf((off, off))
        
        if self.img != -1:
            imageMode(CENTER)
            image(images[self.img][1 if self.active else 0], self.x + off, self.y + off, 50, 50)
            imageMode(CORNER)
            
        if len(self.txt) != 0:
            if self.txt[0] != "g":
                fill(COLORS['UIBACT'])
                setText(1)
                textAlign(LEFT, CENTER)
                text(self.txt, off + self.x - (self.w / 2) + 10, off + self.y)
            else:
                push()
                translate(off, off)
                if self.txt[1:] == "01":
                    noFill()
                    stroke(COLORS['WHITE'])
                    strokeWeight(2)
                    line(self.x - 8, self.y, self.x + 8, self.y)
                    line(self.x, self.y - 8, self.x, self.y + 8)
                else:
                    fill(COLORS['WHITE'])
                    rectMode(CENTER)
                    rect(self.x, self.y, self.w - 6, self.h - 6)
                pop()
        
    def drawSelf(self, off):
        rectMode(CENTER)
        rect(self.x + off[0], self.y + off[1], self.w, self.h)
        rectMode(CORNER)
        
    def drawTooltip(self):
        if self.hoverTime > 50:
            tip = tooltips[self.tool]
            setText(2)
            fill(COLORS['WHITE'])
            rect(self.tip[0] - 2, self.tip[1] - 9, textWidth(tip) + 4, 18)
            fill(COLORS['CLFILL'])
            text(tip, self.tip[0], self.tip[1])
