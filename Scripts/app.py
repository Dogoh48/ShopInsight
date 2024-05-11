"""
app.py: Tkinter application for data visualization.
"""
import tkinter as tk
from controller import DashboardController

class App(tk.Tk):
    """Main application class."""
    def __init__(self):
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
