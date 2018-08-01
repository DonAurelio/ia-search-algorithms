# Base image
FROM python:2.7

# Image mantainer
LABEL maintainer="Aurelio Vivas aurelio.vivas@correounivalle.edu.co"

# Working directory inside the container
WORKDIR /usr/src/app

# Copy the project into the container current workdir
COPY . .

# Installing requirements
# All python packages instaled with apt-get are 
# installed globally in /usr/bin/...
RUN apt-get update && apt-get install -y \
	python-pygraphviz \
	python-matplotlib \
	python-qt4 \
	python-tk \
	python-pip

RUN /usr/bin/python -m pip install -r requirements.txt

# Running the application
ENV QT_GRAPHICSSYSTEM="native"
CMD /usr/bin/python main.py

