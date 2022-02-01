import grid
import vania
import vanib
import popup

savefile = {}

def New():
    print("New")
    for r in vania.rooms:
        if r is None: continue
        vania.deleteRoom(r.id)
    for l in vania.links:
        if l is None: continue
        vania.deleteLink(l.id)
    vania.step()
    for d in vanib.decals:
        if d is None: continue
        vanib.deleteDecal(d.id, 0)
    for m in vanib.marks:
        if m is None: continue
        vanib.deleteDecal(m.id, 1)
    vanib.step()
    
def Open(callback=False):
    global savefile
    
    if not callback:
        selectInput("Open Map...", "OpenStart")
    else:
        New()
        try:
            grid.offset  = savefile["offset"]
            grid.rescale = savefile["zoom"]
            
            ROOMS = savefile["ROOMS"]
            for r in ROOMS["list"]:
                if r is None:
                    vania.rooms.append(None)
                    vania.ID += 1
                    continue
                vr = vania.Room((r["pos"][0], r["pos"][1], r["size"][0], r["size"][1]))
                if vr.id != r["id"]: raise IndexError("Room ID Error")
            if ROOMS["count"] != len(vania.rooms): raise IndexError("Room Length Error")
            
            LINKS = savefile["LINKS"]
            for l in LINKS["list"]:
                if l is None:
                    vania.links.append(None)
                    vania.lID += 1
                    continue
                vl = vania.Link(l["cell"], l["edge"])
                if vl.id != l["id"]: raise IndexError("Link ID Error")
                vl.state = l["state"]
            if LINKS["count"] != len(vania.links): raise IndexError("Link Length Error")
            
            DECALS = savefile["DECALS"]
            for d in DECALS["list"]:
                if d is None:
                    vanib.decals.append(None)
                    vanib.ID += 1
                    continue
                vd = vanib.Decal(d["snap"], d["bind"], d["color"])
                if vd.id != d["id"]: raise IndexError("Decal ID Error")
                vd.state = d["state"]
            if DECALS["count"] != len(vanib.decals): raise IndexError("Decal Length Error")
            
            MARKS = savefile["MARKS"]
            for m in MARKS["list"]:
                if m is None:
                    vanib.marks.append(None)
                    vanib.mID += 1
                    continue
                vm = vanib.Mark(m["snap"][0], m["bind"], 0)
                if vm.id != m["id"]: raise IndexError("Mark ID Error")
                vm.sign = m["sign"]
            if MARKS["count"] != len(vanib.marks): raise IndexError("Mark Length Error")
            
            savefile = {}
            
        except Exception as e:
            print("Exception:", e)
            popup.Pop("Save File Error", "An error has occured while\nloading this save file.\nIt may be corrupted.")
            savefile = {}
    
def Save():
    global savefile
    
    try:
        file = {}
        file["offset"] = grid.offset
        file["zoom"]   = grid.rescale
        file["ROOMS"]  = {}
        file["ROOMS"]["count"] = len(vania.rooms)
        file["ROOMS"]["list"] = []
        for r in vania.rooms:
            if r is None: file["ROOMS"]["list"].append(None)
            else:
                room = {}
                room["id"]   = r.id
                room["pos"]  = r.pos
                room["size"] = r.size
                file["ROOMS"]["list"].append(room)
        if file["ROOMS"]["count"] != len(file["ROOMS"]["list"]): raise IndexError("Room Length Error")
        file["LINKS"] = {}
        file["LINKS"]["count"] = len(vania.links)
        file["LINKS"]["list"] = []
        for l in vania.links:
            if l is None: file["LINKS"]["list"].append(None)
            else:
                link = {}
                link["id"]    = l.id
                link["edge"]  = l.edge 
                link["cell"]  = l.cell
                link["state"] = l.state
                file["LINKS"]["list"].append(link)
        if file["LINKS"]["count"] != len(file["LINKS"]["list"]): raise IndexError("Link Length Error")
        file["DECALS"] = {}
        file["DECALS"]["count"] = len(vanib.decals)
        file["DECALS"]["list"] = []
        for d in vanib.decals:
            if d is None: file["DECALS"]["list"].append(None)
            else:
                decal = {}
                decal["id"]    = d.id
                decal["snap"]  = d.snap
                decal["state"] = d.state
                decal["bind"]  = d.bind
                decal["color"] = d.color
                file["DECALS"]["list"].append(decal)
        if file["DECALS"]["count"] != len(file["DECALS"]["list"]): raise IndexError("Decal Length Error")
        file["MARKS"] = {}
        file["MARKS"]["count"] = len(vanib.marks)
        file["MARKS"]["list"] = []
        for m in vanib.marks:
            if m is None: file["MARKS"]["list"].append(None)
            else:
                mark = {}
                mark["id"]   = m.id
                mark["snap"] = m.snap
                mark["bind"] = m.bind
                mark["sign"] = m.sign
                file["MARKS"]["list"].append(mark)
        if file["MARKS"]["count"] != len(file["MARKS"]["list"]): raise IndexError("Mark Length Error")
        
        savefile = file
        selectOutput("Save map...", "SaveEnd")
            
    except Exception as e:
        print("Exception:", e) 
        popup.Pop("Saving Error " + code, "An error has occured while\nsaving this map.\nIt may be corrupted.")
        savefile = {}
