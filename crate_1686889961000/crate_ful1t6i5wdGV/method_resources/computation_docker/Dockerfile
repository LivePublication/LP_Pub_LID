FROM ubuntu:latest

# Create computation directory structure
# Generic for all computational tasks
RUN mkdir -p /computation
RUN mkdir -p computation/input
RUN mkdir -p computation/output
WORKDIR /computation

# Add directories to enviro variables
ENV INPUT_DIR input
ENV OUTPUT_DIR output

# Add scripts
ADD main.py .
ADD model.lid.top800.epoch20.neg100.dim100.ns.small.min5.ftz .

# Install libraries and dependencies
# May need to change python version depending on the script
RUN apt-get update && apt-get install -y build-essential python3 python3-pip 
# install fastText library
RUN pip3 install fastText==0.9.2

# Execute the script when container is run
ENTRYPOINT [ "python3", "./main.py" ]
# Keeps the container alive for debugging
CMD [""]

