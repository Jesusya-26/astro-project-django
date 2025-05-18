FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md manage.py /app/

RUN sed -i '0,/version = .*/ s//version = "0.1.0"/' pyproject.toml

RUN poetry config virtualenvs.create false && \
    poetry install --with dev --no-root

COPY astro_project /app/astro_project
COPY astrocat /app/astrocat

RUN pip install .

RUN echo "#!/bin/sh" > /entrypoint.sh && \
    echo "python manage.py migrate" >> /entrypoint.sh && \
    echo "python manage.py collectstatic --noinput" >> /entrypoint.sh && \
    echo "python manage.py runserver 0.0.0.0:8000" >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/bin/sh"]
CMD ["/entrypoint.sh"]
