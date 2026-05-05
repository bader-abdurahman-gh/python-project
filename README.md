# Data Structures & Algorithms (DSA) Project

A comprehensive Python implementation of fundamental data structures and algorithms with detailed documentation and type hints.

## Features

### Data Structures
- **Stack** — Last-In-First-Out (LIFO) collection
- **Queue** — First-In-First-Out (FIFO) collection
- **Heap** — Priority queue implementation
- **Linked Lists** — Singly and Doubly linked list implementations
- **Hash Table** — Key-value storage with collision handling
- **Graphs** — Adjacency Matrix and Adjacency List representations
- **Binary Trees** — Binary Tree and Binary Search Tree implementations

### Algorithms
- **Searching** — Linear, Binary, and Interpolation search
- **Sorting** — Bubble, Selection, Insertion, Merge, and Quick sort
- **Graph Traversal** — Depth-First Search (DFS) and Breadth-First Search (BFS)

### Utilities
- **Logging Tools** — Structured logging with file and console output, log filtering, and parsing

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/bader-abdurahman-gh/python-project.git
cd python-project
```

## Usage

### Using Data Structures

```python
from dsa import Stack, Queue, BinarySearchTree

# Stack example
stack = Stack([1, 2, 3])
stack.push(4)
print(stack.pop())  # Output: 4

# Queue example
queue = Queue([1, 2, 3])
queue.enqueue(4)
print(queue.dequeue())  # Output: 1

# Binary Search Tree example
bst = BinarySearchTree()
bst.insert(5)
bst.insert(3)
bst.insert(7)
print(bst.search(3))  # Output: True
```

### Using Algorithms

```python
from dsa import binary_search, merge_sort

# Binary search (requires sorted data)
result = binary_search([1, 3, 5, 7, 9], 5)
print(result)  # Output: 2

# Merge sort
sorted_list = merge_sort([5, 2, 8, 1, 9])
print(sorted_list)  # Output: [1, 2, 5, 8, 9]
```

### Using Logging Tools

```python
from logging_tools import setup_logging, load_logs, filter_logs

# Setup logging
setup_logging()

# Load and filter logs
all_logs = load_logs()
error_logs = filter_logs("ERROR", filter_by="level")
print(f"Found {len(error_logs)} error logs")
```

## Project Structure

```
python-project/
├── src/
│   ├── dsa/
│   │   ├── __init__.py
│   │   ├── data_structures.py
│   │   └── algorithms.py
│   ├── logging_tools.py
│   └── main.py
├── data/
│   ├── sample.yaml
│   └── table.csv
├── docs/
│   └── text.md
└── README.md
```