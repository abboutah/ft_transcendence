FROM python:3.11.4-slim-buster

# ENV PIP_DISABLE_PIP_VERSION_CHECK 1 
# ENV PYTHONDONTWRITEBYTECODE 1 
# ENV PYTHONUNBUFFERED 1 

RUN mkdir src
COPY ./src/piprequirement.txt /src/piprequirement.txt

WORKDIR /src

RUN python -m pip install --upgrade setuptools wheel
RUN python -m pip install -r piprequirement.txt

COPY ./src/* /src

COPY ./scripts /scripts
RUN chmod +x /scripts/*.sh 
CMD ["/scripts/script.sh"]