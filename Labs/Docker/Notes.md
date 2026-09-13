## Introduction

This chapter covers containerization, the basics of pipelines, as well as basic ingestion.

## Docker

Docker is used to containerize applications

You can run a basic container by:
```docker run -it --rm --entrypoint=bash python:3.13.11-slim```

Where:
- `-it`: i=Interactive, t=Terminal. Allows you to interact with the application through your terminal
- `--rm`: Deletes the container after you are done with it so it isn't hanging in the background
- `--entrypoint=bash`: Enters bash so you can run bash commands. This overrides the ENTRYPOINT in the Dockerfile.
- `python:3.13.11-slim`: Docker image that we want. Pulls from the Docker image repository online.


Containers can be customized through Dockerfiles. A simple example is:

```
FROM python:3.13.11-slim

WORKDIR /code

RUN pip install uv && \
	uv init && \
	uv add pandas pyarrow

COPY pipeline/pipeline.py .

ENTRYPOINT ["uv", "run", "pipeline.py"]
```

Here:
- `FROM python:3.13.11-slim`: Every Dockerfile starts with `FROM` and uses an image, which in this case is Python 3.13.11 slim
- `WORKDIR`: This sets the working directory of the subsequent commands
- `RUN`: Runs commands in the environment's shell. Each `RUN` command creates a new layer. To run multiple commands in one layer, each command can be chained with `&& \` between every new line.
- `COPY`: Copies a file from a path to a specified destination
- `ENTRYPOINT`: When this container is booted up, the specified command is run(in exec format aka the first element is a command and the rest are arguments). In this case, we run "uv run pipeline.py" but each binary is enclosed in double quotes and comma separated in square brackets. 

*Note*: Entrypoint receives the arguments passed after the image name


Once you have the Dockerfile built, you can do the following:
1. Build the image
```
docker build -t test:pandas .
```
- `-t test:pandas`: `-t` lets you interact with the app through the terminal, `test` is the image's name, and `pandas` is the tag(so you don't have to refer to the image through a long hash)
- `.` tells Docker where to look for the Dockerfile
2. Run the container from the image
```
docker run --rm test:pandas 5
```


Additionally, you can alter the `PATH` variable of the environment within the dockerfile itself through:
```
ENV PATH="/app/.venv/bin:$PATH"
```

This prepends the path to your virtual environment's binary folder onto your environment's PATH so that any time you run an executable, the shell searches through the virtual environment first.


## PostgreSQL

You can run a simple Postgres container with the following command:

```
docker run -it --rm -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v ny_taxi_postgres_data:/var/lib/postgresql -p 5432:5432 postgres:18
```

- `-e` denotes an environment variable. Each db has a user/pass along with a name
- `-v` is the volume. Here, we use the named Docker volume `ny_taxi_postgres_data` which is on the host host(will be created if doesn't already exist), and mount it onto the container
s `/var/lib/postgresql` location. Any changes made in the container now persist in the host machine's ny_taxi_postgres_data.
- `-p` is the port
- `postgres:18` is the docker image

You can interact with the database from your local machine using

```
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

This opens up an interactive CLI that connects to the host localhost at port 5432 using the root user and ny_taxi database


To connect to your DB in python, you can use the `sqlalchemy` package. You have to create a SQL engine, which you can do by running:
```
engine = create_engine('postgreqsl+psycopg://root:root@localhost:5432/ny_taxi')
```
- `postgresql+psycopg`: SQL dialect + Adapter
- `root:root`: Your user/pass
- `localhost:5432`: Host + port
- `ny_taxi`: DB name


## Ingesting Data

You can create an empty table using the headers of a python dataframe by doing the following:
```
df.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
```

Here you supply your engine that you defined earlier.


Data can be read in many ways, pd.read_parquet is easy and retains datatypes and schema definitions, whereas pd.read_csv reads csvs and requires some more configuration

For really large datasets, you can't just read the entire thing, so you have to break it into smaller chunks.

```
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000,
    nrows = 545000
)
```

`iterator=True` allows you to iterate through the chunks and `chunksize` lets you set the max size of each chunk


You can insert into the table by:
```
df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
```

Since we chunked this data though, you can use a for loop to iterate through the chunks and insert them one by one:
```
for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
```

*tqdm is a package that will let you see a progress bar as the chunks get loaded*


## Containerizing + Networking

If you want to connect two docker images, you can create one common network by running

```
docker network create [network-name]
```

You can then reference it in docker runs with the `--network=[network-name]` tag

In the lab, we created a postgres image that we named by passing it a `--name pgdatabase` tag. This now becomes the `host` that we connect to with our ingestion script.

```
# Run PostgreSQL on the network
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

# In another terminal, run pgAdmin on the same network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

The container names pgdatabase and pgadmin allow the containers to communicate with each other


