import function as f
import grid
import gridfunc
import ui
    
showId = False    
display = [0, 0]
    
def debug():
    noStroke()
    fill(0)
    ui.setText(0)
    text(frameRate, width - 20, 15)
    text("tMouse {:.2f}, {:.2f} : Offset {:.2f}, {:.2f} Scale {:.2f} : Mouse : {:.2f}, {:.2f} : {} {} {} : drawStart {:.2f}, {:.2f}".format(
            grid.tmouse[0], grid.tmouse[1],
            grid.offset[0], grid.offset[1], grid.rescale,
            mouseX, mouseY,
            focused, f.acceptInput, f.mouseDown,
            f.drawStart[0], f.drawStart[1]
        ), 10, height - 8)
    
def indicator():
    noFill()
    stroke(0, 255, 0)
    circle(grid.tmouse[0], grid.tmouse[1], 5)
    noStroke()
            
def key(k):
    global showId
    if k == "`": showId = not showId 
