FROM python:3.12-slim
RUN apt-get update
RUN apt-get -y install python3-pip libpango-1.0-0 libpangoft2-1.0-0
ENV WEASYPRINT_VERSION 62.3
RUN pip install weasyprint==$WEASYPRINT_VERSION

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /shop

RUN pip install --upgrade pip

COPY requirements.txt /shop/
RUN pip install -r requirements.txt

COPY . .

CMD ["./entrypoint.sh"]