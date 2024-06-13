mkdir -p dev-data-psql

docker run -d -ti --rm --name instahyre-psql-dev-server \
    -e POSTGRES_PASSWORD='INSTAHYRE@123' \
    -v ./dev-data-psql:/var/lib/postgresql/data:rw \
    -p 5432:5432 \
    postgres
