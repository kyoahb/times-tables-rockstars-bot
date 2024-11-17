import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os
from selenium.webdriver.common.action_chains import ActionChains
import random
# Load environment variables from secret.env
load_dotenv('secret.env')

# Get credentials from environment variables
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
POST = os.getenv('POST')
# Initialize the undetected Chrome webdriver
driver = uc.Chrome()

def wait_and_get(by, path):
    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((by, path))
    )

sec_per_question = 1.5
randomise = True

try:
    # Navigate to the website
    driver.get("https://play.ttrockstars.com/auth/school/student")  # Replace with your target website

    # Wait for the page to load completely by waiting for a specific element to be present
    school_name = wait_and_get(By.ID, "mat-input-0")
    school_name.click()
    school_name.send_keys(POST)
    
    school_choice = wait_and_get(By.ID, "mat-option-1")
    school_choice.click()

    pass_button = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-login2/ttr-splash/div/div[1]/div/ttr-login-form/div/form/mat-card/div[3]/div[1]/button")
    pass_button.click()

    username = wait_and_get(By.ID, "mat-input-1")
    username.send_keys(USER)

    password = wait_and_get(By.ID, "mat-input-2")
    password.send_keys(PASSWORD)

    login_button = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-login2/ttr-splash/div/div[1]/div/ttr-login-form/div/form/mat-card/mat-card-actions/button")
    login_button.click()

    singleplayer_button = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/ttr-play2-home-nav-btn[1]/a")
    singleplayer_button.click()

    studio_button = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/div/div/ttr-play2-game-list-nav-btn[4]/div/a")
    studio_button.click()

    play_button = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/div/div/div/div/ttr-play2-preview-studio/ttr-play2-game-preview/div[1]/div/div/button")
    play_button.click()

    auto_play = False

    def play(to_randomise = False):
        # random multiplier to get as the final score
        if randomise:
            true_score_mult = 1 + random.randrange(-100, 100)/1000
            print(f"Randomising with a multiplier of {round(true_score_mult, 2)}: true score will be around {round(true_score_mult*sec_per_question, 2)}")
        start = time.time()
        while time.time() - start < 65:
            in_box = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-studio/ttr-game-holder/div/div[1]/div[1]/ttr-game-footpedal/section[2]/section/ttr-game-input")

            actions = ActionChains(driver)
            actions.move_to_element(in_box)
            actions.click()
            # random chance to answer the question wrong
            if to_randomise and random.randrange(0, round((sec_per_question)*20)) == 0 :
                actions.send_keys(str(random.randrange(0, 100)))
                actions.send_keys(Keys.RETURN)
                actions.perform()
                print("Random chance shot, incorrect answer given.")
                continue

            left = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-studio/ttr-game-holder/div/div[1]/div[1]/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span/span[1]")
            operator = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-studio/ttr-game-holder/div/div[1]/div[1]/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span/span[2]")
            right = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-studio/ttr-game-holder/div/div[1]/div[1]/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span/span[3]")
            if operator.text == "×":
                actions.send_keys(str(int(left.text) * int(right.text)))
            elif operator.text == "÷":
                actions.send_keys(str(int(left.text) // int(right.text)))
            actions.send_keys(Keys.RETURN)
            actions.perform()
            sleep_time = round((sec_per_question-0.41), 2)
            # add multiplier to sleep time
            # add random n to sleep time between -0.1 and 0.1 for individual question variance
            if to_randomise:
                sleep_time *= true_score_mult
                sleep_time += random.randrange(-10, 10)/100
                sleep_time = round(sleep_time, 2)
            print(f"Answered question, sleeping for {sleep_time}s [true tps -> {round(sleep_time + 0.41, 2)}s]. {round(65-(time.time() - start), 2)}s left")
            time.sleep(sleep_time)
    while True:
        play(randomise)
        time.sleep(5)
        play_again_button = wait_and_get(By.XPATH, "/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-studio/ttr-game-holder/div/div/ttr-game-results-details/div/div[2]/div/div[1]/div[2]/button[2]")
        if not auto_play: 
            response = input("Hit enter to play again.")
            if response == "auto":
                auto_play = True
        play_again_button.click()

finally:
    # Clean up
    driver.quit()