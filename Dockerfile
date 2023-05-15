FROM python:3.11.1-bullseye

RUN pip install poetry

COPY ./ /opt/app/

COPY pyproject.toml /opt/app/
COPY poetry.lock /opt/app/


WORKDIR /opt/app/

RUN poetry config installer.modern-installation false
RUN poetry install


ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]