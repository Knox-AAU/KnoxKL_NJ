
# syntax=docker/dockerfile:1
# Base image
FROM python:3.8-slim-buster

# Installing Git
RUN apt-get -y update
RUN apt-get -y install git

# Add a user to avoid running as root
RUN useradd -rm -d /home/appuser -s /bin/bash -g root -G sudo -u 1001 appuser
RUN mkdir /home/appuser/app
RUN chown appuser:root /home/appuser/app

USER appuser

# Add -/.local/bin to path, to allow access to non-root installed python packages
ENV PATH="/home/appuser/.local/bin:{$PATH}"

RUN pip install --upgrade pip

# Setting the Work Directory
WORKDIR /home/appuser/app

# Copy the requirements to the work directory
COPY --chown=appuser:root requirements_dev.txt requirements_dev.txt

# Installing Required dependencies
RUN pip install --extra-index-url https://repos.knox.cs.aau.dk/ -r requirements_dev.txt

# Download the required spaCy large Danish model
RUN python3 -m spacy download da_core_news_lg

# Copy the source code to the work directory
COPY --chown=appuser:root . .

EXPOSE 8000

CMD [ "python3", "app.py"]