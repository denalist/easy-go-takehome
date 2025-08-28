FROM python:3.11-slim

WORKDIR /app

# Install runtime deps via pyproject
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy source last
COPY . .

EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000"]
