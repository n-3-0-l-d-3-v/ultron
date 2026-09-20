# Network-less analysis sandbox for Ultron: Ghidra + Ultron in a locked-down container.
FROM eclipse-temurin:21-jre
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip python3-venv unzip curl ca-certificates binwalk \
    && rm -rf /var/lib/apt/lists/*
ARG GHIDRA_URL=https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.4.3_build/ghidra_11.4.3_PUBLIC_20251203.zip
RUN curl -fsSL "$GHIDRA_URL" -o /tmp/g.zip && unzip -q /tmp/g.zip -d /opt && rm /tmp/g.zip && ln -s /opt/ghidra_* /opt/ghidra
ENV GHIDRA_INSTALL_DIR=/opt/ghidra
COPY . /src
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir /src
ENV PATH=/opt/venv/bin:$PATH
RUN useradd -m analyst
USER analyst
WORKDIR /work
ENTRYPOINT ["ultron"]
