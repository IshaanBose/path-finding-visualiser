"""
Path Finding Visualiser
=======================

Provides the following classes:
1. PygameMaze - used to create the maze
2. TkRoot - root window for Tkinter
3. TkMainMenu - used to display the main menu
4. TkInstructions - used to display the instructions
"""

try:
    from tkinter import Tk
    from tkinter import Label
    from tkinter import Entry
    from tkinter import Button
    from tkinter import SOLID
    from tkinter import Radiobutton
    from tkinter import Frame
    from tkinter import Text
    from tkinter import ttk
    from tkinter import font as tkfont
    from tkinter import BooleanVar
    from tkinter import StringVar
    from tkinter import INSERT
    from tkinter.messagebox import showwarning
    from tkinter.messagebox import showinfo
except ModuleNotFoundError:
    print('tkinter module not installed. Refer: https://tkdocs.com/tutorial/install.html')
    quit()

try:
    import pygame
    from pygame.locals import *
    from pygame import draw as pdraw
except ModuleNotFoundError:
    print('pygame module not installed. Run: %installdir%python.exe -m pip install -U pygame --user')
    quit()

import os
import path_finding as pf

ROOT_X, ROOT_Y = 0, 0
COLOURS = {'black' : (0, 0, 0), 'white' : (255, 255, 255), 'green':(0, 255, 0), 'mustard yellow':(255, 208, 0), 
            'light pink': (255, 122, 251), 'red': (255, 0, 0), 'dark blue': (2, 68, 173)}

