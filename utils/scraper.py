import os
import pathlib

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from git import Repo, GitCommandError
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scrape(url, prefix):
    driver = webdriver.Chrome()
    driver.get(url)
    username = driver.find_element(By.ID, 'login_field')
    password = driver.find_element(By.ID, 'password')
    load_dotenv()
    username.send_keys(os.getenv("GH_USERNAME"))
    password.send_keys(os.getenv("GH_PASSWORD"))
    password.send_keys(Keys.ENTER)

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'assignment-repo-list-item'))
    )

    html = driver.page_source
    page = BeautifulSoup(html, "html.parser")

    # init paths to temp store clone repo directories
    data = {
        "paths": [],
        "fileNames": [],
    }

    # find username elements
    items = page.find_all("div", {"class": "assignment-repo-list-item"})

    while True:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'assignment-repo-list-item'))
        )

        html = driver.page_source
        page = BeautifulSoup(html, "html.parser")

        # find username elements
        items += page.find_all("div", {"class": "assignment-repo-list-item"})

        # Check for next page button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
            if not next_button.is_displayed():
                break
            next_button.click()
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]') != next_button
            )
        except:
            break  # No more pages

    for element in items[::-1]:
        # extract username
        username = element.find("img")['alt'].replace('@', '')

        # generate repo url
        url = f"{prefix}-{username}.git"

        # clone repo
        try:
            Repo.clone_from(url, f"clone/{username}")
        except GitCommandError as e:
            print(e)
            continue

        # open repo page
        driver.get(url)
        html = driver.page_source
        repo_page = BeautifulSoup(html, "html.parser")

        # find file elements
        files = repo_page.find("table").find_all(
            "td", {"class": "react-directory-row-name-cell-large-screen"}
        )
        def process_directory(base_url, current_path=""):
            if base_url.endswith(".git"):
                base_url = base_url.split(".git")[0]
            if current_path != "":
                current_path = "/tree/main/" + current_path
            print(base_url, current_path)
            driver.get(base_url + current_path)
            html = driver.page_source
            page_content = BeautifulSoup(html, "html.parser")
            
            sub_files = page_content.find("table").find_all(
                "td", {"class": "react-directory-row-name-cell-large-screen"}
            )
            
            for file in sub_files:
                link = file.find("a", {"class": "Link--primary"})
                if not link:
                    continue

                file_name = file.get_text().strip()
                if file_name in ['.', '..']:
                    continue
                    
                # Check if it's a directory
                is_directory = file.find("svg", {"class": "icon-directory"}) is not None

                # Get the href attribute to construct the full path
                href = link.get('href')
                if href:
                    # Extract the path from the href (remove the domain and repo parts)
                    path_parts = href.split('/tree/main/')
                    if len(path_parts) > 1:
                        full_path = path_parts[1]
                    else:
                        path_parts = href.split('/blob/main/')
                        if len(path_parts) > 1:
                            full_path = path_parts[1]
                        else:
                            continue
                
                if is_directory:
                    # Recursively process subdirectory
                    process_directory(base_url, full_path)
                else:
                    extension = pathlib.Path(file_name).suffix
                    if extension in ['.ipynb', '.py'] and not file_name.startswith("test"):
                        data["paths"].append(f"{username}/{full_path}")
                        data["fileNames"].append(username + "_" + full_path.replace("/", "_"))
                    print(data)
            

        # Start processing from root directory
        process_directory(url)


    # close driver
    driver.quit()

    return data
