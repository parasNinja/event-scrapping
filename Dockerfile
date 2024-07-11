# # Use the official Python base image with version 3.11.8
# FROM python:3.11.8-slim

# ENV TZ=UTC

# WORKDIR /app/

# # Install system dependencies
# RUN apt-get update \
#     && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat-traditional \
#     build-essential libpq-dev unixodbc unixodbc-dev

# # Copy the whole project directory to the container

# COPY . /app/

# # Install Poetry
# RUN pip install poetry

# # Change to the project directory

# # Install project dependencies
# RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

# # Expose the port that Django runs on
# EXPOSE 8001

# # Run the Django development server
# # CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8001"]
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]


# Use the official Python base image with version 3.11.8
FROM python:3.11.8-slim

ENV TZ=UTC

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat-traditional \
    build-essential libpq-dev unixodbc unixodbc-dev

# Set the working directory
WORKDIR /app

# Copy the whole project directory to the container
COPY scrapping_events/ /app/

# Install Poetry
RUN pip install poetry

WORKDIR /app/scrapping_events
# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

# Debug step: list the contents of /app/ to verify manage.py is present

# Expose the port that Django runs on
EXPOSE 8001

# Run the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]
