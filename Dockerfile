FROM python:3.10-slim-bullseye
WORKDIR /kube_re_server
COPY /kube_re_server .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt  
ENTRYPOINT [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]