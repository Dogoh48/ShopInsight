"""
graph.py: This module provides a GraphManager class for managing and displaying graphs in a tkinter-based application.
The GraphManager class allows the creation of various types of graphs, such as bar charts, pie charts, line charts,
scatter plots, histograms, and box plots. It also facilitates updating and displaying graphs based on provided data
 and filters.
"""
import itertools

import tkinter as tk
from tkinter import messagebox

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns

import pandas as pd

class GraphManager:
    """Class for managing and displaying graphs."""

    def __init__(self, app, model, controller, view):
        """
        Initialize the GraphManager.

        Args:
            app: The tkinter application.
            model: The data model.
            controller: The controller object.
            view: The view object.
        """
        self.app = app
        self.model = model
        self.view = view
        self.sidebar = view.sidebar
        self.controller = controller

    def create_graph_area(self):
        """Create the area for displaying graphs."""
        self.middle_frame = tk.Frame(self.app, bg='#282434')
        self.middle_frame.pack(expand=True, fill=tk.BOTH)
        self.bottom_frame = tk.Frame(self.app, bg='#282434')
        self.bottom_frame.pack(expand=True, fill=tk.BOTH)
        self.create_bottom_label()
        if self.view.current_page == "Product":
            self.create_bottom_label()

    def create_bottom_label(self):
        """Create the label in the bottom frame."""
        self.bottom_label = tk.Label(self.bottom_frame, text="", bg='#282434', fg='white', font=('Courier', 10))
        self.bottom_label.pack(fill=tk.BOTH, expand=True)

    def create_category_graph(self):
        """Create the category graph."""
        self.category_frame = tk.Frame(self.middle_frame, bg='#282434', highlightbackground="white", highlightcolor="white", highlightthickness=1, bd=0)
        self.category_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_category = Figure(figsize=(6, 3), facecolor='#282434')
        self.ax_category = self.fig_category.add_subplot(111)
        self.ax_category.tick_params(colors='white')
        for spine in self.ax_category.spines.values():
            spine.set_edgecolor('white')
        self.canvas_category = FigureCanvasTkAgg(self.fig_category, master=self.category_frame)
        self.canvas_category.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_category.draw()

    def create_gender_graph(self):
        """Create the gender graph."""
        self.gender_frame = tk.Frame(self.middle_frame, bg='#282434', highlightbackground="white", highlightcolor="white", highlightthickness=1, bd=0)
        self.gender_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_gender = Figure(figsize=(6, 3), facecolor='#282434')
        self.ax_gender = self.fig_gender.add_subplot(111)
        self.ax_gender.tick_params(colors='white')
        for spine in self.ax_gender.spines.values():
            spine.set_edgecolor('white')
        self.canvas_gender = FigureCanvasTkAgg(self.fig_gender, master=self.gender_frame)
        self.canvas_gender.draw()
        self.canvas_gender.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_shipping_graph(self):
        """Create the shipping graph."""
        self.shipping_frame = tk.Frame(self.bottom_frame, bg='#282434', highlightbackground="white", highlightcolor="white", highlightthickness=1, bd=0)
        self.shipping_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_shipping = Figure(figsize=(6, 3), facecolor='#282434')
        self.axs_shipping = self.fig_shipping.add_subplot(111)
        self.axs_shipping.tick_params(colors='white')
        for spine in self.axs_shipping.spines.values():
            spine.set_edgecolor('white')
        self.canvas_shipping = FigureCanvasTkAgg(self.fig_shipping, master=self.shipping_frame)
        self.canvas_shipping.draw()
        self.canvas_shipping.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_top_items_graph(self):
        """Create the top items graph."""
        self.top_items_frame = tk.Frame(self.middle_frame, bg='#282434', highlightbackground="white", highlightcolor="white", highlightthickness=1, bd=0)
        self.top_items_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fig_top_items = Figure(figsize=(6, 3), facecolor='#282434')
        self.ax_top_items = self.fig_top_items.add_subplot(111)
        self.ax_top_items.tick_params(colors='white')
        for spine in self.ax_top_items.spines.values():
            spine.set_edgecolor('white')
        self.canvas_top_items = FigureCanvasTkAgg(self.fig_top_items, master=self.top_items_frame)
        self.canvas_top_items.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_top_items.draw()
        self.canvas_top_items.mpl_connect('button_press_event', self.on_bar_click)

    def on_bar_click(self, event):
        """Handle the click event on a bar in the top items graph."""
        if event.inaxes == self.ax_top_items:
            for obj in self.bars:
                if isinstance(obj, matplotlib.patches.Rectangle):
                    obj.set_facecolor('lightblue')
            bar_index = int(event.xdata)
            selected_bar = self.bars[bar_index]
            selected_bar.set_facecolor('orange')
            self.canvas_top_items.draw()
            item_name = self.top_items[bar_index]
            self.display_item_details(item_name)

    def display_item_details(self, item_name):
        """Display detailed information about the selected item."""
        category_filters = [option for var, option in zip(self.sidebar.category_vars, self.sidebar.category_options) if var.get()]
        size_filters = [option for var, option in zip(self.sidebar.size_vars, self.sidebar.size_options) if var.get()]
        location = self.sidebar.location_var.get()
        season = self.sidebar.season_var.get()
        filtered_data = self.model.filter_data(category_filters, size_filters, location, season)
        item_data = filtered_data[filtered_data['Item Purchased'] == item_name]
        average_age = item_data['Age'].mean()
        average_purchase_amount = item_data['Purchase Amount (USD)'].mean()
        average_review_rating = item_data['Review Rating'].mean()
        popular_colors = item_data['Color'].value_counts(normalize=True) * 100
        popular_colors = popular_colors.head(5)
        popular_colors_text = ', '.join(f"{color} ({percentage:.1f}%)" for color, percentage in popular_colors.items())
        popular_sizes = item_data['Size'].value_counts(normalize=True) * 100
        popular_sizes = popular_sizes.head(5)
        popular_sizes_text = ', '.join(f"{size} ({percentage:.1f}%)" for size, percentage in popular_sizes.items())
        subscription_percentage = (item_data['Subscription Status'] == 'Yes').mean() * 100
        discount_applied = item_data['Discount Applied'].map({'Yes': 1, 'No': 0}).sum() / len(item_data['Discount Applied']) * 100
        insight_text = f"Average Age: {average_age:.1f}\n"
        insight_text += f"Average Purchase Amount: ${average_purchase_amount:.2f}\n"
        insight_text += f"Average Review Rating: {average_review_rating:.1f}\n"
        insight_text += f"Popular Colors: {popular_colors_text}\n"
        insight_text += f"Popular Sizes: {popular_sizes_text}\n"
        insight_text += f"Subscription Percentage: {subscription_percentage:.1f}%\n"
        insight_text += f"Average Discount Applied: {discount_applied:.1f}%\n"
        self.bottom_label.config(text=insight_text, justify=tk.LEFT)

    def update_category_graph(self, category_counts):
        """Update the category graph based on the provided category counts."""
        self.ax_category.clear()
        category_counts.plot(kind='bar', ax=self.ax_category, color=['skyblue', 'pink', 'lightgreen', 'lightcoral'], edgecolor='black')
        self.ax_category.set_ylabel('Popularity (%)', color='white')
        self.ax_category.set_title('Popularity of Each Category', color='white')
        self.ax_category.tick_params(axis='x', colors='white')
        self.ax_category.tick_params(axis='y', colors='white')
        self.ax_category.set_xticklabels(category_counts.index, rotation=0)
        self.ax_category.grid(False, axis='x')
        self.ax_category.grid(axis='y')
        self.canvas_category.draw()

    def update_gender_graph(self, gender_counts):
        """Update the gender graph based on the provided gender counts."""
        self.ax_gender.clear()
        gender_counts.plot(kind='pie', ax=self.ax_gender, autopct='%1.1f%%', colors=['skyblue', 'pink'], textprops={'color': 'white'})
        self.ax_gender.set_title('Frequency of Gender', color='white')
        self.ax_gender.set_ylabel('')
        self.ax_gender.tick_params(axis='x', colors='white', pad=50)
        self.ax_gender.tick_params(axis='y', colors='white')
        self.ax_gender.set_facecolor('#282434')
        self.canvas_gender.draw()

    def update_shipping_graph(self, shipping_counts):
        """Update the shipping graph based on the provided shipping counts."""
        self.axs_shipping.clear()
        colors = itertools.cycle(['lightblue', 'lightgreen', 'lightcoral'])
        for idx, (category, count) in enumerate(shipping_counts.items()):
            color = next(colors)
            self.axs_shipping.plot(idx, count, marker='o', color=color, linestyle='-')
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
        self.axs_shipping.grid(False, axis='x')
        self.axs_shipping.grid(axis='y')
        self.axs_shipping.set_ylim(min_value - 5, max_value + 5)
        self.canvas_shipping.draw()

    def update_top_items_graph(self, top_items):
        """Update the top items graph based on the provided top items data."""
        self.ax_top_items.clear()
        total_purchases = top_items.sum()
        top_items_percentage = (top_items / total_purchases) * 100
        top_items_percentage = top_items_percentage.head(10)
        colors = list(mcolors.TABLEAU_COLORS.values())
        bars = top_items_percentage.plot(kind='bar', ax=self.ax_top_items, color=colors, edgecolor='black')
        self.ax_top_items.set_ylabel('Percentage of Purchases (%)', color='white')
        self.ax_top_items.set_title('Top 10 Items Purchased', color='white')
        self.ax_top_items.tick_params(axis='x', colors='white')
        self.ax_top_items.tick_params(axis='y', colors='white')
        self.ax_top_items.set_xticklabels(top_items_percentage.index, rotation=45, ha='right')
        for i, value in enumerate(top_items_percentage):
            self.ax_top_items.text(i, value + 1, f'{value:.1f}%', color='black', ha='center')
        max_value = int(max(top_items_percentage))
        y_ticks = list(range(0, max_value + 10, 5))
        self.ax_top_items.set_yticks(y_ticks)
        self.ax_top_items.grid(False, axis='x')
        self.ax_top_items.grid(axis='y')
        self.canvas_top_items.draw()
        self.top_items = top_items_percentage.index.tolist()
        self.bars = bars.get_children()
        self.canvas_top_items.mpl_connect('button_press_event', self.on_bar_click)

    def display_graph_and_stats(self, fig, stats):
        """Display the graph and its descriptive statistics."""
        graph_frame = tk.Frame(self.view.graph_manager.middle_frame, bg='#282434')
        graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stats_frame = tk.Frame(self.view.graph_manager.middle_frame, bg='#282434')
        stats_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        stats_text = tk.Text(stats_frame, wrap=tk.WORD, bg='black', fg='white', font=('Courier', 10))
        stats_text.pack(expand=True, fill=tk.BOTH)
        stats_text.delete('1.0', tk.END)
        stats_text.insert(tk.END, "Descriptive Statistics:\n\n")
        for stat, value in stats.items():
            stats_text.insert(tk.END, f"{stat}: {value}\n")

    def show_bar_chart(self, data, x_title=None, y_title=None):
        """Show a bar chart based on the provided data."""
        data = self.apply_sidebar_filters(data)
        self.clear_middle_frame()
        if isinstance(data, pd.Series):
            data = data.value_counts()
        elif isinstance(data, pd.DataFrame):
            data = data[data.columns[0]].value_counts()
        else:
            messagebox.showerror("Error", "Invalid data type for bar chart.")
            return
        fig, ax = plt.subplots(figsize=(8, 6))
        num_bars = min(len(data.index), 10)
        ax.bar(data.index[:num_bars], data.values[:num_bars], color='skyblue')
        if x_title:
            ax.set_xlabel(x_title, fontsize=12, color='black')
        if y_title:
            ax.set_ylabel(y_title, fontsize=12, color='black')
        ax.set_title("Bar Chart", fontsize=14, color='black')
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        ax.set_xticks(range(len(data.index[:num_bars])))
        ax.set_xticklabels(data.index[:num_bars], rotation=45, ha='right')
        ax.grid(axis='y', color='grey', linestyle='--')
        fig.tight_layout()
        self.display_graph_and_stats(fig, data.describe())

    def show_pie_chart(self, data, title=None):
        """Show a pie chart based on the provided data."""
        data = self.apply_sidebar_filters(data)
        self.clear_middle_frame()
        if isinstance(data, pd.Series):
            data = data.value_counts()
        elif isinstance(data, pd.DataFrame):
            data = data[data.columns[0]].value_counts()
        else:
            messagebox.showerror("Error", "Invalid data type for pie chart.")
            return
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(data.values, labels=data.index, autopct='%1.1f%%', colors=['skyblue', 'pink', 'lightgreen', 'gold'])
        if title:
            ax.set_title(title, fontsize=14, color='black')
        ax.axis('equal')
        fig.tight_layout()
        self.display_graph_and_stats(fig, data.describe())
        if len(data.index) > 1:
            ax.legend(data.index)

    def show_line_chart(self, data, x_title=None, y_title=None):
        """Show a line chart based on the provided data."""
        data = self.apply_sidebar_filters(data)
        self.clear_middle_frame()
        if isinstance(data, pd.DataFrame):
            x_label = data.columns[0]
            y_label = data.columns[1]
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(data[x_label], data[y_label], color='skyblue', label=f'{x_label} vs {y_label}')
            if x_title:
                ax.set_xlabel(x_title, fontsize=12, color='black')
            if y_title:
                ax.set_ylabel(y_title, fontsize=12, color='black')
            ax.set_title("Line Chart", fontsize=14, color='black')
            ax.tick_params(axis='x', colors='black')
            ax.tick_params(axis='y', colors='black')
            ax.grid(axis='both', color='grey', linestyle='--')
            ax.legend()
            fig.tight_layout()
            self.display_graph_and_stats(fig, data.describe())
        else:
            messagebox.showerror("Error", "Invalid data type for line chart.")

    def show_scatter_plot(self, data, x_title=None, y_title=None):
        """Show a scatter plot based on the provided data."""
        data = self.apply_sidebar_filters(data)
        self.clear_middle_frame()
        if isinstance(data, pd.DataFrame) and len(data.columns) == 2:
            x_label, y_label = data.columns
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(data[x_label], data[y_label], color='skyblue', label=f'{x_label} vs {y_label}')
            if x_title:
                ax.set_xlabel(x_title, fontsize=12, color='black')
            if y_title:
                ax.set_ylabel(y_title, fontsize=12, color='black')
            ax.set_title("Scatter Plot", fontsize=14, color='black')
            ax.tick_params(axis='x', colors='black')
            ax.tick_params(axis='y', colors='black')
            ax.grid(axis='both', color='grey', linestyle='--')
            ax.legend()
            fig.tight_layout()
            self.display_graph_and_stats(fig, data.describe())
        else:
            messagebox.showerror("Error", "Invalid data type for scatter plot.")

    def show_histogram(self, data, x_title=None, y_title=None):
        """Show a histogram based on the provided data."""
        data = self.apply_sidebar_filters(data)
        self.clear_middle_frame()
        if isinstance(data, pd.Series):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data, bins=10, color='skyblue', edgecolor='black')
            if x_title:
                ax.set_xlabel(x_title, fontsize=12, color='black')
            if y_title:
                ax.set_ylabel(y_title, fontsize=12, color='black')
            ax.set_title("Histogram", fontsize=14, color='black')
            ax.tick_params(axis='x', colors='black')
            ax.tick_params(axis='y', colors='black')
            ax.grid(axis='y', color='grey', linestyle='--')
            fig.tight_layout(pad=3.0)
            self.display_graph_and_stats(fig, data.describe())
        else:
            messagebox.showerror("Error", "Invalid data type for histogram.")

    def show_box_plot(self, attribute, data, x_title=None, y_title=None):
        """Show a box plot based on the provided attribute and data."""
        data = self.apply_sidebar_filters(data)
        self.clear_middle_frame()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.boxplot(x=data[attribute], ax=ax, color='skyblue')
        if x_title:
            ax.set_xlabel(x_title, fontsize=12, color='black')
        if y_title:
            ax.set_ylabel(y_title, fontsize=12, color='black')
        ax.set_title("Box Plot", fontsize=14, color='black')
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        ax.grid(axis='y', color='grey', linestyle='--')
        fig.tight_layout()
        self.display_graph_and_stats(fig, data[attribute].describe())

    def clear_middle_frame(self):
        """Clear the middle frame containing the graphs."""
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

    def apply_sidebar_filters(self, data):
        """Apply filters based on the sidebar selections to the provided data."""
        location = self.sidebar.location_var.get()
        season = self.sidebar.season_var.get()
        filtered_data = data.copy()
        if location != 'All':
            filtered_data = filtered_data[self.model.df['Location'] == location]
        if season != 'All':
            filtered_data = filtered_data[self.model.df['Season'] == season]
        return filtered_data
