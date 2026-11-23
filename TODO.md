## Immediate goals
- [x] edge weight decrementation algorithm
- [ ] get dataset for GNN
- [ ] update GNN.md with plans 
    - [ ] which GNN model
    - [ ] how and where to train
- [x] add test suite for algorithms
- [ ] update readme for incremental algorithms

## Final goals
- [ ] fully functional PoC prototype
- [ ] measure improvement in performance compared to traditional/existing algorithms
- [ ] check adaptability

## Features in the final demo GUI
- [ ] add vehicles in a road : should dynamically change the feature input for the road, automatically run the GNN and render the new edge weight
- [ ] represent the congestion level of each road in some colour
- [ ] highlight the shortest route of a vehicle when asked : run graph solver and fetch results
- [ ] change weather conditions in a road : same as point 1
- [ ] backend should run GNN and get inference for any change in feature input for any road 