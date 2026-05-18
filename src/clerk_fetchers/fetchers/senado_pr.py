import os

from bs4 import BeautifulSoup
from clerk import Fetcher
from parsedatetime import Calendar

calendar = Calendar()


class SenadoPRFetcher(Fetcher):
    def child_init(self):
        print(f"Initializing Senado Fetcher for {self.site['subdomain']}")
        self.url = "https://senado.pr.gov"
        self.ocr_lang = "spa"

    def fetch_events(self):
        resp = self.request("GET", f"{self.url}/index.cfm?module=session-diary")
        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.select("table tbody tr")
        for row in rows:
            cells = [cell for cell in row.find_all("td")]
            meeting_name = f"{cells[2].text.strip()}--{cells[1].text.strip()}".replace(
                " ", ""
            )
            meeting_name = meeting_name.strip()
            date = cells[3].text
            minutes_url = f"{self.url}/{cells[0].find('a').attrs['href']}"
            pdf_resp = self.request("GET", minutes_url)
            directory = f"{self.minutes_output_dir}/{meeting_name}"
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = f"{date}.pdf"
            if self.check_if_exists(meeting_name, date, "minutes"):
                continue
            with open(f"{directory}/{filename}", "wb") as pdf_file:
                print(f"Writing {directory}/{filename}")
                pdf_resp = self.request("GET", minutes_url)
                pdf_file.write(pdf_resp.content)
