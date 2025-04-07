IoT Device Monitoring System

This project is a simple IoT device monitoring system built using Python, Streamlit, using mocked data. The system allows users to monitor device data in real-time.

### Features

- Real-time data visualization of device metrics.

- Ability to start and stop data streams.

- Logging for debugging and monitoring the application.

### Installation

1. Clone the repository: http://git.ez.win.lab/erdincka/devices.git

2. Install dependencies:

- create and activate venv

`python3 -m venv --system-site-package --prompt devices .venv`
`source .venv/bin/activate`

- mapr-streams-python package

From [Documentation](https://support.hpe.com/hpesc/public/docDisplay?docId=sf000102990en_us&docLocale=en_US):

```bash
sudo dnf install -y python3.11-devel gcc
python3.11 -m venv --prompt devices .venv`
source .venv/bin/activate
pip install streamlit httpx
pip install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python
```

<!-- cp -R .venv/lib/python3.11/site-packages/mapr_streams_python-0.11.0.2-py3.6.egg-info .venv/lib/python3.6/site-packages/mapr_streams_python -->

**If getting librdkafka.so.1 not found error, run this.**

```bash
echo "/opt/mapr/lib" | sudo tee /etc/ld.so.conf.d/mapr-lib.conf`
sudo ldconfig
```

- Authenticate to MapR

`maprlogin password`

- Create stream

```bash

hadoop fs -mkdir iot
maprcli stream create -path iot/device_metrics -produceperm p -consumeperm p -topicperm p

```

### Usage

1. Start the Streamlit app by running `streamlit run main.py`.
2. Enter a topic in the text input field.
3. Click the "Start Stream" button to begin monitoring device data.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
