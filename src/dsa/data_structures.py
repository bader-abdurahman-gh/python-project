from collections import deque
from collections.abc import Callable, Iterable, Iterator, Sequence, MutableSequence
from typing import Any, Optional, Union, overload

__all__: list[str] = [
    "Stack",
    "Queue",
    "Heap",
    "SinglyLinkedList",
    "DoublyLinkedList",
    "HashTable",
    "AdjacencyMatrix",
    "AdjacencyList",
    "BinaryTree",
    "BinarySearchTree",
]

_sentinel: object = object()


# =========================
# Stacks
# =========================

class Stack:
    """A Last-In-First-Out (LIFO) data structure.

    A stack is a linear collection of elements where insertion and deletion
    occur at the same end, called the top. Elements are added and removed
    in reverse order (LIFO).

    Args:
        iterable: Optional iterable to initialize the stack with elements.

    Raises:
        TypeError: If iterable is provided but is not iterable.
    """

    def __init__(self, iterable: Optional[Iterable[Any]] = None) -> None:
        """Initialize a new Stack.

        Args:
            iterable: Optional iterable of items to populate the stack.

        Raises:
            TypeError: If iterable is provided but is not iterable.
        """
        try:
            self.__items: list[Any] = list(iterable or [])
        except TypeError:
            raise TypeError("'Stack' object must be initialized with an iterable")

    # --- Representation ---
    def __repr__(self) -> str:
        """Return a formal string representation of the Stack."""
        return f"Stack({self.__items})"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the Stack."""
        return str(self.__items)

    # --- Length ---
    def __len__(self) -> int:
        """Return the number of items in the stack."""
        return len(self.__items)

    # --- Iteration ---
    def __iter__(self) -> Iterator[Any]:
        """Iterate over items in the stack from bottom to top."""
        return iter(self.__items)

    # --- Indexing ---
    def __validate_top_index(self, index: int) -> int:
        """Validate that index accesses only the top of the stack.

        Args:
            index: The index to validate.

        Returns:
            int: The validated index.

        Raises:
            TypeError: If index is a slice.
            IndexError: If stack is empty or index doesn't point to the top.
        """
        if isinstance(index, slice):
            raise TypeError("'Stack' object does not support slicing")
        if not self.__items:
            raise IndexError("index out of range")
        if index not in (-1, len(self.__items) - 1):
            raise IndexError("access only allowed at the top of the stack")
        return index

    def __getitem__(self, index: int) -> Any:
        """Get the item at the top of the stack.

        Args:
            index: Must be -1 or the last valid index.

        Returns:
            Any: The item at the top of the stack.

        Raises:
            IndexError: If index doesn't point to the top.
        """
        index = self.__validate_top_index(index)
        return self.__items[index]

    def __setitem__(self, index: int, value: Any) -> None:
        """Set the item at the top of the stack.

        Args:
            index: Must be -1 or the last valid index.
            value: The new value to set.

        Raises:
            IndexError: If index doesn't point to the top.
        """
        index = self.__validate_top_index(index)
        self.__items[index] = value

    def __delitem__(self, index: int) -> None:
        """Delete the item at the top of the stack.

        Args:
            index: Must be -1 or the last valid index.

        Raises:
            IndexError: If index doesn't point to the top.
        """
        index = self.__validate_top_index(index)
        del self.__items[index]

    # --- Membership ---
    def __contains__(self, item: Any) -> bool:
        """Check if an item is in the stack."""
        return item in self.__items

    # --- Equality ---
    def __eq__(self, other: Any) -> bool:
        """Check equality with another Stack or iterable."""
        try:
            return self.__items == list(other)
        except TypeError:
            return False

    def __bool__(self) -> bool:
        """Return True if the stack is not empty."""
        return bool(self.__items)

    def __hash__(self) -> None:
        """Stacks are not hashable."""
        raise TypeError("unhashable type: 'Stack'")

    # --- Core Methods ---
    def append(self, item: Any) -> None:
        """Add an item onto the top of the stack."""
        self.__items.append(item)

    def pop(self, index: int = -1) -> Any:
        """Remove and return the item at the top of the stack.

        Args:
            index: Must be -1 or point to the top (default: -1).

        Returns:
            Any: The item removed from the top.

        Raises:
            IndexError: If stack is empty or index doesn't point to the top.
        """
        if not self.__items:
            raise IndexError("pop from empty stack")
        if index not in (-1, len(self.__items) - 1):
            raise IndexError("pop only allowed at the top of the stack")
        return self.__items.pop()

    def extend(self, items: Iterable) -> None:
        """Extend the stack with the items of an iterable."""
        self.__items.extend(items)

    def peek(self) -> Any:
        """Return the top item without removing it.

        Returns:
            Any: The top item.

        Raises:
            IndexError: If stack is empty.
        """
        if not self.__items:
            raise IndexError("peek from empty stack")
        return self.__items[-1]

    def clear(self) -> None:
        """Remove all items from the stack."""
        self.__items.clear()

    def copy(self) -> "Stack":
        """Create a shallow copy of the stack."""
        return Stack(self.__items.copy())

    def count(self, item: Any) -> int:
        """Count occurrences of an item in the stack."""
        return self.__items.count(item)

    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of an item.

        Raises:
            ValueError: If item is not in the stack.
        """
        if item not in self.__items:
            raise ValueError("item not in stack")
        return self.__items.index(item)


# =========================
# Queues
# =========================

class Queue:
    """A First-In-First-Out (FIFO) data structure.

    A queue is a linear collection of elements where insertions occur at one
    end (tail) and deletions occur at the other end (head). Elements are
    processed in the order they were added (FIFO).

    Args:
        iterable: Optional iterable to initialize the queue with elements.

    Raises:
        TypeError: If iterable is provided but is not iterable.
    """

    def __init__(self, iterable: Optional[Iterable[Any]] = None) -> None:
        """Initialize a new Queue.

        Args:
            iterable: Optional iterable of items to populate the queue.

        Raises:
            TypeError: If iterable is provided but is not iterable.
        """
        try:
            self.__items: deque[Any] = deque(iterable or [])
        except TypeError:
            raise TypeError("'Queue' object must be initialized with an iterable")

    # --- Representation ---
    def __repr__(self) -> str:
        """Return a formal string representation of the Queue."""
        return f"Queue({list(self.__items)})"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the Queue."""
        return str(list(self.__items))

    # --- Length ---
    def __len__(self) -> int:
        """Return the number of items in the queue."""
        return len(self.__items)

    # --- Iteration ---
    def __iter__(self) -> Iterator[Any]:
        """Iterate over items in the queue from head to tail."""
        return iter(self.__items)

    # --- Indexing ---
    def __validate_head_index(self, index: int) -> int:
        """Validate that index accesses only the head of the queue."""
        if isinstance(index, slice):
            raise TypeError("'Queue' object does not support slicing")
        if not self.__items:
            raise IndexError("index out of range")
        if index != 0:
            raise IndexError("access only allowed at the head of the queue")
        return index

    def __validate_tail_index(self, index: int) -> int:
        """Validate that index accesses only the tail of the queue."""
        if isinstance(index, slice):
            raise TypeError("'Queue' object does not support slicing")
        if not self.__items:
            raise IndexError("index out of range")
        if index not in (-1, len(self.__items) - 1):
            raise IndexError("access only allowed at the tail of the queue")
        return index

    def __getitem__(self, index: int) -> Any:
        """Get the item at the head of the queue.

        Args:
            index: Must be 0 to access the head.

        Returns:
            Any: The item at the head of the queue.

        Raises:
            IndexError: If index doesn't point to the head.
        """
        index = self.__validate_head_index(index)
        return self.__items[index]

    def __setitem__(self, index: int, value: Any) -> None:
        raise IndexError("queue does not support mutation")

    def __delitem__(self, index: int) -> None:
        """Delete the item at the head of the queue.

        Args:
            index: Must be 0 to access the head.

        Raises:
            IndexError: If index doesn't point to the head.
        """
        index = self.__validate_head_index(index)
        del self.__items[index]

    # --- Membership ---
    def __contains__(self, item: Any) -> bool:
        """Check if an item is in the queue."""
        return item in self.__items

    # --- Equality ---
    def __eq__(self, other: Any) -> bool:
        """Check equality with another Queue or iterable."""
        try:
            return self.__items == deque(other)
        except TypeError:
            return False

    def __bool__(self) -> bool:
        """Return True if the queue is not empty."""
        return bool(self.__items)

    def __hash__(self) -> None:
        """Queues are not hashable."""
        raise TypeError("unhashable type: 'Queue'")

    # --- Core Methods ---
    def append(self, item: Any) -> None:
        """Add an item to the tail of the queue."""
        self.__items.append(item)

    def pop(self) -> Any:
        """Remove and return the item at the head of the queue.

        Returns:
            Any: The item removed from the head.

        Raises:
            IndexError: If queue is empty.
        """
        if not self.__items:
            raise IndexError("pop from empty queue")
        return self.__items.popleft()

    def extend(self, items: Iterable) -> None:
        """Extend the queue with the items of an iterable."""
        self.__items.extend(items)

    def peek(self) -> Any:
        """Return the head item without removing it.

        Returns:
            Any: The head item.

        Raises:
            IndexError: If queue is empty.
        """
        if not self.__items:
            raise IndexError("peek from empty queue")
        return self.__items[0]

    def clear(self) -> None:
        """Remove all items from the queue."""
        self.__items.clear()

    def copy(self) -> "Queue":
        """Create a shallow copy of the queue."""
        return Queue(self.__items.copy())

    def count(self, item: Any) -> int:
        """Count occurrences of an item in the queue."""
        return self.__items.count(item)

    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of an item.

        Raises:
            ValueError: If item is not in the queue.
        """
        if item not in self.__items:
            raise ValueError("item not in queue")
        return self.__items.index(item)


