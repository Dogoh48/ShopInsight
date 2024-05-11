"""
view.py: Module for handling the user interface components.
"""
import tkinter as tk
from UI_Components.widgets import HeaderFrame, SidebarFrame
from UI_Components.graph import GraphManager
from UI_Components.page import HomePage, ProductsPage, Attribute_ExplorerPage

class DashboardUI:
    """Class representing the dashboard user interface."""
    def __init__(self, controller, app, model):
        """Initialize DashboardUI."""
        self.app = app
        self.model = model
        self.controller = controller
        self.app.geometry('1366x768')
        self.app.title('ShopperTrends Analyzer')
        self.current_page = "Home"
        self.init_components()
        self.graph_manager = GraphManager(self.app, self.model, self.controller, self)
        self.page = HomePage(app, controller, model, self)

    def init_components(self):
        """Initialize UI components."""
        self.create_head_frame()
        self.create_sidebar()

    def switch_to_home_page(self):
        """Switch to the Home page."""
        if self.current_page != "Home":
            if self.page.graph_manager.middle_frame:
                self.page.graph_manager.middle_frame.destroy()
                self.page.graph_manager.bottom_frame.destroy()
            self.page = HomePage(self.app, self.controller, self.model, self)
            self.page.switch_to_page(self.current_page)
            self.current_page = "Home"

    def create_head_frame(self):
        """Create the header frame with logo and labels."""
        self.head_frame = HeaderFrame(self.app, self.model)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.pack_propagate(False)

    def create_sidebar(self):
        """Create the sidebar with filter options."""
        self.sidebar = SidebarFrame(self.app, self.controller, self.model, self)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

    def switch_to_products_page(self):
        """Switch to the Products page."""
        if self.current_page != "Products":
                if self.page.graph_manager.middle_frame:
                    self.page.graph_manager.middle_frame.destroy()
                    self.page.graph_manager.bottom_frame.destroy()
                self.page = ProductsPage(self.app, self.controller, self.model, self)
                self.page.switch_to_page(self.current_page)
                self.current_page = "Products"

    def switch_to_attribute_exploerer_page(self):
        """Switch to the Attribute Explorer page."""
        if self.current_page != "Attribute_Explorer":
                if self.page.graph_manager.middle_frame:
                    self.page.graph_manager.middle_frame.destroy()
                    self.page.graph_manager.bottom_frame.destroy()
                self.page = Attribute_ExplorerPage(self.app, self.controller, self.model, self)
                self.page.switch_to_page(self.current_page)
                self.current_page = "Attribute_Exploerer"
