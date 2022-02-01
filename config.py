import ConfigParser
import colors

KEYS = [[], [], [], [], [], [], []]

def openIni():
    try:
        config = ConfigParser.RawConfigParser()
        config.read("preferences.ini")
        
        KEYS[0] = config.get("KEYBINDINGS", "BRUSH").lower().replace(" ", "").split(",")
        KEYS[1] = config.get("KEYBINDINGS", "PENCIL").lower().replace(" ", "").split(",")
        KEYS[2] = config.get("KEYBINDINGS", "KEYS").lower().replace(" ", "").split(",")
        KEYS[3] = config.get("KEYBINDINGS", "MOVE").lower().replace(" ", "").split(",")
        KEYS[4] = config.get("KEYBINDINGS", "DELETE").lower().replace(" ", "").split(",")
        KEYS[5] = config.get("KEYBINDINGS", "PAN").lower().replace(" ", "").split(",")
        KEYS[6] = config.get("KEYBINDINGS", "DECAL").lower().replace(" ", "").split(",")
        
        colors.DECAL[0] = config.get("PALETTE", "RED")
        colors.DECAL[1] = config.get("PALETTE", "ORANGE")
        colors.DECAL[2] = config.get("PALETTE", "YELLOW")
        colors.DECAL[3] = config.get("PALETTE", "GREEN")
        colors.DECAL[4] = config.get("PALETTE", "BLUE")
        colors.DECAL[5] = config.get("PALETTE", "PURPLE")
        colors.DECAL[6] = config.get("PALETTE", "PINK")
        for c in colors.DECAL:
            colors.UIDEC.append(colors.darken(c))
            
        colors.COLORS['UIGREY'] = config.get("UI", "BORDER")
        butcol = config.get("UI", "BUTTONS").split("\n")
        colors.COLORS['UIBUTT'] = butcol[0]
        colors.COLORS['UIHBUT'] = butcol[1]
        colors.COLORS['UIBACT'] = butcol[2]
        colors.COLORS['UIHACT'] = butcol[3]
        colors.COLORS['WHITE'] = config.get("UI", "BACKGROUND")
        colors.COLORS['UILINE'] = config.get("UI", "GRIDLINES")
        colors.COLORS['CLHIGH'] = config.get("UI", "HIGHLIGHT")
        colors.COLORS['CLHTRS'] = colors.alphize(colors.COLORS['CLHIGH'], "AA")
        colors.COLORS['CLHDEL'] = config.get("UI", "DELETING")
        
        colors.COLORS['CLFILL'] = config.get("ROOMS", "ROOM")
        colors.COLORS['CLHFIL'] = config.get("ROOMS", "HIGHLIGHT")
        colors.COLORS['CLHFDL'] = config.get("ROOMS", "DELETING")
        colors.COLORS['CLMDEC'] = config.get("ROOMS", "DECALS")
        colors.COLORS['CLFADE'] = config.get("ROOMS", "HIDDEN")
        colors.COLORS['CLHFAD'] = config.get("ROOMS", "HIDLIGHT")
        
        colors.COLORS['SHADOW'] = colors.alphize(colors.COLORS['CLFILL'], "33")
        colors.COLORS['SHADO2'] = colors.alphize(colors.COLORS['CLFILL'], "11")
        
    except Exception as e:
        print(e)
        with open("preferences.ini", 'w') as file:
            saveStrings(file, [generatePrefs()])
            openIni()
        
def generatePrefs():
    pref = """; This preferences file can be used to customize Mapvania
; To return all preferences to the default, simply delete this file
; Be aware, if any values are entered incorrectly, this file will be
;  reverted to the default values

[KEYBINDINGS]
; Hotkeys used to quickly switch between tools
; Can be customized with any list of characters, each representing
;  a key. All keys must be represented by single characters
; Tools can always be accessed using the number keys
; The Delete tool can always be accessed by double right-clicking
; The Pan tool can always be accessed using the Space key

BRUSH:  B, Q
PENCIL: V, L
KEYS:   C, W
MOVE:   M, D
DELETE: R, E
PAN:    P
DECAL:  Z, S
; Seperate keys using commas.

; DEFAULT
;  BRUSH:  B, Q
;  PENCIL: V, L
;  KEYS:   C, W
;  MOVE:   M, D
;  DELETE: R, E
;  PAN:    P
;  DECAL:  Z, S

[UI]
; Colors used by the UI
; Can be customized with any hexadecimal color code

BORDER: #9977DD
BUTTONS: #BBAAFF
         #AA99EE
         #6666BB
         #7777CC
;note: BUTTONS takes four color codes, used for different states
BACKGROUND: #FFFFFF
GRIDLINES: #BBAADD
HIGHLIGHT: #EEDDFF
DELETING: #FFDDEE

; DEFAULTS
;  BORDER: #9977DD
;  BUTTONS: #BBAAFF
;           #AA99EE
;           #6666BB
;           #7777CC
;  BACKGROUND: #FFFFFF
;  GRIDLINES: #BBAADD
;  HIGHLIGHT: #EEDDFF
;  DELETING: #FFDDEE

[ROOMS]
; Colors used to display rooms in the map
; Can be customized with any hexadecimal color code

ROOM: #300060
HIGHLIGHT: #5500DD
DELETING: #DD0055
DECALS: #FFFFFF
HIDDEN: #9060C0
HIDLIGHT: #B060F0
;note: HIDDEN and HIDLIGHT are used for secret hallways

; DEFAULTS
;  ROOM: #300060
;  HIGHLIGHT: #5500DD
;  DELETING: #DD0055
;  DECALS: #FFFFFF
;  HIDDEN: #9060C0
;  HIDLIGHT: #B060F0

[PALETTE]
; Colors used by the Keys tool
; Can be customized with any hexadecimal color code

RED:    #DD0055
ORANGE: #DD7700
YELLOW: #DDCC00
GREEN:  #00DD77
BLUE:   #00CCDD
PURPLE: #8800DD
PINK:   #CC00DD

; DEFAULTS
;  RED:    #DD0055
;  ORANGE: #DD7700
;  YELLOW: #DDCC00
;  GREEN:  #00DD77
;  BLUE:   #00CCDD
;  PURPLE: #8800DD
;  PINK:   #CC00DD"""
    return pref
