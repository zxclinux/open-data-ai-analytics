## Local microservices stack

### 1. Requirements

- Docker and Docker Compose

### 2. Build & run

From the repository root:

```bash
cd src
docker compose up --build
```

This will start 5 services:

- `web` – main UI and JSON API on `http://localhost:8000`
- `data-load` – downloads CSV and loads it into SQLite
- `data-quality` – basic quality metrics
- `data-research` – analytical research
- `visualization` – charts as PNG

All services share:

- volume `data` – raw CSV + `petitions.db`
- volume `reports` – generated figures

### 3. Workflow

1. Open `http://localhost:8000` in a browser.
2. Press **“Download & Load into DB”** to fetch CSV and fill SQLite.
3. Explore:
   - **Petitions** table and search in the Home page.
   - **Quality**, **Research**, **Charts** tabs in the top navigation.

If needed, you can clear the database from the Home page with the **“Clear DB”** button.

