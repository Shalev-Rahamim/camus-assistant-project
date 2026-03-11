# Setup Instructions

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Create Admin User
```bash
python -m db.create_admin admin 123456
```

### 3. Run the Backend Server
```bash
cd backend
uvicorn main:app --reload
```

The backend will run on: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- API Base URL: `http://localhost:8000/api/v1`

## Frontend Setup

### Option 1: Simple HTTP Server (Python)
```bash
cd frontend
python -m http.server 3000
```

### Option 2: Simple HTTP Server (Node.js)
```bash
cd frontend
npx http-server -p 3000
```

The frontend will run on: `http://localhost:3000`

## Quick Start

1. **Terminal 1 - Backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   python -m http.server 3000
   ```

3. **Open Browser:**
   - Frontend: `http://localhost:3000`
   - Backend API Docs: `http://localhost:8000/docs`

## Environment Variables

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=sqlite+aiosqlite:///./campus_assistant.db
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your-secret-key-change-in-production
```

## Troubleshooting

- **Port already in use?** Change the port: `uvicorn main:app --reload --port 8001`
- **CORS errors?** Make sure backend is running before frontend
- **Database errors?** Run: `python -m db.create_admin admin 123456` first