# =========================
# Heap
# =========================

class Heap:
    """A binary heap for priority queue operations.

    A heap is a specialized tree-based data structure that satisfies the
    heap property. Supports both min-heaps (parent <= children) and max-heaps
    (parent >= children).

    Args:
        iterable: Optional iterable to initialize the heap with elements.
        min_heap: If True, creates a min-heap; if False, creates a max-heap.

    Raises:
        TypeError: If iterable is provided but is not iterable.
    """

    def __init__(
            self, iterable: Optional[Iterable[Any]] = None, *, min_heap: bool = True
    ) -> None:
        """Initialize a new Heap.

        Args:
            iterable: Optional iterable of items to populate the heap.
            min_heap: If True, create a min-heap (default). If False, create a max-heap.

        Raises:
            TypeError: If iterable is provided but is not iterable.
        """
        self.__items: list[Any] = []
        self.__min_heap: bool = min_heap

        if iterable is not None:
            try:
                for item in iterable:
                    self.push(item)
            except TypeError:
                raise TypeError("'Heap' object must be initialized with an iterable")

    # --- Representation ---
    def __repr__(self) -> str:
        """Return a formal string representation of the Heap."""
        kind: str = "min" if self.__min_heap else "max"
        return f"Heap({self.__items}, type='{kind}')"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the Heap."""
        return str(self.__items)

    # --- Length ---
    def __len__(self) -> int:
        """Return the number of items in the heap."""
        return len(self.__items)

    # --- Iteration ---
    def __iter__(self) -> Iterator[Any]:
        """Iterate over items in the heap (heap order, not sorted)."""
        return iter(self.__items)

    # --- Membership ---
    def __contains__(self, item: Any) -> bool:
        """Check if an item is in the heap."""
        return item in self.__items

    # --- Equality ---
    def __eq__(self, other: Any) -> bool:
        """Check equality with another Heap or iterable."""
        try:
            return sorted(self.__items) == sorted(list(other))
        except TypeError:
            return False

    def __bool__(self) -> bool:
        """Return True if the heap is not empty."""
        return bool(self.__items)

    def __hash__(self) -> None:
        """Heaps are not hashable."""
        raise TypeError("unhashable type: 'Heap'")

    # --- Private Helpers ---
    def __compare(self, a: Any, b: Any) -> bool:
        """Compare two elements according to heap type."""
        return a < b if self.__min_heap else a > b

    def __parent(self, i: int) -> int:
        """Get the index of the parent of element at index i."""
        return (i - 1) // 2

    def __left_child(self, i: int) -> int:
        """Get the index of the left child of element at index i."""
        return 2 * i + 1

    def __right_child(self, i: int) -> int:
        """Get the index of the right child of element at index i."""
        return 2 * i + 2

    def __swap(self, i: int, j: int) -> None:
        """Swap two elements in the heap."""
        self.__items[i], self.__items[j] = self.__items[j], self.__items[i]

    def __heapify_up(self, i: int) -> None:
        """Restore heap property by moving element up the tree."""
        while i > 0:
            parent = self.__parent(i)
            if self.__compare(self.__items[i], self.__items[parent]):
                self.__swap(i, parent)
                i = parent
            else:
                break

    def __heapify_down(self, i: int) -> None:
        """Restore heap property by moving element down the tree."""
        size = len(self.__items)
        while True:
            left = self.__left_child(i)
            right = self.__right_child(i)
            target = i

            if left < size and self.__compare(self.__items[left], self.__items[target]):
                target = left
            if (
                    right < size
                    and self.__compare(self.__items[right], self.__items[target])
            ):
                target = right

            if target == i:
                break

            self.__swap(i, target)
            i = target

    # --- Core Methods ---
    def push(self, item: Any) -> None:
        """Insert an item into the heap."""
        self.__items.append(item)
        self.__heapify_up(len(self.__items) - 1)

    def pop(self) -> Any:
        """Remove and return the root element (min or max).

        Returns:
            Any: The root element.

        Raises:
            IndexError: If heap is empty.
        """
        if not self.__items:
            raise IndexError("pop from empty heap")

        root = self.__items[0]
        last = self.__items.pop()

        if self.__items:
            self.__items[0] = last
            self.__heapify_down(0)

        return root

    def peek(self) -> Any:
        """Return the root element without removing it.

        Returns:
            Any: The root element.

        Raises:
            IndexError: If heap is empty.
        """
        if not self.__items:
            raise IndexError("peek from empty heap")
        return self.__items[0]

    def clear(self) -> None:
        """Remove all items from the heap."""
        self.__items.clear()

    def copy(self) -> "Heap":
        """Create a shallow copy of the heap."""
        return Heap(self.__items, min_heap=self.__min_heap)

    def count(self, item: Any) -> int:
        """Count occurrences of an item in the heap."""
        return self.__items.count(item)


# =========================
# Linked List Node
# =========================

class _LLNode:
    """A node in a linked list (private)."""

    __slots__ = ("value", "next", "prev")

    def __init__(
            self,
            value: Any,
            next_node: Optional["_LLNode"] = None,
            prev_node: Optional["_LLNode"] = None,
    ) -> None:
        """Initialize a linked list node."""
        self.value: Any = value
        self.next: Optional[_LLNode] = next_node
        self.prev: Optional[_LLNode] = prev_node


# =========================
# Singly Linked List
# =========================

class SinglyLinkedList(MutableSequence):
    """A singly-linked list where each node points only to the next node.

    A linear data structure where elements are linked in sequence. Each node
    contains data and a reference to the next node. Supports circular linking.

    Args:
        iterable: Optional iterable to initialize the list with elements.
        circular: If True, the last node points back to the first node.

    Attributes:
        circular: Whether the list is circular.
    """

    def __init__(
            self, iterable: Optional[Iterable[Any]] = None, circular: bool = False
    ) -> None:
        """Initialize a new SinglyLinkedList.

        Args:
            iterable: Optional iterable of items to populate the list.
            circular: If True, create a circular linked list (default: False).
        """
        self.__head: Optional[_LLNode] = None
        self.__tail: Optional[_LLNode] = None
        self.circular: bool = circular
        self.__length: int = 0
        if iterable:
            for item in iterable:
                self.append(item)

    # --- Representation ---
    def __repr__(self) -> str:
        """Return a formal string representation."""
        return (
            f"SinglyLinkedList({list(self)}, circular={self.circular})"
        )

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"[{', '.join(str(x) for x in self)}]"

    # --- Length ---
    def __len__(self) -> int:
        """Return the number of items in the list."""
        return self.__length

    # --- Iteration ---
    def __iter__(self) -> Iterator[Any]:
        """Iterate over items from head to tail."""
        node = self.__head
        count = 0
        while node and count < self.__length:
            yield node.value
            node = node.next
            count += 1

    # --- Indexing ---
    def __getitem__(self, index: int | slice) -> Any:
        """Get item(s) at the specified index or slice."""
        if isinstance(index, slice):
            start, stop, step = index.indices(self.__length)
            return [SinglyLinkedList(self[i]) for i in range(start, stop, step)]

        if index < 0:
            index += self.__length
        if index < 0 or index >= self.__length:
            raise IndexError("list index out of range")

        node = self.__head
        for _ in range(index):
            node = node.next
        return node.value

    def __setitem__(self, index: int | slice, value: Any) -> None:
        """Set item(s) at the specified index or slice."""
        if isinstance(index, slice):
            start, stop, step = index.indices(self.__length)
            indices = list(range(start, stop, step))
            if step == 1:
                # Handle contiguous slice assignment
                values = list(value) if hasattr(value, "__iter__") else [value]
                old_len = len(indices)
                new_len = len(values)
                if new_len != old_len:
                    raise ValueError(
                        f"attempt to assign sequence of size {new_len} to extended slice of size {old_len}"
                    )
                for i, val in zip(indices, values):
                    self[i] = val
            else:
                # Extended slice assignment
                values = list(value) if hasattr(value, "__iter__") else [value]
                if len(indices) != len(values):
                    raise ValueError(
                        f"attempt to assign sequence of size {len(values)} to extended slice of size {len(indices)}"
                    )
                for i, val in zip(indices, values):
                    self[i] = val
        else:
            if index < 0:
                index += self.__length
            if index < 0 or index >= self.__length:
                raise IndexError("list index out of range")

            node = self.__head
            for _ in range(index):
                node = node.next
            node.value = value

    def __delitem__(self, index: int | slice) -> None:
        """Delete item(s) at the specified index or slice."""
        if isinstance(index, slice):
            start, stop, step = index.indices(self.__length)
            if step == 1:
                for _ in range(stop - start):
                    self.pop(start)
            else:
                indices = list(range(start, stop, step))
                for idx in reversed(indices):
                    self.pop(idx)
        else:
            self.pop(index)

    # --- Membership ---
    def __contains__(self, value: Any) -> bool:
        """Check if a value is in the list."""
        return any(x == value for x in self)

    # --- Equality ---
    def __eq__(self, other: Any) -> bool:
        """Check equality with another list or iterable."""
        try:
            return list(self) == list(other)
        except TypeError:
            return False

    # --- Addition / Multiplication ---
    def __add__(self, other: Iterable[Any]) -> "SinglyLinkedList":
        """Create a new list with elements from this list and another iterable."""
        return SinglyLinkedList(list(self) + list(other), circular=self.circular)

    def __iadd__(self, other: Iterable[Any]) -> "SinglyLinkedList":
        """Extend this list with elements from another iterable."""
        self.extend(other)
        return self

    def __mul__(self, n: int) -> "SinglyLinkedList":
        """Create a new list with elements repeated n times."""
        return SinglyLinkedList(list(self) * n, circular=self.circular)

    def __imul__(self, n: int) -> "SinglyLinkedList":
        """Repeat this list's elements n times in-place."""
        if n <= 0:
            self.clear()
            return self
        original = list(self)
        for _ in range(n - 1):
            self.extend(original)
        return self

    # --- Core Methods ---
    def append(self, value: Any) -> None:
        """Add an item to the end of the list."""
        node = _LLNode(value)
        if not self.__head:
            self.__head = self.__tail = node
            if self.circular:
                node.next = self.__head
        else:
            self.__tail.next = node
            self.__tail = node
            if self.circular:
                self.__tail.next = self.__head
        self.__length += 1

    def insert(self, index: int, value: Any) -> None:
        """Insert an item at a specific position."""
        if not (0 <= index <= self.__length):
            raise IndexError("list index out of range")
        if index == 0:
            node = _LLNode(value, next_node=self.__head)
            self.__head = node
            if self.__length == 0:
                self.__tail = node
            if self.circular:
                self.__tail.next = self.__head
        elif index == self.__length:
            self.append(value)
            return
        else:
            prev = self.__head
            for _ in range(index - 1):
                prev = prev.next
            node = _LLNode(value, next_node=prev.next)
            prev.next = node
        self.__length += 1

    def pop(self, index: int = -1) -> Any:
        """Remove and return an item at the specified index."""
        if not self.__head:
            raise IndexError("pop from empty list")

        if index < 0:
            index += self.__length
        if index < 0 or index >= self.__length:
            raise IndexError("pop index out of range")

        if index == 0:
            val = self.__head.value
            if self.circular and self.__tail:
                self.__tail.next = self.__head
            if self.__length == 1:
                self.__tail = None
        else:
            prev = self.__head
            for _ in range(index - 1):
                prev = prev.next
            curr = prev.next
            val = curr.value
            prev.next = curr.next
            if curr == self.__tail:
                self.__tail = prev

        self.__length -= 1
        return val

    def extend(self, iterable: Iterable[Any]) -> None:
        """Add multiple items to the end of the list."""
        for item in iterable:
            self.append(item)

    def remove(self, value: Any) -> None:
        """Remove the first occurrence of a value.

        Raises:
            ValueError: If value is not found.
        """
        node = self.__head
        prev: Optional[_LLNode] = None
        count = 0
        while node and count < self.__length:
            if node.value == value:
                if prev:
                    prev.next = node.next
                    if node == self.__tail:
                        self.__tail = prev
                        if self.circular:
                            self.__tail.next = self.__head
                else:
                    self.__head = node.next
                    if self.circular and self.__tail:
                        self.__tail.next = self.__head
                    if node == self.__tail:
                        self.__tail = None
                self.__length -= 1
                return
            prev = node
            node = node.next
            count += 1
        raise ValueError(f"{value} not found in list")

    def clear(self) -> None:
        """Remove all items from the list."""
        self.__head = self.__tail = None
        self.__length = 0

    def index(self, value: Any, **kwargs) -> int:
        """Return the index of the first occurrence of a value.
        """
        node = self.__head
        count = 0
        while count < self.__length:
            if node.value == value:
                return count
            node = node.next
            count += 1
        raise ValueError(f"{value} not in list")

    def count(self, value: Any) -> int:
        """Count occurrences of a value in the list."""
        return sum(1 for x in self if x == value)

    def reverse(self) -> None:
        """Reverse the order of items in-place."""
        prev: Optional[_LLNode] = None
        node = self.__head
        count = 0
        while node and count < self.__length:
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
            count += 1
        self.__head, self.__tail = self.__tail, self.__head
        if self.circular and self.__tail:
            self.__tail.next = self.__head

    def copy(self) -> "SinglyLinkedList":
        """Create a shallow copy of the list."""
        return SinglyLinkedList(self, circular=self.circular)

    # --- Extra Compatibility ---
    def __bool__(self) -> bool:
        """Return True if the list is not empty."""
        return self.__length > 0

    def __reversed__(self) -> Iterator[Any]:
        """Iterate over items in reverse order."""
        return reversed(list(self))

    def __hash__(self) -> None:
        """Singly-linked lists are not hashable."""
        raise TypeError("unhashable type: 'SinglyLinkedList'")


