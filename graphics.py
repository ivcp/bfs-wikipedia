from tkinter import Tk, Button, Label, Entry, Canvas, END
from search import Search
import time

class Window:
    def __init__(self):
        self.width = 600
        self.height = 1000
        self.__root = Tk() 
        self.__root.title('All Clicks Lead To Rome')
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.geometry(f'{self.width}x{self.height}')
        #self.__root.configure(bg='red')
        self.canvas = Canvas(bg='skyblue', height=1000, width=400)
        self.canvas.place(x=200, y=0)
        self.__start_button = Button(self.__root, text='Start', command=self.__click)
        self.__start_button.place(x=10, y=100)
        self.__input = Entry(self.__root)
        self.__input.place(x=10, y=50)   
        self.__rand_button = Button(self.__root, text='Random', command=self.__get_random_page)     
        self.__rand_button.place(x=10, y=150)
        self.running = False

        self.__search = Search()

    def __click(self):
        
        start_page = self.__input.get()
        if start_page == '':
            return        
       
        if self.__search.page_error(start_page):
            #TODO: Clear lables
            Label(self.__root, text=f'Page for {start_page} does not exist. Try another one.', bg='red').pack()
        
        start_time = time.time()
        for i in self.__search.bfs_wikipedia(start_page, 'Rome'):
            self.canvas.delete('all')
            self.draw_nodes(i[0])
            total = Info()
            total.draw_checked(self.canvas, len(i[1]))
            self.__root.update()
        end_time = time.time()
        info = Info()
        info.draw_time(self.canvas, round(end_time - start_time))
        
        # if not found:
        #     Label(self.__root, text=f'Path not found from {start_page} to Rome', bg='red').pack()

    def draw_nodes(self, i):
        y0 = 50
        y1 = 70
        for j in range(len(i)):
            if j:
                y0 += 80
                y1 += 80
            arrow = True
            if j == len(i) - 1:
                arrow = False 
            p = Wiki_Page(200, y0, 220, y1, i[j])
            p.draw(self.canvas, arrow)
      
            
    def __get_random_page(self):
        random_page = self.__search.get_page(random=True)['query']['random'][0]['title']
        self.__input.delete(0, 'end')      
        self.__input.insert(0, random_page)      
           
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False


class Wiki_Page:
    def __init__(self, x0, y0, x1, y1, title):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.title = title

    def draw(self, canvas, arrow):
        canvas.create_oval(self.x0, self.y0, self.x1, self.y1, width=1, fill='orange')
        mid_x = (self.x1 + self.x0) / 2
        canvas.create_text(mid_x, self.y1 + 10, text=self.title)
        if arrow:
            canvas.create_line(mid_x, self.y1 + 25, mid_x, self.y1 + 45, arrow='last')

class Info:    
    def draw_checked(self, canvas, total_checked):
        canvas.create_text(5, 15, text=f'Pages checked: {total_checked}', anchor='nw')

    def draw_time(self, canvas, time):
        t = None
        u = 's' if time < 60 else 'm'
        if time > 60:
            t = round(time / 60)
        else: t = round(time)      
        canvas.create_text(5, 45, text=f'Time: {t}{u}', anchor='nw')
        
