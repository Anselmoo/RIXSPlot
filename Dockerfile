FROM python:3.7
RUN adduser --quiet --disabled-password qtuser


ADD requirements.txt /setup.py  /app/
COPY test /app/test
COPY RIXSPlot /app/RIXSPlot
COPY Interface /app/Interface

WORKDIR /app
RUN pip install -r requirements.txt
# Build Python-Interface
RUN python setup.py build
# Install Python-Interface
RUN python setup.py install
RUN flake8 RIXSPlot
RUN python RIXSPlot
ADD . /app



