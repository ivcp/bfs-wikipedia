from tkinter import Tk, Button, Label, Entry, Canvas, END
from search import Search

class Window:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.__root = Tk() 
        self.__root.title('All Clicks Lead To Rome')
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.geometry(f'{self.width}x{self.height}')
        #self.__root.configure(bg='red')
        self.canvas = Canvas(bg='skyblue', height=600, width=400)
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
        self.canvas.delete('all')
        start_page = self.__input.get()
        if start_page == '':
            return
        found, total_checked, time_passed, error = self.__search.find_path(start_page)
        if error:
            #TODO: Clear lables
            Label(self.__root, text=f'Page for {start_page} does not exist. Try another one.', bg='red').pack()
        else:
            if not found:
                Label(self.__root, text=f'Path not found from {start_page} to Rome', bg='red').pack()
            y0 = 50
            y1 = 70
            for i in range(len(found)):
                if i:
                    y0 += 80
                    y1 += 80
                arrow = True
                if i == len(found) - 1:
                    arrow = False 
                p = Wiki_Page(200, y0, 220, y1, found[i])
                p.draw(self.canvas, arrow)
            info = Info(total_checked, time_passed)
            info.draw(self.canvas)

            
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
    def __init__(self, total_checked, time):
        self.total_checked = total_checked
        self.time = time

    def draw(self, canvas):
        t = self.time
        u = 's' if self.time < 60 else 'm'
        if self.time > 60:
            t = round(self.time / 60)
        canvas.create_text(5, 15, text=f'Pages checked: {self.total_checked}', anchor='nw')
        canvas.create_text(5, 45, text=f'Time: {t}{u}', anchor='nw')
        
