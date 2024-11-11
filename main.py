from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time, os, csv, pandas, http.server, socketserver

port=8000
Handler = http.server.SimpleHTTPRequestHandler

#Current directory must be where your webdriver's extracted files are present
download_dir= os.path.join(os.getcwd(), 'PHYPBL')
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

chrome_options = Options()
prefs = {
    "download.default_directory": r"D:\Karvy\protego totalus\PhyPBL\downloads", 
    "download.prompt_for_download": False,
    "safebrowsing.disable_download_protection": True,
    "download.directory_upgrade": True,
    "profile.default_content_setting_values.automatic_downloads": 1
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=Service(r"D:\Karvy\protego totalus\PhyPBL\chromedriver-win64\chromedriver.exe"), options=chrome_options)
driver.get('http://192.168.29.59:8080/') #this is an example print, insert the current link provided by the phyphox app 

# Click the "More" button to display the menu
more_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'more'))
)
more_button.click()
WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.ID, 'moreMenu'))
)

# Click the "Export Data" button within the menu
export_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, 'export'))
)
export_button.click()

download_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@value='Download Data']"))
)
download_button.click()

time.sleep(3)
driver.quit()

dir= r"D:\Karvy\protego totalus\PhyPBL\downloads"
for filename in os.listdir(dir):
    if filename.endswith('.crdownload'):
        base_name = filename.replace('.crdownload', '')
        full_path = os.path.join(dir, filename)
        new_path = os.path.join(dir, base_name)
        os.rename(full_path, new_path)
        
for filename in os.listdir(dir):
    print(filename)
    df = pandas.read_excel(os.path.join(dir,filename), engine='xlrd') 
    sum=0
    j=0
    for i in df['Illuminance (lx)']:
        sum+=i
        j+=1
    ill_avg=sum/j
    
if 100< ill_avg <300:
    print("optimal")
else:
    print("not optimal")
        
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        if 100< ill_avg <300:
            self.respond_with_content(b"<h1>OPTIMAL illuminance levels found</h1>")
        else:
            self.respond_with_content(b"<h1>NOT OPTIMAL illuminance levels found</h1>")

    def respond_with_content(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8000), SimpleHandler)
    server.serve_forever()
