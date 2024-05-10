import tkinter as tk
from tkinter import ttk

class HeaderFrame(tk.Frame):
    def __init__(self, app, model):
        super().__init__(app, bg='#282434', highlightbackground='black', highlightthickness=1)
        self.model = model
        self.configure(height=70)
        self.create_widgets()

    def create_widgets(self):
        emoji_photo = self.model.load_image("dashboard.png")
        emoji_label = tk.Label(self, image=emoji_photo, bg='#282434')
        emoji_label.image = emoji_photo
        emoji_label.pack(side=tk.LEFT, anchor=tk.W, padx=(20, 0))
        text_label = tk.Label(self, text='ShopperTrends Analyzer', bg='#282434', fg='white', font=('Bold', 15))
        text_label.pack(side=tk.LEFT, anchor=tk.W, padx=15)
        self.total_customers_label = tk.Label(self, text='Total Customers: ', bg='black', fg='white', font=('Bold', 13), highlightbackground="red", highlightthickness=2)
        self.total_customers_label.pack(side=tk.RIGHT, padx=10)
        self.average_rating_label = tk.Label(self, text='Average Rating: ', bg='black', fg='white', font=('Bold', 13), highlightbackground="red", highlightthickness=2)
        self.average_rating_label.pack(side=tk.RIGHT, padx=10)
        self.total_purchases_label = tk.Label(self, text='Total Purchases: ', bg='black', fg='white', font=('Bold', 13), highlightbackground="red", highlightthickness=2)
        self.total_purchases_label.pack(side=tk.RIGHT, padx=10)

class SidebarFrame(tk.Frame):
    def __init__(self, app, controller, model, view):
        super().__init__(app, bg='#282434')
        self.controller = controller
        self.model = model
        self.view = view
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self, bg='#282434')
        frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        btn_box_frame = tk.Frame(frame, bg='black')
        btn_box_frame.pack(fill=tk.BOTH, padx=10)
        filter_box_frame = tk.Frame(frame, bg='black')
        filter_box_frame.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        home_btn = tk.Button(btn_box_frame, text=' 🏠 Home', bg='black', fg='white', font=('Bold', 12), borderwidth=0, highlightthickness=0, anchor='w', command=self.view.switch_to_home_page)
        home_btn.pack(fill=tk.X, pady=10)
        products_btn = tk.Button(btn_box_frame, text=' 📦 Products', bg='black', fg='white', font=('Bold', 12), borderwidth=0, highlightthickness=0, anchor='w', command=self.view.switch_to_products_page)
        products_btn.pack(fill=tk.X, pady=10)
        locations_btn = tk.Button(btn_box_frame, text=' 🌍 Locations', bg='black', fg='white', font=('Bold', 12), borderwidth=0, highlightthickness=0, anchor='w', command=self.view.switch_to_products_page)
        locations_btn.pack(fill=tk.X, pady=10)
        attr_explore_btn = tk.Button(btn_box_frame, text=' 🔍 Attribute Explorer', bg='black', fg='white', font=('Bold', 12), borderwidth=0, highlightthickness=0, anchor='w', command=self.view.switch_to_products_page)
        attr_explore_btn.pack(fill=tk.X, pady=10)
        
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