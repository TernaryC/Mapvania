import grid
import function as f

def real_to_trans(r):
    # Real Coordinates into Translated Coordinates (used in grid.drawGrid())
    return ((r[0] - grid.offset[0]) / grid.rescale, (r[1] - grid.offset[1]) / grid.rescale)

def trans_to_real(t):
    # Translated Coordinates to real coordinates
    return ((t[0] * grid.rescale) + grid.offset[0], (t[1] * grid.rescale) + grid.offset[1]) 

def trans_to_grid(t, aprox=False):
    # Trans Coordinates into Grid Coordinates (used for cell computation)
    # aprox determines the rounding method
    x = map(t[0], 0, grid.LEN, 0, grid.SIZE)
    y = map(t[1], 0, grid.LEN, 0, grid.SIZE)
    x = floor(x) if not aprox else round(x)
    y = floor(y) if not aprox else round(y)
    return (x, y)
    
def grid_to_trans(g):
    # Grid Coordinates into Trans Coordinates
    x = g[0] * grid.CELL
    y = g[1] * grid.CELL
    return (x, y)

def snap_to_grid(t, aprox=False):
    # Runs Trans Coordinates through ttg and gtt in order to snap to the top-left corner
    # aprox determines the rounding method (floor or round)
    return grid_to_trans(trans_to_grid(t, aprox))

def snap_to_edge(t):
    ch = grid.CELL / 2
    st = snap_to_grid(t)
    
    cx = st[0] + ch
    cy = st[1] + ch
  
    xdif = t[0] - cx
    ydif = t[1] - cy
  
    if xdif == ydif == 0: ydif = -1
  
    edge = [0, 0]
    if abs(xdif) > abs(ydif):
        edge[0] = xdif / abs(xdif)
    elif ydif != 0:
        edge[1] = ydif / abs(ydif)
    else:
        print("EDGE ERROR", xdif, ydif)
  
    ex = cx + edge[0] * ch
    ey = cy + edge[1] * ch
    
    dir = 0 if abs(xdif) > abs(ydif) else 1
    side = (0 if xdif < 0 else 2) if dir == 0 else (1 if ydif < 0 else 3)
    return (ex, ey, dir, side)

def snap_to_all(t):
    cell = snap_to_grid(t)
    edge = snap_to_edge(t)
    d0 = dist(t[0], t[1], cell[0] + (grid.CELL / 2), cell[1] + (grid.CELL / 2))
    d1 = dist(t[0], t[1], edge[0], edge[1])
    res = [edge] if d1 < d0 else [cell]
    res.append(0 if d1 > d0 else 1)
    return res

def alignRect(corn0, corn1):
    # Takes in two corners and returns top-left and size for rectangle
    # Takes real, trans, or cell coordinates
    left   = min(corn0[0], corn1[0])
    right  = max(corn0[0], corn1[0]) + grid.CELL
    top    = min(corn0[1], corn1[1])
    bottom = max(corn0[1], corn1[1]) + grid.CELL
    return (left, top, right - left, bottom - top)

def overlap(pos0, size0, pos1, size1):
    bpos0 = (pos0[0] + size0[0], pos0[1] + size0[1])
    bpos1 = (pos1[0] + size1[0], pos1[1] + size1[1])
    x_overlap = max(0, min(bpos0[0], bpos1[0]) - max(pos0[0], pos1[0]))
    y_overlap = max(0, min(bpos0[1], bpos1[1]) - max(pos0[1], pos1[1]))
    return x_overlap * y_overlap