# =========================
# Doubly Linked List
# =========================

class DoublyLinkedList(MutableSequence):
    """A doubly-linked list where each node points to both next and previous nodes.

    A linear data structure where elements are linked bidirectionally. Each node
    contains data and references to both next and previous nodes. Supports
    circular linking.

    Args:
        iterable: Optional iterable to initialize the list with elements.
        circular: If True, the last node points to the first and vice versa.

    Attributes:
        circular: Whether the list is circular.
    """

    def __init__(
            self, iterable: Optional[Iterable[Any]] = None, circular: bool = False
    ) -> None:
        """Initialize a new DoublyLinkedList.

        Args:
            iterable: Optional iterable of items to populate the list.
            circular: If True, create a circular doubly-linked list (default: False).
        """
        self.__head: Optional[_LLNode] = None
        self.__tail: Optional[_LLNode] = None
        self.circular: bool = circular
        self.__length: int = 0
        if iterable:
            for item in iterable:
                self.append(item)

    # --- Representation ---
    def __repr__(self) -> str:
        """Return a formal string representation."""
        return (
            f"DoublyLinkedList({list(self)}, circular={self.circular})"
        )

    def __str__(self) -> str:
        """Return a user-friendly string representation."""
        return f"[{', '.join(str(x) for x in self)}]"

    # --- Length ---
    def __len__(self) -> int:
        """Return the number of items in the list."""
        return self.__length

    # --- Iteration ---
    def __iter__(self) -> Iterator[Any]:
        """Iterate over items from head to tail."""
        node = self.__head
        count = 0
        while node and count < self.__length:
            yield node.value
            node = node.next
            count += 1

    # --- Indexing ---
    def __getitem__(self, index: int | slice) -> Any:
        """Get item(s) at the specified index or slice."""
        if isinstance(index, slice):
            start, stop, step = index.indices(self.__length)
            return [DoublyLinkedList(self[i]) for i in range(start, stop, step)]

        if index < 0:
            index += self.__length
        if index < 0 or index >= self.__length:
            raise IndexError("list index out of range")

        node = self.__head
        for _ in range(index):
            node = node.next
        return node.value

    def __setitem__(self, index: int | slice, value: Any) -> None:
        """Set item(s) at the specified index or slice."""
        if isinstance(index, slice):
            start, stop, step = index.indices(self.__length)
            indices = list(range(start, stop, step))
            if step == 1:
                values = list(value) if hasattr(value, "__iter__") else [value]
                old_len = len(indices)
                new_len = len(values)
                if new_len != old_len:
                    raise ValueError(
                        f"attempt to assign sequence of size {new_len} to extended slice of size {old_len}"
                    )
                for i, val in zip(indices, values):
                    self[i] = val
            else:
                values = list(value) if hasattr(value, "__iter__") else [value]
                if len(indices) != len(values):
                    raise ValueError(
                        f"attempt to assign sequence of size {len(values)} to extended slice of size {len(indices)}"
                    )
                for i, val in zip(indices, values):
                    self[i] = val
        else:
            if index < 0:
                index += self.__length
            if index < 0 or index >= self.__length:
                raise IndexError("list index out of range")

            node = self.__head
            for _ in range(index):
                node = node.next
            node.value = value

    def __delitem__(self, index: int | slice) -> None:
        """Delete item(s) at the specified index or slice."""
        if isinstance(index, slice):
            start, stop, step = index.indices(self.__length)
            if step == 1:
                for _ in range(stop - start):
                    self.pop(start)
            else:
                indices = list(range(start, stop, step))
                for idx in reversed(indices):
                    self.pop(idx)
        else:
            self.pop(index)

    # --- Membership ---
    def __contains__(self, value: Any) -> bool:
        """Check if a value is in the list."""
        return any(x == value for x in self)

    # --- Equality ---
    def __eq__(self, other: Any) -> bool:
        """Check equality with another list or iterable."""
        try:
            return list(self) == list(other)
        except TypeError:
            return False

    # --- Addition / Multiplication ---
    def __add__(self, other: Iterable[Any]) -> "DoublyLinkedList":
        """Create a new list with elements from this list and another iterable."""
        return DoublyLinkedList(list(self) + list(other), circular=self.circular)

    def __iadd__(self, other: Iterable[Any]) -> "DoublyLinkedList":
        """Extend this list with elements from another iterable."""
        self.extend(other)
        return self

    def __mul__(self, n: int) -> "DoublyLinkedList":
        """Create a new list with elements repeated n times."""
        return DoublyLinkedList(list(self) * n, circular=self.circular)

    def __imul__(self, n: int) -> "DoublyLinkedList":
        """Repeat this list's elements n times in-place."""
        if n <= 0:
            self.clear()
            return self
        original = list(self)
        for _ in range(n - 1):
            self.extend(original)
        return self

    # --- Core Methods ---
    def append(self, value: Any) -> None:
        """Add an item to the end of the list."""
        node = _LLNode(value)
        if not self.__head:
            self.__head = self.__tail = node
            if self.circular:
                node.next = self.__head
                node.prev = self.__tail
        else:
            node.prev = self.__tail
            self.__tail.next = node
            self.__tail = node
            if self.circular:
                self.__tail.next = self.__head
                self.__head.prev = self.__tail
        self.__length += 1

    def insert(self, index: int, value: Any) -> None:
        """Insert an item at a specific position."""
        if not (0 <= index <= self.__length):
            raise IndexError("list index out of range")
        node = _LLNode(value)
        if index == 0:
            node.next = self.__head
            if self.__head:
                self.__head.prev = node
            self.__head = node
            if self.__length == 0:
                self.__tail = node
            if self.circular:
                self.__head.prev = self.__tail
                self.__tail.next = self.__head
        elif index == self.__length:
            self.append(value)
            return
        else:
            curr = self.__head
            for _ in range(index):
                curr = curr.next
            node.prev = curr.prev
            node.next = curr
            if curr.prev:
                curr.prev.next = node
            curr.prev = node
        self.__length += 1

    def pop(self, index: int = -1) -> Any:
        """Remove and return an item at the specified index."""
        if not self.__tail:
            raise IndexError("pop from empty list")

        if index < 0:
            index += self.__length
        if index < 0 or index >= self.__length:
            raise IndexError("pop index out of range")

        if index == self.__length - 1:
            val = self.__tail.value
            if self.__length == 1:
                self.__head = self.__tail = None
            else:
                self.__tail = self.__tail.prev
                self.__tail.next = self.__head if self.circular else None
                if self.circular:
                    self.__head.prev = self.__tail
            self.__length -= 1
            return val
        else:
            node = self.__head
            for _ in range(index):
                node = node.next
            val = node.value
            if node.prev:
                node.prev.next = node.next
            else:
                self.__head = node.next
            if node.next:
                node.next.prev = node.prev
            else:
                self.__tail = node.prev
            if self.circular and self.__length > 1:
                self.__head.prev = self.__tail
                self.__tail.next = self.__head
            self.__length -= 1
            return val

    def extend(self, iterable: Iterable[Any]) -> None:
        """Add multiple items to the end of the list."""
        for item in iterable:
            self.append(item)

    def remove(self, value: Any) -> None:
        """Remove the first occurrence of a value.

        Raises:
            ValueError: If value is not found.
        """
        node = self.__head
        count = 0
        while node and count < self.__length:
            if node.value == value:
                if node.prev:
                    node.prev.next = node.next
                else:
                    self.__head = node.next
                if node.next:
                    node.next.prev = node.prev
                else:
                    self.__tail = node.prev
                if self.circular and self.__length > 1:
                    self.__head.prev = self.__tail
                    self.__tail.next = self.__head
                self.__length -= 1
                return
            node = node.next
            count += 1
        raise ValueError(f"{value} not found in list")

    def clear(self) -> None:
        """Remove all items from the list."""
        self.__head = self.__tail = None
        self.__length = 0

    def index(self, value: Any, **kwargs) -> int:
        """Return the index of the first occurrence of a value."""
        node = self.__head
        count = 0
        while count < self.__length:
            if node.value == value:
                return count
            node = node.next
            count += 1
        raise ValueError(f"{value} not in list")

    def count(self, value: Any) -> int:
        """Count occurrences of a value in the list."""
        return sum(1 for x in self if x == value)

    def reverse(self) -> None:
        """Reverse the order of items in-place."""
        node = self.__head
        count = 0
        while node and count < self.__length:
            node.next, node.prev = node.prev, node.next
            node = node.prev
            count += 1
        self.__head, self.__tail = self.__tail, self.__head
        if self.circular:
            self.__head.prev = self.__tail
            self.__tail.next = self.__head

    def copy(self) -> "DoublyLinkedList":
        """Create a shallow copy of the list."""
        return DoublyLinkedList(self, circular=self.circular)

    # --- Extra Compatibility ---
    def __bool__(self) -> bool:
        """Return True if the list is not empty."""
        return self.__length > 0

    def __reversed__(self) -> Iterator[Any]:
        """Iterate over items in reverse order."""
        node = self.__tail
        count = 0
        while node and count < self.__length:
            yield node.value
            node = node.prev
            count += 1

    def __hash__(self) -> None:
        """Doubly-linked lists are not hashable."""
        raise TypeError("unhashable type: 'DoublyLinkedList'")


