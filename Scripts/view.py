import tkinter as tk
from tkinter import ttk
import itertools
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class DashboardUI:
    def __init__(self, master, model, controller):
        """Initialize DashboardUI."""
        self.master = master
        self.model = model
        self.controller = controller
        self.master.geometry('1024x600')
        self.master.title('ShopperTrends Analyzer')
        self.current_page = "Home"
        self.init_components()

    def init_home_page(self):
        """Initialize the Home page UI components."""
        self.current_page = "Home"
        self.init_home_components()

    def init_products_page(self):
        """Initialize the Products page UI components."""
        self.current_page = "Products"
        self.init_product_components()

    def switch_to_home_page(self):
        """Switch to the Home page."""
        if self.current_page != "Home":
            self.destroy_current_page()
            self.init_home_page()

    def switch_to_products_page(self):
        """Switch to the Products page."""
        if self.current_page != "Products":
            self.destroy_current_page()
            self.init_products_page()

    def destroy_current_page(self):
        """Destroy the current page UI components."""
        if self.middle_frame:
            self.middle_frame.destroy()
        if self.shipping_frame:
            self.shipping_frame.destroy()

    def init_components(self):
        """Initialize UI components."""
        self.create_head_frame()
        self.create_sidebar()
        self.create_graph_area()
        self.update_graphs()

    def init_home_components(self):
        """Initialize UI components."""
        self.create_graph_area()
        self.update_graphs()

    def init_product_components(self):
        """Initialize UI components."""
        pass

    def load_image(self, filename):
        """Load image from a specified folder."""
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.dirname(current_directory)
        image_folder = os.path.join(parent_directory, 'Images')
        image_path = os.path.join(image_folder, filename)
        image = Image.open(image_path)
        image = image.resize((50, 50))
        return ImageTk.PhotoImage(image)

    def create_head_frame(self):
        """Create the header frame with logo and labels."""
        self.head_frame = tk.Frame(self.master, bg='#282434', highlightbackground='black', highlightthickness=1)
        self.head_frame.pack(side=tk.TOP, fill=tk.X)
        self.head_frame.pack_propagate(False)
        self.head_frame.configure(height=70)
        emoji_photo = self.load_image("dashboard.png")
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
        self.sidebar = tk.Frame(self.master, bg='#282434')
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
            chk = tk.Checkbutton(filter_box_frame, text=option, variable=var, onvalue=True, offvalue=False, bg='black', fg='white', font=('Bold', 10), command=self.update_graphs)
            chk.pack(anchor='w', padx=10)
        
        # Size filter
        size_label = tk.Label(filter_box_frame, text='Select The Size:', bg='black', fg='white', font=('Bold', 10))
        size_label.pack(anchor='w', padx=10)
        size_options = list(self.model.df['Size'].unique())
        self.size_options = size_options
        self.size_vars = [tk.BooleanVar(value=False) for _ in size_options]
        for var, option in zip(self.size_vars, size_options):
            chk = tk.Checkbutton(filter_box_frame, text=option, variable=var, onvalue=True, offvalue=False, bg='black', fg='white', font=('Bold', 10), command=self.update_graphs)
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
        self.middle_frame = tk.Frame(self.master, bg='#282434')
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
        self.shipping_frame = tk.Frame(self.master, bg='#282434')
        self.shipping_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_shipping, self.axs_shipping = plt.subplots(figsize=(6, 3), facecolor='#282434')
        self.axs_shipping.tick_params(colors='white')
        for spine in self.axs_shipping.spines.values():
            spine.set_edgecolor('white')
        self.canvas_shipping = FigureCanvasTkAgg(self.fig_shipping, master=self.shipping_frame)
        self.canvas_shipping.draw()
        self.canvas_shipping.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_graphs(self, event=None):
        """Update graphs based on selected filters."""
        category_filters = [option for var, option in zip(self.category_vars, self.category_options) if var.get()]
        size_filters = [option for var, option in zip(self.size_vars, self.size_options) if var.get()]
        location = self.location_var.get()
        season = self.season_var.get()
        filtered_data = self.controller.model.filter_data(category_filters, size_filters, location, season)
        category_counts = filtered_data['Category'].value_counts(normalize=True) * 100
        self.ax_category.clear()
        category_counts.plot(kind='bar', ax=self.ax_category, color=['skyblue', 'pink', 'lightgreen', 'lightcoral'], edgecolor='black')
        self.ax_category.set_ylabel('Popularity (%)', color='white')
        self.ax_category.set_title('Popularity of Each Category', color='white')
        self.ax_category.tick_params(axis='x', colors='white')
        self.ax_category.tick_params(axis='y', colors='white')
        self.ax_category.set_xticklabels(category_counts.index, rotation=0)
        self.ax_category.grid(True)

        # Update gender graph
        gender_counts = filtered_data['Gender'].value_counts()
        self.ax_gender.clear()
        gender_counts.plot(kind='pie', ax=self.ax_gender, autopct='%1.1f%%', colors=['skyblue', 'pink'], textprops={'color': 'white'})
        self.ax_gender.set_title('Frequency of Gender', color='white')
        self.ax_gender.set_ylabel('')
        self.ax_gender.tick_params(axis='x', colors='white', pad=50)
        self.ax_gender.tick_params(axis='y', colors='white')
        self.ax_gender.set_facecolor('#282434')

        # Update subscription status graph
        subscription_counts = filtered_data['Subscription Status'].value_counts()
        self.axs_subscription.clear()
        subscription_counts.plot(kind='pie', ax=self.axs_subscription, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'], textprops={'color': 'white'})
        self.axs_subscription.set_title('Subscription Status', color='white')
        self.axs_subscription.set_ylabel('')
        self.axs_subscription.tick_params(axis='x', colors='white')
        self.axs_subscription.tick_params(axis='y', colors='white')
        self.axs_subscription.set_facecolor('#282434')

        # Update shipping type graph
        shipping_counts = filtered_data['Shipping Type'].value_counts()
        self.axs_shipping.clear()
        colors = itertools.cycle(['lightblue', 'lightgreen', 'lightcoral'])
        for idx, (category, count) in enumerate(shipping_counts.items()):
            color = next(colors)
            self.axs_shipping.bar(idx, count, color=color, edgecolor='black')
        self.axs_shipping.set_title('Shipping Type', color='white')
        self.axs_shipping.set_ylabel('Frequency', color='white')
        self.axs_shipping.tick_params(axis='x', colors='white')
        self.axs_shipping.tick_params(axis='y', colors='white')
        min_value = (shipping_counts.min() // 10) * 10
        max_value = (shipping_counts.max() // 10 + 1) * 10
        self.axs_shipping.set_yticks(range(min_value, max_value + 1, 10))
        self.axs_shipping.set_yticklabels([str(y) for y in range(min_value, max_value + 1, 10)], color='white')
        self.axs_shipping.set_xticks(range(len(shipping_counts)))
        self.axs_shipping.set_xticklabels(shipping_counts.index, rotation=0)
        self.axs_shipping.grid(True)
        self.axs_shipping.set_ylim(min_value - 5, max_value + 5)

        self.canvas_category.draw()
        self.canvas_gender.draw()
        self.canvas_subscription.draw()
        self.canvas_shipping.draw()

        # Update labels information
        total_customers = len(filtered_data)
        average_rating = filtered_data['Review Rating'].mean()
        total_purchases = filtered_data['Purchase Amount (USD)'].sum()
        self.update_labels(total_customers, average_rating, total_purchases)

    def update_labels(self, total_customers, average_rating, total_purchases):
        """Update labels for total customers, average rating, and total purchases."""
        self.total_customers_label.config(text=f'Total Customers: {total_customers}', fg='white')
        self.average_rating_label.config(text=f'Average Rating: {average_rating:.2f}', fg='white')
        self.total_purchases_label.config(text=f'Total Purchases: ${total_purchases:.2f}', fg='white')
