from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
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
    times.append(e.text)

print("\nFound " + str(len(times)) + " sessions:")
for time in times:
    print(time)
for time in times:
    print("\nLooking for sits for session: " + time)
    if time.startswith("00"):
        print("I'll add support for night sessions later")
        continue
    driver.find_element_by_xpath("//a[contains(text(), '" + time + "')]").click()
    hall_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hallContainer")))
    price = driver.find_element_by_class_name("ticets_info_blue")
    print("\nPrice is: " + price.text)
    sits_elements = hall_container.find_elements_by_css_selector(".hs-image-0000000001")
    print("\nFound " + str(len(sits_elements)) + " sits:")
    for e in sits_elements:
        print("Row: " + e.get_attribute("exp-data-row") + "; Col: " + e.get_attribute("exp-data-col"))
    driver.get("http://planetakino.ua/showtimes/#imax-3d")
    
driver.close()
