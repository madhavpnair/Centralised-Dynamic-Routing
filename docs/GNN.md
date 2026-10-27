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
- Line graph : each road segment (edge) will be a node
- feature vector : [speed, day-of-week, time, weather, length, lane count,..]
- estimated travel time = length of the road segment / predicted average speed
- Datasets to look for : 
    - MMTD Madrid (Zenodo)
    - METR-LA or PEMS-BAY for benchmarking
    - Smart City Traffic & Urban Mobility (Kaggle) (Synthetic)
    - Urban Traffic Congestion Prediction, Multi-City (Kaggle) (Synthetic)

### Message Passing
```
Message -> Aggregate -> Update -> Repeat k layers (each node now sees k hops away)
```
- Each node updates its own representation by collecting information from its neighbors and combining it with what it already knows

```
new_state(v) = UPDATE( own_state(v), AGGREGATE( MESSAGE(u) for each neighbor u of v ) )
```