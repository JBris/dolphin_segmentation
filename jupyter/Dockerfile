ARG JUPYTER_TAG

FROM jupyter/tensorflow-notebook:${JUPYTER_TAG}

WORKDIR /home/jovyan/work
ADD . /home/jovyan/work

RUN pip install -r requirements.txt
