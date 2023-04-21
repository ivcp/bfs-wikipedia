# BFS Wikipedia Visualized

All clicks lead to Rome. Starting from any Wikipedia article, what's the least amount of clicks to reach the page for Rome?

This solution uses breadth-first search algorithm to find the shortest path.
Crawling the tree of wiki pages is visualized with Tkinter library.
This is achieved by writing the bfs method as a generator function that yields the path at every step and displaying it on the canvas.
Once the path is found the elapsed time is shown.
It can take a while to finish. For example, going from "Python (programming language)" to "Rome" took two minutes.

[bfs_wikipedia.webm](https://user-images.githubusercontent.com/38633663/233460677-99cf26d6-b261-44c3-af98-64bdeb88e68b.webm)

### Prerequisites

- Python3.x
- ttkthemes

### How to run

1. clone repository
2. to start run `python main.py`
