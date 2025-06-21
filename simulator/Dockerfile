FROM python:3.10-slim
WORKDIR /app
RUN pip install pymodbus==2.5.2
COPY server.py .
CMD ["python", "server.py"]

