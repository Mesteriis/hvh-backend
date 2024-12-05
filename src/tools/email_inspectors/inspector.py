import json
import re
from collections.abc import Generator
from pathlib import Path
from typing import Any

import httpx
import openpyxl
from rich.progress import BarColumn, Progress, SpinnerColumn, TimeElapsedColumn

from .constants import EMAIL_RE_PATTERN
from .structs import EmailItem, EmailList


class EmailInspector:
    __emails: list[dict[str, Any]] = []
    __verified_emails: EmailList = None
    __root_domains: list[str] = None
    _path_to_file: str | Path = Path("tools/email_inspectors/output.csv")

    def execute(self):
        if not self.__emails:
            raise ValueError("No emails found")
        email_csv = self._read_csv(self._path_to_file)
        email_set = []
        with Path("tools/email_inspectors/output.csv").open("a") as f:
            with Progress(
                SpinnerColumn(),
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.1f}%",
                TimeElapsedColumn(),
            ) as progress:
                task = progress.add_task("[cyan]Verification...", total=len(self.__emails))
                for el in self.__emails:
                    if el in email_csv:
                        progress.update(task, advance=1)
                        continue
                    try:
                        email = EmailItem.model_validate(el)
                        email_set.append(email)
                        f.write(email.as_csv_string())
                    except Exception as e:
                        print(e)
                    progress.update(task, advance=1)

            self.__verified_emails = EmailList(emails=email_set)

    def _read_csv(self, file_path: str | Path) -> list[str]:
        emails_set = []
        with Path(file_path).open() as f:
            for el in f:
                email = el.strip().split(",")[0]
                emails_set.append(email)
        return emails_set

    @staticmethod
    def _read_xlsx(file_path: str | Path) -> Generator:
        if isinstance(file_path, str):
            file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        yield sheet.iter_rows(values_only=True)

    def _normalize_email(self, email: str) -> str | None:
        self.collect_top_level_domains()
        email = email.replace("%20", "")
        email = email.replace("..", ".")
        if email.count("@") != 1:
            return None
        if email.split(".")[-1] not in self.__root_domains:
            return None
        return email

    def read_xlsx(self, file_path: str | Path) -> None:
        emails_set = {}
        for row in self._read_xlsx(file_path):
            line = "\t".join(str(cell) for cell in row)
            emails_ = re.findall(EMAIL_RE_PATTERN, line)
            for raw_email in emails_:
                if email := self._normalize_email(raw_email):
                    if email not in emails_set:
                        emails_set[email] = {"email": email, "extra_info": {"original": line, "count": 1}}
                    else:
                        emails_set[email]["extra_info"]["count"] += 1
        self.__emails = list(emails_set.values())

    def _collect_input_stat(self):
        if not self.__emails:
            return "No emails found"
        total = len(self.__emails)
        unique = len([el["extra_info"]["count"] for el in self.__emails if el["extra_info"]["count"] == 1])
        duplicates = len([el["extra_info"]["count"] - 1 for el in self.__emails if el["extra_info"]["count"] > 1])
        return {"total": total, "unique": unique, "duplicates": duplicates}

    def _collect_verified_stat(self):
        if not self.__verified_emails:
            return "No emails found"
        total = self.__verified_emails.total
        valid = self.__verified_emails.valid
        invalid = total - valid
        return {"total": total, "valid": valid, "invalid": invalid}

    def stat(self):
        stat = {"input data": self._collect_input_stat(), "verified": self._collect_verified_stat()}
        return json.dumps(stat, indent=2)

    def collect_top_level_domains(self) -> list[str]:
        if self.__root_domains:
            return self.__root_domains
        response = httpx.get("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
        response.raise_for_status()
        self.__root_domains = list(map(lambda x: x.lower(), response.text.split("\n")[1:]))  # noqa: C417
        return self.__root_domains
