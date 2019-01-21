# shopozor-backend

## Development's instructions

### Getting started

1. Init and update `saleor` submodule

```
git submodule init
git submodule update
```

Saleor software will then be accessible at the latest release we granted access to.

2. Create virtual environment

```
virtualenv venv
```

3. Install dependencies

```
./scripts/install/install.sh
./scripts/install/install-dev.sh
```

4. Add the relevant environment variables to the virtual environment (in the file `venv/bin/activate`):

```
export PYTHONPATH=path-to-local-repo/saleor:$PYTHONPATH
export SECRET_KEY=hahahaha
export DJANGO_SETTINGS_MODULE=shopozor.settings
```

### Testing saleor

The purpose of the `shopozor-backend` project is to provide the Shopozor's frontends with a backend. In particular, this means that we don't care at all about saleor's frontend developments. However, it can be that you need to run saleor's tests for some reason. In that case, we recommend you read [these instructions](https://github.com/softozor/shopozor-configuration/blob/master/doc/tests/unit-tests.md).
