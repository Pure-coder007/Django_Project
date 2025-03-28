# Django_Project


## **📌 Project Title: AI-Powered Content Recommendation API**

### **📚 Overview**
This project is a Django-based API that provides:
- **User authentication** using JWT.
- **Content management** with CRUD operations.
- **Subscription plans** (monthly, quarterly, bi-yearly, yearly).
- **User behavior tracking** for better recommendations.
- **AI-powered content recommendations** based on user interactions.
- **Optimized database performance** with caching and indexing.
- **Asynchronous processing** using Celery or Django Channels.

---

## **🛠️ Features**
### **Part 1: API Development**
💪 **User Authentication**  
- JWT-based authentication for secure login and registration.  

💪 **Content Management**  
- CRUD operations for content (title, description, category, tags, AI relevance score).  

💪 **Subscription Plans**  
- Users can subscribe to different plans (monthly, quarterly, bi-yearly, yearly).  
- Auto-renewal feature for seamless user experience.

### **Part 2: Recommendation Engine (AI Logic)**
💪 **Behavior Tracking**  
- Track user interactions (viewed, liked, skipped).  
- Efficient data storage for recommendation calculations.

💪 **Recommendation API**  
- Returns **5 recommended content pieces** based on user history & AI scores.  
- Optimized for handling large datasets efficiently.

### **Part 3: Performance Optimization**
💪 **Database Optimization**  
- Indexing for faster queries.  
- Redis caching to reduce repeated database queries.  

💪 **Asynchronous Processing**  
- **Celery/Django Channels** for background tasks like AI-based recommendations.

---

## **🚀 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone 
cd ai-content-api
```

### **2️⃣ Create a Virtual Environment & Activate**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the project root:
```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
REDIS_URL=redis://localhost:6379/0
```

### **5️⃣ Apply Migrations**
```bash
python manage.py migrate
```

### **6️⃣ Create a Superuser**
```bash
python manage.py createsuperuser
```

### **7️⃣ Run the Development Server**
```bash
python manage.py runserver
```

---

## **🛠️ API Endpoints**
| Method | Endpoint | Description |
|--------|---------|------------|
| **POST** | `/api/auth/register/` | Register a new user |
| **POST** | `/api/auth/login/` | User login & JWT authentication |
| **GET** | `/api/content/` | Get all content |
| **POST** | `/api/content/` | Create new content (Admin only) |
| **GET** | `/api/content/{id}/` | Retrieve a single content item |
| **PUT** | `/api/content/{id}/` | Update content (Admin only) |
| **DELETE** | `/api/content/{id}/` | Delete content (Admin only) |
| **POST** | `/api/subscriptions/` | Subscribe to a plan |
| **GET** | `/api/recommendations/` | Get AI-powered content recommendations |

---

## **📝 Technologies Used**
- **Django Rest Framework (DRF)** – For building REST APIs.
- **PostgreSQL** – As the database.
- **Redis** – For caching and optimization.
- **Celery** – For background tasks.
- **JWT Authentication** – For secure user login.
- **AI Logic** – For personalized recommendations.

---

## **🖥️ Running Celery for Background Tasks**
Start the Celery worker:
```bash
celery -A project_name worker --loglevel=info
```

---

## **👈 Future Improvements**
- Advanced machine learning for better recommendations.
- WebSockets for real-time notifications.
- Multi-language content recommendations.

---

## **📜 License**
This project is licensed under the **MIT License**.

---

## **📲 Support**
For any issues or feature requests, please create an **issue** in the repository or contact the maintainer.