# =========================
# Hash Tables
# =========================

class HashTable:
    """A hash table for storing key-value pairs with collision handling.

    A hash table uses hashing to map keys to buckets containing key-value pairs.
    Collisions are handled using separate chaining (singly-linked lists).
    Supports dynamic resizing.

    Args:
        data: Optional dict or list of (key, value) pairs for initialization.
        capacity: Initial capacity for the hash table (default: 8).
        dynamic: If True, table resizes when load factor exceeds threshold.

    Attributes:
        dynamic: Whether the table resizes dynamically.
    """

    def __init__(
            self,
            data: Optional[Union[dict[Any, Any], list[tuple[Any, Any]]]] = None,
            capacity: int = 8,
            dynamic: bool = True,
    ) -> None:
        """Initialize a new HashTable.

        Args:
            data: Optional dict or list of (key, value) pairs to populate the table.
            capacity: Initial capacity (default: 8). Minimum is 8.
            dynamic: Whether to resize dynamically (default: True).

        Raises:
            ValueError: If data elements are not (key, value) pairs.
            TypeError: If data type is not supported.
        """
        self.__capacity: int = max(8, capacity)
        self.__buckets: list[SinglyLinkedList] = [
            SinglyLinkedList() for _ in range(self.__capacity)
        ]
        self.__size: int = 0
        self.dynamic: bool = dynamic
        self.__load_factor_threshold: float = 0.75
        self.__order: list[Any] = []
        if data:
            self.__load_data(data)

    def __hash(self, key: Any) -> int:
        """Compute the hash of a key."""
        return hash(key) % self.__capacity

    def __bucket(self, key: Any) -> SinglyLinkedList:
        """Get the bucket for a key."""
        return self.__buckets[self.__hash(key)]

    def __load_data(self, data: Union[dict[Any, Any], list[tuple[Any, Any]]]) -> None:
        """Load data into the hash table during initialization."""
        if isinstance(data, dict):
            for k, v in data.items():
                self[k] = v
        elif isinstance(data, (list, tuple)):
            for pair in data:
                if len(pair) != 2:
                    raise ValueError("Each element must be [key, value]")
                self[pair[0]] = pair[1]
        else:
            raise TypeError("Unsupported data type for initialization")

    def __resize(self) -> None:
        """Double the capacity and rehash all entries."""
        old_items = list(self.items())
        self.__capacity *= 2
        self.__buckets = [SinglyLinkedList() for _ in range(self.__capacity)]
        self.__size = 0
        self.__order = []
        for k, v in old_items:
            self[k] = v

    def __getitem__(self, key: Any) -> Any:
        """Get the value associated with a key."""
        bucket = self.__bucket(key)
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        """Set the value associated with a key."""
        if self.dynamic and (self.__size + 1) / self.__capacity > self.__load_factor_threshold:
            self.__resize()
        bucket = self.__bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.remove((k, v))
                bucket.append((key, value))
                return
        bucket.append((key, value))
        self.__size += 1
        self.__order.append(key)

    def __delitem__(self, key: Any) -> None:
        """Delete a key-value pair from the hash table."""
        bucket = self.__bucket(key)
        for k, v in bucket:
            if k == key:
                bucket.remove((k, v))
                self.__size -= 1
                self.__order.remove(key)
                return
        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        """Check if a key is in the hash table."""
        bucket = self.__bucket(key)
        return any(k == key for k, _ in bucket)

    def __iter__(self) -> Iterator[Any]:
        """Iterate over keys in the hash table."""
        return iter(self.__order)

    def __reversed__(self) -> Iterator[Any]:
        """Iterate over keys in reverse insertion order."""
        return reversed(self.__order)

    def __len__(self) -> int:
        """Return the number of key-value pairs in the hash table."""
        return self.__size

    def __repr__(self) -> str:
        """Return a formal string representation of the HashTable."""
        items = ", ".join([f"{k!r}: {v!r}" for k, v in self.items()])
        return f"{{{items}}}"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the HashTable."""
        return repr(self)

    def __eq__(self, other: Any) -> bool:
        """Check equality with another HashTable or dict."""
        if isinstance(other, dict):
            other = HashTable(other)
        if not isinstance(other, HashTable):
            return False
        if len(self) != len(other):
            return False
        for k in self.__order:
            if k not in other or self[k] != other[k]:
                return False
        return True

    def __hash__(self) -> None:
        """Hash tables are not hashable."""
        raise TypeError("unhashable type: 'HashTable'")

    def __bool__(self) -> bool:
        """Return True if the hash table is not empty."""
        return self.__size > 0

    # --- Core Methods ---
    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        """Get the value for a key, returning default if not found."""
        try:
            return self[key]
        except KeyError:
            return default

    def setdefault(self, key: Any, default: Optional[Any] = None) -> Any:
        """Get value for key, setting it to default if not found."""
        if key not in self:
            self[key] = default
        return self[key]

    def pop(self, key: Any, default: Optional[Any] = _sentinel) -> Any:
        """Remove and return the value for a key."""
        bucket = self.__bucket(key)
        for k, v in bucket:
            if k == key:
                bucket.remove((k, v))
                self.__size -= 1
                self.__order.remove(key)
                return v
        if default is not _sentinel:
            return default
        raise KeyError(key)

    def popitem(self) -> tuple[Any, Any]:
        """Remove and return an arbitrary (key, value) pair."""
        if not self.__order:
            raise KeyError("popitem(): dictionary is empty")
        key = self.__order[-1]
        value = self[key]
        del self[key]
        return key, value

    def clear(self) -> None:
        """Remove all key-value pairs from the hash table."""
        self.__buckets = [SinglyLinkedList() for _ in range(self.__capacity)]
        self.__size = 0
        self.__order = []

    def keys(self) -> Iterator[Any]:
        """Iterate over all keys in insertion order."""
        yield from self.__order

    def values(self) -> Iterator[Any]:
        """Iterate over all values in insertion order."""
        for key in self.__order:
            yield self[key]

    def items(self) -> Iterator[tuple[Any, Any]]:
        """Iterate over all (key, value) pairs in insertion order."""
        for key in self.__order:
            yield key, self[key]

    def update(
            self,
            other: Optional[Union[dict[Any, Any], "HashTable", Iterable[tuple[Any, Any]]]] = None,
            **kwargs: Any,
    ) -> None:
        """Update the hash table with key-value pairs from another source."""
        if other:
            if isinstance(other, HashTable):
                for k, v in other.items():
                    self[k] = v
            elif isinstance(other, dict):
                for k, v in other.items():
                    self[k] = v
            elif hasattr(other, "__iter__"):
                for pair in other:
                    if len(pair) != 2:
                        raise ValueError("Iterable elements must be [key, value]")
                    self[pair[0]] = pair[1]
            else:
                raise TypeError("Unsupported type for update()")
        for k, v in kwargs.items():
            self[k] = v

    def copy(self) -> "HashTable":
        """Create a shallow copy of the hash table."""
        return HashTable(list(self.items()), capacity=self.__capacity, dynamic=self.dynamic)

    @classmethod
    def fromkeys(cls, iterable: Iterable[Any], value: Optional[Any] = None) -> "HashTable":
        """Create a new HashTable with keys from an iterable."""
        return cls([(k, value) for k in iterable])


# =========================
# Graphs
# =========================

class AdjacencyMatrix:
    """A graph representation using an adjacency matrix.

    An adjacency matrix is a 2D array where element [i][j] represents the
    weight of the edge from vertex i to vertex j (0 if no edge).

    Args:
        vertices: Optional iterable of vertices to initialize the graph.
        directed: If True, creates a directed graph; if False, undirected.

    Attributes:
        directed: Whether the graph is directed.
    """

    def __init__(
            self, vertices: Optional[Iterable[Any]] = None, directed: bool = False
    ) -> None:
        """Initialize a new AdjacencyMatrix graph."""
        self.directed: bool = directed
        self.__vertices: list[Any] = []
        self.__index: dict[Any, int] = {}
        self.__matrix: list[list[int]] = []

        if vertices:
            for v in vertices:
                self.add_vertex(v)

    # --- Representation ---
    def __repr__(self) -> str:
        """Return a formal string representation of the AdjacencyMatrix."""
        return f"AdjacencyMatrix(vertices={self.__vertices}, directed={self.directed})"

    def __str__(self) -> str:
        """Return a formatted string representation of the adjacency matrix."""
        if not self.__vertices:
            return ""

        width = max(len(str(v)) for v in self.__vertices) + 2
        header = " " * width + "".join(f"{v:>{width}}" for v in self.__vertices)
        rows = [header]

        for i, v in enumerate(self.__vertices):
            row = f"{v:>{width}}" + "".join(f"{x:>{width}}" for x in self.__matrix[i])
            rows.append(row)

        return "\n".join(rows)

    # --- Basic Info ---
    def __len__(self) -> int:
        """Return the number of vertices in the graph."""
        return len(self.__vertices)

    def __contains__(self, v: Any) -> bool:
        """Check if vertex exists in the graph."""
        return v in self.__index

    def __iter__(self) -> Iterator[Any]:
        """Iterate over all vertices in the graph."""
        return iter(self.__vertices)

    def __getitem__(self, key: Any) -> dict[Any, int] | int | None:
        """Support g[v] -> dict(neighbor->weight) and g[u, v] -> Optional[int]."""
        if isinstance(key, tuple) and len(key) == 2:
            u, v = key
            return self.get_weight(u, v)
        else:
            v = key
            if v not in self.__index:
                raise KeyError(v)
            return {
                nbr: self.__matrix[self.__index[v]][self.__index[nbr]]
                for nbr in self.__vertices
                if self.__matrix[self.__index[v]][self.__index[nbr]] != 0
            }

    def __bool__(self) -> bool:
        """Return True if the graph is not empty."""
        return len(self.__vertices) > 0

    def __hash__(self) -> None:
        """Graphs are not hashable."""
        raise TypeError("unhashable type: 'AdjacencyMatrix'")

    # --- Vertex Operations ---
    def vertices(self) -> list[Any]:
        """Get a list of all vertices in the graph."""
        return list(self.__vertices)

    def add_vertex(self, v: Any) -> None:
        """Add a vertex to the graph."""
        if v in self.__index:
            return
        self.__index[v] = len(self.__vertices)
        self.__vertices.append(v)

        for row in self.__matrix:
            row.append(0)
        self.__matrix.append([0] * len(self.__vertices))

    def add_vertices(self, vertices: Iterable[Any]) -> None:
        """Add multiple vertices using an iterable."""
        for v in vertices:
            self.add_vertex(v)

    def remove_vertex(self, v: Any) -> None:
        """Remove a vertex and all associated edges from the graph."""
        if v not in self.__index:
            raise KeyError(v)

        idx = self.__index.pop(v)
        self.__vertices.pop(idx)
        self.__matrix.pop(idx)

        for row in self.__matrix:
            row.pop(idx)

        self.__index = {v: i for i, v in enumerate(self.__vertices)}

    def remove_vertices(self, vertices: Iterable[Any]) -> None:
        """Remove multiple vertices using an iterable."""
        for v in vertices:
            self.remove_vertex(v)

    # --- Edge Operations ---
    def add_edge(self, u: Any, v: Any, weight: int = 1) -> None:
        """Add an edge from vertex u to vertex v."""
        if not isinstance(weight, int):
            raise ValueError("weight must be of type 'int'")

        for node in (u, v):
            if node not in self.__index:
                self.add_vertex(node)

        i, j = self.__index[u], self.__index[v]
        self.__matrix[i][j] = weight

        if not self.directed:
            self.__matrix[j][i] = weight

    def add_edges(self, edge_map: Iterable[tuple[Any, Any] | tuple[Any, Any, int]]) -> None:
        """Add multiple edges using an edge map."""
        for edge in edge_map:
            if len(edge) > 3 or len(edge) < 2:
                raise ValueError('edges in edge map expects 2 vertices and an optional weight')
            if len(edge) == 2:
                u, v = edge
                weight = 1
            else:
                u, v, weight = edge
                if not isinstance(weight, int):
                    raise ValueError("weight must be of type 'int'")
            self.add_edge(u, v, weight)

    def remove_edge(self, u: Any, v: Any) -> None:
        """Remove the edge from vertex u to vertex v."""
        if u not in self.__index or v not in self.__index:
            raise KeyError("Vertex not found")

        i, j = self.__index[u], self.__index[v]
        self.__matrix[i][j] = 0

        if not self.directed:
            self.__matrix[j][i] = 0

    def remove_edges(self, edge_map: Iterable[tuple[Any, Any]]) -> None:
        """Remove multiple edges using an edge map."""
        for edge in edge_map:
            if len(edge) > 2 or len(edge) < 2:
                raise ValueError('edges in edge map expects 2 vertices')
            u, v = edge
            self.remove_edge(u, v)

    def has_edge(self, u: Any, v: Any) -> bool:
        """Check if an edge exists from vertex u to vertex v."""
        if u not in self.__index or v not in self.__index:
            return False
        return self.__matrix[self.__index[u]][self.__index[v]] != 0

    def get_weight(self, u: Any, v: Any) -> Optional[int]:
        """Get the weight of the edge from vertex u to vertex v."""
        if not self.has_edge(u, v):
            return None
        return self.__matrix[self.__index[u]][self.__index[v]]

    def neighbors(self, v: Any, with_weights: bool = False) -> Iterator[Any]:
        """Yield neighbors of v. If with_weights True yields (neighbor, weight)."""
        if v not in self.__index:
            raise KeyError(v)
        i = self.__index[v]
        for j, u in enumerate(self.__vertices):
            w = self.__matrix[i][j]
            if w != 0:
                if with_weights:
                    yield u, w
                else:
                    yield u

    def out_degree(self, v: Any) -> int:
        """Return the out-degree (number of outgoing edges) of vertex v."""
        if v not in self.__index:
            raise KeyError(v)
        i = self.__index[v]
        return sum(1 for w in self.__matrix[i] if w != 0)

    def in_degree(self, v: Any) -> int:
        """Return the in-degree (number of incoming edges) of vertex v."""
        if v not in self.__index:
            raise KeyError(v)
        j = self.__index[v]
        return sum(1 for row in self.__matrix if row[j] != 0)

    def degree(self, v: Any) -> int:
        """Return degree of vertex v."""
        if self.directed:
            return self.in_degree(v) + self.out_degree(v)
        return self.out_degree(v)

    def edges(self) -> Iterator[tuple[Any, Any, int]]:
        """Iterate over all edges in the graph."""
        for i, u in enumerate(self.__vertices):
            for j, v in enumerate(self.__vertices):
                if self.__matrix[i][j] != 0:
                    yield u, v, self.__matrix[i][j]

    def shortest_path(self, start: Any, end: Any) -> tuple[Optional[int], list[Any]]:
        """Return (distance, path) using Dijkstra's algorithm."""
        import heapq

        if start not in self.__index or end not in self.__index:
            raise KeyError("Start or end vertex not found")

        n = len(self.__vertices)
        start_i = self.__index[start]
        end_i = self.__index[end]

        dist = {i: float("inf") for i in range(n)}
        prev = {i: None for i in range(n)}
        dist[start_i] = 0

        heap = [(0, start_i)]

        while heap:
            d, u = heapq.heappop(heap)

            if d > dist[u]:
                continue

            if u == end_i:
                break

            for v in range(n):
                weight = self.__matrix[u][v]
                if weight == 0:
                    continue

                alt = d + weight
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (alt, v))

        if dist[end_i] == float("inf"):
            return None, []

        # Reconstruct path
        path_idx = []
        cur = end_i
        while cur is not None:
            path_idx.append(cur)
            cur = prev[cur]

        path_idx.reverse()
        path = [self.__vertices[i] for i in path_idx]

        return dist[end_i], path


