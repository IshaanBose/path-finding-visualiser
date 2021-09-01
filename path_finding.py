from _datastructs import *
from math import  sqrt

def astar_path(mazegui):
    """
    This function implements the A* path finding algorithm for the maze.
    """
    AVAILABLE = AugList(list())
    VISITED = AugList(list())
    currnode = Node(mazegui.start_node, h=sqrt((mazegui.start_node[0] - mazegui.goal_node[0])**2 + (mazegui.start_node[1] - mazegui.goal_node[1])**2))
    goal = Node(mazegui.goal_node)
    AVAILABLE.append(currnode)
    
    while len(AVAILABLE) != 0:
        if mazegui.stop_path_finding() == 'STOP':
            return
        
        currnode = AVAILABLE[0]
        for node in AVAILABLE:
            if node.f < currnode.f:
                currnode = node
        
        VISITED.append(currnode)
        if mazegui.show_exp:
            mazegui.render_exploration(currnode.pos, 'visited')
        
        if currnode.pos == goal.pos:
            path = list()
            while currnode:
                path.append(currnode.pos)
                currnode = currnode.parent
            return mazegui.show_path(path)
        
        neighbours = list()
        for i in ((-20, -20), (-20, 0), (-20, 20), (0, 20), (20, 20), (20, 0), (20, -20), (0, -20)):
            if currnode.pos[0] + i[0] < 0 or currnode.pos[1] + i[1] < 0 or currnode.pos[0] + i[0] >= mazegui.width or currnode.pos[1] + i[1] >= mazegui.height:
                continue
            
            if (currnode.pos[0] + i[0], currnode.pos[1] + i[1]) in mazegui.blocked:
                continue
            
            if i in ((-20, -20), (-20, 20), (20, 20), (20, -20)):
                node = Node((currnode.pos[0] + i[0], currnode.pos[1] + i[1]), currnode, 28.28)
            else:
                node = Node((currnode.pos[0] + i[0], currnode.pos[1] + i[1]), currnode, 20)
            neighbours.append(node)
            
        newavail = list()
        for node in neighbours:
            if not VISITED.inlist(node)[0]: # heuristic is consistent, so no need to re-visit nodes
                if not AVAILABLE.inlist(node)[0]:
                    node.g += currnode.g
                    node.f = node.g + sqrt((node.pos[0] - goal.pos[0])**2 + (node.pos[1] - goal.pos[1])**2)
                    AVAILABLE.append(node)
                    newavail.append(node)
                else:
                    opennode = AVAILABLE[AVAILABLE.inlist(node)[1]] # if the node is already available to visit, we want to check if there is a better path for it
                    if opennode.g > node.g + currnode.g:
                        opennode.g = node.g + currnode.g
                        opennode.f = opennode.g + sqrt((node.pos[0] - goal.pos[0])**2 + (node.pos[1] - goal.pos[1])**2)
                        opennode.parent = currnode
        if mazegui.show_exp:
            mazegui.render_exploration(newavail, 'available', True)
        
        AVAILABLE.remove(currnode)
    
    mazegui.tk_popup('No Path Found!', "No path found! Press 'Space' to clear the screen.")

def bfs(mazegui):
    """
    This function implements the BFS algorithm for the maze.
    """
    Q = Queue()
    VISITED = AugList(list())
    currnode = Node(mazegui.start_node)
    goal = Node(mazegui.goal_node)
    Q.enqueue(currnode)
    
    while not Q.is_empty():
        if mazegui.stop_path_finding() == 'STOP':
            return
        
        currnode = Q.dequeue()
        VISITED.append(currnode)
        if mazegui.show_exp:
            mazegui.render_exploration(currnode.pos, 'visited')
            
        if currnode.pos == goal.pos:
            path = list()
            while currnode:
                path.append(currnode.pos)
                currnode = currnode.parent
            return mazegui.show_path(path)
        
        newavail = list()
        for i in ((-20, -20), (-20, 0), (-20, 20), (0, 20), (20, 20), (20, 0), (20, -20), (0, -20)):
            if currnode.pos[0] + i[0] < 0 or currnode.pos[1] + i[1] < 0 or currnode.pos[0] + i[0] >= mazegui.width or currnode.pos[1] + i[1] >= mazegui.height:
                continue
            
            if (currnode.pos[0] + i[0], currnode.pos[1] + i[1]) in mazegui.blocked:
                continue
            
            node = Node((currnode.pos[0] + i[0], currnode.pos[1] + i[1]), currnode)
            if not Q.inlist(node)[0] and not VISITED.inlist(node)[0]:
                Q.enqueue(node)
                newavail.append(node)
        
        if mazegui.show_exp:
            mazegui.render_exploration(newavail, 'available', True)
    
    mazegui.tk_popup('No Path Found!', "No path found! Press 'Space' to clear the screen.")

