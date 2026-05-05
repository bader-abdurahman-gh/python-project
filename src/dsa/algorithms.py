from collections import deque
from typing import Any, Callable, Generator, Optional, Union

__all__: list[str] = [
    "linear_search",
    "binary_search",
    "interpolation_search",
    "depth_first_search",
    "breadth_first_search",
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort"
]

_identity: Callable[[Any], Any] = lambda x: x


# =========================
# Searching Algorithms
# =========================

def linear_search(iterable: Any, x: Any, /, start: int = 0, end: Optional[int] = None) -> int:
    """Search for a value in an iterable using linear search (sequential search).

    Linear search examines each element sequentially until the target is found
    or the end is reached. Works on both sorted and unsorted data.

    Time Complexity:
        - Worst case: O(n)
        - Best case: O(1)
        - Average case: O(n)

    Space Complexity: O(1)

    Args:
        iterable: A sequence (list, tuple, string, etc.) to search in.
        x: The value to search for.
        start: The starting index for the search (default: 0).
        end: The ending index for the search (exclusive, default: len(iterable)).

    Returns:
        int: The index of the first occurrence of x.

    Raises:
        IndexError: If start or end are out of valid range.
        ValueError: If x is not found in the iterable.

    Examples:
        >>> linear_search([1, 3, 5, 7, 9], 5)
        2
        >>> linear_search(['a', 'b', 'c', 'd'], 'b')
        1
        >>> linear_search([1, 2, 3], 5)  # Raises ValueError
    """
    if end is None:
        end = len(iterable)

    if start < 0 or end > len(iterable):
        raise IndexError("start/end out of range")

    for i in range(start, end):
        if iterable[i] == x:
            return i

    raise ValueError(f"{x!r} is not in iterable")


def binary_search(iterable: Any, x: Any, /, start: int = 0, end: Optional[int] = None) -> int:
    """Search for a value in a sorted iterable using binary search.

    Binary search divides the search interval in half repeatedly, eliminating
    half of the remaining elements with each comparison. Requires the iterable
    to be sorted.

    Time Complexity:
        - Worst case: O(log n)
        - Best case: O(1)
        - Average case: O(log n)

    Space Complexity: O(1)

    Args:
        iterable: A sorted sequence to search in.
        x: The value to search for.
        start: The starting index for the search (default: 0).
        end: The ending index for the search (exclusive, default: len(iterable)).

    Returns:
        int: The index of x.

    Raises:
        IndexError: If start or end are out of valid range.
        ValueError: If x is not found in the iterable.

    Examples:
        >>> binary_search([1, 3, 5, 7, 9, 11], 7)
        3
        >>> binary_search([1, 2, 3, 4, 5], 1)
        0
        >>> binary_search([1, 3, 5, 7], 4)  # Raises ValueError

    Note:
        The iterable must be sorted in ascending order for correct results.
    """
    if end is None:
        end = len(iterable)

    if start < 0 or end > len(iterable):
        raise IndexError("start/end out of range")

    while start < end:
        mid = (start + end) // 2

        if iterable[mid] < x:
            start = mid + 1
        else:
            end = mid

    if start < len(iterable) and iterable[start] == x:
        return start

    raise ValueError(f"{x!r} is not in iterable")


