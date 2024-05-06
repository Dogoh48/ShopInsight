import pandas as pd

class DashboardModel:
    def __init__(self, csv_file):
        """Initialize DashboardModel with data from a CSV file."""
        self.df = pd.read_csv(csv_file)

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
