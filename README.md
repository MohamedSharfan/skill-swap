# Skill Swap Web App

#### Video Demo: https://youtu.be/ceaK0Ow-ti4?si=tMIblvMP780ROjW6

#### Description:

**Skill Swap** is a web application built for the CS50 final project. It aims to connect individuals who are interested in learning new skills by allowing them to **match with others who possess those skills** and are willing to teach or exchange them.

---

### 🔍 What It Does

The platform allows users to:

- **Create an account and log in securely**
- **List the skills they have** and the **skills they want to learn**
- **Get matched** with users who can teach them, and who want to learn what they know
- **Chat** and **video call** with matched users using an integrated API

---

### 🛠 Technologies Used

- **Python & Flask** – Backend web framework
- **SQLite** – Lightweight relational database for user data and matches
- **HTML, CSS, JavaScript** – Frontend
- **Flask-Session** – For session handling and login persistence
- **Jitsi Meet API** – For live video chat and meetings
- **Jinja2 Templating** – To render dynamic pages based on user data

---

### 📦 Features in Detail

- **Authentication**: Secure signup and login with password hashing using `werkzeug.security`.
- **Matching Algorithm**: Matches users based on overlapping “teach” and “learn” preferences.
- **Chat Room**: Custom chat interface for each match, implemented via Flask routes and template rendering.
- **Video Calls**: Integrated Jitsi API allows real-time video communication directly from the platform.
- **Responsive Design**: Uses media queries to ensure usability across phones, tablets, and desktops.

---

### 🚀 How It Works

1. Users register with their basic details and select skills they know and want to learn.
2. A matching system pairs them with compatible users.
3. Once matched, users can view a **dedicated chat room**.
4. A button in the chat window lets users start a **video call session** with Jitsi Meet.
5. All data is stored securely in an SQLite database (`skill_swap.db`).

---

### 🧪 Challenges Faced

- Creating a clean user interface with responsive design.
- Integrating third-party APIs like Jitsi in a simple, seamless way.
- Designing the database schema to handle many-to-many skill relationships efficiently.

---

### 🌟 Future Improvements

- Integrate OAuth login with Google or GitHub.
- Add real-time chat via WebSockets (e.g., using Flask-SocketIO).
- Enable user rating and reviews after a skill session.
- Include calendar scheduling and reminders for sessions.

---

### 💡 Inspiration

This project was inspired by the idea that **everyone has something to teach and something to learn**. It builds on the growing demand for peer-to-peer learning and creates a digital space for community-driven skill development.

---

Thank you for checking out my project!
