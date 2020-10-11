from __future__ import annotations
from typing import Any
from accessify import private  # , protected
# from abc import ABC, abstractmethod
from random import randint, shuffle


def read_list() -> list:
    file = open('input.txt', 'r')
    line = file.readline()
    file.close()
    data = []
    previous = 0
    number = 0
    for i in line:
        number += 1
        if i == ' ':
            data.append(int(line[previous:number]))
            previous = number
    data.append(int(line[previous:]))
    return data


def write_list(data: list) -> None:
    result = ''
    for i in range(len(data)):
        result += str(data[i]) + ' '
    file = open('output.txt', 'w')
    file.write(result[:len(result) - 1])
    file.close()


def quick_sort(data: list) -> list:
    if len(data) < 2:
        return data
    data_1 = []
    data_2 = []
    for i in data[1:]:
        if i < data[0]:
            data_1.append(i)
        else:
            data_2.append(i)
    return quick_sort(data_1) + [data[0]] + quick_sort(data_2)


def merge_sort(data: list) -> list:
    if len(data) < 2:
        return data
    data_1 = merge_sort(data[:len(data) // 2])
    data_2 = merge_sort(data[len(data) // 2:])
    data = []
    while len(data_1) != 0 and len(data_2) != 0:
        if data_1[0] < data_2[0]:
            data.append(data_1[0])
            data_1.pop(0)
        else:
            data.append(data_2[0])
            data_2.pop(0)
    return data + data_1 + data_2


def test_bst(test_size: int = 10000, test_try: int = 5) -> None:
    saved_try = BinarySearchTree.__try__
    BinarySearchTree.__try__ = test_try

    test_lst = read_list()
    shuffle(test_lst)
    bst = BinarySearchTree(test_lst)

    collisions = 0
    key_list = []
    for v in range(test_size):
        dct = bst.insert(v)
        if dct['collision']:
            collisions += 1
        else:
            key_list.append(dct['key'])

    finding = 'OK'
    shuffle(key_list)
    for k in key_list:
        if bst.search(k).id is None:
            finding = 'ERROR'

    removing = 'OK'
    shuffle(key_list)
    for k in key_list:
        if not bst.remove(k):
            removing = 'ERROR'
    bst.print_tree()

    BinarySearchTree.__try__ = saved_try

    print(F'Inserting:  {len(key_list)}')
    print(F'Collisions: {collisions}')
    print(F'Finding:    {finding}')
    print(F'Removing:   {removing}')


class BinaryHeap(object):
    __none_node__: dict = {'index': None, 'value': None}

    def __init__(self: BinaryHeap,
                 data: list) -> None:
        self.data = data

    def __len__(self: BinaryHeap) -> int:
        return len(self.data)

    def __getitem__(self: BinaryHeap,
                    i:    int) -> int:
        return self.data[i]

    def __setitem__(self:  BinaryHeap,
                    i:     int,
                    value: int) -> None:
        self.data[i] = value

    def node(self: BinaryHeap,
             i:    int) -> dict:
        return {'index': i, 'value': self[i]}

    def parent(self: BinaryHeap,
               i:    int) -> dict:
        if i == 0:
            return BinaryHeap.__none_node__
        index = (i + i % 2) // 2 - 1
        return self.node(index)

    def left_child(self: BinaryHeap,
                   i:    int,
                   size: int) -> dict:
        index = 2 * i + 1
        if index >= size:
            return BinaryHeap.__none_node__
        return self.node(index)

    def right_child(self: BinaryHeap,
                    i:    int,
                    size: int) -> dict:
        index = 2 * i + 2
        if index >= size:
            return BinaryHeap.__none_node__
        return self.node(index)

    def swap(self: BinaryHeap,
             i:    int,
             j:    int) -> None:
        value = self[i]
        self[i] = self[j]
        self[j] = value

    def heapify(self: BinaryHeap,
                i:    int,
                size: int) -> None:
        this = self.node(i)
        left = self.left_child(i, size)
        right = self.right_child(i, size)
        if left['value'] is not None:
            if left['value'] > this['value']:
                this = left
        if right['value'] is not None:
            if right['value'] > this['value']:
                this = right
        if i != this['index']:
            self.swap(i, this['index'])
            self.heapify(this['index'], size)

    def build_heap(self: BinaryHeap) -> None:
        size = len(self)
        for i in range(self.parent(size - 1)['index'], -1, -1):
            self.heapify(i, size)

    def heap_sort(self: BinaryHeap) -> None:
        self.build_heap()
        size = len(self)
        while size > 0:
            size -= 1
            self.swap(0, size)
            self.heapify(0, size)


class BinarySearchTree(object):
    __id__:        int = 0
    __half__:      int = 536870912
    __depth__:     int = -1
    __try__:       int = 100
    __collision__: bool = False

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __init__(self: BinarySearchTree,
                 data: list) -> None:
        if len(data):
            self.__init_id__()
            self.value = data[0]
            self.left = BinarySearchTree(data[1:len(data) // 2 + 1])
            self.right = BinarySearchTree(data[len(data) // 2 + 1:])
            if self.id == 0:
                self.__init_key_and_depth__(0, 0)
        else:
            self.__init_leaf__()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def __str__(self: BinarySearchTree) -> str:
        if self.id is None:
            return '| - - - | - - N O T - F O U N D - - | - - - |'
        else:
            return F'|{self.id:>6} |{self.value:>12} |{self.key:>12} |{self.depth:>6} |'

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __init_leaf__(self: BinarySearchTree) -> None:
        self.id = None
        self.value = None
        self.key = None
        self.depth = None
        self.left = None
        self.right = None

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __init_id__(self: BinarySearchTree) -> None:
        self.id = BinarySearchTree.__id__
        BinarySearchTree.__id__ += 1

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __init_key_and_depth__(self:  BinarySearchTree,
                               key:   int,
                               depth: int) -> None:
        if self.id is not None:
            self.key = key
            self.depth = depth
            depth += 1
            space = BinarySearchTree.__half__ // 2**depth
            self.left.__init_key_and_depth__(key - space, depth)
            self.right.__init_key_and_depth__(key + space, depth)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def print_tree(self: BinarySearchTree) -> None:
        print()
        print('=================== B S T ===================')
        print('| ID    | VALUE       | KEY         | DEPTH |')
        print('|-------|-------------|-------------|-------|')
        self.__print_content__()
        print('=============================================')
        print()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __print_content__(self: BinarySearchTree) -> None:
        print(self)
        if self.id is not None:
            if self.left.id is not None:
                self.left.__print_content__()
            if self.right.id is not None:
                self.right.__print_content__()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def search(self: BinarySearchTree,
               key:  int) -> BinarySearchTree:
        if key == self.key or self.id is None:
            return self
        elif key < self.key:
            return self.left.search(key)
        elif key > self.key:
            return self.right.search(key)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def insert(self:    BinarySearchTree,
               value:   Any,
               key:     int = None,
               replace: bool = False) -> dict:
        if key is None:
            replace = False
            for i in range(BinarySearchTree.__try__):
                key = randint(-BinarySearchTree.__half__, BinarySearchTree.__half__)
                BinarySearchTree.__collision__ = False
                BinarySearchTree.__depth__ = -1
                self.__insert__(value, key, replace)
                if not BinarySearchTree.__collision__:
                    break
        else:
            BinarySearchTree.__collision__ = False
            BinarySearchTree.__depth__ = -1
            self.__insert__(value, key, replace)
        return {'key': key, 'collision': BinarySearchTree.__collision__}

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __insert__(self:    BinarySearchTree,
                   value:   Any,
                   key:     int,
                   replace: bool) -> None:
        BinarySearchTree.__depth__ += 1
        if self.id is None:
            self.__init_id__()
            self.value = value
            self.key = key
            self.depth = BinarySearchTree.__depth__
            self.left = BinarySearchTree([])
            self.right = BinarySearchTree([])
        elif key == self.key:
            if replace:
                self.value = value
                self.key = key
            else:
                BinarySearchTree.__collision__ = True
        elif key < self.key:
            self.left.__insert__(value, key, replace)
        elif key > self.key:
            self.right.__insert__(value, key, replace)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def remove(self: BinarySearchTree,
               key:  int) -> bool:
        if self.id is None:
            return False
        elif key == self.key:
            if self.left.id is None and self.right.id is None:
                self.__init_leaf__()
            elif self.left.id is None or self.right.id is None:
                self.__remove_from_chain__()
            else:
                self.__remove_from_tree__()
            return True
        elif key < self.key:
            return self.left.remove(key)
        elif key > self.key:
            return self.right.remove(key)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __remove_from_chain__(self: BinarySearchTree) -> None:
        if self.right.id is None:
            self.__assign__(self.left)
        else:
            self.__assign__(self.right)
        self.__increment_depth__(-1)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __assign__(self: BinarySearchTree,
                   tree: BinarySearchTree) -> None:
        self.id = tree.id
        self.value = tree.value
        self.key = tree.key
        self.depth = tree.depth
        self.left = tree.left
        self.right = tree.right

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __increment_depth__(self:      BinarySearchTree,
                            increment: int = 1) -> None:
        if self.id is not None:
            self.depth += increment
            self.left.__increment_depth__(increment)
            self.right.__increment_depth__(increment)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __remove_from_tree__(self: BinarySearchTree) -> None:
        value_key = self.right.__remove_min__()
        self.value, self.key = value_key

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @private
    def __remove_min__(self: BinarySearchTree) -> list:
        if self.left.id is None:
            value_key = [self.value, self.key]
            self.__remove_from_chain__()
            return value_key
        else:
            return self.left.__remove_min__()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
