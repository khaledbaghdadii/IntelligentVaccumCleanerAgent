import pygame, sys
import os, sys
import constants
w, h =5,7
SCREEN_WIDTH =500
SCREEN_HEIGHT =500

# NUMBER_OF_BLOCKS_WIDE = 12
# NUMBER_OF_BLOCKS_HIGH = 13

BLOCK_HEIGHT = round((SCREEN_HEIGHT-100)/h)
BLOCK_WIDTH = round(SCREEN_WIDTH/w)

# def get_tile_color(tile_contents):
#     tile_color = constants.GOLD
#     if tile_contents == 0:
#         tile_color = constants.DARKGREY
#     if tile_contents == ".":
#         tile_color = constants.GREEN
#     if tile_contents == "p":
#         tile_color = constants.BLACK
#     if tile_contents == "n":
#         tile_color = constants.RED
#     return tile_color

def draw_map(surface, map_tiles):
    for j, tile in enumerate(map_tiles):
        for i, tile_contents in enumerate(tile):
            # print("{},{}: {}".format(i, j, tile_contents))
            filepath="images/tile.png"
            try:
                image = pygame.image.load(filepath).convert_alpha()
            except:
                s = "Couldn't open: {}".format(filepath)
                raise ValueError(s)
            image = pygame.transform.scale(image, (BLOCK_WIDTH, BLOCK_HEIGHT))
            rect = image.get_rect()
            # rect = rect.move(i*BLOCK_WIDTH, j*BLOCK_HEIGHT,)
            # myrect = pygame.Rect(i*BLOCK_WIDTH, j*BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(surface,(0,0,255), rect,1)
            pygame.display.update()

# def draw_grid(surface):
#     for i in range(w):
#         new_height = round(i * BLOCK_HEIGHT)
#         new_width = round(i * BLOCK_WIDTH)
#         pygame.draw.line(surface, constants.BLACK, (0, new_height), (SCREEN_WIDTH, new_height), 2)     
#         pygame.draw.line(surface, constants.BLACK, (new_width, 0), (new_width, SCREEN_HEIGHT), 2)

def game_loop(surface, ourmap):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        draw_map(surface,ourmap)
        # draw_grid(surface)
        pygame.display.update()

def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(constants.TITLE)
    surface.fill(constants.UGLY_PINK)
    return surface

# def read_map():
#     filepath = os.path.join("", constants.MAPFILE)
#     with open(filepath, 'r') as f:
#         world_map = f.readlines()
#     world_map = [line.strip() for line in world_map]
#     print(world_map)
#     print(type(world_map[0]))
#     print(len(world_map[0]))
#     return (world_map)

def main():
    # world_map = read_map()
    surface = initialize_game()


    ourmap= [[0 for x in range(w)] for y in range(h)]
    print(ourmap)
    game_loop(surface, ourmap)


if __name__=="__main__":
    main()
x=3
y=2
ourmap=[]
for i in range(x):
    ourmap[i]=[]
    for j in range(y):
        ourmap[i][j]=0