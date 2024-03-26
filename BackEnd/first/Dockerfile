# pull official base image
#debian base image 
#slim: minimal set of packages(lightweight)
#bullseye: codename of a specific release of Debian
FROM python:3.11.4-slim-buster

# set default working directory when running the rest of our commands. 
WORKDIR ./

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1 
#turns off an automatic check for pip updates each time
ENV PYTHONDONTWRITEBYTECODE 1 
#means Python will not try to write .pyc files
ENV PYTHONUNBUFFERED 1 
# ensures Docker does not buffer our console output

# install dependencies
#COPY requirements into the image
COPY ./piprequirement.txt .
RUN python -m pip install --upgrade setuptools wheel
RUN python -m pip install Pillow
RUN python -m pip install -r piprequirement.txt


EXPOSE 8000

# copy all files into the wdirectory
COPY . .
ENTRYPOINT ["sh","script.sh"]