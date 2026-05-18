from typing import TypeAlias


import os
import shutil
from datetime import datetime

from clerk import Fetcher
from parsedatetime import Calendar

calendar = Calendar()


class HoustonTXFetcher(Fetcher):
    def child_init(self):
        print(f"Initializing Houston TX Fetcher for {self.site['subdomain']}")

    def fetch_events(self):
        total_events = 0
        total_minutes = 0

        input_dir = f"input/{self.subdomain}"
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory '{input_dir}' not found")

        minutes_dir = f"{self.storage_dir}/{self.subdomain}/pdfs/CityCouncil"
        agendas_dir = f"{self.storage_dir}/{self.subdomain}/_agendas/pdfs/CityCouncil"

        for meeting in os.listdir(input_dir):
            if not meeting.endswith(".pdf"):
                continue
            name_parts = meeting.split("_")
            if name_parts[0] == "Minutes":
                kind = "minutes"
                directory = minutes_dir
                total_minutes += 1
            if name_parts[0] == "Agenda":
                kind = "agenda"
                directory = agendas_dir
            if not os.path.exists(directory):
                os.makedirs(directory)
            date_string = name_parts[1] + "-" + name_parts[2] + "-" + name_parts[3]
            time_struct, _ = calendar.parse(date_string)
            meeting_time = datetime(*time_struct[:6])
            date_string = meeting_time.strftime("%Y-%m-%d")
            filepath = f"{directory}/{date_string}.pdf"
            if self.check_if_exists("CityCouncil", date_string, kind):
                print(f"{filepath} already exists, skipping")
                continue
            shutil.copy(f"{input_dir}/{meeting}", filepath)
            total_events += 1

        return total_events, total_minutes
