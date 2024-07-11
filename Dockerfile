FROM python:3.11.8-slim

ENV TZ=UTC

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat-traditional \
    build-essential libpq-dev unixodbc unixodbc-dev

COPY . /app/

WORKDIR /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

# Expose the port that Django runs on
EXPOSE 8001

# Run the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]
