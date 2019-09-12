FROM python:3.7
RUN adduser --quiet --disabled-password qtuser


ADD requirements.txt /setup.py  /app/
COPY test /app/test
COPY RIXSPlot /app/RIXSPlot
COPY Interface /app/Interface

WORKDIR /app
RUN pip install -r requirements.txt
RUN python setup.py build
RUN python setup.py install
RUN python -m RIXSPlot
ADD . /app



