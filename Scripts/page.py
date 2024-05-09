class Page:
    def __init__(self, app, controller, model, view):
        self.app = app
        self.controller = controller
        self.model = model
        self.view = view
        self.current_page = None

    def switch_to_page(self, page_name):
        if self.current_page != page_name:
            self.destroy_current_page()
            getattr(self, f"init_{self.current_page.lower()}_page")()
            self.controller.update_graphs()

    def destroy_current_page(self):
        if self.view.middle_frame:
            self.view.middle_frame.destroy()
        if self.view.shipping_frame:
            self.view.shipping_frame.destroy()

class HomePage(Page):
    def __init__(self, app, controller, model, view):
        super().__init__(app, controller, model, view)
        self.current_page = "Home"
        self.init_home_page()

    def init_home_page(self):
        self.view.create_graph_area()

class ProductsPage(Page):
    def __init__(self, app, controller, model, view):
        super().__init__(app, controller, model, view)
        self.current_page = "Products"
        self.init_products_page()

    def init_products_page(self):
        pass
