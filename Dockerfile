FROM python:3.10-alpine as build

RUN wget -q -nv -O - https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY . /app

WORKDIR /app

RUN /root/.poetry/bin/poetry build -f wheel

RUN mkdir /dist && mv dist/* /dist



FROM python:3.10-alpine

COPY --from=build /dist /dist

RUN pip install /dist/*.whl && rm -r /dist

ENTRYPOINT [ "localhttps" ]
