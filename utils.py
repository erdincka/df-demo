import json

import pandas as pd
import streamlit as st

from kafkaing import publish, subscribe
import mock
import settings
from streams import consume, produce


def handle_data_ingestion_file(file):
    settings.logger.info(file)

    with open(file, "rb") as f:
        bytes = f.read()
        print(bytes)
        # TODO: Handle the data ingestion here
        pass


def handle_data_ingestion():
    messages = mock.get_samples()
    for msg in messages:
        settings.logger.debug(f"Sending data: {msg}")
        if settings.isStreams:
            if produce(message=json.dumps(msg)):
                settings.logger.info(f"Published: {msg}")
            else:
                settings.logger.warning(f"Failed publish {msg}")
        else:
            publish(message=json.dumps(msg))


def handle_data_consumption():
    if settings.isStreams:
        settings.logger.debug(f"Reading from DF Stream: {settings.STREAM}")
        for message in consume():
            settings.logger.debug(f"Received: {message}")
            st.session_state.topic_data = pd.concat(
                [st.session_state.topic_data, pd.DataFrame([json.loads(message)])]
            )
    else:
        settings.logger.debug(f"Reading from Kafka topic: {settings.KWPS_STREAM}")
        for message in subscribe():
            settings.logger.debug(f"Received: {message}")
            st.session_state.topic_data = pd.concat(
                [st.session_state.topic_data, pd.DataFrame([json.loads(message)])]
            )
