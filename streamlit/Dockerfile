# Use slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit app
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "st_main.py", "--server.port=8501", "--server.address=0.0.0.0"]