from tkinter import Canvas, ttk
from ttkthemes import ThemedTk
from search import Search
import time

class Window:
    def __init__(self):
        self.width = 600
        self.height = 1000
        self.__root = ThemedTk(theme='equilux') 
        self.__root.configure(bg='#414141')      
        self.__root.title('All Clicks Lead To Rome')
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.geometry(f'{self.width}x{self.height}')        
        self.canvas = Canvas(bg='#414141', height=1000, width=400, highlightbackground='#636363')
        self.canvas.place(x=200, y=0)
        self.start_button = ttk.Button(self.__root, text='Start', command=self.click)
        self.start_button.place(x=10, y=100)
        self.stop_button = ttk.Button(self.__root, text='Stop', command=self.stop_search)
        self.stop_button.place(x=10, y=200)
        ttk.Label(text='Starting page:', background='#414141').place(x=10, y=30)        
        self.input = ttk.Entry(self.__root)
        self.input.place(x=10, y=50)   
        self.rand_button = ttk.Button(self.__root, text='Random Page', command=self.get_random_page)     
        self.rand_button.place(x=10, y=150)
        self.search = Search()        
        self.error_message = ttk.Label(self.__root)
        self.error_message.configure(foreground='#E78F7D')
        self.running = False
        self.stop = False

    def stop_search(self):
        self.stop = True
        self.toggle_buttons_state('normal')
  
    def toggle_buttons_state(self, state):
        self.start_button.config(state=state)        
        self.rand_button.config(state=state)  
    
    def click(self):
        self.stop = False
        self.toggle_buttons_state('disabled')       
        start_page = self.input.get()
        if start_page == '':
            self.toggle_buttons_state('normal')
            return        
        
        if self.search.page_error(start_page):
            self.display_error_message(f"Page {start_page} does not exist. Try another one.")
            self.toggle_buttons_state('normal')
            return
        
        self.error_message.pack_forget()         
        start_time = time.time()
        for i in self.search.bfs_wikipedia(start_page, 'Rome'):
            if self.stop:
                return            
            self.canvas.delete('all')
            self.draw_nodes(i[0])
            total = Info()
            total.draw_checked(self.canvas, len(i[1]))
            self.__root.update()
        end_time = time.time()
        info = Info()
        info.draw_time(self.canvas, round(end_time - start_time))
        self.toggle_buttons_state('normal')
                 
    def display_error_message(self, error_message):
        self.error_message.config(text=error_message)
        self.error_message.pack()


    def draw_nodes(self, path_array):
        y0 = 50
        y1 = 70
        for node in range(len(path_array)):
            if node:
                y0 += 80
                y1 += 80
            arrow = True
            if node == len(path_array) - 1:
                arrow = False 
            p = Wiki_Page(200, y0, 220, y1, path_array[node])
            p.draw(self.canvas, arrow)
      
            
    def get_random_page(self):
        random_page = self.search.get_page(random=True)['query']['random'][0]['title']
        self.input.delete(0, 'end')      
        self.input.insert(0, random_page)      
           
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


        canvas.create_oval(self.x0, self.y0, self.x1, self.y1, width=0.1, outline='#636363', fill='#636363')
        mid_x = (self.x1 + self.x0) / 2
        canvas.create_text(mid_x, self.y1 + 10, text=self.title, fill='#D6D6D6')
        if arrow:
            canvas.create_line(mid_x, self.y1 + 25, mid_x, self.y1 + 45, fill='#D6D6D6', arrow='last')

class Info:    
    def draw_checked(self, canvas, total_checked):
        canvas.create_text(5, 15, text=f'Pages checked: {total_checked}', fill='#D6D6D6', anchor='nw')

    def draw_time(self, canvas, time):
        t = None
        u = 's' if time < 60 else 'm'
        if time > 60:
            t = round(time / 60)
        else: t = round(time)      
        canvas.create_text(5, 45, text=f'Time: {t}{u}', fill='#D6D6D6', anchor='nw')
        