class AdjacencyList:
    """A graph representation using adjacency lists.

    An adjacency list is a collection of lists, where each list stores the
    neighbors of a vertex along with edge weights.

    Args:
        vertices: Optional iterable of vertices to initialize the graph.
        directed: If True, creates a directed graph; if False, undirected.

    Attributes:
        directed: Whether the graph is directed.
    """

    def __init__(
            self, vertices: Optional[Iterable[Any]] = None, directed: bool = False
    ) -> None:
        """Initialize a new AdjacencyList graph."""
        self.directed: bool = directed
        self.__adj: HashTable = HashTable()

        if vertices:
            for v in vertices:
                self.add_vertex(v)

    # --- Representation ---
    def __repr__(self) -> str:
        """Return a formal string representation of the AdjacencyList."""
        return f"AdjacencyList({list(self.__adj.items())}, directed={self.directed})"

    def __str__(self) -> str:
        """Return a formatted string representation of the adjacency list."""
        return "\n".join(f"{k}: {list(v)}" for k, v in self.__adj.items())

    # --- Basic Info ---
    def __len__(self) -> int:
        """Return the number of vertices in the graph."""
        return len(self.__adj)

    def __contains__(self, v: Any) -> bool:
        """Check if vertex exists in the graph."""
        return v in self.__adj

    def __iter__(self) -> Iterator[Any]:
        """Iterate over all vertices in the graph."""
        return iter(self.__adj)

    def __getitem__(self, key: Any) -> dict[Any, int] | int | None:
        """Support g[v] -> dict(neighbor->weight) and g[u, v] -> Optional[int]."""
        if isinstance(key, tuple) and len(key) == 2:
            u, v = key
            return self.get_weight(u, v)
        else:
            v = key
            if v not in self.__adj:
                raise KeyError(v)
            return {n: w for n, w in self.__adj[v]}

    def __bool__(self) -> bool:
        """Return True if the graph is not empty."""
        return len(self.__adj) > 0

    def __hash__(self) -> None:
        """Graphs are not hashable."""
        raise TypeError("unhashable type: 'AdjacencyList'")

    # --- Vertex Operations ---
    def vertices(self) -> list[Any]:
        """Get a list of all vertices in the graph."""
        return list(self.__adj.keys())

    def add_vertex(self, v: Any) -> None:
        """Add a vertex to the graph."""
        if v not in self.__adj:
            self.__adj[v] = SinglyLinkedList()

    def add_vertices(self, vertices: Iterable[Any]) -> None:
        """Add multiple vertices using an iterable."""
        for v in vertices:
            self.add_vertex(v)

    def remove_vertex(self, v: Any) -> None:
        """Remove a vertex and all associated edges from the graph."""
        if v not in self.__adj:
            raise KeyError(v)

        del self.__adj[v]

        for key in self.__adj:
            self.__adj[key] = SinglyLinkedList(
                [(n, w) for n, w in self.__adj[key] if n != v]
            )

    def remove_vertices(self, vertices: Iterable[Any]) -> None:
        """Remove multiple vertices using an iterable."""
        for v in vertices:
            self.remove_vertex(v)

    # --- Edge Operations ---
    def add_edge(self, u: Any, v: Any, weight: int = 1) -> None:
        """Add an edge from vertex u to vertex v."""
        if not isinstance(weight, int):
            raise ValueError("weight must be of type 'int'")

        for node in (u, v):
            if node not in self.__adj:
                self.add_vertex(node)

        if not any(n == v for n, _ in self.__adj[u]):
            self.__adj[u].append((v, weight))

        if not self.directed and not any(n == u for n, _ in self.__adj[v]):
            self.__adj[v].append((u, weight))

    def add_edges(self, edge_map: Iterable[tuple[Any, Any] | tuple[Any, Any, int]]) -> None:
        """Add multiple edges using an edge map."""
        for edge in edge_map:
            if len(edge) > 3 or len(edge) < 2:
                raise ValueError('edges in edge map expects 2 vertices and an optional weight')
            if len(edge) == 2:
                u, v = edge
                weight = 1
            else:
                u, v, weight = edge
                if not isinstance(weight, int):
                    raise ValueError("weight must be of type 'int'")
            self.add_edge(u, v, weight)

    def remove_edge(self, u: Any, v: Any) -> None:
        """Remove the edge from vertex u to vertex v."""
        if u not in self.__adj or v not in self.__adj:
            raise KeyError("Vertex not found")

        self.__adj[u] = SinglyLinkedList(
            [(n, w) for n, w in self.__adj[u] if n != v]
        )

        if not self.directed:
            self.__adj[v] = SinglyLinkedList(
                [(n, w) for n, w in self.__adj[v] if n != u]
            )

    def remove_edges(self, edge_map: Iterable[tuple[Any, Any]]) -> None:
        """Remove multiple edges using an edge map."""
        for edge in edge_map:
            if len(edge) > 2 or len(edge) < 2:
                raise ValueError('edges in edge map expects 2 vertices')
            u, v = edge
            self.remove_edge(u, v)

    def has_edge(self, u: Any, v: Any) -> bool:
        """Check if an edge exists from vertex u to vertex v."""
        if u not in self.__adj:
            return False
        return any(n == v for n, _ in self.__adj[u])

    def get_weight(self, u: Any, v: Any) -> Optional[int]:
        """Get the weight of the edge from vertex u to vertex v."""
        if u not in self.__adj:
            return None
        for n, w in self.__adj[u]:
            if n == v:
                return w
        return None

    def neighbors(self, v: Any, with_weights: bool = False) -> Iterator[Any]:
        """Yield neighbors of v. If with_weights True yields (neighbor, weight)."""
        if v not in self.__adj:
            raise KeyError(v)
        for n, w in self.__adj[v]:
            if with_weights:
                yield n, w
            else:
                yield n

    def out_degree(self, v: Any) -> int:
        """Return the out-degree (number of outgoing edges) of vertex v."""
        if v not in self.__adj:
            raise KeyError(v)
        return sum(1 for _ in self.__adj[v])

    def in_degree(self, v: Any) -> int:
        """Return the in-degree (number of incoming edges) of vertex v."""
        if v not in self.__adj:
            raise KeyError(v)
        count = 0
        for key in self.__adj:
            for n, _ in self.__adj[key]:
                if n == v:
                    count += 1
        return count

    def degree(self, v: Any) -> int:
        """Return degree of vertex v."""
        if self.directed:
            return self.in_degree(v) + self.out_degree(v)
        return self.out_degree(v)

    def edges(self) -> Iterator[tuple[Any, Any, int]]:
        """Iterate over all edges in the graph."""
        for u in self.__adj:
            for v, w in self.__adj[u]:
                yield u, v, w

    def shortest_path(self, start: Any, end: Any) -> tuple[Optional[int], list[Any]]:
        """Return (distance, path) using Dijkstra's algorithm."""
        import heapq

        if start not in self.__adj or end not in self.__adj:
            raise KeyError("Start or end vertex not found")

        dist = {v: float("inf") for v in self.__adj}
        prev = {v: None for v in self.__adj}
        dist[start] = 0

        heap = [(0, start)]

        while heap:
            d, u = heapq.heappop(heap)

            if d > dist[u]:
                continue

            if u == end:
                break

            for v, w in self.__adj[u]:
                alt = d + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (alt, v))

        if dist[end] == float("inf"):
            return None, []

        # Reconstruct path
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]

        path.reverse()

        return dist[end], path


