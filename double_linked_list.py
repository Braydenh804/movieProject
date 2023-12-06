class Node(object):

    def __init__(self, d, n=None, p=None):
        self.data = d
        self.next_node = n
        self.prev_node = p

    def get_next(self):
        return self.next_node

    def set_next(self, n):
        self.next_node = n

    def get_prev(self):
        return self.prev_node

    def set_prev(self, p):
        self.prev_node = p

    def get_data(self):
        return self.data

    def set_data(self, d):
        self.data = d


    def has_next(self):
        if self.get_next() is None:
            return False
        return True


class DoublyLinkedList(object):

    def __init__(self, head=None):
        self.head = head
        self.last = head
        self.size = 0

    def get_size(self):
        return self.size

    def add(self, key, values):
        data = {key: values}
        if self.size == 0:
            self.head = Node(data)
            self.last = self.head
        else:
            new_node = Node(data, self.head)
            self.head.set_prev(new_node)
            self.head = new_node
        self.size += 1

    def remove(self, d):
        this_node = self.head
        while this_node is not None:
            if this_node.get_data() == d:
                if this_node.get_prev() is not None:
                    if this_node.has_next():  # delete a middle node
                        this_node.get_prev().set_next(this_node.get_next())
                        this_node.get_next().set_prev(this_node.get_prev())
                    else:  # delete last node
                        this_node.get_prev().set_next(None)
                        self.last = this_node.get_prev()
                else:  # delete head node
                    self.head = this_node.get_next()
                    this_node.get_next().set_prev(self.head)
                self.size -= 1
                return True  # data removed
            else:
                this_node = this_node.get_next()
        return False  # data not found

    def find(self, d):
        this_node = self.head
        while this_node is not None:
            if this_node.get_data() == d:
                return d
            elif this_node.get_next() == self.head:
                return False
            else:
                this_node = this_node.get_next()
