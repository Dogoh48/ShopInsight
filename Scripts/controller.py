import tkinter as tk
from tkinter import messagebox
from model import DashboardModel
from view import DashboardUI
import os

class DashboardController:
    def __init__(self, app):
        """Initialize DashboardController."""
        self.app = app
        self.setup_directories()
        self.setup_model()
        self.setup_view()
        self.bind_events()

    def setup_directories(self):
        """Set up directories."""
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.dirname(current_directory)
        self.dataset_folder = os.path.join(parent_directory, 'Dataset')
        self.dataset = os.path.join(self.dataset_folder, 'shopping_trends_updated.csv')

    def setup_model(self):
        """Set up model."""
        self.model = DashboardModel(self.dataset)

    def setup_view(self):
        """Set up view."""
        self.view = DashboardUI(self.app, self.model, self)
        
    def bind_events(self):
        """Bind events to UI components."""
        for var in self.view.category_vars:
            var.trace('w', lambda *args, var=var: self.view.update_graphs)

        for var in self.view.size_vars:
            var.trace('w', lambda *args, var=var: self.view.update_graphs)

        self.view.location_dropdown.bind('<<ComboboxSelected>>', self.view.update_graphs)
        self.view.season_dropdown.bind('<<ComboboxSelected>>', self.view.update_graphs)

    def reset_filters(self):
        """Reset all filters and update graphs."""
        for var in self.view.category_vars:
            var.set(False)
        for var in self.view.size_vars:
            var.set(False)
        self.view.location_var.set('All')
        self.view.season_var.set('All')
        self.view.update_graphs()

    def on_close(self):
        """Handle window close events."""
        quit_ok = messagebox.askokcancel(
                      title="Confirm Quit",
                      message="Do you really want to quit?")
        if quit_ok:
            self.app.destroy()

if __name__ == "__main__":
    app = tk.Tk()
    controller = DashboardController(app)
    app.mainloop()
