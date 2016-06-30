import random,sys,time
from collections import deque
import pygame as pg
from pygame.locals import *

# sum constants
redColor = (255,0,0)
blueColor = (0,0,255)
K_BLACK = (0,0,0)
K_SILVER = (192,192,192)
K_GREY = (102,102,102)
K_WHITE = (255,255,255)
K_LIGHT_GREY = (160,160,160)
K_LEFT_CLICK = 1
K_RIGHT_CLICK = 3
K_MIDDLE_CLICK = 2
K_SCROLL_UP = 4
K_SCROLL_DOWN = 5


class MineBoard:
    def __init__(self,x,y,mines):
        self.length = x
        self.height = y
        self.mines = mines
        self.array = [['0']*x for _i in range(y)]
        self.random(mines)
        self.updateDeque = deque()
        self.flags = set()

        # when indexing, y is first then x

    def get(self,x,y):
        return self.array[y][x]

    def regen(self):
        self.array = [['0']*self.length for _i in range(self.height)]
        self.random(self.mines)
        self.updateDeque.clear()


    def dfs(self,start, item):
        # a dfs using start and the array
        # all are coordinates(x,y)
        stack,visited = [start], set()
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                if self.get_tuple(vertex) == item:
                    visited.add(vertex)

                    x = vertex[0]
                    y = vertex[1]
                    y_min = vertex[1] - 1
                    y_add = vertex[1] + 1
                    x_min = vertex[0] - 1
                    x_add = vertex[0] + 1

                    ret_iter = []
                    if y_min >= 0:
                        # middle
                        ret_iter.append((x,y_min))
                        if x_min >= 0:
                            ret_iter.append((x_min,y_min))
                        # right
                        if x_add <= self.length-1:
                            ret_iter.append((x_add, y_min))



                    # middle row
                    #left
                    if x_min >= 0:
                        ret_iter.append((x_min, y))
                    #right
                    if x_add <= self.length-1:
                        ret_iter.append((x_add,y))

                    # bottom row
                    if y_add <= self.height - 1:
                        # middle
                        ret_iter.append((x,y_add))

                        #left
                        if x_min >= 0:
                            ret_iter.append((x_min,y_add))
                        # right
                        if x_add <= self.length -1:
                            ret_iter.append((x_add,y_add))

                    for element in ret_iter:
                        if self.get_tuple(element) == item:
                            stack.append(element)

        final_ret = []
        for element in visited:
            x = element[0]
            y = element[1]
            x_min = x-1
            y_min = y-1
            x_add = x+1
            y_add = y+1

            # top row
            if y_min >= 0:
                # middle
                final_ret.append((x,y_min))
                # left
                if x_min >= 0:
                    final_ret.append((x_min,y_min))
                # right
                if x_add <= self.length-1:
                    final_ret.append((x_add, y_min))

            # middle row
            #left
            if x_min >= 0:
                final_ret.append((x_min, y))
            #right
            if x_add <= self.length-1:
                final_ret.append((x_add,y))

            # bottom row
            if y_add <= self.height - 1:
                # middle
                final_ret.append((x,y_add))
                #left
                if x_min >= 0:
                    final_ret.append((x_min,y_add))
                # right
                if x_add <= self.length -1:
                    final_ret.append((x_add,y_add))

        visited.update(set(final_ret))

        return visited




    def random(self, number):
        for _i in range(number):
            counter = 0
            _x = random.randint(0,self.length-1)
            _y = random.randint(0,self.height-1)
            while self.get(_x,_y) == '*': # if random number generated already is a bomb
                counter += 1
                _x = random.randint(0,self.length-1)
                _y = random.randint(0,self.height-1)
                if counter > 100:
                    print("SKIPPING")
                    return -1
            self.set(_x,_y,'*')
            self.update(_x,_y)


    def update(self, x, y):
        '''
        :param x: x cord of bomb
        :param y: y cord of bomb
        :return:  None
        Increases non- bombs around the point by 1
        '''
        ret_iter = []
        x_min = x-1
        y_min = y-1
        x_add = x+1
        y_add = y+1

        # top row
        if y_min >= 0:
            # middle
            ret_iter.append((x,y_min))
            # left
            if x_min >= 0:
                ret_iter.append((x_min,y_min))
            # right
            if x_add <= self.length-1:
                ret_iter.append((x_add, y_min))

        # middle row
        #left
        if x_min >= 0:
            ret_iter.append((x_min, y))
        #right
        if x_add <= self.length-1:
            ret_iter.append((x_add,y))

        # bottom row
        if y_add <= self.height - 1:
            # middle
            ret_iter.append((x,y_add))
            #left
            if x_min >= 0:
                ret_iter.append((x_min,y_add))
            # right
            if x_add <= self.length -1:
                ret_iter.append((x_add,y_add))

        for coord in ret_iter:
            item = self.get_tuple(coord)
            if item != '*':
                self.set_tuple(coord, str(int(item) + 1))







    def get_tuple(self,x_y_tuple):
        return self.array[x_y_tuple[1]][x_y_tuple[0]]

    def set_tuple(self,x_y, item):
        self.array[x_y[1]][x_y[0]] = item


    def set_mul_tuple(self,*args):
        """Tuples must be (x,y,item)"""
        for i in args:
            x,y,item = i
            if x < 0 or y < 0:
                print('Negative x or y')
                raise Exception
            else:
                try:
                    self.array[y][x] = item
                except IndexError:
                    print(i, 'is TOO BIG')
                    raise

    def __str__(self):
        return '\n'.join(list(map(' '.join,self.array)))

    def set(self, x,y,item):
        if x < 0 or y < 0:
            print('Negative x or y')
            raise Exception
        else:
            try:
                self.array[y][x] = item
            except IndexError:
                    print(x,y,item, 'is TOO BIG')
                    raise

    def press(self,x,y):
        if (x,y) not in self.flags:
            item = self.get(x,y)
            if item == '*':
                return '*'
            if item == '0':
                # start a dfs
                self.updateDeque.extend(self.dfs((x,y), '0'))
            else:
                self.updateDeque.append((x,y))