def interpolation_search(iterable: Any, x: Any, /, start: int = 0, end: Optional[int] = None) -> int:
    """Search for a value in a sorted iterable using interpolation search.

    Interpolation search estimates the position of the target value based on
    its value relative to the range of values. Works best on uniformly
    distributed sorted data. Falls back to binary search behavior on
    non-uniform distributions.

    Time Complexity:
        - Best case (uniform distribution): O(log log n)
        - Worst case (non-uniform distribution): O(n)
        - Average case (uniform distribution): O(log log n)

    Space Complexity: O(1)

    Args:
        iterable: A sorted sequence to search in.
        x: The value to search for.
        start: The starting index for the search (default: 0).
        end: The ending index for the search (exclusive, default: len(iterable)).

    Returns:
        int: The index of x.

    Raises:
        IndexError: If start or end are out of valid range.
        ValueError: If x is not found in the iterable.

    Examples:
        >>> interpolation_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 7)
        6
        >>> interpolation_search([10, 20, 30, 40, 50], 30)
        2

    Note:
        The iterable must be sorted in ascending order. Performance is optimal
        on uniformly distributed data (e.g., numeric sequences with consistent gaps).
    """
    if end is None:
        end = len(iterable)

    if start < 0 or end > len(iterable):
        raise IndexError("start/end out of range")

    while start < end and iterable[start] <= x <= iterable[end - 1]:
        low_val = iterable[start]
        high_val = iterable[end - 1]

        if low_val == high_val:
            if low_val == x:
                return start
            break

        probe = start + int((end - start - 1) * (x - low_val) / (high_val - low_val))

        probe = max(start, min(probe, end - 1))

        if iterable[probe] < x:
            start = probe + 1
        elif iterable[probe] > x:
            end = probe
        else:
            return probe

    raise ValueError(f"{x!r} is not in iterable")


def depth_first_search(
        structure: Any,
        start: Any,
        target: Any,
        /,
        *,
        neighbors: Optional[Callable[[Any, Any], Generator[Any, None, None]]] = None,
        value: Optional[Callable[[Any], Any]] = None
) -> list[Any]:
    """Find a path from start to target using depth-first search (DFS).

    Depth-first search explores as far as possible along each branch before
    backtracking. Uses a stack (LIFO) to manage the frontier. Automatically
    detects the neighbor function for common graph and tree structures.

    Time Complexity: O(V + E), where V is vertices and E is edges.
    Space Complexity: O(V) for the visited set and stack.

    Args:
        structure: A graph or tree structure to search. Can be:
            - AdjacencyList or AdjacencyMatrix (graph)
            - BinaryTree or TreeNode (tree)
        start: The starting node/vertex.
        target: The value to search for.
        neighbors: Optional callable that takes (structure, node) and yields neighbors.
            If not provided, auto-detects based on structure type.
        value: Optional callable to extract the value from a node.
            If not provided, uses node.value attribute or node itself.

    Returns:
        list[Any]: A list representing the path from start to target
            (as node values/identifiers).

    Raises:
        TypeError: If structure type is not recognized and neighbors is not provided.
        ValueError: If target is not reachable from start, or if a node is not in the structure.

    Examples:
        >>> # Graph example with AdjacencyList
        >>> graph = AdjacencyList(['A', 'B', 'C', 'D'])
        >>> graph.add_edge('A', 'B')
        >>> graph.add_edge('A', 'C')
        >>> graph.add_edge('B', 'D')
        >>> depth_first_search(graph, 'A', 'D')
        ['A', 'B', 'D']

    Note:
        - DFS does not guarantee the shortest path.
        - Auto-detection works with AdjacencyList, AdjacencyMatrix, and trees.
        - The order of returned path depends on the order neighbors are yielded.
    """
    if value is None:
        value = lambda x: getattr(x, "value", x)

    # --- Auto-detect neighbors ---
    if neighbors is None:
        if hasattr(structure, "_adj"):  # AdjacencyList
            neighbors = lambda g, v: (n for n, _ in g._adj[v])
        elif hasattr(structure, "_matrix"):  # AdjacencyMatrix
            neighbors = lambda g, v: (
                g._vertices[j]
                for j, w in enumerate(g._matrix[g._index[v]])
                if w != 0
            )
        elif hasattr(structure, "root"):  # Tree
            neighbors = lambda g, node: (
                child for child in (node.left, node.right) if child
            )
            start = structure.root
        else:
            raise TypeError("Unsupported structure or missing neighbors function")

    visited: set[Any] = set()
    stack: list[tuple[Any, list[Any]]] = [(start, [value(start)])]

    while stack:
        node, path = stack.pop()

        if value(node) == target:
            return path

        if node in visited:
            continue

        visited.add(node)

        try:
            for neighbor in neighbors(structure, node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [value(neighbor)]))
        except KeyError:
            raise ValueError(f"{node!r} is not in structure")

    raise ValueError(f"{target!r} is not reachable")


