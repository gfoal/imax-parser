from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
driver.get("http://planetakino.ua/showtimes/#imax-3d")
print("Opened page with title: " + driver.title)
movie_title_elements = driver.find_elements_by_css_selector(".showtime-movie-container :not(.hidden).movie-title")
print("\nFound " + str(len(movie_title_elements)) + " movies:")
for e in movie_title_elements:
    print(e.text)

top_date_sessions_container = driver.find_element_by_css_selector(":not(.hidden).p-one-day")

top_date_str = top_date_sessions_container.find_element_by_css_selector(".dates").text
print("\nTop date: " + top_date_str)

session_time_elements = top_date_sessions_container.find_elements_by_css_selector(".t-imax-3d .time:not(.past)")
times = []
for e in session_time_elements:
    times.append(e.text.strip())

print("\nFound " + str(len(times)) + " sessions:")
for time in times:
    print(time)
for time in times:
    print("\nLooking for sits for session: " + time)
    if time.startswith("00"):
        print("I'll add support for night sessions later")
        continue
    try:
        link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'p-one-day') and not(contains(@class, 'hidden'))]//a[contains(text(), '" + time + "')]")))
        link.click()
        hall_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hallContainer")))
        price = driver.find_element_by_class_name("ticets_info_blue")
        print("\nPrice is: " + price.text)
        sits_elements = hall_container.find_elements_by_css_selector(".hs-image-0000000001")
        print("\nFound " + str(len(sits_elements)) + " sits:")
        sits = {}
        for e in sits_elements:
            row = int(e.get_attribute("exp-data-row"))
            col = int(e.get_attribute("exp-data-col"))
            if row in list(sits.keys()):
                sits[row].append(col)
            else:
                sits[row] = [col]
        driver.get("http://planetakino.ua/showtimes/#imax-3d")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "showtimes-body")))

        #for k, v in sits.items():
        #    print("Row: " + k + "; Sits: " + str(v))

        hall = ""
        #print(sits)
        for row in range(3, 13):
            hall += str(row)
            if row < 10:
                hall += " : |"
            else:
                hall += ": |"
            for col in range(24, 0, -1):
                if row in list(sits.keys()) and col in sits[row]:
                    hall += str(col)
                    if col < 10:
                         hall += " "
                else:
                    hall += ". "
                hall += "|"
            hall += "\n"
        print(hall)
    except TimeoutError:
        error_container = driver.find_element_by_class_name("error-messages")
        print("There is a problem getting tickets fot that session:\n" + error_container.text)
        continue

driver.close()
driver.quit()
