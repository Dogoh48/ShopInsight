import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import itertools

class GraphManager:
    def __init__(self, parent_frame, model, controller):
        self.parent_frame = parent_frame
        self.model = model
        self.controller = controller

    def create_graph_area(self):
        """Create the area for displaying graphs."""
        self.middle_frame = tk.Frame(self.parent_frame, bg='#282434')
        self.middle_frame.pack(expand=True, fill=tk.BOTH)
        self.bottom_frame = tk.Frame(self.parent_frame, bg='#282434')
        self.bottom_frame.pack(expand=True, fill=tk.BOTH)        

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
        self.canvas_gender.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
        self.shipping_frame = tk.Frame(self.bottom_frame, bg='#282434')
        self.shipping_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_shipping, self.axs_shipping = plt.subplots(figsize=(6, 3), facecolor='#282434')
        self.axs_shipping.tick_params(colors='white')
        for spine in self.axs_shipping.spines.values():
            spine.set_edgecolor('white')
        self.canvas_shipping = FigureCanvasTkAgg(self.fig_shipping, master=self.shipping_frame)
        self.canvas_shipping.draw()
        self.canvas_shipping.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_category_graph(self, category_counts):
        self.ax_category.clear()
        category_counts.plot(kind='bar', ax=self.ax_category, color=['skyblue', 'pink', 'lightgreen', 'lightcoral'], edgecolor='black')
        self.ax_category.set_ylabel('Popularity (%)', color='white')
        self.ax_category.set_title('Popularity of Each Category', color='white')
        self.ax_category.tick_params(axis='x', colors='white')
        self.ax_category.tick_params(axis='y', colors='white')
        self.ax_category.set_xticklabels(category_counts.index, rotation=0)
        self.ax_category.grid(True)

    def update_gender_graph(self, gender_counts):
        self.ax_gender.clear()
        gender_counts.plot(kind='pie', ax=self.ax_gender, autopct='%1.1f%%', colors=['skyblue', 'pink'], textprops={'color': 'white'})
        self.ax_gender.set_title('Frequency of Gender', color='white')
        self.ax_gender.set_ylabel('')
        self.ax_gender.tick_params(axis='x', colors='white', pad=50)
        self.ax_gender.tick_params(axis='y', colors='white')
        self.ax_gender.set_facecolor('#282434')
    
    def update_subscription_graph(self, subscription_counts):
        self.axs_subscription.clear()
        subscription_counts.plot(kind='pie', ax=self.axs_subscription, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'], textprops={'color': 'white'})
        self.axs_subscription.set_title('Subscription Status', color='white')
        self.axs_subscription.set_ylabel('')
        self.axs_subscription.tick_params(axis='x', colors='white')
        self.axs_subscription.tick_params(axis='y', colors='white')
        self.axs_subscription.set_facecolor('#282434')
    
    def update_shipping_graph(self, shipping_counts):
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
