FROM ubuntu

RUN apt-get update -y && apt-get install -y python3-pip
RUN apt-get install -y python3.9

ADD /engine/requirements.txt /ca/

RUN pip3 install -r /ca/requirements.txt

COPY . ca/

WORKDIR /ca

RUN ["python3", "setup.py", "install"]

CMD python3 -m nltk.downloader all

EXPOSE 5000

#ENTRYPOINT ["gunicorn", "wsgi:app", "--timeout", "0", "-w"]
#CMD ["1"]
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
