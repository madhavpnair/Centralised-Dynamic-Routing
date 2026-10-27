## GNN
- GNN stands for Graph Neural Network
- In this project, we will be using GNN to predict the edge weights which is equivalent to the travel time between two cities

The tentative tech stack is described below
### `Spatio-Temporal GNN` (STGNN)
- travel time depends on
    1. **Space** : congestion spreads between connected roads
    2. **Time** : Date, Time, Daily and Weekly cycles, recent trend, weather changes
- graph component handles space and a temporal component handles time
- Main model : [`Graph WaveNet`](https://arxiv.org/abs/1906.00121)
- feature vector : [speed, day-of-week, time, weather, length, lane count,..]
- estimated travel time = length of the road segment / predicted average speed
- Datasets to look for : 
    - MMTD Madrid (Zenodo)
    - METR-LA or PEMS-BAY for benchmarking
    - Smart City Traffic & Urban Mobility (Kaggle) (Synthetic)
    - Urban Traffic Congestion Prediction, Multi-City (Kaggle) (Synthetic)

#### Two graphs
1. **Routing graph** - intersections are nodes and roads are edges. Dynamic SSSP runs on this.
2. **Line graph** 
                  - for the GNN. roads are nodes. GNN runs on this.<br>
                  - GNN produces one output per node - travel time or avg.speed of that road<br>
                  - we write this onto the matching edge of the routing graph as its edge weight

### Message Passing
```
Message -> Aggregate -> Update -> Repeat k layers (each node now sees k hops away)
```
- Each node updates its own representation by collecting information from its neighbors and combining it with what it already knows

```
new_state(v) = UPDATE( own_state(v), AGGREGATE( MESSAGE(u) for each neighbor u of v ) )
```