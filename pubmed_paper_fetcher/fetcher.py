import csv
import re
import logging
from typing import List, Dict
from Bio import Entrez

# Configure Entrez
Entrez.email = "kunaalsai@gmail.com"  # Replace with your email

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch papers from PubMed based on a query."""
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, retmode="xml")
        record = Entrez.read(handle)
        handle.close()
        pubmed_ids = record["IdList"]

        papers = []
        for pmid in pubmed_ids:
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
            record = handle.read()
            handle.close()
            papers.append(parse_medline_record(record))
        return papers
    except Exception as e:
        logger.error(f"Error fetching papers: {e}")
        return []

def parse_medline_record(record: str) -> Dict:
    """Parse a MEDLINE record into a dictionary."""
    paper = {}
    for line in record.split("\n"):
        if line.startswith("PMID-"):
            paper["PubmedID"] = line.split("-")[1].strip()
        elif line.startswith("TI  -"):
            paper["Title"] = line[5:].strip()
        elif line.startswith("DP  -"):
            paper["PublicationDate"] = line[5:].strip()
        elif line.startswith("AU  -"):
            paper.setdefault("Authors", []).append(line[5:].strip())
        elif line.startswith("AD  -"):
            paper["Affiliation"] = line[5:].strip()
        elif re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", line):
            email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", line)
            if email_match:
                paper["Email"] = email_match.group()
    return paper

def identify_non_academic_authors(authors: List[str], affiliations: List[str], emails: List[str]) -> List[str]:
    """Identify non-academic authors based on affiliation heuristics and email patterns."""
    non_academic_keywords = ["pharma", "biotech", "inc", "corporation", "company", "llc", "ltd"]
    academic_keywords = ["university", "college", "institute", "lab", "research center"]
    non_academic_domains = ["gmail.com", "yahoo.com", "outlook.com"]

    non_academic_authors = []

    for author, affiliation, email in zip(authors, affiliations, emails):
        # Extract domain from email
        domain = email.split("@")[-1] if "@" in email else ""
        
        # Check for non-academic keywords in the affiliation or non-academic email domains
        if any(keyword in affiliation.lower() for keyword in non_academic_keywords) or domain in non_academic_domains:
            non_academic_authors.append(author)
        # Exclude academic keywords in the affiliation
        elif not any(keyword in affiliation.lower() for keyword in academic_keywords):
            non_academic_authors.append(author)

    return non_academic_authors


def save_to_csv(papers: List[Dict], filename: str) -> None:
    """Save paper information to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["PubmedID", "Title", "PublicationDate", "Non-academic Authors", "Affiliation", "E-mail"]
        )
        writer.writeheader()
        for paper in papers:
            authors = paper.get("Authors", [])
            affiliation = paper.get("Affiliation", "")
            email = paper.get("Email", "")
            
            # Ensure all arguments are in list format for `identify_non_academic_authors`
            non_academic_authors = identify_non_academic_authors(
                authors,
                [affiliation] * len(authors),  # Repeat the affiliation for each author
                [email] * len(authors)        # Repeat the email for each author
            )

            writer.writerow({
                "PubmedID": paper.get("PubmedID", ""),
                "Title": paper.get("Title", ""),
                "PublicationDate": paper.get("PublicationDate", ""),
                "Non-academic Authors": ", ".join(non_academic_authors),
                "Affiliation": affiliation,
                "E-mail": email,
            })
