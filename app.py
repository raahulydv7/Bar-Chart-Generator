import dash
from dash import dcc, html, callback, Input, Output, State, ALL, MATCH
import dash_bootstrap_components as dbc
from datasets import get_datasets, get_dataset_names, get_dataset, add_dataset
from utils import validate_inputs, create_chart


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)


app.layout = html.Div(
    [
        html.H1("Bar Chart Generator", className="header"),
        
        html.Div(
            [
                html.Label("Select Dataset:"),
                dcc.Dropdown(
                    id="dataset-dropdown",
                    options=[
                        {"label": dataset, "value": dataset}
                        for dataset in get_dataset_names()
                    ],
                    value=get_dataset_names()[0] if get_dataset_names() else None,
                    className="dropdown",
                ),
                html.Div(id="input-container", className="input-container"),
                html.Div(
                    [
                        html.Button(
                            "Generate Chart",
                            id="submit-button",
                            className="submit-button",
                        ),
                        html.Button(
                            "Add New Dataset",
                            id="toggle-add-dataset",
                            className="toggle-button",
                        ),
                    ],
                    style={"display": "flex"},
                ),
                html.Div(id="validation-message", className="validation-message"),
            ],
            className="controls-container",
        ),
        
        html.Div(
            [
                html.H3("Add New Dataset"),
                html.Div(
                    [
                        html.Label("Dataset Name:"),
                        dcc.Input(
                            id="new-dataset-name",
                            type="text",
                            placeholder="Enter dataset name",
                        ),
                    ],
                    style={"marginBottom": "15px"},
                ),
                html.Div(
                    [
                        html.Label("Number of Categories:"),
                        dcc.Input(
                            id="num-categories",
                            type="number",
                            min=1,
                            max=10,
                            value=4,
                            style={"width": "80px"},
                        ),
                        html.Button(
                            "Create Input Fields",
                            id="create-fields-button",
                            className="submit-button",
                            style={"marginLeft": "10px"},
                        ),
                    ],
                    style={"marginBottom": "15px"},
                ),
                html.Div(id="category-input-container", className="category-inputs"),
                html.Div(
                    [
                        html.Button(
                            "Save Dataset",
                            id="save-dataset-button",
                            className="add-dataset-button",
                            style={"display": "none"},
                        )
                    ],
                    style={"marginTop": "15px"},
                ),
                html.Div(id="add-dataset-message", className="validation-message"),
            ],
            id="add-dataset-container",
            className="add-dataset-container",
            style={"display": "none"},
        ),
       
        dcc.Graph(id="bar-chart", className="chart-container"),
        
        dcc.Store(id="input-values-store"),
    ],
    className="app-container",
)



@callback(
    Output("add-dataset-container", "style"),
    Input("toggle-add-dataset", "n_clicks"),
    State("add-dataset-container", "style"),
    prevent_initial_call=True,
)
def toggle_add_dataset_form(n_clicks, current_style):
    if current_style and current_style.get("display") == "block":
        return {"display": "none"}
    else:
        return {"display": "block"}


@callback(
    [
        Output("category-input-container", "children"),
        Output("save-dataset-button", "style"),
    ],
    Input("create-fields-button", "n_clicks"),
    State("num-categories", "value"),
    prevent_initial_call=True,
)
def create_category_fields(n_clicks, num_categories):
    if not num_categories or num_categories < 1:
        return [], {"display": "none"}

    category_fields = []
    for i in range(num_categories):
        category_fields.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Label(f"Category {i+1}:", className="category-label"),
                            dcc.Input(
                                id={"type": "new-category", "index": i},
                                type="text",
                                placeholder=f"Category {i+1}",
                            ),
                        ],
                        style={"marginRight": "20px"},
                    ),
                    html.Div(
                        [
                            html.Label(
                                f"Default Value {i+1}:", className="category-label"
                            ),
                            dcc.Input(
                                id={"type": "new-value", "index": i},
                                type="number",
                                value=0,
                            ),
                        ]
                    ),
                ],
                className="category-field",
            )
        )

    return category_fields, {"display": "block"}



