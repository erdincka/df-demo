import json
import logging
from typing import Any
import streamlit as st
import pandas as pd

import iceberger
from messaging import publish, subscribe
import mock
import settings


logger = logging.getLogger(__name__)


def publish_messages():
    for message in st.session_state.topic_data.to_dict(orient="records"):
        logger.info(message)
        if publish(message=json.dumps(message)):
            logger.debug(f"Published: {message}")
        else:
            logger.warning(f"Failed to publish message: {message}")

@st.dialog("File upload")
def handle_file_upload():
    file = st.file_uploader("CSV or JSON files", ["csv", "json"], accept_multiple_files=False)
    if file:
        match file.type:
            case "text/csv":
                # contents = file.getvalue().decode("utf-8")
                st.session_state.topic_data = pd.read_csv(file)
            case "application/json":
                contents = json.load(file)
                st.session_state.topic_data = pd.DataFrame(contents)
            case _:
                st.error("Unsupported file type")
        publish_messages()
        st.rerun()


def handle_sample_data():
    messages = mock.get_samples()
    st.session_state.topic_data = pd.DataFrame(messages)
    publish_messages()
    #         new_metric['timestamp'] = pd.to_datetime(int(message["timestamp"]), unit="s")
    #         new_metric.set_index('timestamp', inplace=True)


def handle_topic_consume():
    logger.debug(f"Streaming from {settings.STREAM}")

    # Subscribe to the stream
    for message in subscribe():
        # logger.debug(f"Received: {message}")
        st.session_state.topic_data = pd.concat(
            [st.session_state.topic_data, pd.DataFrame([json.loads(message)])]
        )
        st.rerun()
    logger.debug("Done with streaming!")
    # FIX: Enable this after testing
    # copy streamed data into bronze table
    # st.session_state.bronze_data = st.session_state.topic_data.copy()


def label_category(metric: Any):
    # Simulating AI inferencing for labeling
    # TODO: Replace this with actual AI model inference
    return type(metric).__name__


def save_to_silver(df: pd.DataFrame):
    if iceberger.write(
        tier="silver",
        tablename="refined",
        # "records": df.to_dict(orient="records"),
        records=df.to_dict(orient="series"),  # pyright: ignore
    ):
        st.session_state.silver_data = iceberger.find_all("silver", "refined")
    else:
        st.error("Failed to save silver data.")    


def save_to_gold(df: pd.DataFrame):
    table_name = f"group_by_{st.session_state.group_by}_aggr_by_{'_'.join(st.session_state.aggr_by)}"
    if iceberger.write(
        tier="gold",
        tablename=table_name,
        records=df.to_dict(orient="series"), # pyright: ignore
    ):
        st.session_state.gold_data = iceberger.find_all("gold", table_name)
    else:
        st.error("Failed to save gold data.")    

