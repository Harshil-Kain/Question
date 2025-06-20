from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    content = soup.find("div", {"class": "mw-parser-output"})
    if not content:
        return {"error": "content not found"}
    headings = content.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    markdown = "## Contents\n\n" + f"# {country}\n\n"
    for tag in headings:
        level = int(tag.name[1])
        markdown += f"{'#' * level} {tag.get_text(strip=True)}\n\n"
    return {"country": country, "markdown_outline": markdown}

handler = Mangum(app)
