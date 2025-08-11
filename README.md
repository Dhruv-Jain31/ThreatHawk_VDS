# ThreatHawk - Vulnerability Assessment Scanner

Threat Hawk – Vulnerability Assessment Scanner is an open-source, security tool designed to identify and report vulnerabilities in both web applications and network environments. It combines the capabilities of existing tools like OWASP ZAP and Nmap while introducing enhanced features such as custom vulnerability modules, BFS-based crawling, and pattern matching using the Boyer-Moore algorithm. Built for scalability and ease of use, the scanner leverages modern architectures (Node.js + Flask) and asynchronous task processing via queues to ensure efficient and parallel vulnerability detection. Its modular design supports integration with containerized environments like Kubernetes and OpenStack, enabling flexible deployment across diverse infrastructures.
Threat Hawk empowers individuals, startups, and enterprises to proactively detect and mitigate security flaws, contributing to a safer digital ecosystem.

---

# Main Objective

To develop a high-performance, cloud-native vulnerability scanner that:
Recognizes security threats in web applications and networks
Creates detailed security reports with risk classification and remediation steps
This tool will help organizations anticipate and fix vulnerabilities efficiently, offering a scalable, affordable, and open-source solution.

## 📁 Project Structure

```
ThreatHawk-Vulnerability-Assessment-Scanner/
├── scanner/                 # Flask-based vulnerability scanner
├── prisma/                  # Prisma schema and DB setup
├── frontend/                # Next.js + Tailwind frontend
├── app/                     # Node.js backend APIs
├── package.json             # Backend dependencies
└── README.md                # Project documentation
```

---

##  Getting Started

### 🔧 Prerequisites

- Python 3.8+
- Node.js (v16+)
- npm
- PostgreSQL (local or hosted on Web)
- [Prisma](https://www.prisma.io/docs/getting-started)

---

## ⚙️ Backend - Flask Scanner (`scanner/`)

1. **Navigate to the scanner directory**

   ```bash
   cd scanner
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Start the Flask server**

   ```bash
   python app/main.py
   ```

---

## 🔌 Backend - Node.js + Prisma API

1. **Navigate to the project root**

   ```bash
   cd ThreatHawk-Vulnerability-Assessment-Scanner
   ```

2. **Generate Prisma Client**

   ```bash
   npx prisma generate
   ```

3. **Build the backend**

   ```bash
   npm run build
   ```

4. **Start the backend in development mode**

   ```bash
   npm run dev
   ```

---

## 🖥️ Frontend - Next.js + Tailwind

1. **Navigate to the project root (if not already)**

   ```bash
   cd ThreatHawk-Vulnerability-Assessment-Scanner
   ```

2. **Start the frontend**

   ```bash
   npm run dev
   ```

3. **Access the UI**

   Open your browser and navigate to:  
   [http://localhost:3000](http://localhost:3000)

---

## 🔍 Features

- ✅ Scan websites for vulnerabilities using OWASP, Nmap, etc.
- 📊 View scan results in a modern, responsive dashboard
- 📂 Store and retrieve scan data
- 🧠 Supports multiple scan types with real-time feedback
- 🧾 Exportable reports and severity-based visualization

---

## 🛠️ Technologies Used

- **Frontend:** Next.js, Tailwind CSS, React
- **Backend (API):** Node.js, Express.js, Prisma
- **Scanner:** Flask, Python
- **Database:** PostgreSQL(via Prisma ORM)
- **Other:** Docker (for containerisation), Postman (for API testing)

---

## 📌 Todo / Coming Soon
- [ ] Role-based dashboards (admin/user)
- [ ] Scan history & scheduling
- [ ] Export scan reports (PDF)
- [ ] Docker support for deployment

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---
