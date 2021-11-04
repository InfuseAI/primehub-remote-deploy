FROM infuseai/docker-stacks:base-notebook-e7725c59

ADD . / /src/primehub-remote-deploy/

USER root
WORKDIR /src/primehub-remote-deploy
RUN pip install -r requirements.txt
RUN python setup.py install

USER jovyan
WORKDIR /home/jovyan