def breadth_first_search(
        structure: Any,
        start: Any,
        target: Any,
        /,
        *,
        neighbors: Optional[Callable[[Any, Any], Generator[Any, None, None]]] = None,
        value: Optional[Callable[[Any], Any]] = None
) -> list[Any]:
    """Find the shortest path from start to target using breadth-first search (BFS).

    Breadth-first search explores all nodes at the current depth before moving
    to nodes at the next depth. Uses a queue (FIFO) to manage the frontier.
    Guarantees the shortest path in unweighted graphs. Automatically detects
    the neighbor function for common graph and tree structures.

    Time Complexity: O(V + E), where V is vertices and E is edges.
    Space Complexity: O(V) for the visited set and queue.

    Args:
        structure: A graph or tree structure to search. Can be:
            - AdjacencyList or AdjacencyMatrix (graph)
            - BinaryTree or TreeNode (tree)
        start: The starting node/vertex.
        target: The value to search for.
        neighbors: Optional callable that takes (structure, node) and yields neighbors.
            If not provided, auto-detects based on structure type.
        value: Optional callable to extract the value from a node.
            If not provided, uses node.value attribute or node itself.

    Returns:
        list[Any]: A list representing the shortest path from start to target
            (as node values/identifiers).

    Raises:
        TypeError: If structure type is not recognized and neighbors is not provided.
        ValueError: If target is not reachable from start, or if a node is not in the structure.

    Examples:
        >>> # Graph example with AdjacencyList
        >>> graph = AdjacencyList(['A', 'B', 'C', 'D', 'E'])
        >>> graph.add_edge('A', 'B')
        >>> graph.add_edge('A', 'C')
        >>> graph.add_edge('B', 'D')
        >>> graph.add_edge('C', 'D')
        >>> breadth_first_search(graph, 'A', 'D')
        ['A', 'B', 'D']  # or ['A', 'C', 'D'] (shortest path of length 2)

    Note:
        - BFS guarantees the shortest path in unweighted graphs.
        - Auto-detection works with AdjacencyList, AdjacencyMatrix, and trees.
        - For weighted graphs, use Dijkstra'q algorithm instead.
    """
    if value is None:
        value = lambda x: getattr(x, "value", x)

    # --- Auto-detect neighbors ---
    if neighbors is None:
        if hasattr(structure, "_adj"):  # AdjacencyList
            neighbors = lambda g, v: (n for n, _ in g._adj[v])
        elif hasattr(structure, "_matrix"):  # AdjacencyMatrix
            neighbors = lambda g, v: (
                g._vertices[j]
                for j, w in enumerate(g._matrix[g._index[v]])
                if w != 0
            )
        elif hasattr(structure, "root"):  # Tree
            neighbors = lambda g, node: (
                child for child in (node.left, node.right) if child
            )
            start = structure.root
        else:
            raise TypeError("Unsupported structure or missing neighbors function")

    visited: set[Any] = {start}
    queue: deque[tuple[Any, list[Any]]] = deque([(start, [value(start)])])

    while queue:
        node, path = queue.popleft()

        if value(node) == target:
            return path

        try:
            for neighbor in neighbors(structure, node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [value(neighbor)]))
        except KeyError:
            raise ValueError(f"{node!r} is not in structure")

    raise ValueError(f"{target!r} is not reachable")


# =========================
# Sorting Algorithms
# =========================

