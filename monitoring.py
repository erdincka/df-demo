import logging
import pandas as pd

from streams import stream_metrics
logger = logging.getLogger(__name__)

def get_recent_data(STREAM: str, TOPIC: str):
    for metric in stream_metrics(STREAM, TOPIC):
        data = {
            "Timestamp": [metric["timestamp"]],
            "Published": [
                metric["data"][0]["maxoffset"] + 1
            ],  # Assuming maxoffset is the last offset + 1
            "Consumed": [metric["data"][0]["minoffsetacrossconsumers"]],
        }

        logger.debug(f"Got topic metric: {data}")

        df = pd.DataFrame(data, columns=["Timestamp", "Published", "Consumed"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")
        df.set_index("Timestamp", inplace=True)
        return df

