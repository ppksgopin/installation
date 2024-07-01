FROM python:3.11.9

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn
RUN apt-get update -y && apt-get install tzdata
 
COPY fastAPI_intern_ver.py /run
WORKDIR /run
ENV TZ = "Asia/Taipei"

CMD ["uvicorn", "fastAPI_intern_ver:app", "--host", "0.0.0.0", "--port", "8192"]