def bubble_sort(
        iterable: Any,
        *,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False
) -> list[Any]:
    """Sort an iterable using bubble sort algorithm.

    Bubble sort repeatedly steps through the list, compares adjacent elements,
    and swaps them if they are in the wrong order. The algorithm continues
    until no more swaps are needed. Known for poor performance on large datasets.

    Time Complexity:
        - Worst case: O(n²)
        - Best case: O(n) - when list is already sorted
        - Average case: O(n²)

    Space Complexity: O(1) - only swaps in place (before converting to list)

    Args:
        iterable: A sequence to sort.
        key: Optional callable that takes an element and returns a value to sort by.
            If not provided, elements are compared directly.
        reverse: If True, sort in descending order; if False, ascending (default: False).

    Returns:
        list[Any]: A new sorted list.

    Raises:
        TypeError: If iterable is not iterable.

    Examples:
        >>> bubble_sort([3, 1, 4, 1, 5, 9])
        [1, 1, 3, 4, 5, 9]
        >>> bubble_sort([3, 1, 4], reverse=True)
        [4, 3, 1]
        >>> bubble_sort(['apple', 'pie', 'a'], key=len)
        ['a', 'pie', 'apple']

    Note:
        Bubble sort is mainly used for educational purposes. Use Python'q built-in
        sorted() or list.sort() for production code.
    """
    try:
        iterable = list(iterable)
    except TypeError:
        raise TypeError("bubble_sort expects an iterable")

    key = key or _identity

    keys: list[Any] = [key(item) for item in iterable]
    n: int = len(iterable)

    for i in range(n - 1):
        swapped: bool = False

        for j in range(n - 1 - i):
            if (keys[j] > keys[j + 1] and not reverse) or (
                    keys[j] < keys[j + 1] and reverse
            ):
                keys[j], keys[j + 1] = keys[j + 1], keys[j]
                iterable[j], iterable[j + 1] = iterable[j + 1], iterable[j]
                swapped = True

        if not swapped:
            break

    return iterable


def selection_sort(
        iterable: Any,
        *,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False
) -> list[Any]:
    """Sort an iterable using selection sort algorithm.

    Selection sort divides the input into a sorted and unsorted region. It
    repeatedly finds the minimum (or maximum for reverse) element from the
    unsorted region and moves it to the sorted region.

    Time Complexity:
        - Worst case: O(n²)
        - Best case: O(n²)
        - Average case: O(n²)

    Space Complexity: O(1) - only swaps in place (before converting to list)

    Args:
        iterable: A sequence to sort.
        key: Optional callable that takes an element and returns a value to sort by.
            If not provided, elements are compared directly.
        reverse: If True, sort in descending order; if False, ascending (default: False).

    Returns:
        list[Any]: A new sorted list.

    Raises:
        TypeError: If iterable is not iterable.

    Examples:
        >>> selection_sort([3, 1, 4, 1, 5])
        [1, 1, 3, 4, 5]
        >>> selection_sort(['dog', 'cat', 'a'], key=len)
        ['a', 'cat', 'dog']
        >>> selection_sort([1, 2, 3], reverse=True)
        [3, 2, 1]

    Note:
        Selection sort makes fewer swaps than bubble sort but still has O(n²)
        time complexity. Better for situations where swap operations are expensive.
    """
    try:
        iterable = list(iterable)
    except TypeError:
        raise TypeError("selection_sort expects an iterable")

    key = key or _identity

    keys: list[Any] = [key(item) for item in iterable]
    n: int = len(iterable)

    for i in range(n - 1):
        selected: int = i

        for j in range(i + 1, n):
            if (keys[j] < keys[selected] and not reverse) or (
                    keys[j] > keys[selected] and reverse
            ):
                selected = j

        if selected != i:
            keys[i], keys[selected] = keys[selected], keys[i]
            iterable[i], iterable[selected] = iterable[selected], iterable[i]

    return iterable


