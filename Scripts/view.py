import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from page import HomePage, ProductsPage

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
        self.head_frame = tk.Frame(self.app, bg='#282434', highlightbackground='black', highlightthickness=1)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=70)
        emoji_photo = self.model.load_image("dashboard.png")
        emoji_label = tk.Label(self.head_frame, image=emoji_photo, bg='#282434')
        emoji_label.image = emoji_photo
        emoji_label.pack(side=tk.LEFT, anchor=tk.W, padx=(20, 0))
        text_label = tk.Label(self.head_frame, text='ShopperTrends Analyzer', bg='#282434', fg='white', font=('Bold', 15))
        text_label.pack(side=tk.LEFT, anchor=tk.W, padx=15)
        self.total_customers_label = tk.Label(self.head_frame, text='Total Customers: ', bg='black', fg='white', font=('Bold', 13), highlightbackground="red", highlightthickness=2)
        self.total_customers_label.pack(side=tk.RIGHT, padx=10)
        self.average_rating_label = tk.Label(self.head_frame, text='Average Rating: ', bg='black', fg='white', font=('Bold', 13), highlightbackground="red", highlightthickness=2)
        self.average_rating_label.pack(side=tk.RIGHT, padx=10)
        self.total_purchases_label = tk.Label(self.head_frame, text='Total Purchases: ', bg='black', fg='white', font=('Bold', 13), highlightbackground="red", highlightthickness=2)
        self.total_purchases_label.pack(side=tk.RIGHT, padx=10)

    def create_sidebar(self):
        """Create the sidebar with filter options."""
        self.sidebar = tk.Frame(self.app, bg='#282434')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        frame = tk.Frame(self.sidebar, bg='#282434')
        frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        btn_box_frame = tk.Frame(frame, bg='black')
        btn_box_frame.pack(fill=tk.BOTH, padx=10)
        filter_box_frame = tk.Frame(frame, bg='black')
        filter_box_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        home_btn = tk.Button(btn_box_frame, text=' 🏠 Home', bg='black', fg='white', font=('Bold', 12), borderwidth=0, highlightthickness=0, anchor='w', command=self.switch_to_home_page)
        home_btn.pack(fill=tk.X, pady=10)
        products_btn = tk.Button(btn_box_frame, text=' 📦 Products', bg='black', fg='white', font=('Bold', 12), borderwidth=0, highlightthickness=0, anchor='w', command=self.switch_to_products_page)
        products_btn.pack(fill=tk.X, pady=10)
        
        # Return to Default button
        default_btn = tk.Button(btn_box_frame, text=' 🔄 Return to Default', bg='black', fg='white', font=('Bold', 12), borderwidth=0, highlightthickness=0, anchor='w', command=self.controller.reset_filters)
        default_btn.pack(fill=tk.X, pady=10)

        # Category filter
        category_label = tk.Label(filter_box_frame, text='Select The Category:', bg='black', fg='white', font=('Bold', 10))
        category_label.pack(anchor='w', padx=10)
        category_options = list(self.model.df['Category'].unique())
        self.category_options = category_options
        self.category_vars = [tk.BooleanVar(value=False) for _ in category_options]
        for var, option in zip(self.category_vars, category_options):
            chk = tk.Checkbutton(filter_box_frame, text=option, variable=var, onvalue=True, offvalue=False, bg='black', fg='white', font=('Bold', 10), command=self.controller.update_graphs)
            chk.pack(anchor='w', padx=10)
        
        # Size filter
        size_label = tk.Label(filter_box_frame, text='Select The Size:', bg='black', fg='white', font=('Bold', 10))
        size_label.pack(anchor='w', padx=10)
        size_options = list(self.model.df['Size'].unique())
        self.size_options = size_options
        self.size_vars = [tk.BooleanVar(value=False) for _ in size_options]
        for var, option in zip(self.size_vars, size_options):
            chk = tk.Checkbutton(filter_box_frame, text=option, variable=var, onvalue=True, offvalue=False, bg='black', fg='white', font=('Bold', 10), command=self.controller.update_graphs)
            chk.pack(anchor='w', padx=10)

        # Location filter
        locations_label = tk.Label(filter_box_frame, text='Location:', bg='black', fg='white', font=('Bold', 10))
        locations_label.pack(anchor='w', padx=10)
        location_options = ['All'] + list(self.model.df['Location'].unique())
        self.location_var = tk.StringVar(value='All')
        self.location_dropdown = ttk.Combobox(filter_box_frame, textvariable=self.location_var, values=location_options, state='readonly')
        self.location_dropdown.pack(anchor='w', padx=10)

        # Season filter
        season_label = tk.Label(filter_box_frame, text='Season:', bg='black', fg='white', font=('Bold', 10))
        season_label.pack(anchor='w', padx=10)
        season_options = ['All'] + list(self.model.df['Season'].unique())
        self.season_var = tk.StringVar(value='All')
        self.season_dropdown = ttk.Combobox(filter_box_frame, textvariable=self.season_var, values=season_options, state='readonly')
        self.season_dropdown.pack(anchor='w', padx=10)

    def create_graph_area(self):
        """Create the area for displaying graphs."""
        self.middle_frame = tk.Frame(self.app, bg='#282434')
        self.middle_frame.pack(expand=True, fill=tk.BOTH)
        self.create_category_graph()
        self.create_gender_graph()
        self.create_subscription_graph()
        self.create_shipping_graph()

    def create_category_graph(self):
        self.category_frame = tk.Frame(self.middle_frame, bg='#282434')
        self.category_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_category, self.ax_category = plt.subplots(figsize=(6, 3), facecolor='#282434')
        self.ax_category.tick_params(colors='white')
        for spine in self.ax_category.spines.values():
            spine.set_edgecolor('white')
        self.canvas_category = FigureCanvasTkAgg(self.fig_category, master=self.category_frame)
        self.canvas_category.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_category.draw()

    def create_gender_graph(self):
        self.gender_frame = tk.Frame(self.middle_frame, bg='#282434')
        self.gender_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_gender, self.ax_gender = plt.subplots(figsize=(6, 3), facecolor='#282434')
        self.ax_gender.tick_params(colors='white')
        for spine in self.ax_gender.spines.values():
            spine.set_edgecolor('white')
        self.canvas_gender = FigureCanvasTkAgg(self.fig_gender, master=self.gender_frame)
        self.canvas_gender.draw()
        self.canvas_gender.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_subscription_graph(self):
        self.subscription_frame = tk.Frame(self.middle_frame, bg='#282434')
        self.subscription_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_subscription, self.axs_subscription = plt.subplots(figsize=(6, 3), facecolor='#282434')
        self.axs_subscription.tick_params(colors='white')
        for spine in self.axs_subscription.spines.values():
            spine.set_edgecolor('white')
        self.canvas_subscription = FigureCanvasTkAgg(self.fig_subscription, master=self.subscription_frame)
        self.canvas_subscription.draw()
        self.canvas_subscription.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_shipping_graph(self):
        self.shipping_frame = tk.Frame(self.app, bg='#282434')
        self.shipping_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_shipping, self.axs_shipping = plt.subplots(figsize=(6, 3), facecolor='#282434')
        self.axs_shipping.tick_params(colors='white')
        for spine in self.axs_shipping.spines.values():
            spine.set_edgecolor('white')
        self.canvas_shipping = FigureCanvasTkAgg(self.fig_shipping, master=self.shipping_frame)
        self.canvas_shipping.draw()
        self.canvas_shipping.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_labels(self, total_customers, average_rating, total_purchases):
        """Update labels for total customers, average rating, and total purchases."""
        self.total_customers_label.config(text=f'Total Customers: {total_customers}', fg='white')
        self.average_rating_label.config(text=f'Average Rating: {average_rating:.2f}', fg='white')
        self.total_purchases_label.config(text=f'Total Purchases: ${total_purchases:.2f}', fg='white')
