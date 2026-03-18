# OilWatch 🛢️

OilWatch is a full-stack AI-powered geospatial application designed to automatically detect oil spills using synthetic aperture radar (SAR) imagery, primarily targeting the Niger Delta region. It uses a PyTorch U-Net model and fetches Sentinel-1 imagery via Google Earth Engine (GEE).

## Architecture

*   **Frontend**: Streamlit dashboard with interactive PyDeck/Folium mapping.
*   **Backend**: FastAPI application exposing endpoints for detection and history.
*   **Database**: PostgreSQL for storing detection events and metadata.
*   **ML Pipeline**: PyTorch-based U-Net model for segmentation of SAR imagery.
*   **Infrastructure**: Fully containerized using Docker and `docker-compose`.

## Prerequisites

*   [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure

```text
oilwatch/
├── backend/            # FastAPI app, GEE/inference services, SQLAlchemy models
├── frontend/           # Streamlit dashboard
├── ml/                 # PyTorch training, dataset, and evaluation scripts
├── docker-compose.yml  # Docker Compose orchestration
├── Dockerfile.backend  # Build instructions for FastAPI
├── Dockerfile.frontend # Build instructions for Streamlit
├── requirements.txt    # Shared Python dependencies
└── README.md
```

## Setup & Running Locally

1.  **Clone / Navigate to the directory:**
    ```bash
    cd oilwatch
    ```

2.  **Environment Variables (Optional but recommended):**
    By default, `docker-compose.yml` configures everything you need.
    To connect to Google Earth Engine or use a specific model checkpoint, you can uncomment and modify the `environment` section in `docker-compose.yml`.
    If no model checkpoint is found, the backend will generate a mock mask, ensuring the app remains fully runnable for demo purposes.

3.  **Start the Application:**
    Run the following command to build and start the containers:
    ```bash
    docker-compose up --build
    ```

4.  **Access the Services:**
    *   **Dashboard (Frontend)**: Go to [http://localhost:8501](http://localhost:8501)
    *   **API Docs (Backend)**: Go to [http://localhost:8000/docs](http://localhost:8000/docs)

## Key Features

- **Graceful Fallbacks**: If the backend is unreachable, the Streamlit frontend continues to function and gracefully warns the user.
- **Mock Inference**: If GEE credentials or a trained ML weights file isn't present, the system defaults to a mock generator so the UI can be tested.
- **Historical Tracking**: All detections are saved to PostgreSQL and displayed on the dashboard's History tab.

## Training the Model

If you have SAR patch data and masks, place them in `ml/data/patches/` and `ml/data/masks/` respectively.
You can run the training script locally (install `requirements.txt` via `pip` first):
```bash
# In the project root dir
python -m ml.train
```
This will generate `backend/checkpoints/best_model.pth`.
