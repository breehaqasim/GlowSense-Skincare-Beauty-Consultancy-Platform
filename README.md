# 💄 GlowSense - Skincare & Beauty Consultancy Platform  
Glow Sense's Skincare &amp; Beauty Consultancy Platform connects users with beauty experts for personalized skincare advice, product recommendations, and consultations. The platform offers expert matching, virtual consultations, and trending makeup products, providing a seamless experience for users seeking beauty and skincare solutions.

---

## 📌 Project Overview  
A **full-stack platform** enabling users to:  
- Receive personalized skincare recommendations  
- Book virtual consultations with dermatologists/beauty experts  
- Purchase trending makeup products *(non-personalized)*  
- Manage follow-ups and reviews  

**Developed by**: Breeha Qasim, Namel Shahid, Ashbah Faisal, Rameez Wasif  
**Institution**: Habib University  

---

## 🛠️ Tech Stack (Per Document)  

### **Frontend**  
| Component       | Technology       |  
|-----------------|------------------|  
| Core Framework  | HTML/CSS/JavaScript |  
| Styling         | Bootstrap        |  
| Responsiveness  | CSS Media Queries|  

### **Backend**  
| Component            | Technology       |  
|----------------------|------------------|  
| Server Language      | Python (Flask/Django) |  
| Performance Modules  | C++              |  
| API Framework        | RESTful API      |  

### **Infrastructure**  
| Component          | Technology       |  
|--------------------|------------------|  
| Hosting            | DigitalOcean VPS |  
| Database           | MySQL/MongoDB    |  
| Authentication     | Session-based    |  
| Payment Processing | Google Pay/Apple Pay/Cards |  

---

## 🚀 System Features  

### **User Features**  
✅ Profile creation with skin type analysis  
✅ Expert matching algorithm  
✅ Secure video consultations (WebRTC)  
✅ Product recommendation engine *(skincare only)*  
✅ Trending makeup product listings  

### **Expert Features**  
✅ Verified profile system  
✅ Consultation scheduling  
✅ Video tutorial uploads  
✅ Client messaging system  

### **Admin Features**  
✅ User/expert management dashboard  
✅ Transaction monitoring  
✅ Content moderation  

---

## 🔧 Installation  

### Prerequisites  
- Python 3.8+  
- MySQL/MongoDB  
- Node.js (for frontend testing)  

### Backend Setup  
```bash
# Clone repository
git clone https://github.com/your-repo/skincare-platform.git
cd skincare-platform/backend

# Install dependencies
pip install -r requirements.txt

# Configure database (MySQL example)
mysql -u root -p
CREATE DATABASE glowskin_db;

# Run migrations
python manage.py migrate

# Start server
python app.py
```
### Frontend Setup  
```bash
cd ../frontend

# Install dependencies (if using Node)
npm install

# Launch development server
python -m http.server 8000  # Basic HTTP server for HTML/CSS/JS
```

## 🌐 API Endpoints

(Base URL: [https://api.glowsense.com](https://api.glowsense.com))

| Endpoint                        | Method | Description                                |
|----------------------------------|--------|--------------------------------------------|
| /login                           | POST   | User authentication                       |
| /submit-skincare-concerns        | POST   | Submit skin analysis form                  |
| /match-expert                    | POST   | Get matched with professionals            |
| /schedule-consultation           | POST   | Book video consultation                    |
| /trending-makeup-products        | GET    | Browse trending products                  |

Full API documentation is available in `docs/API.md`.


## 🧪 Testing Strategy

### Unit Testing:
* **Authentication module**: Ensure that user login and registration functions correctly.
* **Expert matching algorithm**: Verify that users are matched with the right professionals based on skin concerns.

### Integration Testing:
* **Payment gateway connection**: Ensure that the payment gateway works seamlessly with the platform.
* **Video consultation workflow**: Test the scheduling, initiation, and termination of video consultations.

### Security Testing:
* **SSL encryption verification**: Ensure that all communication between the frontend and backend is encrypted using SSL.
* **Session hijacking tests**: Perform tests to ensure session management is secure and resistant to hijacking attempts.

Refer to Chapter 5.6 of the project documentation for the complete test plan.

## 📄 Documentation
* **Software Architecture**: Refer to Chapter 3 of the project documentation for an overview of the system architecture.
* **System Requirements**: See Chapters 2 & 5 for functional and non-functional requirements.
* **Deployment Guide**: Section 1.6.3 in the project documentation provides deployment instructions.

## 📜 License
MIT License - See [LICENSE](LICENSE)

## 📬 Contact
**Team Lead**: Breeha Qasim  
**Email**: breeha.qasim@habib.edu.pk  
**Institution**: Habib University, Karachi