# =========================
# Trees
# =========================

class _TreeNode:
    """A node in a binary tree (private)."""

    __slots__ = ("value", "left", "right", "height")

    def __init__(
            self,
            value: Any,
            left: Optional["_TreeNode"] = None,
            right: Optional["_TreeNode"] = None,
            height: int = 1,
    ) -> None:
        """Initialize a tree node."""
        self.value: Any = value
        self.left: Optional[_TreeNode] = left
        self.right: Optional[_TreeNode] = right
        self.height: int = height


class BinaryTree:
    """A binary tree data structure.

    A tree where each node has at most two children (left and right).
    Supports list-like indexing for in-order traversal.

    Args:
        iterable: Optional iterable to initialize the tree with elements.

    Attributes:
        None - use list-like indexing instead of node access.
    """

    def __init__(self, iterable: Optional[Iterable[Any]] = None) -> None:
        """Initialize a new BinaryTree.

        Args:
            iterable: Optional iterable of items to populate the tree (in order).
        """
        self._root: Optional[_TreeNode] = None
        if iterable:
            for item in iterable:
                self.insert(item)

    # --- Representation ---
    def __repr__(self) -> str:
        """Return a formal string representation of the BinaryTree."""
        return f"BinaryTree({list(self)})"

    def __str__(self) -> str:
        """Return a formatted tree diagram as a string."""
        if not self._root:
            return "<empty tree>"

        def build(node: _TreeNode, prefix: str = "", is_tail: bool = True) -> str:
            result = []
            connector = "└── " if is_tail else "├── "
            result.append(prefix + connector + str(node.value))

            children = [c for c in (node.left, node.right) if c is not None]

            for i, child in enumerate(children):
                last = i == len(children) - 1
                extension = "    " if is_tail else "│   "
                result.append(build(child, prefix + extension, last))

            return "\n".join(result)

        lines = [str(self._root.value)]
        children = [c for c in (self._root.left, self._root.right) if c is not None]

        for i, child in enumerate(children):
            last = i == len(children) - 1
            lines.append(build(child, "", last))

        return "\n".join(lines)

    # --- Length ---
    def __len__(self) -> int:
        """Return the number of nodes in the tree."""
        return sum(1 for _ in self)

    # --- Iteration ---
    def __iter__(self) -> Iterator[Any]:
        """Iterate over tree values in in-order traversal."""
        yield from self.__inorder(self._root)

    def __inorder(self, node: Optional[_TreeNode]) -> Iterator[Any]:
        """Perform in-order traversal of the tree."""
        if node:
            yield from self.__inorder(node.left)
            yield node.value
            yield from self.__inorder(node.right)

    def __preorder(self, node: Optional[_TreeNode]) -> Iterator[Any]:
        """Perform pre-order traversal of the tree."""
        if node:
            yield node.value
            yield from self.__preorder(node.left)
            yield from self.__preorder(node.right)

    def __postorder(self, node: Optional[_TreeNode]) -> Iterator[Any]:
        """Perform post-order traversal of the tree."""
        if node:
            yield from self.__postorder(node.left)
            yield from self.__postorder(node.right)
            yield node.value

    # --- Indexing ---
    def __getitem__(self, index: int) -> Any:
        """Get item at index using in-order traversal."""
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError("tree index out of range")
        for i, val in enumerate(self):
            if i == index:
                return val
        raise IndexError("tree index out of range")

    def __setitem__(self, index: int, value: Any) -> None:
        """Set item at index using in-order traversal."""
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError("tree index out of range")

        def set_at_index(node: Optional[_TreeNode], idx: int) -> tuple[Optional[_TreeNode], int]:
            if not node:
                return node, idx
            node.left, idx = set_at_index(node.left, idx)
            if idx == 0:
                node.value = value
                return node, -1
            idx -= 1
            node.right, idx = set_at_index(node.right, idx)
            return node, idx

        self._root, _ = set_at_index(self._root, index)

    def __delitem__(self, index: int) -> None:
        """Delete item at index using in-order traversal."""
        if index < 0:
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError("tree index out of range")

        target_val = self[index]
        self.remove(target_val)

    # --- Membership ---
    def __contains__(self, value: Any) -> bool:
        """Check if a value is in the tree."""
        return any(x == value for x in self)

    # --- Equality ---
    def __eq__(self, other: Any) -> bool:
        """Check equality with another tree or iterable."""
        try:
            return list(self) == list(other)
        except TypeError:
            return False

    def __bool__(self) -> bool:
        """Return True if the tree is not empty."""
        return self._root is not None

    def __hash__(self) -> None:
        """Trees are not hashable."""
        raise TypeError("unhashable type: 'BinaryTree'")

    # --- Core Methods ---
    def insert(self, value: Any) -> None:
        """Insert a value into the tree."""
        new_node = _TreeNode(value)

        if not self._root:
            self._root = new_node
            return

        q = Queue([self._root])
        while q:
            current = q.pop()

            if not current.left:
                current.left = new_node
                return
            else:
                q.append(current.left)

            if not current.right:
                current.right = new_node
                return
            else:
                q.append(current.right)

    def remove(self, value: Any) -> None:
        """Remove a value from the tree."""
        if not self._root:
            raise ValueError(f"{value} not found in tree")

        q = Queue([self._root])
        node_to_remove = None
        last_node = None
        parent_of_last = None

        while q:
            current = q.pop()

            if current.value == value:
                node_to_remove = current

            if current.left:
                parent_of_last = current
                q.append(current.left)

            if current.right:
                parent_of_last = current
                q.append(current.right)

            last_node = current

        if not node_to_remove:
            raise ValueError(f"{value} not found in tree")

        node_to_remove.value = last_node.value

        if parent_of_last:
            if parent_of_last.right == last_node:
                parent_of_last.right = None
            else:
                parent_of_last.left = None
        else:
            self._root = None

    def clear(self) -> None:
        """Remove all nodes from the tree."""
        self._root = None

    def copy(self) -> "BinaryTree":
        """Create a shallow copy of the tree."""
        return BinaryTree(self)

    # --- Traversals ---
    def inorder(self) -> Iterator[Any]:
        """Iterate in in-order (left, root, right)."""
        return self.__inorder(self._root)

    def preorder(self) -> Iterator[Any]:
        """Iterate in pre-order (root, left, right)."""
        return self.__preorder(self._root)

    def postorder(self) -> Iterator[Any]:
        """Iterate in post-order (left, right, root)."""
        return self.__postorder(self._root)

    def height(self) -> int:
        """Return the height of the tree."""

        def __height(node: Optional[_TreeNode]) -> int:
            if not node:
                return 0
            return 1 + max(__height(node.left), __height(node.right))

        return __height(self._root)


