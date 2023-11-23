FROM python:3.11-alpine

WORKDIR /app

# Copy app src
COPY api ./api

# Copy the poetry lock file and project definition
COPY poetry.lock pyproject.toml ./

# Install the package & dependencies globally
RUN pip install .

CMD ["python", "api/main.py"]
