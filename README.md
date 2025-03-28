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
