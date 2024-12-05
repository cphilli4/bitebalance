
FROM python:3.9-slim

# Set environment variables.
ARG stage
ENV STAGE=$stage
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY requirements*.txt entrypoint.sh /
RUN if [ "${STAGE}" = "dev" ]; then pip install --no-cache-dir -r requirements-dev.txt; else pip install --no-cache-dir -r requirements.txt; fi

# Make entrypoint script executable
RUN chmod +x /entrypoint.sh

USER 1000
COPY app app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["start"]