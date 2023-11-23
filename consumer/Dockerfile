FROM python:3.11-alpine

WORKDIR /app

# Copy app src
COPY consumer ./consumer

# Copy the poetry lock file and project definition
COPY poetry.lock pyproject.toml ./

# Install the package & dependencies globally
RUN pip install .

CMD ["python", "consumer/main.py"]
