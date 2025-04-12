import json

import pandas as pd
import streamlit as st

from kafkaing import publish, subscribe
import mock
import settings
from streams import consume, produce


def handle_file_upload(file):
    settings.logger.info(file)

    with open(file, "rb") as f:
        bytes = f.read()
        print(bytes)
        # TODO: Handle the data ingestion here
        pass


def handle_sample_data():
    messages = mock.get_samples()
    for message in messages:
        settings.logger.debug(f"Sending data: {message}")
        data_sent = produce(message=json.dumps(message)) if settings.isStreams else publish(message=json.dumps(message))
        if data_sent:
            settings.logger.info(f"Published: {message}")
        else:
            settings.logger.warning(f"Failed publish {message}")


def handle_data_consumption():
    settings.logger.debug(f"Reading from DF Stream: {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}")
    
    for message in consume() if settings.isStreams else subscribe():
        settings.logger.debug(f"Received: {message}")
        st.session_state.topic_data = pd.concat(
            [st.session_state.topic_data, pd.DataFrame([json.loads(message)])]
        )