class BinarySearchTree(BinaryTree):
    """A binary search tree (BST) for efficient searching and sorting.

    A binary tree where for each node, all values in the left subtree are
    less than the node's value, and all values in the right subtree are greater.

    Inherits from BinaryTree.
    """

    def insert(self, value: Any) -> None:
        """Insert a value into the binary search tree.

        Args:
            value: The value to insert.
        """

        def __insert(node: Optional[_TreeNode], value: Any) -> _TreeNode:
            if not node:
                return _TreeNode(value)
            if value < node.value:
                node.left = __insert(node.left, value)
            elif value > node.value:
                node.right = __insert(node.right, value)
            return node

        self._root = __insert(self._root, value)

    def remove(self, value: Any) -> None:
        """Remove a value from the binary search tree.

        Args:
            value: The value to remove.

        Raises:
            ValueError: If value is not found in the tree.
        """

        def __min(node: _TreeNode) -> _TreeNode:
            while node.left:
                node = node.left
            return node

        def __remove(node: Optional[_TreeNode], value: Any) -> Optional[_TreeNode]:
            if not node:
                raise ValueError(f"{value} not found in BinarySearchTree")

            if value < node.value:
                node.left = __remove(node.left, value)
            elif value > node.value:
                node.right = __remove(node.right, value)
            else:
                if not node.left:
                    return node.right
                if not node.right:
                    return node.left

                temp = __min(node.right)
                node.value = temp.value
                node.right = __remove(node.right, temp.value)

            return node

        self._root = __remove(self._root, value)

    def __contains__(self, value: Any) -> bool:
        """Check if a value is in the binary search tree.

        Args:
            value: The value to search for.

        Returns:
            bool: True if a node contains the value or False if not found.
        """
        node = self._root
        while node:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False
