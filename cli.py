import argparse
import logging
from pubmed_paper_fetcher.fetcher import fetch_papers, save_to_csv, identify_non_academic_authors

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed and identify authors affiliated with non-academic institutions."
    )
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file to save results.", default=None)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-m", "--max_results", type=int, help="Maximum number of results to fetch.", default=10)
    
    args = parser.parse_args()

    # Enable debug mode if specified
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled.")

    logger.info(f"Fetching papers for query: {args.query}")
    papers = fetch_papers(args.query, max_results=args.max_results)

    if args.file:
        save_to_csv(papers, args.file)
        logger.info(f"Results saved to {args.file}")
    else:
        for paper in papers:
            # Extract fields with default values
            authors = paper.get("Authors", [])
            affiliations = [paper.get("Affiliation", "")] * len(authors)
            emails = [paper.get("Email", "")] * len(authors)
            
            non_academic_authors = identify_non_academic_authors(authors, affiliations, emails)
            
            print(f"PubmedID: {paper.get('PubmedID', 'N/A')}")
            print(f"Title: {paper.get('Title', 'N/A')}")
            print(f"Publication Date: {paper.get('PublicationDate', 'N/A')}")
            print(f"Non-academic Authors: {', '.join(non_academic_authors) if non_academic_authors else 'N/A'}")
            print(f"Affiliation: {paper.get('Affiliation', 'N/A')}")
            print(f"Email: {paper.get('Email', 'N/A')}")
            print("-" * 80)

if __name__ == "__main__":
    main()
