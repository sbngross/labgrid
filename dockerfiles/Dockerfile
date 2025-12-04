FROM debian:trixie-slim AS labgrid-base

LABEL maintainer="eha@deif.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN set -e ;\
    apt update -q=2 ;\
    apt install -q=2 --yes --no-install-recommends \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-tomlkit \
        git \
        build-essential \
        ;\
    pip3 config --site set global.break-system-packages true && \
    pip3 config --site set global.root-user-action ignore && \
    apt clean ;\
    rm -rf /var/lib/apt/lists/*

COPY ./dockerfiles/dump-requirements.py ./pyproject.toml /tmp/docker/

RUN set -e ;\
    cd /tmp/docker ;\
    python3 dump-requirements.py requirements.txt ;\
    pip3 install -r requirements.txt ;\
    cd ;\
    rm -rf /tmp/docker

#
# Client
#
FROM labgrid-base AS labgrid-client

RUN pip3 install yq && \
    apt update -q=2  && \
    apt install -q=2 --yes --no-install-recommends microcom openssh-client rsync jq qemu-system qemu-utils && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]

ARG VERSION
COPY ./ /opt/labgrid/
RUN set -e ;\
    cd /opt/labgrid ;\
    SETUPTOOLS_SCM_PRETEND_VERSION="$VERSION" pip3 install --no-cache-dir .

#
# Coordinator
#
FROM labgrid-base AS labgrid-coordinator

VOLUME /opt/coordinator

EXPOSE 20408

WORKDIR /opt/coordinator

CMD ["/usr/local/bin/labgrid-coordinator"]

ARG VERSION
COPY ./ /opt/labgrid/
RUN set -e ;\
    cd /opt/labgrid ;\
    SETUPTOOLS_SCM_PRETEND_VERSION="$VERSION" pip3 install --no-cache-dir .

#
# Exporter
#
FROM labgrid-base AS labgrid-exporter

RUN apt update -q=2 && \
    apt install -q=2 --yes --no-install-recommends ser2net && \
    rm -rf /var/lib/apt/lists/*

COPY dockerfiles/exporter/entrypoint.sh /entrypoint.sh

VOLUME /opt/conf

CMD ["/entrypoint.sh"]

ARG VERSION
COPY ./ /opt/labgrid/
RUN set -e ;\
    cd /opt/labgrid ;\
    SETUPTOOLS_SCM_PRETEND_VERSION="$VERSION" pip3 install --no-cache-dir .
