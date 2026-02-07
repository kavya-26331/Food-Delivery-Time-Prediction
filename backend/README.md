# Food Delivery AI Assistant - Backend

A comprehensive AI-powered backend service for a food delivery platform, built with FastAPI, machine learning, and large language models.

## Overview

This backend provides intelligent features for a food delivery system including:

- **ETA Prediction**: Machine learning model to predict delivery times based on various factors
- **RAG Chatbot**: Retrieval-Augmented Generation chatbot for customer support using FAQ data
- **Rider AI Assistant**: AI-powered assistant for delivery riders
- **Location Tracking**: Real-time location updates for deliveries
- **Authentication & Orders**: User management and order processing (currently disabled)

## Architecture

### Tech Stack

- **Framework**: FastAPI (Python) - High-performance web framework for building APIs with automatic OpenAPI documentation.
- **Database**: SQLite (configured for simplicity; originally PostgreSQL) with SQLAlchemy ORM - ORM for database interactions.
- **Machine Learning**: scikit-learn (for model training/prediction), pandas (data manipulation), joblib (model serialization).
- **AI/LLM**: LangChain (framework for LLM applications), Ollama (local LLM server for Llama 3.1), FAISS (vector database for semantic search).
- **Authentication**: JWT tokens with passlib (password hashing) and python-jose (JWT handling).
- **Frontend**: Streamlit (for demo interface), requests (HTTP client for API calls).
- **Other Libraries**: pydantic (data validation), uvicorn (ASGI server), sentence-transformers (embeddings), python-dotenv (environment variables).

### Project Structure and File Explanations

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point - Initializes the FastAPI app, includes routers, and sets up database tables.
│   ├── config.py            # Configuration settings - Loads environment variables, defines API keys, database URLs, and model paths.
│   ├── database.py          # Database connection and setup - Creates SQLAlchemy engine, session, and base class for models.
│   ├── models.py            # SQLAlchemy models - Defines database tables (e.g., Delivery) using ORM.
│   ├── schemas.py           # Pydantic schemas for API - Data models for request/response validation (e.g., ETAPredict, ChatRequest).
│   ├── routers/             # API route handlers
│   │   ├── predict.py       # ETA prediction endpoint - Handles POST /predict/eta, calls ML service for ETA prediction.
│   │   ├── rag_api.py       # RAG chatbot endpoint - Handles POST /rag/chat, integrates with RAG chatbot for customer queries.
│   │   ├── rider_ai.py      # Rider AI assistant endpoint - Handles POST /ai/rider, uses Ollama for rider-specific AI responses.
│   │   ├── location.py      # Location tracking endpoint (not implemented in current code).
│   │   ├── auth.py          # Authentication (disabled) - Would handle user auth with JWT.
│   │   └── orders.py        # Order management (disabled) - Would manage orders, users, restaurants.
│   ├── services/            # Business logic services
│   │   ├── eta_predictor.py # ML prediction service - Loads ML model/scaler, preprocesses features, predicts ETA.
│   │   └── weather.py       # Weather service (removed) - Would integrate weather APIs (e.g., OpenWeatherMap).
│   ├── ml/                  # Machine learning components
│   │   ├── model.pkl        # Trained ML model - Serialized scikit-learn model for ETA prediction.
│   │   ├── scaler.pkl       # Feature scaler - StandardScaler for normalizing numerical features.
│   │   ├── preprocessing.py # Data preprocessing - Utilities for cleaning and preparing data (not used in current code).
│   │   └── model_utils.py   # Model utilities (removed) - Would contain helper functions for ML.
│   ├── llm/                 # Large language model components
│   │   ├── rag_chat.py      # RAG chatbot implementation - Builds FAISS index, searches docs, generates responses using Ollama.
│   │   ├── rag_loader.py    # Document loading and vectorization - Loads and embeds documents for vector store (not used in current code).
│   │   └── data/            # Training data
│   │       ├── faq.txt      # FAQ documents - Text data for RAG chatbot training.
│   │       ├── delivery_rules.txt # Delivery rules - Additional context for chatbot.
│   │       ├── refund_policy.txt  # Refund policy - More context data.
│   │       └── vectorstore/ # FAISS vector database
│   │           └── index.faiss # FAISS index file - Pre-built vector index for fast similarity search.
│   └── utils/
│       └── text_cleaning.py # Text preprocessing utilities - Functions for cleaning text data (not used in current code).
├── requirements.txt         # Python dependencies - List of all required packages with versions.
└── README.md               # This file - Project documentation.
```

## Features

### 1. ETA Prediction

- **Endpoint**: `POST /predict/eta`
- **Description**: Predicts estimated time of arrival for food deliveries
- **Input**: Distance, weather, time factors, rider details, etc.
- **Output**: ETA in minutes
- **ML Model**: Trained regression model using scikit-learn

### 2. RAG Chatbot

- **Endpoint**: `POST /rag/chat`
- **Description**: AI-powered customer support chatbot
- **Technology**: Retrieval-Augmented Generation with Ollama Llama 3.1
- **Data**: FAQ documents, delivery rules, refund policies
- **Vector DB**: FAISS for semantic search

### 3. Rider AI Assistant

- **Endpoint**: `POST /ai/rider`
- **Description**: AI assistant for delivery riders
- **Features**: Route optimization, customer communication tips, etc.

### 4. Location Tracking

- **Endpoint**: `POST /location/update`
- **Description**: Real-time location updates for deliveries
- **Features**: GPS tracking, delivery status updates

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Ollama with Llama 3.1 model
- Virtual environment (recommended)

### Installation

1. **Clone the repository** (if applicable)

   ```bash
   git clone <repository-url>
   cd food_delivery/backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   - Create a PostgreSQL database
   - Update connection settings in `app/config.py`
   - Run database migrations (if applicable)

5. **Set up Ollama**
   - Install Ollama: https://ollama.ai/
   - Pull Llama 3.1 model: `ollama pull llama3.1`

6. **Run the application**

   ```bash
   # Backend API
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Frontend (in another terminal)
   streamlit run frontend/app.py
   ```

## API Documentation

Once the server is running, visit:

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

## Configuration

Key configuration files:

- `app/config.py`: Database URLs, API keys, model paths
- Environment variables can be set for sensitive data

## Machine Learning Model

The ETA prediction uses a trained regression model with features including:

- Distance (km)
- Weather conditions
- Time of day/week
- Traffic levels
- Rider rating and experience
- Vehicle condition
- Preparation time

Model files are stored in `app/ml/` directory.

## LLM Integration

The RAG system uses:

- **LLM**: Ollama Llama 3.1
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **Documents**: FAQ, delivery rules, refund policies

## Frontend

A Streamlit-based demo interface is available in the `frontend/` directory, providing:

- ETA prediction form
- RAG chatbot interface
- Rider AI assistant
- Live map demo

## Development

### Running Tests

```bash
# Backend integration tests
python backend/test_integration.py
```

### Code Quality

- Follow PEP 8 style guidelines
- Use type hints
- Add docstrings to functions

## Deployment

### Production Considerations

- Set `DEBUG=False` in configuration
- Use environment variables for secrets
- Set up proper logging
- Configure CORS appropriately
- Use a production WSGI server (gunicorn)
- Set up database connection pooling
- Implement proper error handling

### Docker Deployment (Example)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper tests
4. Submit a pull request

## License

[Add license information here]

## Contact

[Add contact information here]
