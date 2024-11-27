# personal_secretary
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

# deploy
```
rm -rf personal_secretary && tar xvf personal_secretary.tgz
```

```
cd personal_secretary/
```

```
docker-compose build && docker-compose down && docker-compose up -d
```