class PygameMaze():
    """
    This class creates the maze GUI and contains functions that implements many path finding algorithms.
    """
    def __init__(self, maze_dim, start_node, goal_node, show_exp, algo, x=50, y=50):
        """
        Initialises the maze GUI.
        
        Parameter
        ---------
        `maze_dim: list/tuple`
            Dimensions of the maze in cells.
            
        `start_node: list/tuple`
            Co-ordinates of starting node.
            
        `goal_node: list/tuple`
            Co-ordinates of goal node.
            
        `show_exp: bool`
            If True, shows the exploration path. If False, directly shows the path from starting node to goal node.
            
        `algo: str`
            Contains which path finding algorithm to use.
            
        `x: int`
            X-axis point where window will be placed.
            
        `y: int`
            Y-axis point where window will be placed.
        """
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y) # to place window at (x, y) position
        
        self._running = False
        self._display = None
        self.show_exp = show_exp
        self.algo = algo
        self.mouse_drag = False
        self.clear_obs = False
        self.start_node = (start_node[0] * 20, start_node[1] * 20)
        self.goal_node = (goal_node[0] * 20, goal_node[1] * 20)
        self.blocked = list()
        self.width, self.height = maze_dim[0] * 20, maze_dim[1] * 20
        
    def on_init(self):
        """
        For initialising data before the display surface is shown and drawing all static elements of the maze.
        """
        self._display = pygame.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF)
        pygame.display.set_caption('Path Finding Visualiser')
        
        self.draw_maze()
        
        self._running = True
        pygame.init()
        
    def on_event(self, event):
        """
        For handling all events on the dislpay surface.
        """
        if event.type == QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                self.draw_maze()
                self.redraw_obstacles()
                if self.algo == 'A*':
                    pf.astar_path(self)
                elif self.algo == 'BFS':
                    pf.bfs(self)
                elif self.algo == 'DFS':
                    pf.dfs(self)
                elif self.algo == 'RBFS':
                    pf.rbfs(self, self.start_node)
            elif event.key == K_SPACE and pygame.key.get_mods() & KMOD_CTRL:
                self.draw_maze()
                self.redraw_obstacles()
            elif event.key == K_SPACE:
                self.blocked.clear()
                self.draw_maze()
            elif event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4:
                if event.key == K_1:
                    self.algo = 'A*'
                elif event.key == K_2:
                    self.algo = 'BFS'
                elif event.key == K_3:
                    self.algo = 'DFS'
                elif event.key == K_4:
                    self.algo = 'RBFS'
                self.tk_popup('Algorithm Changed!', 'Algorithm changed to ' + self.algo, 'info')
        elif event.type == MOUSEBUTTONDOWN:
            self.mouse_drag = True
            pos = pygame.mouse.get_pos()
            
            if len(self.blocked) == 0:
                self.modify_obstacle(pos)
                return
            else:
                for i in self.blocked:
                    if (pos[0] >= i[0] and pos[1] >= i[1]) and (pos[0] <= i[0] + 20 and pos[1] <= i[1] + 20) and i not in [self.start_node, self.goal_node]:
                        self.clear_obs = True
                        break
                    self.clear_obs = False
                self.modify_obstacle(pos, self.clear_obs)
        elif event.type == MOUSEMOTION:
            if self.mouse_drag:
                pos = pygame.mouse.get_pos()
                self.modify_obstacle(pos, self.clear_obs)
        elif event.type == MOUSEBUTTONUP:
            self.mouse_drag = False
    
    def stop_path_finding(self):
        """
        This function is used to stop the execution of the path finding algorithm.
        """
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return 'STOP'
            elif event.type == QUIT:
                self.on_cleanup()
    
    def tk_popup(self, title, message, poptype='warning'):
        """"
        This function is used to bring up a popup window using Tkinter.
        """
        temp = Tk()
        temp.geometry('0x0')
        temp.wm_withdraw()
        if poptype == 'warning':
            showwarning(title, message)
        else:
            showinfo(title, message)
        temp.destroy()
    
    def render_exploration(self, point, rtype, group=False):
        """
        This function is used to show how nodes are explored when the path finding algo runs.
        """
        if group:
            for node in point:
                pdraw.rect(self._display, COLOURS['green'], (node.pos[0] + 1, node.pos[1] + 1, 19, 19))
        else:
            if rtype == 'visited':
                pdraw.rect(self._display, COLOURS['red'], (point[0] + 1, point[1] + 1, 19, 19))
            elif rtype == 'clear':
                pdraw.rect(self._display, COLOURS['white'], (point[0] + 1, point[1] + 1, 19, 19))
        
        pygame.time.wait(50) # defines time interval between each update of exploration
        pygame.display.update()
    
    def show_path(self, path):
        """
        This function is used to show the final path from the start node to goal node.
        """
        if self.show_exp:
            pygame.time.wait(1000) # giving time for user to look at finished exploration, time is given in ms
            self.draw_maze()
            self.redraw_obstacles()
        
        for i in path:
            if i != self.start_node and i != self.goal_node:
                pdraw.rect(self._display, COLOURS['light pink'], (i[0] + 1, i[1] + 1, 19, 19))
    
    def draw_maze(self):
        """
        This function is used to draw/redraw the maze.
        """
        self._display.fill(COLOURS['white'])
        
        for i in range(0, self.width + 1, 20):
            pdraw.line(self._display, COLOURS['black'], (i, 0), (i, self.height))
        for i in range(0, self.height + 1, 20):
            pdraw.line(self._display, COLOURS['black'], (0, i), (self.width, i))
        
        pdraw.rect(self._display, COLOURS['mustard yellow'], (self.start_node[0] + 1, self.start_node[1] + 1, 19, 19)) # start node
        pdraw.rect(self._display, COLOURS['dark blue'], (self.goal_node[0] + 1, self.goal_node[1] + 1, 19, 19)) # goal node
    
    def redraw_obstacles(self):
        """
        This function is used to redraw the obstacles after redrawing the maze.
        """
        for i in self.blocked:
            pdraw.rect(self._display, COLOURS['black'], (i[0], i[1], 19, 19))
    
    def modify_obstacle(self, mouse_pos, clear=False):
        """
        This function is used to draw/remove an obstacle on the square the user clicks on.
        """
        for i in range(0, self.width - 19, 20):
            for j in range(0, self.height - 19, 20):
                if (mouse_pos[0] >= i and mouse_pos[1] >= j) and (mouse_pos[0] <= i + 20 and mouse_pos[1] <= j + 20) and (i, j) not in [self.start_node, self.goal_node]:
                    if not clear:
                        if not (i, j) in self.blocked:
                            self.blocked.append((i, j))
                            pdraw.rect(self._display, COLOURS['black'], (i, j, 19, 19))
                            return
                    else:
                        if (i, j) in self.blocked:
                            self.blocked.remove((i, j))
                            pdraw.rect(self._display, COLOURS['white'], (i + 1, j + 1, 19, 19))
                            return
    
    def on_cleanup(self):
        """
        For handling all operations to be done before the game loop is broken.
        """
        pygame.quit()
        del self # deletes current instance of of the maze
        TkRoot()
    
    def on_execute(self):
        """
        For handling all operations to be done while executing the program.
        """
        self.on_init()
        
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            pygame.display.update()
        self.on_cleanup()

