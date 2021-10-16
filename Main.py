from Game import Game
from BFS import BFS
from time import sleep
def main():
    mygame = Game(7,7)
    # mygame.read_data()
    mygame.main()
    bfs=BFS(mygame.Tiles.tiles)
    bfs.clean(0,0)
    for i in bfs.path:
        if(len(i)!=0):
            previousTile=i[0]
            if(len(i)>1):
                for j in i[1:]:
                    dx=j.x-previousTile.x
                    dy=j.y-previousTile.y
                    #call move vacuum cleaner method
                    mygame.VacuumCleaner.move(dx,dy)
                    mygame.draw()
                    sleep(0.5)
                    previousTile=j

if __name__ == "__main__":
    main()
