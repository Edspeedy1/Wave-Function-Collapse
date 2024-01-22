import pygame, random
GRIDSIZE = 80,40
SCALE = 18, 18
SCREEN = pygame.display.set_mode((GRIDSIZE[0]*SCALE[0],GRIDSIZE[1]*SCALE[1]))

POSIBLE = [(0,0,0,1),(0,0,1,0),(0,1,0,0),(1,0,0,0)], #(1,0,1,1),(0,1,1,1),(1,1,0,1),(1,1,1,0),(1,1,1,1)]

class tile:
    def __init__(self, x, y):
        self.tiles = POSIBLE[:]
        self.set = None
        self.x = x
        self.y = y
        allTiles.append(self)

    def collapse(self):
        self.set = random.choice(self.tiles)
        self.tiles = [self.set]
        return (self.set, self.x, self.y)


allTiles = []        
grid = [[tile(i,j) for i in range(GRIDSIZE[0])] for j in range(GRIDSIZE[1])]

imgSet = {
    (0,0,0,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/dot.png'), 0), 

    (0,0,0,1): pygame.transform.rotate(pygame.image.load('Wave Collapse/dash.png'), 180),
    (0,0,1,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/dash.png'), 270),
    (0,1,0,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/dash.png'), 0),
    (1,0,0,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/dash.png'), 90),
    
    (0,1,0,1): pygame.transform.rotate(pygame.image.load('Wave Collapse/line.png'), 0),
    (1,0,1,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/line.png'), 90),

    (1,1,1,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/T.png'), 270),
    (1,1,0,1): pygame.transform.rotate(pygame.image.load('Wave Collapse/T.png'), 0),
    (1,0,1,1): pygame.transform.rotate(pygame.image.load('Wave Collapse/T.png'), 90),
    (0,1,1,1): pygame.transform.rotate(pygame.image.load('Wave Collapse/T.png'), 180),

    (1,1,1,1): pygame.transform.rotate(pygame.image.load('Wave Collapse/x.png'), 0),
    }

# imgSet = {(1,0,0,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/dash.png'), 90), (0,0,1,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/dash.png'), 270),(1,0,1,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/line.png'), 90), (1,0,1,0): pygame.transform.rotate(pygame.image.load('Wave Collapse/line.png'), 90)}

def test(cell, x, y):
    if x != 0:
        options = []
        for i in grid[x-1][y].tiles:
            if i[1] not in options:
                options.append(i[1])
        for i in cell.tiles:
            if i[3] not in options:
                cell.tiles.remove(i)
    if y != 0:
        options = []
        for i in grid[x][y-1].tiles:
            if i[0] not in options:
                options.append(i[0])
        for i in cell.tiles:
            if i[2] not in options:
                cell.tiles.remove(i)
    if x < GRIDSIZE[1]-1:
        options = []
        for i in grid[x+1][y].tiles:
            if i[3] not in options:
                options.append(i[3])
        for i in cell.tiles:
            if i[1] not in options:
                cell.tiles.remove(i)
    if y < GRIDSIZE[0]-1:
        options = []
        for i in grid[x][y+1].tiles:
            if i[2] not in options:
                options.append(i[2])
        for i in cell.tiles:
            if i[0] not in options:
                cell.tiles.remove(i)

def updateGrid(grid): 
    global allTiles
    allTiles.sort(key=lambda x: len(x.tiles))
    for i in allTiles:
        if i.set != None:
            allTiles.remove(i)
        else:
            break
    if not updating: return
    if len(allTiles) == 0:
        allTiles = [] 
        for i in grid:
            allTiles += i
    count = 0 
    l = len(allTiles[0].tiles)
    for i in allTiles:
        if len(i.tiles) == l:
            count += 1
        else:
            break
    
    T = allTiles[random.randint(0, count-1)].collapse()
    try:
        SCREEN.blit(pygame.transform.scale(imgSet[T[0]], (SCALE[0], SCALE[1])), (T[1]*SCALE[0],T[2]*SCALE[1]))
    except: pass

    for i in range(GRIDSIZE[1]):
        for j in range(GRIDSIZE[0]):
            cell = grid[i][j]
            test(cell, i, j)
            for _ in range(3):
                if cell.tiles == []: 
                    cell.tiles = POSIBLE[:]
                    test(cell, i, j)
                else: break
            else:
                for tilex in range(-5,5):
                    for tiley in range(-5,5):
                        try:
                            grid[i+tilex][j+tiley].tiles = POSIBLE[:]
                            grid[i+tilex][j+tiley].set = None
                            allTiles.append(grid[i+tilex][j+tiley])
                            pygame.draw.rect(SCREEN, (0,0,0), ((j+tiley)*SCALE[0],(i+tilex)*SCALE[1],SCALE[0],SCALE[1]))
                        except: pass
                print(1)
    return grid


updating = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                for i in range(GRIDSIZE[1]-1):
                    for j in range(GRIDSIZE[0]-1):
                        retest(grid[i+1][j+1], i+1, j+1)
                print('retested')
            if event.key == pygame.K_SPACE:
                allTiles = []        
                grid = [[tile(i,j) for i in range(GRIDSIZE[0])] for j in range(GRIDSIZE[1])]
            if event.key == pygame.K_s:
                i = 0
                while True:
                    try: pygame.image.load(f'Wave Collapse\\Pictures\\{i}.png')
                    except: break
                    i += 1
                pygame.image.save(SCREEN, f'Wave Collapse\\Pictures\\{i}.png')
    grid = updateGrid(grid)
    pygame.display.update()