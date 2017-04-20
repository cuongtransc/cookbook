# Lambda Architecture Basic

## Deploy

Step 1: Create lambda-back network

```sh
docker network create lambda-back
```

Step 2: Deploy

```
make up
```

## List topic

```
make list-topic
```

## Run producer

```
make producer
```

## Run consumer

```
make consumer
```
