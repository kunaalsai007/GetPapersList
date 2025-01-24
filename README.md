# **PubMed Research Paper Fetcher**

## **Overview**
This project fetches research papers from PubMed based on a user-specified query and identifies authors affiliated with non-academic institutions (e.g., pharmaceutical or biotech companies). The results are saved to a CSV file or displayed in the console.

---

## **Features**
1. Fetch research papers using PubMed's API.
2. Identify non-academic authors using heuristic-based methods.
3. Export results to a CSV file.
4. Simple command-line interface for execution.

---

## **Code Organization**

### **Directory Structure**
```
.
├── fetcher.py             # Module for fetching and processing PubMed data
├── cli.py                 # Command-line interface script
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── output.csv             # Example output file (if generated)
```

### **Files and Purpose**
1. **`fetcher.py`**:
   - Core logic for interacting with PubMed, parsing results, identifying non-academic authors, and exporting to CSV.
2. **`cli.py`**:
   - Command-line interface to accept user queries, configure options, and execute the program.
3. **`requirements.txt`**:
   - List of Python dependencies for easy installation.
4. **`README.md`**:
   - Documentation for the project.

---

## **Installation Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/pubmed-fetcher.git
cd pubmed-fetcher
```

### **2. Set Up Python Environment**
- Install Python 3.8 or later from [Python.org](https://www.python.org/).
- (Optional) Create a virtual environment:
  ```bash
  python -m venv env
  source env/bin/activate  # For Linux/Mac
  env\Scripts\activate     # For Windows
  ```

### **3. Install Dependencies**
- Install required libraries using `pip`:
  ```bash
  pip install -r requirements.txt
  ```

### **4. Set Up Entrez Email**
- Open `fetcher.py` and replace the placeholder `your_email@example.com` with your email address in the following line:
  ```python
  Entrez.email = "your_email@example.com"
  ```

---

## **Usage Instructions**

### **Run the Program**
Execute the command-line script with your query:
```bash
python cli.py "COVID-19 vaccine" --file output.csv --max_results 10 --debug
```

### **Command-Line Options**
| Option           | Description                                                                                       |
|------------------|---------------------------------------------------------------------------------------------------|
| `query`          | (Required) Search query for PubMed.                                                              |
| `-f, --file`     | (Optional) Specify the filename to save the results as a CSV. Default: Print results to console.  |
| `-d, --debug`    | (Optional) Enable debug mode to print execution details.                                         |
| `-m, --max_results` | (Optional) Specify the maximum number of results to fetch. Default: 10.                         |
| `-h, --help`     | Show help message and usage instructions.                                                        |

---

## **Example Output**

### **Command**
```bash
python cli.py "COVID-19 vaccine" --file output.csv --max_results 5 --debug
```

### **Result**
Generated `output.csv` file:

| PubmedID | Title                                | PublicationDate | Non-academic Authors       | Affiliation                         |  
|----------|--------------------------------------|----------------|----------------------------|-------------------------------------|  
| 12345678 | The Role of Vaccines in COVID-19    | 2023           | Dr. John Doe, Pfizer Inc.  | Pfizer Inc., New York, USA         |  
| 87654321 | Advances in Biotech and Vaccines    | 2022           | Jane Smith, Biotech Corp.  | Biotech Corp., Cambridge, USA      |  

---

## **Dependencies**
- **BioPython**: Library for interacting with PubMed.  
  - [Documentation](https://biopython.org/)
- **Python**: Version 3.8 or later.  
  - [Python Download](https://www.python.org/downloads/)

---

## **Tools Used**
1. **BioPython**:
   - Used to fetch and parse PubMed data.
   - [Learn More](https://biopython.org/)
2. **Heuristic-Based Filtering**:
   - Identifies non-academic authors using keywords and email patterns.
3. **Python Libraries**:
   - `csv` for writing results to CSV files.
   - `argparse` for command-line options.
   - `logging` for debug mode.

---

## **Limitations**
1. Relies on heuristic rules for classifying non-academic affiliations, which might miss certain cases.
2. Requires a valid Entrez email for PubMed API.

---

## **Future Enhancements**
1. Integrate Machine Learning models to classify affiliations more accurately.
2. Extend the tool to fetch data from additional scientific databases.
3. Build a web-based interface for broader accessibility.

