# 1. Βάση
FROM python:3.14-rc-slim
WORKDIR /app

# 2. Εγκατάσταση Microsoft ODBC Driver 18
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    unixodbc \
    odbcinst \
    curl \
    gnupg2 \
    && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Βιβλιοθήκες Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Αρχεία
COPY .env .
COPY src/ ./src/

# 5. Εκτέλεση
CMD ["python", "src/generator.py"]