FROM postgres:16.2

#RUN apt update && \
#    apt install -y git make gcc postgresql-server-dev-9.6 bison flex sudo && \
#    apt clean && \
#    rm -rf /var/lib/apt/lists/*


COPY ./docker/db/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/* \
    && mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance

COPY ./docker/db/entrypoints/* /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/*

EXPOSE 5432/tcp
