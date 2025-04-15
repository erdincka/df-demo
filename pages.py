import streamlit as st
import iceberger
import settings
import pandas as pd

from utils import label_category, set_topic_index


@st.fragment
def info_page():
    with st.expander("Building an End-to-End Data Pipeline using Data Fabric"):
        st.image("./app_flow.svg")
        st.write("This demo showcases the data fabric pipeline.")
        st.write("The pipeline consists of three main components:")
        st.write(
            "- Data Ingestion: Data is ingested from various sources and published to a Kafka topic."
        )
        st.write(
            "- Data Processing: Data is processed in real-time and published to a Kafka topic."
        )
        st.write(
            "- Data Storage: Data is stored in a data warehouse for long-term storage and analysis."
        )
        st.write(
            "The pipeline is designed to be scalable and resilient, with built-in monitoring and alerting."
        )


@st.fragment
def show_bronze_data():
    keys = st.session_state.topic_data.keys()
    cols = st.columns(3, gap="medium", vertical_alignment="center")
    with cols[0]:
        st.multiselect(
            "Remove", keys, placeholder="Columns to remove", key="remove_columns"
        )
        st.write(f"Remove: {st.session_state.remove_columns}")
    with cols[1]:
        st.selectbox(
            "Mask",
            [k for k in keys if k not in st.session_state.remove_columns],
            index=None,
            placeholder="Column to mask",
            key="mask_column",
        )
        st.write(f"Mask: {st.session_state.mask_column}")
    with cols[2]:
        st.selectbox(
            "Label",
            [k for k in keys if k not in st.session_state.remove_columns],
            index=None,
            placeholder="Apply category using AI",
            key="label_column",
        )
        st.write(f"Label: {st.session_state.label_column}")

    # Data transformation
    df: pd.DataFrame = st.session_state.topic_data.copy()
    if st.session_state.remove_columns:
        df.drop(columns=st.session_state.remove_columns, inplace=True)
    if st.session_state.mask_column:
        df[st.session_state.mask_column] = df[st.session_state.mask_column].apply(
            lambda x: str(x)[:2] + "*****"
        )
    if st.session_state.label_column:
        df["category_type"] = df[st.session_state.label_column].apply(
            lambda x: label_category(x)
        )
    st.dataframe(df, height=300)
    st.button(
        "Save transformed data",
        on_click=iceberger.write,
        kwargs={
            "tier": "bronze",
            "tablename": "transformed_data",
            "records": df.to_dict(orient="records"),
            "id_field": "timestamp",
        },
    )


@st.fragment
def show_silver_data():
    try:
        with open(settings.SILVER_DATA_PATH, "r") as f:
            silver_data = pd.read_csv(f)
        # Show ingested data (silver)
        st.dataframe(silver_data, height=300, hide_index=True)
    except FileNotFoundError:
        st.error(f"File not found at {settings.SILVER_DATA_PATH}")
        silver_data = None


@st.fragment
def show_gold_data():
    try:
        with open(settings.GOLD_DATA_PATH, "r") as f:
            gold_data = pd.read_csv(f)
        # Show ingested data (gold)
        st.dataframe(gold_data, height=300, hide_index=True)
    except FileNotFoundError:
        st.error(f"File not found at {settings.GOLD_DATA_PATH}")
        gold_data = None


@st.fragment
def ingestion_page():
    if not st.session_state.topic_data.empty:
        fields = st.session_state.topic_data.columns
        st.selectbox(
            "Choose Index",
            fields,
            index=None,
            key="topic_index",
            placeholder="Select an index",
            on_change=set_topic_index,
        )
        st.write(st.session_state.topic_index)

    st.line_chart(
        st.session_state.bronze_data,
        height=180,
    )
    # with i_code:
    #     # st.code(get_code_for("__main__", "handle_data_ingestion_file"))
    #     # st.code(get_code_for("__main__", "handle_data_ingestion"))
    # with i_details:
    #     st.write(f"Read from topic: {st.session_state.topic_data.shape}")
    #     st.dataframe(st.session_state.topic_data, height=300, hide_index=True)
    #     st.write(f"Written to bronze: {st.session_state.bronze_data.shape if st.session_state.bronze_data is not None else 'None'}")
    #     st.dataframe(st.session_state.bronze_data, height=300, hide_index=True)


@st.fragment
def bronze_page():
    # bronze_tab, bronze_code, bronze_details = st.tabs(
    #     ["Bronze Data", "Code", "Details"]
    # )
    # with bronze_tab:
    #     # Read data from file
    show_bronze_data()


# with bronze_code:
#     # st.code(get_code_for("iceberger", "find_all"))
#     st.code(None)
# with bronze_details:
#     st.write("Details about the bronze data")


@st.fragment
def silver_page():
    silver_tab, silver_code, silver_details = st.tabs(
        ["Silver Data", "Code", "Details"]
    )
    with silver_tab:
        # Read data from file
        show_silver_data()
    with silver_code:
        # st.code(get_code_for("iceberger", "find_all"))
        st.code(None)
    with silver_details:
        st.write("Details about the silver data")


@st.fragment
def gold_page():
    gold_tab, gold_code, gold_details = st.tabs(["Gold Data", "Code", "Details"])
    with gold_tab:
        # Read data from file
        show_gold_data()
    with gold_code:
        # st.code(get_code_for("iceberger", "find_all"))
        st.code(None)
    with gold_details:
        st.write("Details about the gold data")
