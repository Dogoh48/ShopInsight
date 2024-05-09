class Page:
    def __init__(self, app, controller, model, view):
        self.app = app
        self.controller = controller
        self.model = model
        self.view = view
        self.graph_manager = self.view.graph_manager
        self.current_page = None

    def switch_to_page(self, page_name):
        if self.current_page != page_name:
            self.destroy_current_page()
            getattr(self, f"init_{self.current_page.lower()}_page")()
            self.controller.update_graphs()

    def destroy_current_page(self):
        if self.graph_manager.middle_frame:
            self.graph_manager.middle_frame.destroy()
        if self.graph_manager.bottom_frame:
            self.graph_manager.bottom_frame.destroy()

class HomePage(Page):
    def __init__(self, app, controller, model, view):
        super().__init__(app, controller, model, view)
        self.current_page = "Home"
        self.init_home_page()

    def init_home_page(self):
        self.graph_manager.create_graph_area()
        self.graph_manager.create_category_graph()
        self.graph_manager.create_gender_graph()
        self.graph_manager.create_subscription_graph()
        self.graph_manager.create_shipping_graph()

class ProductsPage(Page):
    def __init__(self, app, controller, model, view):
        super().__init__(app, controller, model, view)
        self.current_page = "Products"
        self.init_products_page()

    def init_products_page(self):
        pass
