import tkinter as tk
from tkinter import messagebox
from model import DashboardModel
from view import DashboardUI
import itertools

class DashboardController:
    def __init__(self, app):
        """Initialize DashboardController."""
        self.app = app
        self.model = DashboardModel()
        self.view = DashboardUI(self, self.app, self.model)
        self.graph_manager = self.view.graph_manager
        self.bind_events()
        self.update_graphs()
        
    def bind_events(self):
        """Bind events to UI components."""
        for var in self.view.category_vars:
            var.trace('w', lambda *args, var=var: self.update_graphs)

        for var in self.view.size_vars:
            var.trace('w', lambda *args, var=var: self.update_graphs)

        self.view.location_dropdown.bind('<<ComboboxSelected>>', self.update_graphs)
        self.view.season_dropdown.bind('<<ComboboxSelected>>', self.update_graphs)

    def update_graphs(self, event=None):
        """Update graphs based on selected filters."""
        category_filters = [option for var, option in zip(self.view.category_vars, self.view.category_options) if var.get()]
        size_filters = [option for var, option in zip(self.view.size_vars, self.view.size_options) if var.get()]
        location = self.view.location_var.get()
        season = self.view.season_var.get()
        filtered_data = self.model.filter_data(category_filters, size_filters, location, season)
        category_counts = filtered_data['Category'].value_counts(normalize=True) * 100
        self.graph_manager.ax_category.clear()
        category_counts.plot(kind='bar', ax=self.graph_manager.ax_category, color=['skyblue', 'pink', 'lightgreen', 'lightcoral'], edgecolor='black')
        self.graph_manager.ax_category.set_ylabel('Popularity (%)', color='white')
        self.graph_manager.ax_category.set_title('Popularity of Each Category', color='white')
        self.graph_manager.ax_category.tick_params(axis='x', colors='white')
        self.graph_manager.ax_category.tick_params(axis='y', colors='white')
        self.graph_manager.ax_category.set_xticklabels(category_counts.index, rotation=0)
        self.graph_manager.ax_category.grid(True)

        # Update gender graph
        gender_counts = filtered_data['Gender'].value_counts()
        self.graph_manager.ax_gender.clear()
        gender_counts.plot(kind='pie', ax=self.graph_manager.ax_gender, autopct='%1.1f%%', colors=['skyblue', 'pink'], textprops={'color': 'white'})
        self.graph_manager.ax_gender.set_title('Frequency of Gender', color='white')
        self.graph_manager.ax_gender.set_ylabel('')
        self.graph_manager.ax_gender.tick_params(axis='x', colors='white', pad=50)
        self.graph_manager.ax_gender.tick_params(axis='y', colors='white')
        self.graph_manager.ax_gender.set_facecolor('#282434')

        # Update subscription status graph
        subscription_counts = filtered_data['Subscription Status'].value_counts()
        self.graph_manager.axs_subscription.clear()
        subscription_counts.plot(kind='pie', ax=self.graph_manager.axs_subscription, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'], textprops={'color': 'white'})
        self.graph_manager.axs_subscription.set_title('Subscription Status', color='white')
        self.graph_manager.axs_subscription.set_ylabel('')
        self.graph_manager.axs_subscription.tick_params(axis='x', colors='white')
        self.graph_manager.axs_subscription.tick_params(axis='y', colors='white')
        self.graph_manager.axs_subscription.set_facecolor('#282434')

        # Update shipping type graph
        shipping_counts = filtered_data['Shipping Type'].value_counts()
        self.graph_manager.axs_shipping.clear()
        colors = itertools.cycle(['lightblue', 'lightgreen', 'lightcoral'])
        for idx, (category, count) in enumerate(shipping_counts.items()):
            color = next(colors)
            self.graph_manager.axs_shipping.bar(idx, count, color=color, edgecolor='black')
        self.graph_manager.axs_shipping.set_title('Shipping Type', color='white')
        self.graph_manager.axs_shipping.set_ylabel('Frequency', color='white')
        self.graph_manager.axs_shipping.tick_params(axis='x', colors='white')
        self.graph_manager.axs_shipping.tick_params(axis='y', colors='white')
        min_value = (shipping_counts.min() // 10) * 10
        max_value = (shipping_counts.max() // 10 + 1) * 10
        self.graph_manager.axs_shipping.set_yticks(range(min_value, max_value + 1, 10))
        self.graph_manager.axs_shipping.set_yticklabels([str(y) for y in range(min_value, max_value + 1, 10)], color='white')
        self.graph_manager.axs_shipping.set_xticks(range(len(shipping_counts)))
        self.graph_manager.axs_shipping.set_xticklabels(shipping_counts.index, rotation=0)
        self.graph_manager.axs_shipping.grid(True)
        self.graph_manager.axs_shipping.set_ylim(min_value - 5, max_value + 5)
        self.graph_manager.canvas_category.draw()
        self.graph_manager.canvas_gender.draw()
        self.graph_manager.canvas_subscription.draw()
        self.graph_manager.canvas_shipping.draw()

        # Update labels information
        total_customers = len(filtered_data)
        average_rating = filtered_data['Review Rating'].mean()
        total_purchases = filtered_data['Purchase Amount (USD)'].sum()
        self.view.update_labels(total_customers, average_rating, total_purchases)

    def reset_filters(self):
        """Reset all filters and update graphs."""
        for var in self.view.category_vars:
            var.set(False)
        for var in self.view.size_vars:
            var.set(False)
        self.view.location_var.set('All')
        self.view.season_var.set('All')
        self.update_graphs()

    def on_close(self):
        """Handle window close events."""
        quit_ok = messagebox.askokcancel(
                      title="Confirm Quit",
                      message="Do you really want to quit?")
        if quit_ok:
            self.app.destroy()
