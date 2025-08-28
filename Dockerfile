FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir --upgrade pip uv

# Copy project metadata and source (so install reads pyproject deps)
COPY pyproject.toml ./
COPY src/ ./src

# Install from pyproject (installs declared dependencies)
RUN uv pip install --system .

EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000"]
