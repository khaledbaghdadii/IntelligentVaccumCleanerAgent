# IntelligentVaccumCleanerAgent



## Description
This is an intelligent vacuum cleaner was implemented that cleans the dirty tiles according to different searching algorithms. It works in a static environment were dirts are preplaced, and in non-static environment where there is other agents in the environment that are creating dirts.
It is a multi-agent envrionment as it can be extended to add multiple vacuum cleaners and multiple dirt producing agents.
The environment can be fully visible and partially visible where an agent can only view a specific set of tiles around it.

## Introduction

Making decisions and performing services based on the environment is what intelligent agents do. In the past few years, designing and implementing such agents was very important in facilitating human lives and showing how technology can go further. The aim is to design an intelligent vacuum cleaner, which its objective is to clean all the dirty tiles without human intervention, taking into consideration different searching algorithm and measuring their corresponding performance.
In a real-life scenario, there might exist multiple cleaning agents and multiple dirt agents that throw dirt. That's why the scenario is extended to a multi-agent scenario, where vacuum cleaners can clean intelligently, and the dirt agents can either randomly throw dirt or throw dirt intelligently. 

## Algorithms Used
</br> 

**Single Agent Scenario**
<br />
-Modified Breadth First Search
<br />
-Dijkstra’s Algorithm
<br />
-A* Algorithm
<br />
-Combined Traveled Salesman Problem (TSP) and Best First Search Algorithm)

<br />
<br />

**Multi Agent Scenario**
<br />
-Modified MiniMax<br />
-Modified Alphabeta Pruning <br />

## Technologies Used
<br />
Python and PyGame

## Screenshots
![Multi Agent](https://i.ibb.co/NxWJ4HQ/multiagent.png)