def bin_search(sortedlist, item):
    first = 0
    last = len(sortedlist)-1
    found = False

    while first<=last and not found:
        midpoint = (first + last)//2
        if sortedlist[midpoint] == item:
            found = True
        else:
            if item < sortedlist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1

    return found






pg.init()
fpsClock = pg.time.Clock()

mainFont = pg.font.Font(pg.font.get_default_font(), 13)




R_PADDING = 0#5
L_PADDING = R_PADDING
T_PADDING = 0#5
B_PADDING = T_PADDING
H_HEIGHT = 30
K_BOX_WIDTH = 16

displayscreen = pg.display.set_mode((640,480))
revealed_mine = set() # a set of revealed coordinates


def game_select_screen():
    pg.display.set_caption('something')

def create_header(width):
    global displayscreen
    displayscreen.fill(K_WHITE, Rect(0,0,L_PADDING+R_PADDING+width*K_BOX_WIDTH,H_HEIGHT))


def create_rect(x,y=None):
    print(x,y)
    if y is None:
        y = x[1]
        x = x[0]

    return Rect(x*K_BOX_WIDTH + L_PADDING + 1,
        y*K_BOX_WIDTH + H_HEIGHT + T_PADDING + 1,
        K_BOX_WIDTH-2,
        K_BOX_WIDTH-2
                )

def pause(display_text, x=0,y=0,exit = 0,fill=True):
    # setup
    global displayscreen
    if fill:
        displayscreen.fill(K_WHITE)
    displayscreen.blit(mainFont.render(display_text,True,K_BLACK), (x,y))
    pg.display.update()
    if exit:
        time.sleep(exit)
        pg.quit()
        sys.exit()

    while True:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                return



