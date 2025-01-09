from typing import Dict, List, Optional, Set, TypeVar

T = TypeVar("T")


class _LinkedListNode[T]:
    value: T
    next: Optional["_LinkedListNode[T]"]
    partition: "_Partition"

    def __init__(
        self,
        value: T,
        next_: "_LinkedListNode[T]" = None,
        partition: "_Partition" = None
    ) -> None:
        self.value = value
        self.next = next_
        self.partition = partition


class _Partition[T]:
    head: _LinkedListNode[T]
    tail: _LinkedListNode[T]
    length: int

    def __init__(self, element: _LinkedListNode[T]) -> None:
        self.head = element
        self.tail = element
        self.length = 1

    def get_representative(self) -> T:
        return self.head.value

    def get_elements(self) -> Set[T]:
        elements = set()
        cur_node = self.head
        while cur_node is not None:
            elements.add(cur_node.value)
            cur_node = cur_node.next
        return elements


class DisjointSetLinkedList[T]:
    elements: Dict[T, _LinkedListNode[T]]
    partitions: Set[_Partition[T]]

    def __init__(self, values: List[T]) -> None:
        self.elements = {}
        self.partitions = set()

        for value in values:
            if value in self.elements:
                continue

            node = _LinkedListNode(value)
            node.partition = _Partition(node)
            self.elements[value] = node
            self.partitions.add(node.partition)

    def make_set(self, value: T) -> bool:
        if value in self.elements:
            return False

        node = _LinkedListNode(value, None, None)
        node.partition = _Partition(node)
        self.elements[value] = node
        self.partitions.add(node.partition)
        return True

    def find_set(self, value: T) -> Optional[T]:
        if value not in self.elements:
            return None
        return self.elements[value].partition.get_representative()

    def union(self, this: T, that: T) -> Optional[T]:
        if this not in self.elements and that in self.elements:
            return that
        if this in self.elements and that not in self.elements:
            return this
        if this not in self.elements and that not in self.elements:
            return None

        this_partition = self.elements[this].partition
        that_partition = self.elements[that].partition
        if this_partition == that_partition:
            return None

        if this_partition.length >= that_partition.length:
            bigger_partition = this_partition
            smaller_partition = that_partition
        else:
            bigger_partition = that_partition
            smaller_partition = this_partition

        bigger_partition.tail.next = smaller_partition.head
        bigger_partition.tail = smaller_partition.tail
        bigger_partition.length += smaller_partition.length

        cur_node = smaller_partition.head
        while cur_node is not None:
            cur_node.partition = bigger_partition
            cur_node = cur_node.next

        self.partitions.remove(smaller_partition)
        return bigger_partition.head.value

    def same_set(self, this: T, that: T) -> bool:
        return self.find_set(this) == self.find_set(that)

    def subsets(self) -> List[Set[T]]:
        return [partition.get_elements() for partition in self.partitions]
