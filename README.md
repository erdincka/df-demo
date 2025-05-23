# Data Fabric Demo

This project is a simple data processing pipeline using MapR Streams. It demonstrates a basic data ingestion, transformation, and visualization system.

### Features

- Real-time data visualization of device metrics.

- Ability to start and stop data streams.

- Logging for debugging and monitoring the application.

### Installation

#### If needed, start dev sandbox in local docker machine and run future commands inside the container.

`docker run -d --name mapr --privileged -p 8443:8443 -p 8501:8501 -p 9000:9000 -p 2222:22 -e clusterName=maprdemo.io -e isSecure --hostname maprdemo.io maprtech/dev-sandbox-container`

and then

`docker exec -it mapr bash`

1. Clone the repository: `apt update && apt install git -y && git clone https://github.com/erdincka/df-demo.git; cd df-demo`

2. Create venv: `apt install python3.11-venv -y && python3.11 -m venv .venv`

3. Activate venv: `source .venv/bin/activate`

4. Install requirements: `pip install -r requirements.txt`

5. Authenticate to MapRP: `echo mapr | maprlogin password`

6. Create volume: `maprcli volume create -name demo -path /demo -minreplication 1 -nsminreplication 1 -replication 1 -nsreplication 1`

7. Run the application: `streamlit run main.py`.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