def insertion_sort(
        iterable: Any,
        *,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False
) -> list[Any]:
    """Sort an iterable using insertion sort algorithm.

    Insertion sort builds the sorted array one node at a time. It iterates
    through an input list, and for each element, finds the correct position
    in the sorted portion and inserts it. Efficient for small datasets and
    nearly sorted data.

    Time Complexity:
        - Worst case: O(n²)
        - Best case: O(n) - when list is already sorted
        - Average case: O(n²)

    Space Complexity: O(1) - only shifts elements in place

    Args:
        iterable: A sequence to sort.
        key: Optional callable that takes an element and returns a value to sort by.
            If not provided, elements are compared directly.
        reverse: If True, sort in descending order; if False, ascending (default: False).

    Returns:
        list[Any]: A new sorted list.

    Raises:
        TypeError: If iterable is not iterable.

    Examples:
        >>> insertion_sort([3, 1, 4, 1, 5])
        [1, 1, 3, 4, 5]
        >>> insertion_sort([5, 2, 8, 1], reverse=True)
        [8, 5, 2, 1]
        >>> insertion_sort(['apple', 'pie', 'a'], key=len)
        ['a', 'pie', 'apple']

    Note:
        Insertion sort performs well on nearly sorted data and is often used
        as the final step in hybrid sorting algorithms like Timsort.
    """
    try:
        iterable = list(iterable)
    except TypeError:
        raise TypeError("insertion_sort expects an iterable")

    key = key or _identity

    keys: list[Any] = [key(item) for item in iterable]

    for i in range(1, len(iterable)):
        temp_key: Any = keys[i]
        temp_item: Any = iterable[i]
        j: int = i - 1

        if not reverse:
            while j >= 0 and keys[j] > temp_key:
                keys[j + 1] = keys[j]
                iterable[j + 1] = iterable[j]
                j -= 1
        else:
            while j >= 0 and keys[j] < temp_key:
                keys[j + 1] = keys[j]
                iterable[j + 1] = iterable[j]
                j -= 1

        keys[j + 1] = temp_key
        iterable[j + 1] = temp_item

    return iterable


def merge_sort(
        iterable: Any,
        *,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False
) -> list[Any]:
    """Sort an iterable using merge sort algorithm (divide-and-conquer).

    Merge sort divides the input in half recursively until single elements
    remain, then merges the sorted halves back together. Guarantees O(n log n)
    time complexity and maintains stability.

    Time Complexity:
        - Worst case: O(n log n)
        - Best case: O(n log n)
        - Average case: O(n log n)

    Space Complexity: O(n) - requires additional space for merging

    Args:
        iterable: A sequence to sort.
        key: Optional callable that takes an element and returns a value to sort by.
            If not provided, elements are compared directly.
        reverse: If True, sort in descending order; if False, ascending (default: False).

    Returns:
        list[Any]: A new sorted list.

    Raises:
        TypeError: If iterable is not iterable.

    Examples:
        >>> merge_sort([3, 1, 4, 1, 5, 9])
        [1, 1, 3, 4, 5, 9]
        >>> merge_sort(['apple', 'pie', 'a'], key=len)
        ['a', 'pie', 'apple']
        >>> merge_sort([5, 2, 3], reverse=True)
        [5, 3, 2]

    Note:
        Merge sort is stable (preserves relative order of equal elements) and
        guarantees O(n log n) time. The main drawback is O(n) extra space usage.
        Good choice for external sorting and when stability is important.
    """
    try:
        iterable = list(iterable)
    except TypeError:
        raise TypeError("merge_sort expects an iterable")

    key = key or _identity

    paired: list[tuple[Any, Any]] = [(key(item), item) for item in iterable]

    def merge(left: list[tuple[Any, Any]], right: list[tuple[Any, Any]]) -> list[tuple[Any, Any]]:
        """Merge two sorted lists maintaining order and respecting reverse flag.

        Args:
            left: First sorted list of (key, node) tuples.
            right: Second sorted list of (key, node) tuples.

        Returns:
            list[tuple[Any, Any]]: Merged sorted list.
        """
        result: list[tuple[Any, Any]] = []
        i: int = 0
        j: int = 0

        while i < len(left) and j < len(right):
            if (left[i][0] <= right[j][0] and not reverse) or (
                    left[i][0] > right[j][0] and reverse
            ):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _merge_sort(arr: list[tuple[Any, Any]]) -> list[tuple[Any, Any]]:
        """Recursively divide and sort using merge sort.

        Args:
            arr: List of (key, node) tuples to sort.

        Returns:
            list[tuple[Any, Any]]: Sorted list of tuples.
        """
        if len(arr) <= 1:
            return arr

        mid: int = len(arr) // 2
        left: list[tuple[Any, Any]] = _merge_sort(arr[:mid])
        right: list[tuple[Any, Any]] = _merge_sort(arr[mid:])

        return merge(left, right)

    sorted_pairs: list[tuple[Any, Any]] = _merge_sort(paired)
    return [item for _, item in sorted_pairs]


