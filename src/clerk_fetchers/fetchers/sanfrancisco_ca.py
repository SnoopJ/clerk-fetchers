import os
from datetime import datetime

from bs4 import BeautifulSoup
from clerk import Fetcher
from parsedatetime import Calendar

calendar = Calendar()


class SanFranciscoCAFetcher(Fetcher):
    def child_init(self):
        print(f"Initializing San Francisco CA Fetcher for {self.site['subdomain']}")

    def fetch_events(self):
        today = datetime.now()

        input_dir = f"input/{self.subdomain}"
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory '{input_dir}' not found")

        minutes_dir = f"{self.storage_dir}/{self.subdomain}/pdfs/"
        agendas_dir = f"{self.storage_dir}/{self.subdomain}/_agendas/pdfs/"

        for page in os.listdir(input_dir):
            if not page.endswith(".html"):
                continue
            with open(f"{input_dir}/{page}", "r") as html_file:
                soup = BeautifulSoup(html_file, "html.parser")
                rows = soup.select(
                    "#ctl00_ContentPlaceHolder1_gridCalendar tbody .rgRow"
                )
                rows += soup.select(
                    "#ctl00_ContentPlaceHolder1_gridCalendar tbody.rgAltRow"
                )
                for row in rows:
                    tds = row.find_all("td")
                    time_struct, _ = calendar.parse(tds[1].text.strip())
                    meeting_time = datetime(*time_struct[:6])
                    date_string = meeting_time.strftime("%Y-%m-%d")
                    for td in tds:
                        if td("a") and td("a")[0].attrs.get("id").endswith("_hypBody"):
                            meeting_name = td("a")[0].text.strip().replace(" ", "")
                        if (
                            meeting_time >= today
                            and td("a")
                            and td("a")[0].attrs.get("id").endswith("_hypAgenda")
                            and td("a")[0].attrs.get("href")
                        ):
                            doc_link = td("a")[0].attrs.get("href")
                            directory = f"{agendas_dir}{meeting_name}/"
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            filename = f"{date_string}.pdf"
                            pdf_resp = self.request("GET", doc_link)
                            with open(f"{directory}{filename}", "wb") as pdf_file:
                                print("Writing", f"{directory}{filename}")
                                pdf_file.write(pdf_resp.content)
                            break
                        if (
                            meeting_time < today
                            and td("a")
                            and td("a")[0].attrs.get("id").endswith("_hypMinutes")
                            and td("a")[0].attrs.get("href")
                        ):
                            kind = "minutes"
                            doc_link = td("a")[0].attrs.get("href")
                            directory = f"{minutes_dir}{meeting_name}/"
                            if not os.path.exists(directory):
                                os.makedirs(directory)
                            filename = f"{date_string}.pdf"
                            if self.check_if_exists(meeting_name, date_string, kind):
                                print(f"Skipping {directory}{filename}, already exists")
                                break
                            pdf_resp = self.request("GET", doc_link)
                            with open(f"{directory}{filename}", "wb") as pdf_file:
                                print("Writing", f"{directory}{filename}")
                                pdf_file.write(pdf_resp.content)
                            break
        return 0, 0
