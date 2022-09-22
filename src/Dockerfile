FROM ubuntu

RUN apt-get update -y && apt-get install -y python3-pip && python3.10
#RUN apt-get install -y python3-pip && apt-get install -y python3.10

#FROM python:3.9
#RUN apk update
#RUN apk add make automake gcc g++ subversion python3-dev
ADD src/requirements.txt .

RUN pip3 install -r requirements.txt

COPY . ca/

WORKDIR /ca

RUN python3 -m nltk.downloader all

EXPOSE 5000

#ENTRYPOINT ["gunicorn", "wsgi:app", "--timeout", "0", "-w"]
#CMD ["1"]
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
