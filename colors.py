COLORS = {
'WHITE'  : '#000000', 
'SHADOW' : '#000000',  # Shadows for all elements
'SHADO2' : '#000000',  # Shadow for Drop menu

'UILINE' : '#000000',  # Gridlines
'UIGREY' : '#000000',  # UI Border
'UIBUTT' : '#000000',  # UI Button 
'UIHBUT' : '#000000',  # UI Button - Hovered
'UIBACT' : '#000000',  # UI Button - Active
'UIHACT' : '#000000',  # UI Button - Active and Hovered

'CLHIGH' : '#000000',  # Cell - Hovered
'CLHTRS' : '#000000',  # Cell - Hovered Transparent
'CLFILL' : '#000000',  # Room
'CLHFIL' : '#000000',  # Room - Hovered
'CLHDEL' : '#000000',  # Cell - Deleting
'CLHFDL' : '#000000',  # Room - Deleting
'CLMDEC' : '#000000',  # Decals and Marks
'CLFADE' : '#000000',  # Links - Faded
}

DECAL = [0, 0, 0, 0, 0, 0, 0]
UIDEC = []

def getRGB(c):
    R = int(unhex(c[1:3]))
    G = int(unhex(c[3:5]))
    B = int(unhex(c[5:7]))
    return [R, G, B]

def makeRGB(rgb):
    return hex(rgb[0])[-2:] + hex(rgb[1])[-2:] + hex(rgb[2])[-2:]

def darken(c):
    rgb = getRGB(c)
    rgb[0] = int(rgb[0] * 0.45)
    rgb[1] = int(rgb[1] * 0.45)
    rgb[2] = int(rgb[2] * 0.45)
    return '#' + makeRGB(rgb) 

def alphize(c, a):
    rgb = getRGB(c)
    return eval('0x' + a + makeRGB(rgb))

SHADOW = alphize("#300060", "33")
