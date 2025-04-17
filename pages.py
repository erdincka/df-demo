import streamlit as st
import settings
import pandas as pd

from utils import handle_file_upload, handle_sample_data, label_category, save_to_gold, save_to_silver


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
def show_refined_data():
    # This page is used to display the refined data before it is written to the data warehouse.
    # Silver data is where the refined & stored data is shown & processed.

    # Data transformation
    df: pd.DataFrame = st.session_state.topic_data.copy()
    if st.session_state.index_column:
        df.set_index(st.session_state.index_column, inplace=True)
        # if st.session_state.index_column.lower() == "timestamp":
        #     df.index = pd.to_datetime(st.session_state.topic_data['timestamp'], unit="s")
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
    # st.code(df.head())
    st.button(
        "Save Refined Data",
        on_click=save_to_silver,
        args=[df]
    )


def streaming_page():
    cols = st.columns([20, 80], gap='medium')
    cols[0].button(
        "Publish sample data",
        on_click=handle_sample_data,
        help=f"Generate sample data and publish to Kafka topic: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}",
        use_container_width=True,
    )
    cols[0].button(
        "Publish from file",
        on_click=handle_file_upload,
        help=f"Upload a file and publish to Kafka topic: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}",
        use_container_width=True,
    )
        
    with cols[1]:
        if st.session_state.topic_data.empty:
            st.error("No data in topic, start streaming...")
            return
        else:
            st.write(f"Read from topic: {st.session_state.topic_data.shape}")
            st.dataframe(st.session_state.topic_data, height=180)


def bronze_page():
    if st.session_state.topic_data.empty:
        st.error("No raw data yet.")
        return
    else:
        keys = st.session_state.topic_data.columns
        cols = st.columns(4, gap="medium", vertical_alignment="center")
        with cols[0]:
            st.selectbox("Index", 
                options=keys, 
                index=None, 
                placeholder="Select column for index",
                key="index_column")
            st.write(f"Index: {st.session_state.index_column}")
        with cols[1]:
            st.multiselect(
                "Remove", [k for k in keys if k != st.session_state.index_column], placeholder="Columns to remove", key="remove_columns"
            )
            st.write(f"Remove: {st.session_state.remove_columns}")
        with cols[2]:
            st.selectbox(
                "Mask",
                [k for k in keys if k not in st.session_state.remove_columns and k != st.session_state.index_column],
                index=None,
                placeholder="Column to mask",
                key="mask_column",
            )
            st.write(f"Mask: {st.session_state.mask_column}")
        with cols[3]:
            st.selectbox(
                "Label",
                [k for k in keys if k not in st.session_state.remove_columns and k != st.session_state.index_column],
                index=None,
                placeholder="Apply category using AI",
                key="label_column",
            )
            st.write(f"Label: {st.session_state.label_column}")
        show_refined_data()


st.fragment
def silver_page():
    if st.session_state.silver_data.empty:
        st.error("No refined data yet.")
    else:
        cols = st.columns(2)
        cols[0].selectbox("Group By",
            st.session_state.silver_data.columns,
            index=None,
            key="group_by",
            placeholder="Select column to group by",
        )
        cols[1].multiselect("Aggregate",
            ["sum", "mean", "min", "max", "avg"],
            key="aggr_by",
            placeholder="Select functions to aggregate",
        )
        df: pd.DataFrame = st.session_state.silver_data.copy()
        if st.session_state.group_by:
            print(df.groupby(st.session_state.group_by).head())
        if len(st.session_state.aggr_by) > 0:
            df.agg(st.session_state.aggr_by)
        st.dataframe(df, height=300)
        if st.button("Save to feature data store"):
            save_to_gold(df)


@st.fragment
def gold_page():
    if st.session_state.gold_data.empty:
        st.error("No consolidated data yet.")
    else:
        st.dataframe(st.session_state.gold_data)
