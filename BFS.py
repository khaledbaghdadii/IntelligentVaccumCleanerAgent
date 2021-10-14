from Tiles import Tiles
from Tiles import Tile
class BFS():
    def clean(self,tilesArray,agentX,agentY):
        queue=[]
        # prevTileArray=
        currentTile= tilesArray[agentX][agentY]

        for i in range(len(tilesArray)):
            for j in range(len(tilesArray[0])):
                self.Tiles.tiles[i][j].printTile()

    # def getNeighbours(self, currentTile,tilesArray):
    #     if(!currentTile.hasWallLeft):
    #         a = currentTile.x-1
    #         b =
