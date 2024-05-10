from tkinter import messagebox
from model import DashboardModel
from view import DashboardUI

class DashboardController:
    def __init__(self, app):
        """Initialize DashboardController."""
        self.app = app
        self.model = DashboardModel()
        self.view = DashboardUI(self, self.app, self.model)
        self.head_frame = self.view.head_frame
        self.sidebar = self.view.sidebar
        self.graph_manager = self.view.graph_manager
        self.bind_events()
        self.update_graphs()
        
    def bind_events(self):
        """Bind events to UI components."""
        for var in self.sidebar.category_vars:
            var.trace('w', lambda *args, var=var: self.update_graphs)

        for var in self.sidebar.size_vars:
            var.trace('w', lambda *args, var=var: self.update_graphs)

        self.sidebar.location_dropdown.bind('<<ComboboxSelected>>', self.update_graphs)
        self.sidebar.season_dropdown.bind('<<ComboboxSelected>>', self.update_graphs)

    def update_graphs(self, event=None):
        """Update graphs based on selected filters."""
        category_filters = [option for var, option in zip(self.sidebar.category_vars, self.sidebar.category_options) if var.get()]
        size_filters = [option for var, option in zip(self.sidebar.size_vars, self.sidebar.size_options) if var.get()]
        location = self.sidebar.location_var.get()
        season = self.sidebar.season_var.get()
        filtered_data = self.model.filter_data(category_filters, size_filters, location, season)
        category_counts = filtered_data['Category'].value_counts(normalize=True) * 100
        gender_counts = filtered_data['Gender'].value_counts()
        subscription_counts = filtered_data['Subscription Status'].value_counts()
        shipping_counts = filtered_data['Shipping Type'].value_counts()
        self.graph_manager.update_category_graph(category_counts)
        self.graph_manager.update_gender_graph(gender_counts)
        self.graph_manager.update_subscription_graph(subscription_counts)
        self.graph_manager.update_shipping_graph(shipping_counts)
        total_customers = len(filtered_data)
        average_rating = filtered_data['Review Rating'].mean()
        total_purchases = filtered_data['Purchase Amount (USD)'].sum()
        self.update_labels(total_customers, average_rating, total_purchases)

    def update_labels(self, total_customers, average_rating, total_purchases):
        """Update labels for total customers, average rating, and total purchases."""
        self.head_frame.total_customers_label.config(text=f'Total Customers: {total_customers}', fg='white')
        self.head_frame.average_rating_label.config(text=f'Average Rating: {average_rating:.2f}', fg='white')
        self.head_frame.total_purchases_label.config(text=f'Total Purchases: ${total_purchases:.2f}', fg='white')

    def reset_filters(self):
        """Reset all filters and update graphs."""
        for var in self.sidebar.category_vars:
            var.set(False)
        for var in self.sidebar.size_vars:
            var.set(False)
        self.sidebar.location_var.set('All')
        self.sidebar.season_var.set('All')
        self.update_graphs()

    def on_close(self):
        """Handle window close events."""
        quit_ok = messagebox.askokcancel(
                      title="Confirm Quit",
                      message="Do you really want to quit?")
        if quit_ok:
            self.app.destroy()
