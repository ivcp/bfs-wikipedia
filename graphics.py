from tkinter import Tk, Button, Label, Entry, Canvas
from main import main

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
        self.__button = Button(self.__root, text='Start', command=self.__click)
        self.__button.place(x=10, y=100)
        self.__input = Entry(self.__root)
        self.__input.place(x=10, y=50)


        self.canvas.create_line(1, 0, 1, 600, width=3)     
        

        self.running = False

    def __click(self):
        start = self.__input.get()
        path, total_checked, time_passed, error = main(start)
        if error:
            Label(self.__root, text='Page does not exist.').pack()
        else:
            Label(self.__root, text=path).pack()
            Label(self.__root, text=total_checked).pack()
            Label(self.__root, text=time_passed).pack()
            

    def draw_page(self, circle):
        x = (circle.x1 + circle.x0) / 2
        y = circle.y1 + 10
        circle.draw(self.canvas)        
        self.canvas.create_text(x, y, text=circle.title)
        self.canvas.create_line(x, y + 10, x, y + 40, arrow='last')

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False


class Circle:
    def __init__(self, x0, y0, x1, y1, title):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.title = title

    def draw(self, canvas):
        canvas.create_oval(self.x0, self.y0, self.x1, self.y1, width=1, fill='orange')


win = Window()
c = Circle(200, 10, 220, 30, 'First page')
c2 = Circle(200, 90, 220, 110, 'Second page')
win.draw_page(c)
win.draw_page(c2)
win.wait_for_close()