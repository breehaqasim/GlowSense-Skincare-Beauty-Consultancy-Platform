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

## 🛠️ Technology Stack  

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
| Database           | Supabase         |  


---

## 🚀 System Features  

### **User Features**  
✅ Profile creation with skin type analysis  
✅ Expert matching algorithm   
✅ Product recommendation engine *(skincare only)*  
✅ Trending makeup product listings  

---

## 🔧 Installation  

### Prerequisites  
- Python 3.8+  
- MySQL/MongoDB  
- Node.js (for frontend testing)  

### Backend Setup Instructions

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd GlowSense-Skincare-Beauty-Consultancy-Platform
```

2. Navigate to the backend directory:
```bash
cd backend
```

3. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
   - Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and add your Supabase credentials:
     - Get your Supabase URL and anon key from your Supabase project settings
     - Replace the placeholder values in `.env`

6. Run the application:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

#### Environment Variables
- `SECRET_KEY`: Flask secret key for session management
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon/public key

#### Database Setup
The application uses Supabase as the backend database. No local database setup is required.

#### API Documentation
The API endpoints are documented in the API Definition Document in the Documentations folder.

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

Full API documentation is available in `Documentations/API Definition Document.pdf`.


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

Refer to Testing Strategy documentation for the complete test plan available in `Documentations/Testing Strategy.pdf`.

## 🎨 Interface Design 
#### **Login Page**
![Login Page](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/public/login%20page.png)

#### **Sign Up Page**
![Sign Up Page](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/public/sign%20up%20page.png)

Complete High Fidelity Prototype is available in `Documentations/GlowSense - High Fidelity Prototype.pdf`.

<!--#### **Home Page**
![Home Page](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/public/home%20page.png)

#### **Skincare Page**
![Skincare Page](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/public/Skincare.jpeg)

#### **Skincare Concern Form**
![Skincare Concern Form](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/public/Skincare%20Concern%20Form.png)

#### **Booking Consultation Form**
![Booking Consultation Form](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/public/Booking%20Consultation.png)

#### **Makeup Products Page**
![Makeup Products Page](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/public/Makeup.jpeg)

#### **Contact Us Page**
![Contact Us Page](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/public/Contact%20Us.jpeg)-->


## 📄 Documentation
* [**Software Architecture**](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/Documentations/Software%20Architecture%20Document.pdf)
* [**API Definition Document**](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/Documentations/API%20Definition%20Document.pdf)
* [**Specification Document**](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/Documentations/Specification_Document.pdf)
* [**Testing Strategy**](https://github.com/breehaqasim/GlowSense-Skincare-Beauty-Consultancy-Platform/blob/main/Documentations/Test%20Strategy.pdf)

## 📬 Contact
**Team Member 1**: Breeha Qasim  **Email**: bq08283@habib.edu.pk  

**Team Member 2**: Namel Shahid 
**Email**: ns08327@habib.edu.pk  

**Team Member 3**: Ashbah Faisal 
**Email**: af08271@habib.edu.pk  

**Team Member 4**: Rameez Wasif 
**Email**: rw08479@habib.edu.pk  

**Institution**: Habib University, Karachi