def dfs(mazegui):
    """
    This function implements the DFS algorithm for the maze.
    """
    stack = Stack()
    VISITED = AugList(list())
    currnode = Node(mazegui.start_node)
    goal = Node(mazegui.goal_node)
    stack.push(currnode)
    
    while not stack.is_empty():
        if mazegui.stop_path_finding() == 'STOP':
            return
        
        currnode = stack.pop()
        VISITED.append(currnode)
        if mazegui.show_exp:
            mazegui.render_exploration(currnode.pos, 'visited')
        
        if currnode.pos == goal.pos:
            path = list()
            while currnode:
                path.append(currnode.pos)
                currnode = currnode.parent
            return mazegui.show_path(path)
        
        newavail = list()
        for i in ((-20, -20), (-20, 0), (-20, 20), (0, 20), (20, 20), (20, 0), (20, -20), (0, -20)):
            if currnode.pos[0] + i[0] < 0 or currnode.pos[1] + i[1] < 0 or currnode.pos[0] + i[0] >= mazegui.width or currnode.pos[1] + i[1] >= mazegui.height:
                continue
            
            if (currnode.pos[0] + i[0], currnode.pos[1] + i[1]) in mazegui.blocked:
                continue
            
            node = Node((currnode.pos[0] + i[0], currnode.pos[1] + i[1]), currnode)
            if not stack.inlist(node)[0] and not VISITED.inlist(node)[0]:
                stack.push(node)
                newavail.append(node)
        
        if mazegui.show_exp:
            mazegui.render_exploration(newavail, 'available', True)
    
    mazegui.tk_popup('No Path Found!', "No path found! Press 'Space' to clear the screen.")

def rbfs(mazegui, currnode, flimit=float('inf')):
    """
    This function implements the RBFS path finding algorithm for the maze.
    """
    if not isinstance(currnode, Node):
        currnode = Node(currnode, Node((-1, -1)))
    if mazegui.show_exp:
            mazegui.render_exploration(currnode.pos, 'visited')
    
    if currnode.pos == mazegui.goal_node:
        path = list()
        node = currnode
        
        while node:
            if node.pos != (-1, -1):
                path.append(node.pos)
            node = node.parent
        mazegui.show_path(path)
        return True
    
    neighbours = list()
    for i in ((-20, -20), (-20, 0), (-20, 20), (0, 20), (20, 20), (20, 0), (20, -20), (0, -20)):
        newx, newy = currnode.pos[0] + i[0], currnode.pos[1] + i[1]
        if newx < 0 or newy < 0 or newx >= mazegui.width or newy >= mazegui.height:
                continue
        
        if (newx, newy) == currnode.parent.pos:
            continue
        
        if (newx, newy) in mazegui.blocked:
            continue
        
        if i in ((-20, -20), (-20, 20), (20, 20), (20, -20)):
            node = Node((newx, newy), currnode, 28.28 + currnode.g, sqrt((newx - mazegui.goal_node[0])**2 + (newy - mazegui.goal_node[1])**2))
        else:
            node = Node((newx, newy), currnode, 20 + currnode.g, sqrt((newx - mazegui.goal_node[0])**2 + (newy - mazegui.goal_node[1])**2))
        neighbours.append(node)
    
    if not neighbours:
        currnode.f = float('inf')
        mazegui.render_exploration(currnode.pos, 'clear')
        return False
    
    for node in neighbours: # to ensure we're not unnecessarily moving away from the goal node
        node.f = max(node.f, currnode.f)
    
    result = False
    while not result:
        if mazegui.stop_path_finding() == 'STOP':
            return 
        lnode = Node(None)
        lnode.f, altf = float('inf'), float('inf')
        
        for node in neighbours:
            if node.f < lnode.f:
                if lnode.f != float('inf'):
                    altf = lnode.f
                lnode = node
            elif node.f < altf:
                altf = node.f
        if lnode.f > flimit:
            currnode.f = lnode.f
            mazegui.render_exploration(currnode.pos, 'clear')
            return False
        else:
            result = rbfs(mazegui, lnode, min(altf, flimit))
        if result:
            return True