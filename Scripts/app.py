import tkinter as tk
from controller import DashboardController

class App(tk.Tk):
    def __init__(self, *args):
        """Initialize the application."""
        super().__init__()
        self.controller = DashboardController(self)
        self.protocol("WM_DELETE_WINDOW", self.controller.on_close)

def main():
    """Entry point of the application."""
    root = App()
    root.mainloop()

if __name__ == "__main__":
    main()
