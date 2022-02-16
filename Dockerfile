ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 py3-pip


WORKDIR /app

# Copy data for add-on
COPY run.sh /app
COPY . /app
RUN pip3 install -r requirements.txt

RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]