def mine_sweep():
    # setup
    # . = nothing, f = flag
    assert isinstance(mine_game, MineBoard)
    global displayscreen
    icon = pg.image.load("mine.png").convert_alpha()
    pg.display.set_icon(icon)
    pg.display.set_caption("Bomb Defuser")

    width = mine_game.length
    height = mine_game.height

    total_len = width * K_BOX_WIDTH + R_PADDING + L_PADDING
    total_height = height * K_BOX_WIDTH + B_PADDING + T_PADDING + H_HEIGHT

    x_straight = width*K_BOX_WIDTH # a line that goes straigt through a X axis and straight
    y_straight = height*K_BOX_WIDTH

    pg.display.set_mode([total_len,total_height])
    displayscreen.fill(K_WHITE)
    start_point = [R_PADDING, T_PADDING+H_HEIGHT]
    for iterat,_i in enumerate(range(width)):
        if iterat == width - 1:
            pg.draw.line(displayscreen,K_SILVER,start_point, (start_point[0], start_point[1] + y_straight))
            start_point[0] += K_BOX_WIDTH-1
            pg.draw.line(displayscreen,K_SILVER,start_point, (start_point[0], start_point[1] + y_straight))
            break


        pg.draw.line(displayscreen,K_SILVER,start_point, (start_point[0], start_point[1] + y_straight))
        start_point[0] += K_BOX_WIDTH-1
        pg.draw.line(displayscreen,K_SILVER,start_point, (start_point[0], start_point[1] + y_straight))
        start_point[0] += 1

    start_point = [R_PADDING, T_PADDING+H_HEIGHT]
    for iter,_i in enumerate(range(height)):
        pg.draw.line(displayscreen,K_SILVER,start_point, (start_point[0]+x_straight, start_point[1]))
        start_point[1] += K_BOX_WIDTH-1
        pg.draw.line(displayscreen,K_SILVER,start_point, (start_point[0]+x_straight, start_point[1]))
        start_point[1] += 1

    for y,_i in enumerate(range(height)):
        for x, _i in enumerate(range(width)):
            pg.draw.rect(displayscreen, K_GREY, create_rect(x,y))






    # create the header with some basic buttons



    pg.display.update()
    currentBlock = None
    canwin = set() # true if flags are in right position

    while True:
        if len(revealed_mine) == width*height and not canwin:
                pause("WINNER!", K_BOX_WIDTH*(width//2) + R_PADDING, K_BOX_WIDTH*(height//2)+T_PADDING + H_HEIGHT, 5)




        """ EVENT HANDLER"""
        for event in pg.event.get ():




            if event.type == QUIT:
                print(QUIT)
                pg.quit()
                sys.exit()

            if event.type == MOUSEMOTION:
                if not (0 <= event.pos[0] <= total_len and 0 <= event.pos[1] <= total_height):
                    continue

                mousex,mousey = event.pos
                mousex -= R_PADDING
                mousey -= H_HEIGHT+T_PADDING
                cord = (mousex//K_BOX_WIDTH, mousey//K_BOX_WIDTH)
                print(currentBlock,'|',event.pos,'|', (cord[0], cord[1]) )
                if currentBlock and (cord[0], cord[1]) != currentBlock and cord[0] >= 0  <= cord[1] and cord not in revealed_mine:
                    pg.draw.rect(displayscreen, K_GREY, create_rect(currentBlock[0],currentBlock[1]))
                    currentBlock = cord
                    pg.draw.rect(displayscreen, K_SILVER, create_rect(cord[0], cord[1]))





            if event.type == MOUSEBUTTONDOWN:
                mousex,mousey = event.pos
                mousex -= R_PADDING
                mousey -= H_HEIGHT+T_PADDING

                temp_cord = (mousex//K_BOX_WIDTH, mousey//K_BOX_WIDTH)
                if mousex >= 0 and mousey >= 0 and temp_cord not in revealed_mine and temp_cord not in mine_game.flags:
                    currentBlock = (mousex//K_BOX_WIDTH, mousey//K_BOX_WIDTH)
                    pg.draw.rect(displayscreen, K_SILVER, create_rect(currentBlock[0], currentBlock[1]))




            if event.type == MOUSEBUTTONUP:

                mousex,mousey = event.pos
                mousex -= R_PADDING
                mousey -= H_HEIGHT+T_PADDING

                temp_cord = (mousex//K_BOX_WIDTH, mousey//K_BOX_WIDTH)
                if event.button == K_LEFT_CLICK:
                    if mousex >= 0 and mousey >= 0 and temp_cord not in revealed_mine and temp_cord not in mine_game.flags:
                        if mine_game.press(currentBlock[0], currentBlock[1]) == '*':
                            print("BLOW UP")
                            pause("GAME OVER",exit=5)
                            pg.quit()
                            sys.exit()
                        else:
                            for updated in mine_game.updateDeque:
                                render(updated) #TODO FINISH
                                revealed_mine.add(updated)

                if event.button == K_RIGHT_CLICK:
                    # place a flag
                    if temp_cord in mine_game.flags:
                        # remove the flag
                        mine_game.flags.remove(temp_cord)
                        revealed_mine.remove(temp_cord)
                        if temp_cord in canwin:
                            canwin.remove(temp_cord)
                        pg.draw.rect(displayscreen, K_GREY,create_rect(temp_cord))

                    elif mousex >= 0 and mousey >= 0 and temp_cord not in revealed_mine and temp_cord: # make sure its a valid pos
                        revealed_mine.add(temp_cord)
                        mine_game.flags.add(temp_cord)
                        if mine_game.get_tuple(temp_cord) != '*':
                            print("THAT WAS NOT AN MINE YOU SCREWED UP")
                            canwin.add(temp_cord)
                        render(temp_cord, True)

                currentBlock = None



            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()

                if event.key == K_f:
                    mousex,mousey = pg.mouse.get_pos()
                    print(pg.mouse.get_pos())
                    mousex -= R_PADDING
                    mousey -= H_HEIGHT+T_PADDING

                    temp_cord = (mousex//K_BOX_WIDTH, mousey//K_BOX_WIDTH)

                    # place a flag
                    if temp_cord in mine_game.flags:
                        # remove the flag
                        mine_game.flags.remove(temp_cord)
                        revealed_mine.remove(temp_cord)
                        if temp_cord in canwin:
                            canwin.remove(temp_cord)
                        pg.draw.rect(displayscreen, K_GREY,create_rect(temp_cord))

                    elif mousex >= 0 and mousey >= 0 and temp_cord not in revealed_mine and temp_cord: # make sure its a valid pos
                        revealed_mine.add(temp_cord)
                        mine_game.flags.add(temp_cord)
                        if mine_game.get_tuple(temp_cord) != '*':
                            print("THAT WAS NOT AN MINE YOU SCREWED UP")
                            canwin.add(temp_cord)
                        pg.draw.rect(displayscreen, K_SILVER, create_rect(temp_cord))
                        render(temp_cord, True)
                    currentBlock = None

                if event.key == K_p:
                    pause("PAUSED", 10,10,fill = False)
                    create_header(width)

        pg.display.update()
        fpsClock.tick(30)


def coordToAbs(x_or_tuple,y=None):
    if not y:
        y = x_or_tuple[1]
        x_or_tuple = x_or_tuple[0]

    return (x_or_tuple*K_BOX_WIDTH + L_PADDING + 1,
            y*K_BOX_WIDTH + H_HEIGHT + T_PADDING
            )




def render(x_y, text = None):
    global displayscreen
    if text:
        displayscreen.blit(mainFont.render('F',True,K_BLACK), coordToAbs(x_y)) # TODO USE A NICE PICTURE INSTEAD
        return
    assert isinstance(int(mine_game.get_tuple(x_y)), int)
    if mine_game.get_tuple(x_y) == '0':
        pg.draw.rect(displayscreen, K_LIGHT_GREY, create_rect(x_y[0],x_y[1]))
    else:
        pg.draw.rect(displayscreen, K_LIGHT_GREY, create_rect(x_y[0],x_y[1]))
        displayscreen.blit(mainFont.render(mine_game.get_tuple(x_y),True,K_BLACK), coordToAbs(x_y))


    revealed_mine.add(x_y)



mine_game = MineBoard(15,20,50) # 15*20 / 50 = 6
mine_sweep()


