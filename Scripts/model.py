"""
model.py: Module for managing and processing data.
"""
import os
import pandas as pd
from PIL import Image, ImageTk

class DashboardModel:
    """Class for loading and filtering dataset."""
    def __init__(self):
        """Initialize DashboardModel with data from a CSV file."""
        self.setup_directories()
        self.df = pd.read_csv(self.dataset)

    def setup_directories(self):
        """Set up directories."""
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.dirname(current_directory)
        self.dataset_folder = os.path.join(parent_directory, 'Dataset')
        self.dataset = os.path.join(self.dataset_folder, 'shopping_trends_updated.csv')

    def filter_data(self, category_filters, size_filters, location, season):
        """Filter data based on given filters."""
        filtered_df = self.df.copy()
        if category_filters:
            filtered_df = filtered_df[filtered_df['Category'].isin(category_filters)]
        if size_filters:
            filtered_df = filtered_df[filtered_df['Size'].isin(size_filters)]
        if location != 'All':
            filtered_df = filtered_df[filtered_df['Location'] == location]
        if season != 'All':
            filtered_df = filtered_df[filtered_df['Season'] == season]
        return filtered_df

    def load_image(self, filename):
        """Load image from a specified folder."""
        current_directory = os.path.dirname(__file__)
        parent_directory = os.path.dirname(current_directory)
        image_folder = os.path.join(parent_directory, 'Images')
        image_path = os.path.join(image_folder, filename)
        image = Image.open(image_path)
        image = image.resize((50, 50))
        return ImageTk.PhotoImage(image)

    def get_row_by_item_name(self, item_name):
        """Retrieve the row corresponding to the given item_name."""
        row = self.df[self.df['Item Purchased'] == item_name]
        return row if not row.empty else None
