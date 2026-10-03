# Sonu Sharma — QA Analyst & Test Automation Portfolio

A modern, high-performance developer portfolio and QA automation showcase engineered with responsive design, dynamic typography, interactive CLI terminal, and smooth micro-animations.

---

## 🌟 Highlights & Features

- **Interactive Terminal Emulator (`⌘K`)**: Built-in interactive CLI supporting commands (`help`, `me`, `skills`, `experience`, `projects`, `clear`).
- **Dynamic Physics & Canvas Background**: Subtle floating node graph and particle mesh responding to cursor physics.
- **Defect Lifecycle & Experience Timeline**: Interactive commit-graph view detailing roles at **Sterling Wells Services** (FigsFlow TMS & Client Portal), Brahmabyte Lab (Chatboq.com), Heal Home Care, and Freelancer Unit.
- **Project Showcases**: Live breakdowns of test automation frameworks, SaaS QA suites, smart contracts, and full-stack systems.
- **REST API Endpoints**: Self-hosted mock API endpoints (`/api/v1/me`, `/api/v1/skills`, `/api/v1/experience`, `/api/v1/projects`).
- **Live Visitor Guestbook (`tail -f visitors.log`)**: Real-time interactive visitor messages.
- **Automated Test Suite**: Integrated Selenium WebDriver UI and API contract test suite (`tests/test_portfolio.py`).

---

## 🛠️ Tech Stack

- **Frontend Architecture**: Modern HTML5 / Next.js Server Components snapshot / Vanilla CSS tokens
- **Styling**: Tailored Dark Ink theme (`--accent: #c6f432`, `--accent-2: #ff5a36`), glassmorphism, responsive grid
- **Typography**: Custom variable fonts (*Bricolage Grotesque*, *JetBrains Mono*, *Instrument Serif*)
- **Test Automation**: Python, Selenium WebDriver, Playwright, Pytest (Page Object Model)
- **Defect Tracking**: Microsoft Azure Boards, ClickUp, Jira
- **API Testing**: Postman, Python `requests`, RESTful APIs
- **Backend & Serving**: Python HTTP Server with REST routing & CORS support

---

## 🚀 Quick Start

### 1. Run Locally

To launch the portfolio locally on port `3000`:

```bash
# Using Python
python server.py

# Or using npm
npm start
```

Open your browser and navigate to:
```
http://localhost:3000/
```

### 2. Run Automated QA Tests

Execute the Selenium automation test suite against the running server:

```bash
python -m unittest tests/test_portfolio.py
```

Or using Pytest:
```bash
pytest tests/ -v
```

---

## 📁 Project Structure

```
portfolio/
├── _next/                # Optimized static CSS, JS chunks & WOFF2 font bundles
├── api_data/             # REST API response payloads (me, skills, experience, projects)
├── media/                # Images, profile assets & avatars
├── tests/                # Automated QA test suite (Selenium & unittest)
│   ├── __init__.py
│   └── test_portfolio.py
├── .gitignore            # Git ignore configuration
├── favicon.svg           # Vector favicon
├── index.html            # Core HTML application bundle
├── package.json          # Node project manifest & scripts
├── portfolio_content.json# Master portfolio data schema
├── README.md             # Project documentation
└── server.py             # Python HTTP dev & production server
```

---

## 📬 Contact & Links

- **Name**: Sonu Sharma
- **Role**: QA Analyst & Test Automation Engineer
- **Current Company**: Sterling Wells Services
- **Location**: Chabahil, Kathmandu, Nepal
- **Email**: [sonushar059@gmail.com](mailto:sonushar059@gmail.com)
- **Phone**: [+977 9860476428](tel:+9779860476428)
- **GitHub**: [github.com/SonuSharma2](https://github.com/SonuSharma2)