def quick_sort(
        iterable: Any,
        *,
        key: Optional[Callable[[Any], Any]] = None,
        reverse: bool = False
) -> list[Any]:
    """Sort an iterable using quick sort algorithm (divide-and-conquer).

    Quick sort selects a pivot element and partitions the list into elements
    less than and greater than the pivot, then recursively sorts the partitions.
    Uses median-of-three pivot selection for improved performance.

    Time Complexity:
        - Worst case: O(n²) - when pivots are poorly chosen
        - Best case: O(n log n) - with good pivot selection
        - Average case: O(n log n)

    Space Complexity: O(log n) - due to recursion stack

    Args:
        iterable: A sequence to sort.
        key: Optional callable that takes an element and returns a value to sort by.
            If not provided, elements are compared directly.
        reverse: If True, sort in descending order; if False, ascending (default: False).

    Returns:
        list[Any]: A new sorted list.

    Raises:
        TypeError: If iterable is not iterable.

    Examples:
        >>> quick_sort([3, 1, 4, 1, 5, 9])
        [1, 1, 3, 4, 5, 9]
        >>> quick_sort(['apple', 'pie', 'a'], key=len)
        ['a', 'pie', 'apple']
        >>> quick_sort([5, 2, 3, 1], reverse=True)
        [5, 3, 2, 1]

    Note:
        Quick sort is not stable (may change relative order of equal elements).
        Uses median-of-three pivot selection to reduce worst-case probability.
        Good practical choice for in-place sorting of large datasets.
    """
    try:
        iterable = list(iterable)
    except TypeError:
        raise TypeError("quick_sort expects an iterable")

    key = key or _identity
    keys: list[Any] = [key(item) for item in iterable]

    def median_of_three(low: int, mid: int, high: int) -> int:
        """Find the median of three elements and return its index.

        Args:
            low: Index of first element.
            mid: Index of middle element.
            high: Index of last element.

        Returns:
            int: Index of the median element.
        """
        trio: list[tuple[Any, int]] = [(keys[low], low), (keys[mid], mid), (keys[high], high)]
        trio.sort(key=lambda x: x[0])
        return trio[1][1]

    def partition(low: int, high: int) -> int:
        """Partition the array around a pivot using median-of-three selection.

        Args:
            low: Start index of partition range.
            high: End index of partition range.

        Returns:
            int: The final pivot index.
        """
        mid: int = (low + high) // 2
        pivot_index: int = median_of_three(low, mid, high)

        keys[pivot_index], keys[high] = keys[high], keys[pivot_index]
        iterable[pivot_index], iterable[high] = iterable[high], iterable[pivot_index]

        pivot_key: Any = keys[high]
        i: int = low - 1

        for j in range(low, high):
            if (keys[j] <= pivot_key and not reverse) or (
                    keys[j] >= pivot_key and reverse
            ):
                i += 1
                keys[i], keys[j] = keys[j], keys[i]
                iterable[i], iterable[j] = iterable[j], iterable[i]

        keys[i + 1], keys[high] = keys[high], keys[i + 1]
        iterable[i + 1], iterable[high] = iterable[high], iterable[i + 1]

        return i + 1

    def _quick_sort(low: int, high: int) -> None:
        """Recursively sort using quick sort on a range.

        Args:
            low: Start index of range to sort.
            high: End index of range to sort.
        """
        if low < high:
            pivot_index: int = partition(low, high)
            _quick_sort(low, pivot_index - 1)
            _quick_sort(pivot_index + 1, high)

    _quick_sort(0, len(iterable) - 1)
    return iterable