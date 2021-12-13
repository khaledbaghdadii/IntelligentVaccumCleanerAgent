import keras
from keras.engine import training
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.backend import reshape
from keras.utils.np_utils import to_categorical
from keras.models import model_from_json
from random import randint
import numpy as np

# n is number of columns
# m in number of rows
class SupervisedML:
    def __init__(self,n,m,cleaning_agent_pos,dirt_agent_pos,tiles_array,dirts_array_pos):
        self.n=n
        self.m=m
        self.cleaning_agent_pos=cleaning_agent_pos
        self.dirt_agent_pos=dirt_agent_pos
        self.tiles_array=tiles_array
        self.dirts_array_pos=dirts_array_pos

    def getModel(self):
        numCells = self.n*self.m
        outcomes = 2
        model = Sequential()
        model.add(Dense(300, activation='relu', input_shape=(numCells, )))
        model.add(Dropout(0.2))
        model.add(Dense(200, activation='relu'))
        model.add(Dense(100, activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(outcomes, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
        return model

    def evaluateMove(self,old_pos,new_pos):
        old_cleaning_agents_tiles=self.getCleaningAgents(old_pos)
        new_cleaning_agents_tiles=self.getCleaningAgents(old_pos)
        old_dirts=self.getDirts(old_pos)
        new_dirts=self.getDirts(new_pos)
        old_score=self.getScoreMulti(old_cleaning_agents_tiles,old_dirts)
        new_score=self.getScoreMulti(new_cleaning_agents_tiles,new_dirts)
        return new_score-old_score


    def generateDataset(self):
        dataX=[]
        dataY=[]
        for i in range(10000):
            rand_x=randint(0,self.m-1)
            rand_y=randint(0,self.n-1)
            dirts=self.generateRandomDirts(5,(rand_x,rand_y))
            cleaning_agent_tiles=[self.tiles_array[rand_x][rand_y]]
            board=self.create_board(cleaning_agent_tiles,dirts)
            score=self.getScoreMulti(cleaning_agent_tiles,dirts)
            board=np.array(board).reshape((-1, self.n*self.m))
            dataX.append(board)
            if score<-10:
                dataY.append(np.array([1,0]))
            else:
                dataY.append(np.array([0,1]))

        trainNum = int(len(dataX) * 0.8)
        return (dataX[:trainNum], dataX[trainNum:], dataY[:trainNum], dataY[trainNum:])




    def trainModel(self):
        X_train, X_test, y_train, y_test = self.generateDataset()
        model = self.getModel()
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=100)
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("model.h5")
        print("Saved model to disk")



    def create_board(self,cleaning_agents_tile,dirts):
        board=[[0 for x in range(self.m)] for y in range(self.n)]

        for i in range(len(cleaning_agents_tile)):
            cleaning_agent_tile=cleaning_agents_tile[i]
            board[cleaning_agent_tile.x][cleaning_agent_tile.y]=1
        for i in range(len(dirts)):
            dirt=dirts[i]
            board[dirt[0]][dirt[1]]=-1
        return board





    def generateRandomDirts(self,n,vacuum_pos):
        dirts=[]
        for i in range(n):
            rand_x=randint(0,self.m-1)
            rand_y=randint(0,self.n-1)
            while((rand_x,rand_y) in dirts or (rand_x,rand_y)==vacuum_pos ):
                rand_x=randint(0,self.m-1)
                rand_y=randint(0,self.n-1)
            dirts.append((rand_x,rand_y))


    def getDistance(self,x1,y1,x2,y2):
        return abs(y2-y1)+abs(x2-x1)


    def getScoreMulti(self,cleaning_agents_tiles,dirts_array):
        score=0
        for cleaningAgentTile in cleaning_agents_tiles:
            for i in range(len(dirts_array)):
                dirt=dirts_array[i]

                dirtX=dirt[0]
                dirtY=dirt[1]
                #vacuum_position is a tuple in the form of (x,y)
                vacuumX=cleaningAgentTile.x
                vacuumY=cleaningAgentTile.y
                score=score+self.getDistance(vacuumX,vacuumY,dirtX,dirtY)
        return score

        #empty tiles is 0
        #cleaning agent is 1
        #dirt  is -1
        pass

    def getCleaningAgents(self,positions):
        cleaning_agents=[]
        for i in range(len(positions)):
            for j in range(len(positions[0])):
                if positions[i][j]==1:
                    cleaning_agent=self.tiles_array[i][j]
                    cleaning_agents.append(cleaning_agent)
        return cleaning_agent
    def getDirts(self,positions):
        dirts=[]
        for i in range(len(positions)):
            for j in range(len(positions[0])):
                if positions[i][j]==-1:
                    dirt=self.tiles_array[i][j]
                    dirts.append(dirt)
        return dirts







