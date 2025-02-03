# Health Check

This project is a **Health Check Monitoring Tool** that continuously monitors HTTP endpoints defined in a YAML configuration file. It logs the availability of each endpoint and calculates the **availability percentage** for each domain over the lifetime of the program.

---

- [Health Check](#health-check)
    - [Features](#features)
  - [Project Structure](#project-structure)
  - [Setup Instructions](#setup-instructions)
    - [1️⃣ Clone the Repository](#1️⃣-clone-the-repository)
    - [2️⃣ Create and Activate a Virtual Environment (Optional but Recommended)](#2️⃣-create-and-activate-a-virtual-environment-optional-but-recommended)
    - [3️⃣ Install Dependencies](#3️⃣-install-dependencies)
    - [4️⃣ Setup Python Modules](#4️⃣-setup-python-modules)
  - [Running the Program](#running-the-program)
    - [🔹 Running Health Check Monitoring](#-running-health-check-monitoring)
    - [🔹 Sample Output](#-sample-output)
  - [Running Tests](#running-tests)
  - [Implementation Details](#implementation-details)
    - [🔹 `health_check.py`](#-health_checkpy)
    - [🔹 `logger.py`](#-loggerpy)
  - [Example YAML Configuration](#example-yaml-configuration)
  - [License](#license)
  - [Contributing](#contributing)
    - [📧 Contact](#-contact)

---

### Features
- Reads a **YAML configuration file** that specifies multiple HTTP endpoints.
- Periodically (every **15 seconds**) sends requests to the endpoints.
- Determines if an endpoint is **UP** or **DOWN** based on response status and latency.
- Logs domain availability percentages in real-time.
- Graceful exit when the user manually stops execution.

---

## Project Structure

```
health-check-monitoring/
│── configs/
│   ├── sample_config.yaml      # Sample configuration file
│   ├── ...
| 
│── src/
│   ├── __init__.py             # Marks src as a package
│   ├── health_check.py         # Main monitoring script
│   ├── logger.py               # Handles logging of availability percentages
│
│── tests/
│   ├── test_health_check.py    # Unit tests for health_check.py
│   ├── test_logger.py          # Unit tests for logger.py
│
│── requirements.txt            # Required dependencies
│── README.md                   # Project documentation
│── .gitignore                  # Ignore unnecessary files
```

---

## Setup Instructions

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/health-check-monitoring.git
cd health-check-monitoring
```

### 2️⃣ Create and Activate a Virtual Environment (Optional but Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Setup Python Modules
```sh
python3 setup.py install
```

---

## Running the Program

### 🔹 Running Health Check Monitoring
To run the health check monitoring tool, provide a valid **YAML configuration file** as an argument:
```sh
python src/health_check.py configs/sample_config.yaml
```
The tool will start monitoring the endpoints and will log **availability percentages** every 15 seconds.

### 🔹 Sample Output
```
fetch.com has 33% availability percentage
www.fetchrewards.com has 100% availability percentage
fetch.com has 67% availability percentage
www.fetchrewards.com has 50% availability percentage
```
Press **CTRL + C** to stop the program.

---

## Running Tests
This project uses **pytest** for unit testing. To run the tests, execute:
```sh
pytest tests/
```
This will run all tests and generate a **code coverage report**.

---

## Implementation Details

### 🔹 `health_check.py`
- **Loads the YAML configuration file** containing endpoint details.
- **Sends periodic HTTP requests** (every 15 seconds) to each endpoint.
- **Determines UP/DOWN status** based on response status and latency.
- **Logs availability percentages** using `logger.py`.

### 🔹 `logger.py`
- Maintains a **record of total checks** per domain.
- Tracks **successful UP checks** and **computes availability percentages**.
- Logs results to the console after every monitoring cycle.

---

## Example YAML Configuration
A valid YAML configuration file should follow this structure:
```yaml
- name: "Fetch Index Page"
  url: "https://fetch.com"
  method: "GET"

- name: "Fetch Careers Page"
  url: "https://fetch.com/careers"
  method: "GET"

- name: "Fetch Rewards API"
  url: "https://www.fetchrewards.com/api"
  method: "POST"
  headers:
    Content-Type: "application/json"
  body: '{"query": "rewards"}'
```

---

## License
This project is open-source and available under the **MIT License**.

---

## Contributing
Contributions are welcome! Feel free to submit **issues** or **pull requests** to improve the tool.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes and commit: `git commit -m "Added new feature"`
4. Push your branch: `git push origin feature-branch`
5. Open a Pull Request 🚀

---

### 📧 Contact
For any questions or issues, feel free to reach out!
*masonware15@gmail.com*
