FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN pip install --user Flask==2.0.3 && \
    pip install --user xmltodict && \
    pip install --user pytest

RUN wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml
RUN wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT05.xml

COPY app.py /app/app.py
COPY test_app.py /app/test_app.py

ENTRYPOINT ["python"]
CMD ["app.py"]