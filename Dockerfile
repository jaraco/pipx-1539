FROM ubuntu:jammy

RUN apt update
RUN apt upgrade -y
RUN apt install -y software-properties-common
RUN apt-add-repository -y ppa:deadsnakes
RUN apt update

# Disable interactive on the installs below
ENV DEBIAN_FRONTEND=noninteractive

# Set TZ to avoid spurious errors from Sphinx (nektos/act#1853)
ENV TZ=UTC

# Install Pythons
RUN apt install -y python3.10 python3.10-dev python3.10-venv
RUN apt install -y python3.12 python3.12-dev python3.12-venv

RUN apt install -y python3-setuptools python3-pip

RUN python3 -m pip install pipx

CMD pipx run --python 3.12 --spec setuptools python -c "import setuptools"
