# BiteBalanceBackend

## Prerequisites
1. `docker` environment
2. `docker-compose`
3. Python 3.9 for development


## Development

### 1. Create and update local .env

``` Bash
cp .env.example .env
```

### 2. Setup virtual env and install dependencies
``` Bash
> python -m venv venv
> source ./venv/bin/activate
> pip install pip-tools
> make dependencies
> pip-sync requirements-dev.txt
> code .
```

### 3. Run dev version, please refer to the Makefile for other options and operations.
``` Bash
> make devlocal 
```

#### How to resolve some possible errors:
```bash
port conflicts ?
> sudo lsof -i :<port number>
> sudo kill -9 <PID>

unable to start container process: exec: "./entrypoint.sh" 
> chmod +x ./entrypoint.sh
```

Then open `http://localhost:<port_defined_in_env>/api/docs`
