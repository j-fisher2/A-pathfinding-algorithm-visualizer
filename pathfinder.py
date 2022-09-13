import pygame 
from queue import PriorityQueue
pygame.init()

WIDTH=800
WIN=pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A*")

WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BLACK=(0,0,0)
PURPLE=(128,0,128)
ORANGE=(255,165,0)
GREY=(128,128,128)
TURQUOISE=(64,224,208)

class Spot:
    def __init__(self,row,col,width,total_rows,isStart=False,isEnd=False):
        self.row=row
        self.col=col
        self.width=width
        self.total_rows=total_rows
        self.x=col*width
        self.y=row*width 
        self.color=WHITE
        self.neighbors=list()
        self.isStart=isStart
        self.isEnd=isEnd

    def get_pos(self):
        return self.row,self.col
    def is_closed(self):
        return self.color==RED
    def is_open(self):
        return self.color==GREEN
    def is_barrier(self):
        return self.color==BLACK
    def is_start(self):
        return self.color==ORANGE 
    def is_end(self):
        return self.color==TURQUOISE
    def reset(self):
        self.color=WHITE 
    def make_start(self):
        self.color=ORANGE 
    def make_closed(self):
        self.color=RED 
    def make_open(self):
        self.color=GREEN 
    def make_barrier(self):
        self.color=BLACK 
    def make_end(self):
        self.color=TURQUOISE
    def draw(self):
        pygame.draw.rect(WIN,self.color,(self.x,self.y,self.width,self.width))
    def make_path(self):
        self.color=PURPLE
    def update_neighbors(self,grid):
        if self.row>0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        if self.row<len(grid)-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        if self.col>0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
        if self.col<len(grid[0])-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])


def make_grid(rows,width):
    grid=[]
    gap=width//rows 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot=Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid 

def draw(grid,width,rows):
    gap=width//rows
    WIN.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw()
    for i in range(len(grid)):
        pygame.draw.line(WIN,BLACK,(0,i*gap),(width,i*gap))
        for j in range(len(grid[0])):
            pygame.draw.line(WIN,BLACK,(j*gap,0),(j*gap,width))
    pygame.display.update()
    
def algorithm(grid,startNode,endNode,ROWS):
    count=0
    q=PriorityQueue()
    q.put((0,count,startNode))
    open_set_hash={startNode}

    gScore={spot:float("inf") for row in grid for spot in row}
    fScore={spot:float("inf") for row in grid for spot in row}

    gScore[startNode]=0
    fScore[startNode]=h(startNode.get_pos(),endNode.get_pos())
    cameFrom={startNode:startNode}

    while not q.empty():
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        curNode=q.get()[2]
        open_set_hash.remove(curNode)

        if curNode==endNode:
            while curNode!=startNode:
                curNode.make_path()
                draw(grid,WIDTH,ROWS)
                curNode=cameFrom[curNode]
            return True 

        temp_g_score=gScore[curNode]+1
        for neighbour in curNode.neighbors:
            if temp_g_score<gScore[neighbour]:
                gScore[neighbour]=temp_g_score
                fScore[neighbour]=temp_g_score+h(neighbour.get_pos(),endNode.get_pos())
                cameFrom[neighbour]=curNode
                if neighbour not in open_set_hash:
                    count+=1
                    q.put((fScore[neighbour],count,neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw(grid,WIDTH,ROWS)

        if curNode!=startNode:
            curNode.make_closed()

def h(node1,node2):
    r1,c1=node1
    r2,c2=node2 
    return abs(r1-r2)+abs(c1-c2)

def main():
    ROWS=50
    grid=make_grid(ROWS,WIDTH)
    start=end=None 
    startPos=endPos=None 

    run=True 
    while run:
        draw(grid,WIDTH,ROWS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False 
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                mx,my=pos 
                gap=WIDTH//ROWS
                row=my//gap
                col=mx//gap
                spot=grid[row][col]
                if not start:
                    start=spot 
                    spot.make_start()
                    startPos=(row,col)
                    print(spot.row)
                elif start and not end:
                    end=spot 
                    spot.make_end()
                    endPos=(row,col)
                else:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                mx,my=pos 
                gap=WIDTH//ROWS 
                row=my//gap
                col=mx//gap 
                spot=grid[row][col]
                if spot.is_barrier() and not spot.is_start() and not spot.is_end():
                    spot.reset()
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(grid,start,end,ROWS)

    pygame.quit()


main()
