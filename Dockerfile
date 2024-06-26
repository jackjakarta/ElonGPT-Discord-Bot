FROM ubuntu:22.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 git && \
    apt-get install -y python3-pip python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install nano if needed
# RUN apt-get install nano

RUN cd ~ && \
    git clone https://github.com/jackjakarta/ElonGPT-Discord-Bot && \
    cd ElonGPT-Discord-Bot/ && \
    python3 -m venv env && \
    . env/bin/activate && \
    pip3 install -r requirements.txt

# Set the entrypoint script
ENTRYPOINT ["/root/ElonGPT-Discord-Bot/entrypoint.sh"]
