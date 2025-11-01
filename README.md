# fastapi-unsubscription-service
📨 FastAPI Unsubscription Management Service

A robust backend service built with **FastAPI** and **PostgreSQL** to handle user unsubscriptions efficiently.
This project enables businesses to manage email or service subscriptions, track analytics, and provide transparency for both users and administrators.

---

## 🚀 Features

* ✅ **User Unsubscription API** – Allows users to unsubscribe with reasons.
* 👤 **Admin Dashboard APIs** – Retrieve unsubscribed users, view analytics, and search/filter records.
* 📊 **Analytics Module** – Displays insights on unsubscribe trends and user activity.
* 🧩 **Database Integration** – Powered by PostgreSQL with SQLAlchemy ORM.
* 🧾 **Logging & Exception Handling** – Structured logs and custom exception handling for reliability.
* 🧪 **Unit Tests** – Includes `pytest` test cases to ensure functionality.
* ✨ **Code Quality** – Follows `Flake8` formatting and naming conventions.
* 📘 **Interactive API Docs** – Auto-generated Swagger UI and ReDoc documentation.

---

## 🏗️ Project Structure

```
unsubscription_service/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   │   ├── users.py
│   │   └── owners.py
│   ├── database.py
│   ├── schemas.py
│   ├── utils/
│   │   ├── logger.py
│   │   └── exceptions.py
├── tests/
│   ├── test_users.py
│   └── test_owners.py
├── requirements.txt
├── .flake8
├── README.md
└── LICENSE
```

---

## ⚙️ Tech Stack

| Component  | Technology                  |
| ---------- | --------------------------- |
| Framework  | FastAPI                     |
| Database   | PostgreSQL                  |
| ORM        | SQLAlchemy                  |
| Testing    | Pytest                      |
| Linting    | Flake8                      |
| Docs       | Swagger / ReDoc             |
| Deployment | Uvicorn / Docker (optional) |

---

## 🧭 API Endpoints Overview

| Method | Endpoint              | Description                    |
| ------ | --------------------- | ------------------------------ |
| `POST` | `/unsubscribe`        | Unsubscribe a user             |
| `GET`  | `/status/{email}`     | Check user subscription status |
| `GET`  | `/admin/unsubscribed` | List all unsubscribed users    |
| `GET`  | `/admin/analytics`    | View unsubscribe analytics     |
| `GET`  | `/admin/search`       | Search users by email/date     |

---

## 🧩 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/fastapi-unsubscription-service.git
cd fastapi-unsubscription-service
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://username:password@localhost:5432/unsub_db
```

### 5️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

Now visit **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** for the Swagger UI.

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📊 Future Enhancements

* Add email notifications for unsubscribe confirmations
* Integrate dashboards using Streamlit or React
* Include role-based authentication for admin access

---

## 🧑‍💻 Author

**Yanamala Akhil Kumar Reddy**
🎓 B.Tech – Computer Science & Engineering
🏫 Annamacharya Institute of Technology & Sciences, Rajampet
📧 [akhi4uy@gmail.com](mailto:akhi4uy@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/akhilkumarreddyyanamala) 

---


