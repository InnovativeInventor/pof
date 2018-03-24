## Proof of Freshness
This is just to demonstrate different ways to prove freshness when making documents or files.

## Running
```bash
export FLASK_APP=app.py
flask run
```

## Running using Docker
```bash
docker build . -t pof_flask && docker run --name pof_flask -p 8000:8000 pof_flask
```

Notes:
- You might need to use `sudo` for Docker to work.
