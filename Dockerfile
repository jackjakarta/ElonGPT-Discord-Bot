FROM ubuntu:20.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 git python3-pip python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install nano if needed
# RUN apt-get install nano

RUN cd ~ && \
    git clone https://github.com/jackjakarta/ElonGPT-Discord-Bot && \
    cd ElonGPT-Discord-Bot/ && \
    python3 -m venv env && \
    . env/bin/activate && \
    pip3 install -r requirements.txt

# Create an entrypoint script
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'tail -f /dev/null &' >> /entrypoint.sh && \
    echo 'TAIL_PID=$!' >> /entrypoint.sh && \
    echo 'cd /root/ElonGPT-Discord-Bot/' >> /entrypoint.sh && \
    echo 'git pull' >> /entrypoint.sh && \
    echo 'source env/bin/activate' >> /entrypoint.sh && \
    echo 'pip3 install --upgrade -r requirements.txt' >> /entrypoint.sh && \
    echo 'nohup python3 main.py > activity.log 2>&1 &' >> /entrypoint.sh && \
    echo 'trap "kill $TAIL_PID" EXIT' >> /entrypoint.sh && \
    echo 'wait' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
