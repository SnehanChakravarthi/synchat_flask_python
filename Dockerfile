# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.11.0
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY --chown=appuser:appuser . .


# Create and change ownership of the media directory
RUN mkdir -p /app/app/actions/media && chown -R appuser:appuser /app/app/actions/media


ENV ACCESS_TOKEN=EAADplHaVy4gBO6xrcpa2NhP1FRZBFNFNksEUI7W1zvZBN6d0AlbdWjixWRraiBLd8bNL8vW4fK4LcK4k1ZAR5AdHrl1FlKUnrgL7vXTdmwcFHC0Oh2NP3Am9ejYBc6GfeoHAfSCIHWuN1gnG6zMBEmWAHZCjckvYfO8nW9zPBqL8peGZAxEVUgWrkNVWttjMzWQhBfHAX2hehRVMxPerea8F9crWz2x6wcVhruR4ZD PHONE_NUMBER_ID=217444478114678 VERIFICATION_TOKEN=bitbotbitbot APP_SECRET=b0356fc9c3a1dc8a8ffe9fa01df6b74f OPENAI_API_KEY=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

# Expose the port that the application listens on.
EXPOSE 3000

# Switch to the non-privileged user
USER appuser


# Run the application.
CMD python run.py
