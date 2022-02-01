import ui
from colors import *
import function as f
import debug
import grid
import gridfunc
import vania
import vanib
import config
import filesys
import popup

debugging = False

rightTimer = 0

def setup():
    config.openIni()
    size(900,650)
    ui.setup()
    ui.buttons[0].activate()
    ui.buttons[ui.BC + 1].activate()
    
def draw():
    global rightTimer
    
    if rightTimer > 0: rightTimer -= 1
    
    rectMode(CORNER)
    background(COLORS['WHITE'])
    ui.setText(0)
    push()
    # Draw Grid
    if not popup.popping: grid.step()
    grid.drawGrid()
    if not popup.popping: vania.step()
    if not popup.popping: vanib.step()
    vanib.drawDecals(0, True)
    vania.drawLinkages()
    vania.drawLinks()
    vanib.drawDecals(1)
    vania.drawRooms()
    vanib.drawDecals(0)
    pop()
    # Draw UI
    ui.decalMenu = False
    if f.checkTool("PAINT"): ui.decalMenu = True
    if not popup.popping: ui.step()
    ui.draw() 
    if popup.popping:
        popup.step()
        popup.draw()
    # Draw Debug
    if debugging:
        debug.debug()
        if len(vania.rooms) > 0 and not vania.rooms[0] is None:
            r = vania.rooms[0]
            actual = gridfunc.trans_to_real(r.pos)
            scaled = (r.size[0] * grid.rescale, r.size[1] * grid.rescale)
            noFill()
            stroke(255, 0, 255)
            rect(actual[0], actual[1], scaled[0], scaled[1])

def mousePressed():
    if mouseButton == LEFT:
        f.mouseDown = True
        if not popup.popping and ui.mouseInside():
            if f.checkTool("BRUSH"):
                f.startRoom()
            if f.checkTool("MOVE"):
                f.moveRoom()
            if f.checkTool("DELETE"):
                f.deleteStart()
    
def mouseReleased():
    if mouseButton == LEFT:
        f.mouseDown = False
        if not popup.popping:
            if not ui.mouseInside():
                f.disable()
                for b in ui.buttons:
                    if b.hovered:
                        b.activate()
                        break
            else:
                if f.checkTool("BRUSH"):
                    f.addRoom()
                if f.checkTool("MOVE"):
                    f.dropRoom()
                if f.checkTool("DELETE"):
                    f.deleteRoom(all=True)
                if f.checkTool("LINK"):
                    f.addLink()
                if f.checkTool("PAINT"):
                    f.addDecal()
                if f.checkTool("MARK"):
                    f.addMark(1)
    if not popup.popping and mouseButton == RIGHT:
        if not f.checkTool("MARK"): doubleRight()
        if not f.checkTool(("BRUSH", "DELETE", "LINK", "PAINT", "MARK")):
            ui.buttons[4].activate()
        elif f.checkTool("LINK"):
            f.deleteLink()
        elif f.checkTool("PAINT"):
            f.deleteDecal()
        elif f.checkTool("MARK"):
            f.addMark(-1)
        else:
            f.deleteStart()
            f.deleteRoom()

def doubleRight():
    global rightTimer
    
    if rightTimer == 0: rightTimer = 10
    else:
        rightTimer = 0
        ui.buttons[4].activate()

def mouseDragged():
    if not popup.popping:
        if ui.mouseInside() and ((f.checkTool("PAN") and mouseButton == LEFT) or mouseButton == CENTER):
            grid.pan()

def mouseWheel(e):
    if not popup.popping:
        dif = e.getCount()
        grid.zoom(dif)

def OpenStart(f):
    if not f is None:
        sf = str(f)
        if sf[-4:] != ".map": sf += ".map"
        with open(sf, 'r') as fs:
            filesys.savefile = eval(loadStrings(fs)[0])
            filesys.Open(True)

def SaveEnd(f):
    if not f is None:
        sf = str(f)
        if sf[-4:] != ".map": sf += ".map"
        with open(sf, 'w') as fs:
            saveStrings(fs, [str(filesys.savefile)])
        filesys.savefile = {}

def keyPressed():
    global debugging
    
    if not popup.popping:
        if not any((f.shift, f.ctrl, f.alt)):
            if key == "1" or key in config.KEYS[0]: ui.buttons[0].activate()
            if key == "2" or key in config.KEYS[1]: ui.buttons[1].activate()
            if key == "3" or key in config.KEYS[2]: ui.buttons[2].activate()
            if key == "4" or key in config.KEYS[3]: ui.buttons[3].activate()
            if key == "5" or key in config.KEYS[4]: ui.buttons[4].activate()
            if key == "6" or key in config.KEYS[5] or key == " ": ui.buttons[5].activate()
            if key == "7" or key in config.KEYS[6]: ui.buttons[6].activate()
        if key == "N": filesys.New()
        if key == "S": filesys.Save()
        if key == "O": filesys.Open()

    if debugging and key == "0":
        popup.Pop("Test Popup", "This is a test message\nincluding linebreaks")

    if debugging: debug.key(key)
    if keyCode == 112: debugging = not debugging  # F1
    
    if keyCode == SHIFT:   f.shift = True
    if keyCode == CONTROL: f.ctrl  = True
    if keyCode == ALT:     f.alt   = True
    
def keyReleased():
    if keyCode == SHIFT:   f.shift = False
    if keyCode == CONTROL: f.ctrl  = False
    if keyCode == ALT:     f.alt   = False
