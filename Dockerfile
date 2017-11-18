FROM arm32v6/alpine
RUN apk add --update python py-pip
RUN mkdir /server
WORKDIR /server
COPY requirements.txt /server
RUN pip install -r requirements.txt
COPY server.py /server
ENTRYPOINT ["python"]
CMD ["server.py"]
