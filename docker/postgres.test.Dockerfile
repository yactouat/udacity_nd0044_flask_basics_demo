FROM postgres:12.11

RUN mkdir /sql
COPY ./docker/sql/seed.psql /sql/seed.psql
COPY ./docker/sql/seed.sh /docker-entrypoint-initdb.d/seed.sh

CMD ["-p", "5433"]