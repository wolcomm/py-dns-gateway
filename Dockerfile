ARG  VERSION
FROM python:${VERSION}-slim

WORKDIR /root

# update package index
RUN apt-get -q update

COPY . .

# install package
RUN pip install --upgrade pip
RUN pip install --requirement packaging/requirements-test.txt
RUN pip install --editable .

ENTRYPOINT ["bash"]
