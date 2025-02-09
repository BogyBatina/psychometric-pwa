# 🧠 Psychometric Testing PWA

## 📌 Project Overview
**Psychometric Testing PWA** is a modular, scalable web application built using **Django (backend) and Next.js (frontend)** for administering and analyzing **psychometric tests**. The project supports **AI-powered interpretation** and **adaptive testing (IRT)**, allowing users to receive personalized feedback while maintaining full control over data privacy.

## 🚀 Features
✅ **Modular Design** - Easily expandable test collection  
✅ **Standalone & AI-Powered Interpretations** - Users can choose AI-based insights  
✅ **Classical & Adaptive Testing** - Supports standard and AI-driven assessments  
✅ **Multilingual Support** - Starting with IPIP translations, including Serbian  
✅ **Role-Based Access Control (RBAC)** - Multi-tiered user permissions (User, Researcher, Admin)  
✅ **User Feedback Integration** - AI refines tests based on responses  
✅ **Deployed as a Progressive Web App (PWA)**  

## 🏗️ Tech Stack
### **Backend**
- Django REST Framework (DRF) - API and authentication  
- PostgreSQL - Structured psychometric data storage  
- Redis - Caching and task queues  
- Flask - AI-based psychometric interpretation  

### **Frontend**
- Next.js (React) - Dynamic, modern frontend  
- TailwindCSS - Prebuilt UI components  
- TypeScript - Scalability and type safety  

### **Deployment**
- **Backend**: Render (Free Hosting)  
- **Frontend**: Vercel (Next.js Deployment)  
- **Database**: Supabase (PostgreSQL)  

## 🔥 Installation & Setup
### **1️⃣ Clone Repository**
```bash
git clone https://github.com/BogyBatina/psychometric-pwa.git
cd psychometric-pwa
2️⃣ Backend Setup (Django)
bash
Copy
Edit
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
3️⃣ Frontend Setup (Next.js)
bash
Copy
Edit
cd ../frontend
npm install
npm run dev
App will run at http://localhost:3000/

🌍 Deployment
Backend: Deployed on Render
Frontend: Hosted on Vercel
Database: PostgreSQL via Supabase
🤖 AI-Powered Features (Upcoming)
Adaptive Testing (IRT)
AI-Generated Personality Reports
Benchmarking AI Personality Constructs
User Feedback-Driven Test Refinements
🎯 Roadmap
 Initial Django & Next.js Setup
 Classic Reporting MVP
 AI-Powered Interpretation
 Adaptive Testing Implementation
 Research & AI Validation
🛠 Contributing
Fork the repo
Create a feature branch
bash
Copy
Edit
git checkout -b feature/new-feature
Commit and push
bash
Copy
Edit
git add .
git commit -m "Added new feature"
git push origin feature/new-feature
Create a Pull Request (PR)
🔐 License
This project is open-source under the MIT License.

✉️ Contact
For questions, contact BogyBatina on GitHub.