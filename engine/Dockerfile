# Start with a base that has Python and common build tools
FROM python:3.10-slim

# Install C, C++, and Java (OpenJDK)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# No COPY needed here!
# We will use this image as an environment to run commands.
CMD ["python3"]