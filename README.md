# SASTRA Timetable Generation
[![CodeQL Advanced](https://github.com/SASTRA-Projects/SASTRA/actions/workflows/codeql.yml/badge.svg)](https://github.com/SASTRA-Projects/SASTRA/actions/workflows/codeql.yml)
[![Flask Health Check](https://github.com/SASTRA-Projects/SASTRA/actions/workflows/test-app.yml/badge.svg)](https://github.com/SASTRA-Projects/SASTRA/actions/workflows/test-app.yml)
## 📘 Project Overview

The **SASTRA Timetable Generation System** is an initiative to automate the complex process of class scheduling at [`SASTRA DEEMED To Be University`](https://www.sastra.edu). This system leverages modern technologies to create conflict-free timetables, reducing manual work and enhancing efficiency.

Despite being a leader in technological adoption, SASTRA has managed timetables manually — at least until **January 2025**. This project addresses that gap by automating the timetable generation process using a well-structured database and an intelligent scheduling algorithm.


## 🚀 Features

- **Automated Timetable Generation:** Dynamically generates schedules without time or venue clashes.
- **Conflict Resolution:** Ensures no overlap of classes for faculty or students.
- **Flexible Design:** Supports elective courses, multiple sections, and variable room capacities.
- **User-Friendly Interface:** Built with a responsive front end for easy interaction.
- **Real-Time Updates:** Updates schedules instantly upon data changes.


## 🛠️ Tools & Technologies Used

- **Backend:** [Flask](https://flask.palletsprojects.com/en/stable/) (Python)
- **Frontend:** [HTML](https://html.com/), [CSS](https://css3.com/), [JavaScript](https://www.javascript.com/)
- **Database:** [MySQL](https://www.mysql.com/)
- **Visualization:** [Mermaid.js](https://mermaid-js.github.io/) for ER diagrams


## 🎯 Project Mission

At SASTRA, the pursuit of academic excellence has always been supported by innovation. This project aligns with that legacy by removing the burden of manual timetable calculation. 

The goal is simple: **Let people focus on teaching and learning — not on figuring out class schedules.**

Through precise rule enforcement, the system prevents common scheduling issues, like:

- Double-booked rooms or faculties
- Elective clashes across sections
- Invalid class-to-stream/course mappings


## 🏗️ Database & Schema Design

The database is meticulously designed with normalized tables, optimized queries, and robust constraints. Key components include:

- **Campus, Schools, Departments** for organizing physical locations
- **Sections, Streams, Programmes, Courses** for curriculum management
- **Faculty, Students, Classes** for mapping human and infrastructure resources

Triggers, stored procedures, and functions enforce data integrity, while the system architecture supports easy scalability.


## ⚡ Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [MySQL Client](https://dev.mysql.com/downloads/) (Optional)

### Installation

1. **Clone the Repository:**
```sh
  git clone https://github.com/SASTRA-Projects/SASTRA/
  cd SASTRA
```

2. **Set Up a Virtual Environment:**

- **Linux/macOS:**
```sh
  python3 -m venv venv
  source venv/bin/activate
```

- **Windows (CMD):**
```sh
  python -m venv venv
  venv\Scripts\activate
```

- **Windows (PowerShell):**
```sh
  python -m venv venv
  .\venv\Scripts\Activate.ps1
```

3. **Install Dependencies:**
```sh
  pip install -r requirements.txt
```

4. **Configure MySQL Database:**
Create a `.env` file for your DB credentials.

5. **Run the Application:**
```sh
  python app.py
```

6. **Access the Web Interface:**
Open [http://localhost:5000](http://localhost:5000) in your browser.


## 🧠 Future Scope

- **Timetable Optimization:** Prioritize faculties preferences and students convenience.
- **Room & Resource Management:** Track lab availability, equipment, etc.
- **Notifications & Alerts:** Notify users of timetable updates via email or app.
- **Analytics & Reports:** Visualize schedule patterns, faculty workloads, etc.


## 📜 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for detailed information.

Additional attribution details can be found in the [NOTICE](NOTICE) file.


## 🤝 Contributing

Contributions are welcome! Whether you want to report an issue, submit a pull request, or enhance the existing features, we’d love to have you on board.

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a collaborative and respectful environment.

1. **Fork the Repository:** Click the “Fork” button on the [GitHub page](https://github.com/your-repo/sastra-timetable).
2. **Create a Branch:**
```sh
  git checkout -b feature/your-feature-name
```
3. **Commit Your Changes:**
```sh
  git commit -m "Add your feature description"
```
4. **Push to Your Branch:**
```sh
  git push origin feature/your-feature-name
```
5. **Submit a Pull Request:** Navigate to the **Pull Requests** tab on GitHub and submit your PR.

---

Happy Coding 🚀! Let’s build something awesome together!
