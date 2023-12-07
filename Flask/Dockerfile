FROM python:3.11

EXPOSE 80

WORKDIR /Flask

COPY . /Flask
RUN pip install -r requirements.txt
RUN curl -L https://github.com/kubernetes/kompose/releases/download/v1.30.0/kompose-linux-amd64 -o /usr/local/bin/kompose
RUN chmod a+x /usr/local/bin/kompose
RUN wget https://github.com/mikefarah/yq/releases/download/v4.35.1/yq_linux_amd64 -O /usr/bin/yq
RUN chmod +x /usr/bin/yq
