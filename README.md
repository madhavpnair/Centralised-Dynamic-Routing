# Centralised-Dynamic-Routing
Proof of Concept for Centralised Routing using dynamic edge weights predicted by a GNN model and graph solver for successive shortest path algorithm

Click to go to the [Overleaf Project](https://www.overleaf.com/read/tjqdtrbgdsqr#af76e8)

## Overview
### Problem Statement
- `N` vehicles want to go from A to B. There can be many routes connecting A and B.
- Minimize the time taken by all vehicles to reach the destination (**System Optimal**)
### Model
- GNN model predicts the travel time for each road (edge)
- Here the edge weights are not mere static physical length of the road segment but the estimated travel time dynamically changing subject to potential factors including but not limited to
    - Climate
    - Date and Time
    - Current congestion
    - Geographic features
    - Number of outgoing and ingoing roads
- The model is trained using above input features and ground truth
### Graph Solver
- Once we get the edge weights, we need to direct vehicles to paths
- This is done by successive shortest path algorithm
- We have to add congestion penalty to a path when a vehicle is allowed to travel on that route

