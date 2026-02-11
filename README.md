# WIT Beyond Binary Project Setup

## Environment Setup

After cloning the repository, you need to set up your environment files:

### Backend Setup

1. Navigate to the `backend/` directory
2. Copy the sample environment file:
   ```bash
   cp env.sample .env
   ```
3. Edit `.env` with your configuration:
   - `MONGO_URI`: Your MongoDB connection string
   - `JWT_SECRET_KEY`: A secure random string for JWT tokens

### Frontend Setup

1. Navigate to the `frontend-lynx/` directory
2. Copy the sample environment file:
   ```bash
   cp env.sample .env
   ```
3. Edit `.env` with your configuration:
   - `EXPO_PUBLIC_API_BASE_URL`: Your backend API URL
   - `REACT_APP_API_BASE_URL`: Fallback API URL

## Running the Application

### Backend

```bash
cd backend
python app.py
```

### Frontend

```bash
cd frontend-lynx
npm install
npm start
```

## Important Notes

- Never commit your actual `.env` files to Git (they contain sensitive information)
- Always use the `.env.sample` files as templates
- Each developer should have their own `.env` files with their specific configurations
