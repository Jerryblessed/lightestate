# LightEstate 

🚀 **LightEstate** is a smart application that enhances property management, agreements and learning about real estate through an easy-to-use, efficient, and intelligent interface. Experience seamless control with cutting-edge DocuSign API integration and automation! 

## 🎥 Live Demo

Check out the live demo of the application in action: [Watch on YouTube](https://youtu.be/pvZPDkFuDW8)

🌐 Try the live application here: [LightEstate on Render](https://lightestate.onrender.com/)

---

## 🏗️ Architectural Diagram

The architectural structure of the LightEstate application is illustrated below:

![Architectural Diagram](https://github.com/Jerryblessed/lightestate/blob/main/app/static/assets/diagram-export-1-27-2025-10_46_46-AM.png?raw=true)

---

## ⚡ Features

### What It Does

LightEstate is an AI-powered web application that simplifies and automates real estate agreement management. Here’s what it offers:

- **✍️ Streamlined Signing**: Enables users to sign agreements themselves or send agreements to multiple parties seamlessly through DocuSign APIs.
- **📄 Document Generation with AI**: Users can generate customized real estate agreements using Azure AI's GPT-4o model, ensuring speed and accuracy.
- **🔒 Multifactor Authentication**: Ensures security by requiring phone authentication for recipients via Docusign API.
- **📊 Data Insights**: Unlocks critical insights from agreements by using AI to extract renewal dates, terms, and conditions, helping users make better decisions.
- **🤖 Conversational AI**: Offers an avatar-based AI assistant powered by Azure Cognitive Services, allowing users to interact conversationally for agreement-related queries and tasks.

---

## 🛠️ How to Run the Application

Follow these steps to get started with LightEstate:

### Option 1: Run via Docker

1. Ensure Docker is installed on your system. [Install Docker](https://docs.docker.com/get-docker/)
2. Clone the repository:
   ```bash
   git clone https://github.com/Jerryblessed/lightestate.git
   ```
3. Navigate to the project directory:
   ```bash
   cd lightestate
   ```
4. Build and run the Docker container:
   ```bash
   docker build -t lightestate .
   docker run -p 3000:3000 lightestate
   ```
5. Open your browser and navigate to `http://localhost:3000`.

### Option 2: Run Locally with `run.py`

1. Ensure you have Python 3 installed. [Install Python](https://www.python.org/downloads/)
2. Clone the repository:
   ```bash
   git clone https://github.com/Jerryblessed/lightestate.git
   ```
3. Navigate to the project directory:
   ```bash
   cd lightestate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python run.py
   ```
6. Open your browser and navigate to `http://localhost:3000`.

---

## 🌟 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker
- **IoT Integration**: Smart devices and automation protocols
- **AI**: Azure AI GPT-4o, Azure Cognitive Services, and DocuSign APIs

---

## 🤝 Contributing

We welcome contributions to make LightEstate even better! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💬 Feedback and Support

If you have any feedback, suggestions, or issues, please feel free to reach out by creating an issue in the repository or contacting us directly.

Happy coding! ✨