import logging
import pandas as pd
import streamlit as st

import messaging

st.set_page_config(page_title="Data Fabric Pipeline", layout="wide", initial_sidebar_state="collapsed")

st.session_state.setdefault("logs", "")
st.session_state.setdefault("topic_stats", None)
st.session_state.setdefault("topic_data", pd.DataFrame())
st.session_state.setdefault("bronze_data", pd.DataFrame())
st.session_state.setdefault("silver_data", pd.DataFrame())
st.session_state.setdefault("gold_data", pd.DataFrame())

# Import these after setting the session state
from pages import (
    bronze_page,
    info_page,
    gold_page,
    streaming_page,
    silver_page,
)

logger = logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def log_viewer():
    st.code(st.session_state.logs, language="text", height=200, line_numbers=True)


def main():
    def send_message():
        message = st.text_input("Enter a message to send:")
        if message:
            try:
                # Send the message with a topic
                messaging.producer.produce('mytopic', key='key', value=message.encode('utf-8'))
                messaging.producer.flush()  # Ensure the message is sent
                st.success("Message sent successfully!")
            except Exception as e:
                st.error(f"Error sending message: {e}")

    st.title("Kafka Message Producer (confluent_kafka)")

    # send_message()
    # st.title("Kafka Message Consumer")

    # st.subheader("Messages from Kafka:")
    # for message in messaging.consumer:
    #     st.write(f"Received: {message.value.decode('utf-8')}")

    # info_page()

    # with st.container(border=True):
    #     st.write("Data ingestion")
    #     streaming_page()

    # with st.container(border=True):
    #     st.write("Data Transformation")
    #     bronze_page()

    # with st.container(border=True):
    #     st.write("Data Aggregation")
    #     silver_page()

    # with st.container(border=True):
    #     st.write("Data Products")
    #     gold_page()

    # log_viewer()

    # Start streaming from topic at app start
    # handle_topic_consume()

if __name__ == "__main__":
    main()
