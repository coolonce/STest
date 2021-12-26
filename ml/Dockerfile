FROM python:3.8-alpine

RUN apk update && apk add postgresql-dev \
                                python3-dev 

RUN apk add py3-numpy py3-pandas

COPY requirements.txt /ml/

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r /ml/requirements.txt

COPY . /ml

COPY ../model.sav /ml/storage/

CMD ["python", "/ml/main.py"]