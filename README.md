# bitebalance **Diet Analyzer Application**


## **Overview**  
The Diet Analyzer is an AI-powered dietary analysis application tailored to enhance user well-being. Designed with senior citizens in mind, the app features a user-friendly interface, gamification elements, and seamless integration with healthcare providers to deliver nutritional insights and health tracking.

---

## **Key Features**  
- **Image-Based Food Recognition**: Analyze uploaded images to derive nutritional information.  
- **Health Scoring**: Personalized health scores based on dietary patterns, aligned with the USDA’s Healthy Eating Index (HEI).  
- **Gamification**: Engaging features such as streaks, health goals, and rewards for consistent healthy habits.  
- **Doctor-Patient Interaction**: A dedicated portal for healthcare providers to monitor patients' dietary habits.  
- **Past Meal Calendar**: Track and revisit meal data for improved health management.

---
## **Core Functionality Sequence Diagram**  

![Sequence Diagram for dietary analysis](#) (./imges/Sequence-diagram.jpg)


## **Deployment Diagram**  

![AWS Cloud Architecture](#) (./images/Cloud-Architecture.jpg)   

**Key Components**:
- **Frontend**: Built with React Native for mobile platforms.  
- **Backend**: FastAPI serving as the REST API layer.  
- **AWS Services**: 
  - **ECS**: Orchestrates containerized backend services.
  - **RDS**: Manages the PostgreSQL database for storing user data.
  - **S3**: Handles secure storage of user-uploaded food images.
  - **Secrets Manager**: Protects sensitive environment variables.
- **AI Analysis**: Uses the ChatGPT API for image-based food recognition.

---

## **Getting Started**  

### **Prerequisites**  
- Docker  
- Python 3.9+  
- Node.js 16+  
- AWS CLI configured with necessary permissions  

### **Setup Instructions**  

#### 1. Clone the Repository  
```bash
git clone 
cd bitebalance
```

#### 2. Use the readme.md file for BiteBalance for the frontend and BiteBalanceBackend for the backend  


## **Deployment**  
The backend API can be accessed between (12/04/2024 to 12/30/2024), using the linke stated below:  
[http://100.24.38.89:5000/api/docs](http://100.24.38.89:5000/api/docs)

The Diet Analyzer application is deployed on AWS using the following services:  
- **Amazon ECS**: Manages containerized backend services.  
- **Amazon RDS**: PostgreSQL database for data storage.  
- **Amazon S3**: Secure storage for user-uploaded images.  
- **AWS Secrets Manager**: Safeguards sensitive environment variables.  

Refer to the deployment diagram for an overview of the system architecture.  

---

## **Future Development**  

- **Enhanced AI Capabilities**: Improve recognition accuracy and introduce personalized dietary suggestions.  
- **New Endpoints**: Add endpoints for family and doctor interaction.  
- **Expanded Gamification**: Introduce streak tracking and goal-setting features.  
- **Third-Party Integrations**: Connect with fitness trackers and meal planners.  

---