class TkRoot(Tk):
    """
    Contains root window of Tkinter.
    """
    def __init__(self,  width=500, height=500, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        self.title('Path Finder')
        
        global ROOT_X, ROOT_Y
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        ROOT_X = (screen_width // 4) - (width // 2)
        ROOT_Y = int(screen_height / 2.5) - (height // 2)
        
        self.geometry('500x500+' + str(ROOT_X) + '+' + str(ROOT_Y))
        self.resizable(False, False)
        
        self.frames = dict()
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for F in (TkMainMenu, TkInstructions):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(TkMainMenu)
        self.mainloop()

    def show_frame(self, cont):
        """
        Used to display frames.
        """
        frame = self.frames[cont]
        frame.tkraise()

class TkMainMenu(Frame):
    """
    Creates the main menu frame.
    """
    def __init__(self, parent, controller: TkRoot, max_width = 70, max_height = 35):
        """
        Parameter
        ---------
        `max_width: int, optional`
            Defines the maximum width, in terms of cells, allowed for the creation of the maze.
            
        `max_height: int, optional`
            Defines the maximum height, in terms of cells, allowed for the creation of the maze.
        """
        Frame.__init__(self, parent)
        
        self.controller = controller
        self.max_width = max_width
        self.max_height = max_height
        self.title_font = tkfont.Font(family='Times', size=32, weight='bold')
        self.label_font = tkfont.Font(family='Times', size=16)
        self.button_font = tkfont.Font(family='Times', size=13)
        
        self._add_widgets()
    
    def _add_widgets(self):
        """
        Adds all widgets to the GUI.
        """
        # Label: Path Finding Viusaliser
        Label(self, text='Path Finding Viusaliser', font=self.title_font).grid(row=0, column=0, columnspan=4, ipadx=30, ipady=30)
        # Label: Maze Dimensions
        Label(self, text='Maze Dimensions:', font=self.label_font).grid(row=1, column=0, ipadx=30, ipady=10)
        # Entry: for getting maze dimensions
        maze_dim = Entry(self, width=40, bd=1, relief=SOLID)
        maze_dim.grid(row=1, column=1, columnspan=2)
        #Label: Start Node:
        Label(self, text='Start Node:', font=self.label_font).grid(row=2, column=0, ipady=10)
        #Entry: for getting starting node
        start_node = Entry(self, width=40, bd=1, relief=SOLID)
        start_node.grid(row=2, column=1, columnspan=2)
        #Label: Goal Node:
        Label(self, text='Goal Node:', font=self.label_font).grid(row=3, column=0, ipady=10)
        #Entry: for getting goal node
        goal_node = Entry(self, width=40, bd=1, relief=SOLID)
        goal_node.grid(row=3, column=1, columnspan=2)
        #Label: Show Exploration:
        Label(self, text='Show Exploration:', font=self.label_font).grid(row=4, column=0, ipady=10)
        #Radiobutton: configurations for radio buttons
        show_exp = BooleanVar()
        show_exp.set(False)
        r1 = Radiobutton(self, text='Yes', variable=show_exp, value=True)
        r2 = Radiobutton(self, text='No', variable=show_exp, value=False)
        r1['font'] = r2['font'] = self.label_font
        r1.grid(row=4, column=1)
        r2.grid(row=4, column=2)
        #Label: Path finding algo
        Label(self, text='Path Finding Algo:', font=self.label_font).grid(row=5, column=0, ipady=10)
        #Dropdown list: config for dropdown list
        algo = StringVar()
        algo_cb = ttk.Combobox(self, width=20, textvariable=algo, state='readonly')
        algo_cb['values'] = ('A*', 'BFS', 'DFS', 'RBFS')
        algo_cb.current(0)
        algo_cb.grid(row=5, column=1, columnspan=2, ipadx=50)
        #Button: configuration for button
        button = Button(self, text='Create Maze', width=20, bg='white', bd=1, relief=SOLID, 
                        command=lambda: self.check_maze_constraints(maze_dim.get(), start_node.get(), goal_node.get(), show_exp.get(), algo.get()))
        button['font'] = self.button_font
        button.grid(row=6, column=0, columnspan=3, ipady=5, pady=30)
        #Instructions
        inst = Label(self, text='Instructions', fg='blue', font=('Times 10'))
        inst.grid(row=7, column=0, columnspan=3)
        inst.bind('<Button-1>', self.show_instructions)

    def show_instructions(self, event):
        """
        Displays the instructions frame.
        """
        self.controller.show_frame(TkInstructions)

    def check_maze_constraints(self, maze_dim, start_node, goal_node, show_exp, algo):
        """
        Checks the maze constraints entered by user to make sure they are vaiid for the creation of the maze. 
        """
        error = [False, '']
        
        try:
            maze_dim = [int(i) for i in maze_dim.split()]
            start_node = [int(i) for i in start_node.split()]
            goal_node = [int(i) for i in goal_node.split()]
        except ValueError:
            showwarning('Invalid maze constraints', 'Input must be numerical!')
            return
        
        if len(maze_dim) != 2 or len(start_node) != 2 or len(goal_node) != 2:
            showwarning('Invalid maze constraints', 'Give input in the form of: x y')
            return
        
        try:
            if maze_dim[0] > self.max_width or maze_dim[1] > self.max_height:
                error[1] += 'Max maze dimension allowed: 70 35! '
                error[0] = True
            if start_node[0] >= maze_dim[0] or start_node[1] >= maze_dim[1] or start_node[0] < 0 or start_node[1] < 0:
                error[1] += 'Start node must be within maze dimensions! '
                error[0] = True
            if goal_node[0] >= maze_dim[0] or goal_node[1] >= maze_dim[1] or goal_node[0] < 0 or goal_node[1] < 0:
                error[1] += 'Goal node must be within maze dimensions! '
                error[0] = True
        except IndexError:
            error[1] += "Cannot leave constraints empty!"
            error[0] = True
        
        if error[0]:
            showwarning("Invalid maze constraints!", error[1])
        else:
            global ROOT_X, ROOT_Y
            self.controller.destroy()
            PygameMaze(maze_dim, start_node, goal_node, show_exp, algo, ROOT_X, ROOT_Y).on_execute()

class TkInstructions(Frame):
    """
    Creates the Instructions frame.
    """
    def __init__(self, parent, controller: TkRoot):
        Frame.__init__(self, parent)
        
        self.controller = controller
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.display_instructions()
        
    def display_instructions(self):
        """
        Sets instruction text.
        """
        dirname = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dirname, 'resources', 'docs', 'instructions.txt')
        with open(filename) as f:
            instmsg = f.read()

        inst = Text(self, wrap='word', font=('Times 15'), padx=5, bg=self.controller.cget('bg'), relief='flat')
        inst.insert(INSERT, instmsg)
        inst.configure(state='disabled')
        inst.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        scrollb = ttk.Scrollbar(self, command=inst.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        inst['yscrollcommand'] = scrollb.set
        
        back = Label(self, text='Go Back', fg='blue', font=('Times 10'))
        back.grid(row=1, column=0)
        back.bind('<Button-1>', self.go_back)
    
    def go_back(self, event):
        """
        Used to go back to main menu.
        """
        self.controller.show_frame(TkMainMenu)