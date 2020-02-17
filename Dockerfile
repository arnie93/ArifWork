FROM python:3

ADD src /src

RUN pip install pystrich

CMD [ "python", "./src/my_script.py" ]

##Successfully integrated pyCharm with Python and Git

