Bar Chart Generator
A Dash web application that allows users to select datasets, input values, and generate interactive bar charts. Users can also add their own custom datasets with a simple interface.
Features

Select from predefined datasets (Fruits, Countries, Products)
Add new custom datasets through the UI
Input custom values for each category
Generate dynamic bar charts based on user input
Input validation to ensure numerical values
Clean, responsive user interface with Bootstrap styling

Screenshots
Add screenshots of your application here after implementation
Requirements

Python 3.6+
Dash
Plotly
Pandas
Dash Bootstrap Components

Installation

Clone this repository or extract the zip file

bashCopygit clone https://github.com/yourusername/bar-chart-generator.git
cd bar-chart-generator

Install the required dependencies:

bashCopypip install dash plotly pandas dash-bootstrap-components
Running the Application
To run the application, execute the following command:
bashCopypython app.py
The application will start a local server, typically at http://127.0.0.1:8050/. Open this URL in your web browser to access the application.
Usage
Generating Charts

Select a dataset from the dropdown menu
Input your desired values for each category (or use the default values)
Click the "Generate Chart" button to generate/update the bar chart
View the validation message to ensure inputs are correct

Adding New Datasets

Click the "Add New Dataset" button to toggle the dataset creation form
Enter a unique name for your dataset
Specify the number of categories you want to include
Click "Create Input Fields" to generate the category input form
Fill in all category names and their default values
Click "Save Dataset" to add your new dataset to the application
Your new dataset will appear in the dropdown menu and can be used immediately

Project Structure
Copybar-chart-generator/
│
├── app.py            # Main application file
├── datasets.py       # Dataset configuration and management
├── utils.py          # Utility functions for chart creation and validation
├── assets/
│   └── styles.css    # CSS styling for the application
└── README.md         # Documentation
Predefined Datasets
The application comes with three predefined datasets:

Fruits

Categories: Apples, Bananas, Cherries, Dates
Default Values: 10, 15, 7, 5


Countries

Categories: USA, Canada, Mexico, Brazil
Default Values: 30, 20, 25, 10


Products

Categories: Laptops, Tablets, Smartphones, Desktops
Default Values: 100, 75, 50, 40



Programmatically Adding New Datasets
Developers can also add new datasets by modifying the datasets.py file:
pythonCopyfrom datasets import add_dataset

# Add a new dataset
add_dataset(
    name="New Dataset",
    categories=["Category1", "Category2", "Category3"],
    default_values=[10, 20, 30]
)
Or by directly editing the datasets dictionary in the datasets.py file.