@callback(
    [
        Output("add-dataset-message", "children"),
        Output("add-dataset-message", "className"),
        Output("dataset-dropdown", "options"),
        Output("new-dataset-name", "value"),
        Output("num-categories", "value"),
    ],
    Input("save-dataset-button", "n_clicks"),
    [
        State("new-dataset-name", "value"),
        State("num-categories", "value"),
        State({"type": "new-category", "index": ALL}, "value"),
        State({"type": "new-value", "index": ALL}, "value"),
    ],
    prevent_initial_call=True,
)
def save_new_dataset(
    n_clicks, dataset_name, num_categories, category_values, default_values
):
    if not dataset_name:
        return (
            "Please enter a dataset name.",
            "error-message",
            [{"label": name, "value": name} for name in get_dataset_names()],
            dash.no_update,
            dash.no_update,
        )

    if dataset_name in get_dataset_names():
        return (
            f"Dataset '{dataset_name}' already exists.",
            "error-message",
            dash.no_update,
            dash.no_update,
            dash.no_update,
        )

    if not all(category_values):
        return (
            "Please fill in all category names.",
            "error-message",
            dash.no_update,
            dash.no_update,
            dash.no_update,
        )

    if not all(val is not None for val in default_values):
        return (
            "Please provide all default values.",
            "error-message",
            dash.no_update,
            dash.no_update,
            dash.no_update,
        )


    success = add_dataset(dataset_name, category_values, default_values)

    if success:
        return (
            f"Dataset '{dataset_name}' added successfully!",
            "success-message",
            [{"label": name, "value": name} for name in get_dataset_names()],
            "",
            4,
        )
    else:
        return (
            "Failed to add dataset. Please check your inputs.",
            "error-message",
            dash.no_update,
            dash.no_update,
            dash.no_update,
        )


@callback(Output("input-container", "children"), Input("dataset-dropdown", "value"))
def update_input_fields(selected_dataset):
    if selected_dataset:
        dataset = get_dataset(selected_dataset)
        if dataset:
            categories = dataset["categories"]
            default_values = dataset["default_values"]

            input_fields = []
            for i, category in enumerate(categories):
                input_fields.append(
                    html.Div(
                        [
                            html.Label(f"{category}:"),
                            dcc.Input(
                                id={
                                    "type": "dynamic-input",
                                    "index": i,
                                }, 
                                type="number",
                                value=default_values[i],
                                className="number-input",
                            ),
                        ],
                        className="input-field",
                    )
                )

            return input_fields
    return []



@callback(
    Output("input-values-store", "data"),
    Input({"type": "dynamic-input", "index": ALL}, "value"),
    State("dataset-dropdown", "value"),
    prevent_initial_call=True,
)
def store_input_values(input_values, selected_dataset):
    if not selected_dataset:
        return {}

    dataset = get_dataset(selected_dataset)
    if not dataset:
        return {}

   
    return {"dataset": selected_dataset, "values": input_values}



@callback(
    [
        Output("bar-chart", "figure"),
        Output("validation-message", "children"),
        Output("validation-message", "className"),
    ],
    Input("submit-button", "n_clicks"),
    State("input-values-store", "data"),
    prevent_initial_call=True,
)
def update_chart(n_clicks, stored_data):
    if not stored_data:
        return dash.no_update, "No data available.", "error-message"

    selected_dataset = stored_data.get("dataset")
    input_values = stored_data.get("values", [])

    if not selected_dataset:
        return dash.no_update, "Please select a dataset.", "error-message"

    dataset = get_dataset(selected_dataset)
    if not dataset:
        return (
            dash.no_update,
            f"Dataset '{selected_dataset}' not found.",
            "error-message",
        )

    categories = dataset["categories"]

   
    is_valid, error_message = validate_inputs(input_values, categories)
    if not is_valid:
        return dash.no_update, error_message, "error-message"

    
    fig = create_chart(selected_dataset, categories, input_values[: len(categories)])

    return fig, "Chart updated successfully!", "success-message"



@callback(
    Output("bar-chart", "figure", allow_duplicate=True),
    Input("dataset-dropdown", "value"),
    prevent_initial_call=True,
)
def initialize_chart(selected_dataset):
    if selected_dataset:
        dataset = get_dataset(selected_dataset)
        if dataset:
            categories = dataset["categories"]
            default_values = dataset["default_values"]

            fig = create_chart(selected_dataset, categories, default_values)
            return fig

    return {}


if __name__ == "__main__":
    app.run_server(debug=True)
