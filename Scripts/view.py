import tkinter as tk
from UI_Components.widgets import HeaderFrame, SidebarFrame
from UI_Components.graph import GraphManager
from UI_Components.page import HomePage, ProductsPage

class DashboardUI:
    def __init__(self, controller, app, model):
        """Initialize DashboardUI."""
        self.app = app
        self.model = model
        self.controller = controller
        self.app.geometry('1024x600')
        self.app.title('ShopperTrends Analyzer')
        self.current_page = "Home"
        self.init_components()
        self.graph_manager = GraphManager(self.app, self.model, self.controller)
        self.home_page = HomePage(app, controller, model, self)
        self.products_page = ProductsPage(app, controller, model, self)

    def init_components(self):
        """Initialize UI components."""
        self.create_head_frame()
        self.create_sidebar()

    def switch_to_home_page(self):
        """Switch to the Home page."""
        self.home_page.switch_to_page(self.current_page)
        self.current_page = "Home"

    def switch_to_products_page(self):
        """Switch to the Products page."""
        self.products_page.switch_to_page(self.current_page)
        self.current_page = "Products"

    def create_head_frame(self):
        """Create the header frame with logo and labels."""
        self.head_frame = HeaderFrame(self.app, self.model)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.pack_propagate(False)

    def create_sidebar(self):
        """Create the sidebar with filter options."""
        self.sidebar = SidebarFrame(self.app, self.controller, self.model, self)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
