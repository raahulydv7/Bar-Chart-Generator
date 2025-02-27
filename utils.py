import pandas as pd
import plotly.express as px


def validate_inputs(values, categories):

    input_values = list(values[: len(categories)])

    if not all(
        isinstance(val, (int, float)) or (isinstance(val, str) and val.isdigit())
        for val in input_values
        if val is not None
    ):
        return (False,)

    if any(val is None or val == "" for val in input_values):
        return (False,)

    return True, ""


def create_chart(selected_dataset, categories, values):

    input_values = [float(val) if isinstance(val, str) else val for val in values]

    df = pd.DataFrame({"Category": categories, "Value": input_values})

    fig = px.bar(df, x="Category", y="Value", title=f"{selected_dataset} Chart")
    fig.update_layout(
        xaxis_title="Categories", yaxis_title="Values", template="plotly_white"
    )

    return fig
