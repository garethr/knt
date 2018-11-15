FROM python:3-alpine

COPY . /src
RUN cd src && pip install -e .

ENTRYPOINT ["/usr/local/bin/knt"]
CMD ["--help"]
