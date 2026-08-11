FROM python:3.11-slim-bookworm AS build

WORKDIR /opt/Tourney

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . /opt/Tourney

RUN pip install --no-cache-dir -r requirements.txt \
    && for d in Tourney/plugins/*; do \
        if [ -f "$d/requirements.txt" ]; then \
            pip install --no-cache-dir -r "$d/requirements.txt";\
        fi; \
    done;


FROM python:3.11-slim-bookworm AS release
WORKDIR /opt/Tourney

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libffi8 \
        libssl3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=1001:1001 . /opt/Tourney

RUN useradd \
    --no-log-init \
    --shell /bin/bash \
    -u 1001 \
    tourney \
    && mkdir -p /var/log/Tourney /var/uploads \
    && chown -R 1001:1001 /var/log/Tourney /var/uploads /opt/Tourney \
    && chmod +x /opt/Tourney/docker-entrypoint.sh

COPY --chown=1001:1001 --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

USER 1001
EXPOSE 8000
ENTRYPOINT ["/opt/Tourney/docker-entrypoint.sh"]
