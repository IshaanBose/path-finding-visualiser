"""
Contains custom data structures.
"""

class _Any:
    """A class that returns True whenever it is compared with anything."""
    def __init__(self):
        pass

    def __eq__(self, value):
        return True

class IncorrectDataTypeError(Exception):
    """Used to raise an error when the incorrect data type is entered."""
    pass

class Node:
    """
    This class is used to create tangible nodes for the A* algo to work on.
    """
    def __init__(self, pos, parent=None, g=0, h=0):
        self.pos = pos
        self.parent = parent
        self.g = g
        self.h = h
        self.f = self.g + self.h

class AugList(list):
    """
    Behaves like a list with an added functionality used to find Nodes in it.
    """
    def inlist(self, node):
        for i in range(len(self)):
            if self[i].pos == node.pos:
                return [True, i]
        return [False, None]

class Queue(AugList):
    """
        Queue
        =====
        This class is used to create a QUEUE and manipulate data within it.

        Attributes
        ----------
        `QUEUE: list`
            Stores the values in the QUEUE.

        `_inptype`
            Stores the type of data that the QUEUE can contain.

        Methods
        -------
        `enqueue(data)`
            Adds data into the queue.
        
        `dequeue()`
            Removes data from the queue.

        `is_empty()`
            Returns True if QUEUE is empty, else False.

        Examples
        --------
        >>> from datastructs import Queue
        >>> q = Queue() # a queue which allows insertion of all types of data.
        >>> q.enqueue(9) # add 9 into QUEUE
        >>> q.dequeue() # returns 9 and removes it from QUEUE
        >>> q = Queue(str) # a queue which only accepts <class 'str'> type values.
    """
    def __init__(self, _inptype = _Any()):
        """
            `Queue(_inptype)`

            Creates a QUEUE.

            If user does not provide any arguments then QUEUE is able to take any input, regardless of its data types. The user can
            restrict the type of data that is inserted into the QUEUE by passing it as the argument.

            Parameter
            ---------
            `_inptype optional`
                Stores type of data that can be inserted into the QUEUE. (By default, the QUEUE will accept any type of data)

            Examples
            --------
            >>> QUEUE() # accepts any type of data
            >>> QUEUE(str) # accepts only <class 'str'> data
            >>> QUEUE(list) # accepts only <class 'list'> data
        """
        self._inptype = _inptype

    def __str__(self):
        msg = ''
        for i in self:
            msg += str(i) + ' | '
        return msg

    def enqueue(self, data):
        """
            `Queue.enqueue(data)`

            Puts data into the QUEUE.

            The type of data is dependent upon the `_inptype` data member, passed during the initialisation of the `Queue` object.

            Parameter
            ---------
            `data`
                Value to be pushed into the QUEUE.

            Raises
            ------
            `IncorrectDataTypeError` 
                If the data enterered is not of type passed in `_inptype`.
        """
        if type(data) == self._inptype:
            self.append(data)
        else:
            raise IncorrectDataTypeError("Queue was initialised to take " + str(self._inptype) + " data.")

    def dequeue(self):
        """
            `Queue.dequeue()`

            Removes the first element from the queue.

            Returns
            -------
            `data`
                Data at the start of the QUEUE (type depenedent on `_inptype`)

            `None`
                If QUEUE is empty.
            """
        if len(self) != 0:
            val = self[0]
            self.remove(self[0])
            return val
        return None

    def is_empty(self) -> bool:
        """
            `Queue.is_empty()`

            Returns bool value depending upon the number of values in the QUEUE.

            Returns
            -------
            `True`
                If there is no data in the QUEUE.

            `False`
                If there is one or more data in the QUEUE.
        """
        return len(self) == 0

class Stack(AugList):
    """
        Stack
        =====
        This class is used to create a STACK and manipulate data within it.

        Attributes
        ----------
        `STACK: list`
            Stores the values for the STACK.

        `_inptype`
            Stores the type of data that the STACK can contain.

        Methods
        -------
        `push(data)`
            Pushes data on top of the STACK.

        `pop()`
            Pops the data at the top of the STACK.

        `is_empty()`
            Returns True if STACK is empty, else False.

        Examples
        --------
        >>> from datastructs import Stack
        >>> stack = Stack()
        >>> stack.push(9) # pushes 9 into the STACK
        >>> stack.pop(9) # removes 9 from the STACK
        >>> stack.is_empty() # returns True as the STACK is empty
    """
    def __init__(self, _inptype = _Any()):
        """
            `Stack(_inptype)`

            Creates a STACK.

            If user does not provide any arguments then STACK is able to take any input, regardless of its data types. The user can
            restrict the type of data that is inserted into the STACK by passing it as the argument.

            Parameter
            ---------
            `_inptype optional`
                Stores type of data that can be inserted into the STACK. (By default, the STACK will accept any type of data)

            Examples
            --------
            >>> Stack() # accepts any type of data
            >>> Stack(str) # accepts only <class 'str'> data
            >>> Stack(list) # accepts only <class 'list'> data
        """
        self._inptype = _inptype

    def __str__(self):
        string = ''
        for i in range(len(self) - 1, -1, -1):
            string += str(self[i]) + '\n'
        string += 'END OF STACK'
        return string

    def push(self, data):
        """
            `Stack.push(data)`

            Pushes data into the STACK.

            The type of data is dependent upon the `_inptype` data member, passed during the initialisation of the `Stack` object.

            Parameter
            ---------
            `data`
                Value to be pushed into the STACK.

            Raises
            ------
            `IncorrectDataTypeError` 
                If the data enterered is not of type passed in `_inptype`.
        """
        if type(data) == self._inptype:
            self.insert(0, data)
        else:
            raise IncorrectDataTypeError("Stack was initialised to take " + str(self._inptype) + " data.")

    def pop(self):
        """
            `Stack.pop()`

            Pops the data from the top of the STACK.

            This function returns the data from the top of the STACK and removes it as well.

            Returns
            -------
            `data`
                Data from top of STACK whose data type is dependent upon `_inptype`.

            `"EOS"`
                If there is no data in the STACK.
        """
        try:
            val = self[0]
            self.remove(self[0])
            return val
        except IndexError:
            return 'EOS'

    def is_empty(self) -> bool:
        """
            `Stack.is_empty()`

            Returns bool value depending upon the number of values in the STACK.

            Returns
            -------
            `True`
                If there is no data in the STACK.

            `False`
                If there is one or more data in the STACK.
        """
        return len(self) == 0