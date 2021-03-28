# Indiana-Jones
Indiana-Jones is a maze explorer. He will move around and explore the maze. He'll stop when he's explored it all. 

Indy spawns in a random cell facing a random direction. Then he will try to move forward. If forward is blocked he'll move left, then right and lastly backwards. When he moves he'll also discover the adjacent cells. If there are more adjacent cells to move to than one, they'll be added to a list of available cells to explore in the future. If all of the adjacent cells are either already explored or unavailable Indy will chose a cell to move to in the list of explorable cells. He'll chose the one with the shortest path to it.

There can be more than one Indy! They'll all work as a group and share explored cells among themselves.

# Requirements
* [Opencv](https://opencv.org/)
* [Numpy](https://numpy.org/)
* [Networkx](https://networkx.org/)
