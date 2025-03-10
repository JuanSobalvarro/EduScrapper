"""
So, we found that student codes works as:
AYY carrera id
IME : 01
IMS : 02
IGI : 03
ICE : 04
ISKA: 0?
XX ano ingreso
SS sexo
F: 00
M: 01


XX - AYYSS - ZZZZ

ZZZZ is student number auto incremented, unique for each year (XX)
"""
from src.driver.driver import get_driver
from enum import Enum
from bs4 import BeautifulSoup
import requests


class ScrappingOptions(Enum):
    Students = 0
    Documents = 1
    Personal = 2


class Sive:
    def __init__(self, url: str = "https://sive.ulsa.edu.ni", output_file: str = "output"):
        self.driver = get_driver()

        if not self.driver:
            print("Error loading driver")

        self.url = url
        self.output_file = output_file

    def run(self):
        print("Select an option to scrap:")
        print(f"{ScrappingOptions.Students.value}: Students")
        print(f"{ScrappingOptions.Documents.value}: Documents")
        print(f"{ScrappingOptions.Personal.value}: Personal")
        option = int(input("> "))

        if option not in ScrappingOptions:
            print("Invalid option")
            return

        data = None
        if option == ScrappingOptions.Students.value:
            data = self.student_scrapping()

        elif option == ScrappingOptions.Documents.value:
            data = self.documents_scrapping()

        elif option == ScrappingOptions.Personal.value:
            data = self.personal_scrapping()

        if data:
            self.save_output(data)
        else:
            print("No data to save")

        self.driver.close()

    def save_output(self, data):
        with open(self.output_file, 'w') as file:
            file.write(data)

    def student_scrapping(self):
        if not self.driver:
            print("Driver not initialized")
            return

        # Navigate to login page
        self.driver.get(self.url)

        # Get cookies and headers
        cookies = {cookie["name"]: cookie["value"] for cookie in self.driver.get_cookies()}

        # print("Cookies generated: ", cookies)

        # Headers that mimic XHR request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",  # To indicate XHR
            "Content-Type": "application/x-www-form-urlencoded",  # Data is typically in form URL-encoded format
            "Referer": self.url
        }

        # Test request for a known student code
        test_code = "22-A0401-0168"
        api_url = "https://sive.ulsa.edu.ni/documentos/infoEstudiante"

        payload = {"codigo": test_code}

        test_response = requests.get(api_url, params=payload, cookies=cookies, headers=headers)
        print(f"Test response: {test_response.status_code}")
        if test_response.content == b'':
            print("Failed to get data for test code")
            return

        results = []
        for year in range(22, 25):
            # Since it should be x students, check for sex and career until find the correct one
            result = False
            for student in range(50, 100):
                # First check for male since it's the most common
                for sexo in ["01", "00"]:
                    # Then check for a career
                    for carrera in range(1, 5):
                        student_code = f"{year:02d}-A{carrera:02d}{sexo}-{student:04d}"
                        payload = {"codigo": student_code}
                        student_data = self.fetch_student_data(payload, cookies, headers)
                        if student_data:
                            print(f"Found student data for {student_code}: {student_data}")
                            results.append(student_data)
                            result = True
                            break
                        else:
                            print(f"Student data not found for {student_code}")
                    if result:
                        break

        print(results)
        return "\n".join(results)

    def fetch_student_data(self, payload, cookies, headers):
        api_url = "https://sive.ulsa.edu.ni/documentos/infoEstudiante"
        response = requests.get(api_url, params=payload, cookies=cookies, headers=headers)
        if response.content != b'':
            real_data = self.parse_student_data(response.text)
            if real_data is None:
                return None
            return real_data
        else:
            print(f"Failed for {payload} - Status {response.status_code}")

    def personal_scrapping(self):
        pass

    def documents_scrapping(self):
        pass

    @staticmethod
    def generate_student_codes():
        for year in range(21, 25):
            # Since it should be x students, check for sex and career until find the correct one
            result = False
            for student in range(10):
                # First check for male since it's the most common
                for sexo in ["01", "00"]:
                    # Then check for a career
                    for carrera in range(1, 5):
                        student_code = f"{year:02d}-A{carrera:02d}{sexo}-{student:04d}"

    def parse_student_data(self, data):
        """
        Parses student data from an HTML string and extracts the relevant information.
        :param data: The HTML data as a string.
        :return: A dictionary with parsed student details.
        """
        soup = BeautifulSoup(data, 'html.parser')

        # Create a dictionary to hold the extracted student information
        student_info = {}

        # Extracting the student's full name (combining both first and last names)
        full_name = soup.find('span', class_='font-weight-bold')
        if full_name:
            student_info['full_name'] = full_name.text.strip() + " " + full_name.find_next('span').text.strip()

        # Extracting the student's email
        email_tag = soup.find('a', href=True)
        if email_tag:
            student_info['email'] = email_tag['href'].replace('mailto:', '').strip()

        # Extracting the student's ID (Carnet)
        carnet_tag = soup.find(string="Carnet:")
        if carnet_tag:
            carnet_value = carnet_tag.find_next('div').text.strip()
            student_info['carnet'] = carnet_value

        # Extracting the student's status (Estado)
        status_tag = soup.find(string="Estado:")
        if status_tag:
            status_value = status_tag.find_next('div').text.strip()
            student_info['status'] = status_value

        # Extracting the program/career
        program_tag = soup.find(string="Programa/Carrera:")
        if program_tag:
            program_value = program_tag.find_next('div').text.strip()
            student_info['program'] = program_value

        # Extracting the student's entry date (Fecha de ingreso)
        entry_date_tag = soup.find(string="Fecha de ingreso:")
        if entry_date_tag:
            entry_date_value = entry_date_tag.find_next('div').text.strip()
            student_info['entry_date'] = entry_date_value

        # Extracting the student's shift (Turno)
        shift_tag = soup.find(string="Turno:")
        if shift_tag:
            shift_value = shift_tag.find_next('div').text.strip()
            student_info['shift'] = shift_value

        # Extracting the student's career
        career_tag = soup.find(string="Programa/Carrera:")
        if career_tag:
            career_value = career_tag.find_next('div').text.strip()
            student_info['career'] = career_value

        return student_info
