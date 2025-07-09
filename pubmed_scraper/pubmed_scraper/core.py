from typing import List, Dict
import requests
from lxml import etree
import re

from pubmed_scraper.utils import is_non_academic, extract_company_name, extract_email


PUBMED_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def fetch_pubmed_ids(query: str, retmax: int = 50) -> List[str]:
    response = requests.get(
        PUBMED_ESEARCH_URL,
        params={"db": "pubmed", "term": query, "retmax": retmax, "retmode": "json"},
    )
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]


def fetch_pubmed_metadata(pubmed_ids: List[str]) -> List[Dict]:
    if not pubmed_ids:
        return []

    response = requests.get(
        PUBMED_EFETCH_URL,
        params={"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"},
    )
    response.raise_for_status()

    tree = etree.fromstring(response.content)
    articles = tree.findall(".//PubmedArticle")

    results = []

    for article in articles:
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "N/A"
        pmid = article.findtext(".//PMID")
        author_list = article.findall(".//Author")
        non_academic_authors = []
        company_affils = []
        corresponding_email = ""

        for author in author_list:
            affil = author.findtext(".//AffiliationInfo/Affiliation") or ""
            name_parts = [
                author.findtext("ForeName") or "",
                author.findtext("LastName") or "",
            ]
            full_name = " ".join(name_parts).strip()

            if is_non_academic(affil):
                non_academic_authors.append(full_name)
                if m := extract_company_name(affil):
                    company_affils.append(m)

            if email := extract_email(affil):
                corresponding_email = email

        if company_affils:
            results.append(
                {
                    "PubmedID": pmid,
                    "Title": title,
                    "Publication Date": pub_date,
                    "Non-academic Author(s)": "; ".join(non_academic_authors),
                    "Company Affiliation(s)": "; ".join(set(company_affils)),
                    "Corresponding Author Email": corresponding_email,
                }
            )

    return results
