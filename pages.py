import streamlit as st
import icons
import settings
import pandas as pd

from utils import handle_data_ingestion, handle_data_ingestion_file


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
def show_topic_data():
    try:
        # read_from_topic()
        pass
    except Exception as e:
        st.error(e)
    st.dataframe(st.session_state.topic_data, height=300, hide_index=True)


@st.fragment
def show_bronze_data():
    try:
        with open(settings.BRONZE_DATA_PATH, "r") as f:
            bronze_data = pd.read_csv(f)
        # Show ingested data (bronze)
        st.dataframe(bronze_data, height=300, hide_index=True)
    except FileNotFoundError:
        st.error(f"File not found at {settings.BRONZE_DATA_PATH}")
        bronze_data = None


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
    i_tab, i_code, i_details = st.tabs(["Ingestion", "Code", "Details"])
    with i_tab:
        # Present ingestion source
        cols = st.columns(2)
        cols[0].button(
            "Ingest sample data",
            on_click=handle_data_ingestion,
            help=f"Generate sample data and publish to Kafka topic: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}",
            use_container_width=True,
        )
        cols[0].button(
            "Upload CSV",
            on_click=handle_data_ingestion_file,
            help=f"Upload a CSV file and publish to Kafka topic: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}",
            use_container_width=True,
        )
        # Consume Kafka messages

    with i_code:
        pass
        # st.code(get_code_for("__main__", "handle_data_ingestion_file"))
        # st.code(get_code_for("__main__", "handle_data_ingestion"))
        # st.code(get_code_for("__main__", "read_from_topic"))
    with i_details:
        st.image(
            icons.INGESTION_SOURCES, caption="You can ingest from other sources too"
        )
        st.dataframe(st.session_state.bronze_data, height=300, hide_index=True)


@st.fragment
def bronze_page():
    bronze_tab, bronze_code, bronze_details = st.tabs(
        ["Bronze Data", "Code", "Details"]
    )
    with bronze_tab:
        # Read data from file
        show_bronze_data()
    with bronze_code:
        # st.code(get_code_for("iceberger", "find_all"))
        st.code(None)
    with bronze_details:
        st.write("Details about the bronze data")


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
