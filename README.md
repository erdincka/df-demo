# Data Fabric Demo

This project is a simple data processing pipeline using MapR Streams. It demonstrates a basic data ingestion, transformation, and visualization system.

### Features

- Real-time data visualization of device metrics.

- Ability to start and stop data streams.

- Logging for debugging and monitoring the application.

### Installation

#### If needed, start dev sandbox in local docker machine and run future commands inside the container.

`docker run -d --name mapr --privileged -p 8443:8443 -p 8501:8501 -p 9000:9000 -e clusterName=maprdemo.io -e isSecure --hostname maprdemo.io maprtech/dev-sandbox-container`

and then

`docker exec -it mapr bash`


1. Clone the repository: http://git.ez.win.lab/erdincka/df-pipeline.git

2. Install dependencies:


Refer to [Documentation](https://support.hpe.com/hpesc/public/docDisplay?docId=sf000102990en_us&docLocale=en_US) for installing mapr-streams-python library.

```bash
sudo apt install -y python3.11-dev gcc
python3.11 -m venv --prompt demo .venv
source .venv/bin/activate
pip install streamlit httpx
pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python
```

**If getting librdkafka.so.1 not found error, run this.**

```bash
echo "/opt/mapr/lib" | sudo tee /etc/ld.so.conf.d/mapr-lib.conf`
sudo ldconfig
```

- Authenticate to MapR

`echp mapr | maprlogin password`

- Create stream

```bash

hadoop fs -mkdir demo
maprcli stream create -path demo/metrics -produceperm p -consumeperm p -topicperm p

```

### Usage

1. Start the Streamlit app by running `LD_LIBRARY_PATH=/opt/mapr/lib streamlit run main.py`.
2. Enter a topic in the text input field.
3. Click the "Start Stream" button to begin monitoring device data.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
