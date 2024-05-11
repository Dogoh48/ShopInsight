"""
page.py: Module for defining the different pages of the application.
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Page:
    """Base class for different pages in the application."""
    def __init__(self, app, controller, model, view):
        """Initialize the Page object."""
        self.app = app
        self.controller = controller
        self.model = model
        self.view = view
        self.graph_manager = self.view.graph_manager
        self.current_page = None

    def switch_to_page(self, page_name):
        """Switch to the specified page."""
        if self.current_page != page_name:
            self.destroy_current_page()
            getattr(self, f"init_{self.current_page.lower()}_page")()
            self.controller.update_graphs()

    def destroy_current_page(self):
        """Destroy the current page."""
        if self.graph_manager.middle_frame:
            self.graph_manager.middle_frame.destroy()
        if self.graph_manager.bottom_frame:
            self.graph_manager.bottom_frame.destroy()

class HomePage(Page):
    """Class representing the home page of the application."""
    def __init__(self, app, controller, model, view):
        """Initialize the HomePage object."""
        super().__init__(app, controller, model, view)
        self.current_page = "Home"
        self.init_home_page()

    def init_home_page(self):
        """Initialize the home page."""
        self.graph_manager.create_graph_area()
        self.graph_manager.create_category_graph()
        self.graph_manager.create_gender_graph()
        self.graph_manager.create_shipping_graph()

class ProductsPage(Page):
    """Class representing the products page of the application."""
    def __init__(self, app, controller, model, view):
        """Initialize the ProductsPage object."""
        super().__init__(app, controller, model, view)
        self.current_page = "Products"
        self.init_products_page()

    def init_products_page(self):
        """Initialize the products page."""
        self.graph_manager.create_graph_area()
        self.graph_manager.create_top_items_graph()

class Attribute_ExplorerPage(Page):
    """Class representing the attribute explorer page of the application."""
    def __init__(self, app, controller, model, view):
        """Initialize the Attribute_ExplorerPage object."""
        super().__init__(app, controller, model, view)
        self.current_page = "Attribute_Explorer"
        self.init_attribute_explorer_page()

    def init_attribute_explorer_page(self):
        """Initialize the attribute explorer page."""
        self.graph_manager.create_graph_area()
        self.init_attribute_dropdowns()
        self.init_graph_type_dropdown()
        self.init_generate_button()

    def init_attribute_dropdowns(self):
        """Initialize the attribute dropdowns."""
        self.attribute_frame = tk.Frame(self.graph_manager.bottom_frame, bg='#282434')
        self.attribute_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.attribute_label = tk.Label(self.attribute_frame, text="Select Attribute:", bg='black', fg='white', font=('Bold', 10))
        self.attribute_label.pack(anchor='w', padx=10)

        attributes = list(self.model.df.columns)
        attributes.insert(0, "None")
        self.attribute_var1 = tk.StringVar(value=attributes[0])
        self.attribute_var2 = tk.StringVar(value=attributes[0])

        self.attribute_dropdown1 = ttk.Combobox(self.attribute_frame, textvariable=self.attribute_var1, values=attributes, state='readonly')
        self.attribute_dropdown1.pack(anchor='w', padx=10)

        self.attribute_dropdown2 = ttk.Combobox(self.attribute_frame, textvariable=self.attribute_var2, values=attributes, state='readonly')
        self.attribute_dropdown2.pack(anchor='w', padx=10)

    def init_graph_type_dropdown(self):
        """Initialize the graph type dropdown."""
        self.graph_type_frame = tk.Frame(self.graph_manager.bottom_frame, bg='#282434')
        self.graph_type_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.graph_type_label = tk.Label(self.graph_type_frame, text="Select Graph Type:", bg='black', fg='white', font=('Bold', 10))
        self.graph_type_label.pack(anchor='w', padx=10)

        graph_types = ["Bar Chart", "Pie Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot"]
        self.graph_type_var = tk.StringVar(value=graph_types[0])

        self.graph_type_dropdown = ttk.Combobox(self.graph_type_frame, textvariable=self.graph_type_var, values=graph_types, state='readonly')
        self.graph_type_dropdown.pack(anchor='w', padx=10)

    def init_generate_button(self):
        """Initialize the generate button."""
        self.generate_button_frame = tk.Frame(self.graph_manager.bottom_frame, bg='#282434')
        self.generate_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.generate_button = tk.Button(self.generate_button_frame, text="Generate Graph", bg='black', fg='white', font=('Bold', 10), command=self.generate_graph)
        self.generate_button.pack(pady=10, padx=20)

    def generate_graph(self):
        """Generate the selected graph."""
        attribute1 = self.attribute_var1.get()
        attribute2 = self.attribute_var2.get()
        graph_type = self.graph_type_var.get()
        if attribute1 == "None" or (graph_type in ["Scatter Plot", "Box Plot"] and attribute2 == "None"):
            messagebox.showerror("Error", "Please select valid attribute(s) for the selected graph type.")
            return
        data = self.model.df[attribute1]
        if attribute2 != "None":
            data2 = self.model.df[attribute2]
        else:
            data2 = None
        if graph_type == "Bar Chart":
            self.graph_manager.show_bar_chart(data, x_title=attribute1, y_title="Count")
        elif graph_type == "Pie Chart":
            self.graph_manager.show_pie_chart(data, title=attribute1)
        elif graph_type == "Line Chart":
            if data2 is not None:
                data = self.model.df[[attribute1, attribute2]]
                x_title = attribute1 if data.columns[0] == attribute1 else attribute2
                y_title = attribute2 if data.columns[1] == attribute2 else attribute1
            else:
                x_title, y_title = attribute1, None
            self.graph_manager.show_line_chart(data, x_title=x_title, y_title=y_title)
        elif graph_type == "Scatter Plot":
            if data2 is not None:
                data = self.model.df[[attribute1, attribute2]]
            self.graph_manager.show_scatter_plot(data, x_title=attribute1, y_title=attribute2)
        elif graph_type == "Histogram":
            self.graph_manager.show_histogram(data, x_title=attribute1, y_title="Frequency")
        elif graph_type == "Box Plot":
            if data2 is not None:
                data = self.model.df[[attribute1, attribute2]]
            self.graph_manager.show_box_plot(attribute1, data, x_title=attribute1, y_title=attribute2)
