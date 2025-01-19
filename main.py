#empty
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import logging
import time

from useful.smartinput import Input

logging.basicConfig(level=logging.INFO, filename="log.txt", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

class Driver(uc.Chrome):
    def __init__(self, *args):
        super().__init__(args)
    
    def wait_for(self, by, value, timeout=10):
        return WebDriverWait(self, timeout).until(EC.presence_of_element_located((by, value)))

def clean_exception(e : Exception):
    logging.exception(e)
    print(e.args[0])
    quit()

def print_log(s : str):
    print(s)
    logging.info(s)

class Login():
    ENV_NOT_FOUND = FileNotFoundError("LOGIN CLASS -> login() -> File secret.env not found. Please ensure it exists and contains required USER, PASSWORD, and POSTCODE fields.")
    INVALID_ENV = KeyError('''LOGIN CLASS -> login() -> Invalid secret.env setup. Could not find USER, PASSWORD, or POSTCODE fields.
Please ensure secret.env contains USER, PASSWORD, and POSTCODE fields.
Example format: 
USER=john
PASSWORD=1234
POSTCODE=ABC 123''')
    SCHOOL_NOT_FOUND = Exception("LOGIN CLASS -> login() -> School not found. Please ensure the POSTCODE field in secret.env is correct.")
    INCORRECT_LOGIN = Exception("LOGIN CLASS -> login() -> Incorrect login details. Please ensure the USER and PASSWORD fields in secret.env are correct.")
    
    def __init__(self, driver : Driver):
        self.driver = driver
        self.load_user_fields()

    def load_user_fields(self):
        PATH_TO_ENV = "secret.env"
        if not os.path.exists(PATH_TO_ENV):
            clean_exception(Login.ENV_NOT_FOUND)
            exit()
        load_dotenv(PATH_TO_ENV)

        self.USER = os.getenv("USER")
        self.PASSWORD = os.getenv("PASSWORD")
        self.POSTCODE = os.getenv("POSTCODE")

        if None in [self.USER, self.PASSWORD, self.POSTCODE]:
            clean_exception(Login.INVALID_ENV)
            exit()

        logging.info("LOGIN CLASS -> load_user_fields() -> Loaded user fields.")
            
    def login(self):
        self.driver.get("https://play.ttrockstars.com/auth/school/student")

        school_name = self.driver.wait_for(by=By.ID, value="mat-input-0")
        school_name.send_keys(self.POSTCODE)

        # check school is valid by checking to see if confirm box appears
        try:
            school_confirm = self.driver.wait_for(by=By.ID, value="mat-option-1")
            school_confirm.click()
        except (Exception) as e:
            clean_exception(Login.SCHOOL_NOT_FOUND)
            print(e)

        username = self.driver.wait_for(by=By.ID, value="mat-input-1")
        username.send_keys(self.USER)

        pass_button = self.driver.wait_for(by=By.XPATH, value="/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-login2/ttr-splash/div/div[1]/div/ttr-login-form/div/form/mat-card/div[3]/div[1]/button")
        pass_button.click()
        
        password = self.driver.wait_for(by=By.ID, value="mat-input-2")
        password.send_keys(self.PASSWORD)

        login_button = self.driver.wait_for(by=By.XPATH, value="/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-login2/ttr-splash/div/div[1]/div/ttr-login-form/div/form/mat-card/mat-card-actions/button")
        login_button.click()

        # check login is correct by seeing if singleplayer button appears
        try:
            self.driver.wait_for(by=By.XPATH, value="/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/ttr-play2-home-nav-btn[1]/a", timeout=5)
            # if we reach this point, we have failed to login
            logging.info("LOGIN CLASS -> login() -> Successfully logged in.")
            return True
        except:
            clean_exception(Login.INCORRECT_LOGIN)

class Play():
    def __init__(self, driver : Driver, ideal_seconds_per_question : float = 1.0):
        self.driver = driver

        self.ideal_spq = ideal_seconds_per_question
        print_log(f"PLAY CLASS -> __init__() -> Ideal seconds per question: {self.ideal_spq}")

    def click_singleplayer(self):
        singleplayer_button = self.driver.wait_for(by=By.XPATH, value="/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/ttr-play2-home-nav-btn[1]/a")
        singleplayer_button.click()

    def studio(self):
        print_log("PLAY CLASS -> studio() -> Starting studio mode.")
        self.click_singleplayer()

        studio_button = self.driver.wait_for(by=By.XPATH, value="/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/div/div/ttr-play2-game-list-nav-btn[4]/div/a")
        studio_button.click()

        play_button = self.driver.wait_for(by=By.XPATH, value="/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/div/div/div/div/ttr-play2-preview-studio/ttr-play2-game-preview/div[1]/div/div/button")
        play_button.click()
        self.play(origin="studio")

    def garage(self):
        print_log("PLAY CLASS -> garage() -> Starting garage mode.")
        self.click_singleplayer()

        garage_button = self.driver.wait_for(by=By.XPATH, value="/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/div/div/ttr-play2-game-list-nav-btn[3]/div/a")
        garage_button.click()

        play_button = self.driver.wait_for(by=By.XPATH, value="/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ng-component/div/ng-component/div/div/div/div/div/ttr-play2-preview-garage/ttr-play2-game-preview/div[1]/div/div/button")
        play_button.click()

        self.play(origin="garage")

    def play_again(self, origin : str):
        play_again_button = self.driver.wait_for(by=By.XPATH, value=f"/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-{origin}/ttr-game-holder/div/div/ttr-game-results-details/div/div[2]/div/div[1]/div[2]/button[2]")
        
        i = Input("Would you like to play again?")
        i.add_choices(["yes", "no"])
        response = i.get_response()

        if response == "yes":
            play_again_button.click()
            self.play(origin)
        else:
            print_log(f"PLAY CLASS -> play_again({origin}) -> Exiting.")
            quit()

    def play(self, origin : str ):
        print_log(f"PLAY CLASS -> play({origin}) -> Starting to answer questions.")
        questions_answered = 0

        # xpaths 
        left_xpath = f"/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-{origin}/ttr-game-holder/div/div[1]/div[1]/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span/span[1]"
        center_xpath = f"/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-{origin}/ttr-game-holder/div/div[1]/div[1]/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span/span[2]"
        right_xpath = f"/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-{origin}/ttr-game-holder/div/div[1]/div[1]/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span/span[3]"
        inbox_xpath = f"/html/body/ttr-root/ttr-root-app/div/mat-sidenav-container/mat-sidenav-content/div/section/ttr-{origin}/ttr-game-holder/div/div[1]/div[1]/ttr-game-footpedal/section[2]/section/ttr-game-input"

        # wait for the game to load first
        in_box = self.driver.wait_for(by=By.XPATH, value=inbox_xpath)
        
        true_start_time = time.time() # Current time when t=0s in the game
        
        

        def answer_loop(questions_answered):
            left = self.driver.wait_for(by=By.XPATH, value=left_xpath)
            center = self.driver.wait_for(by=By.XPATH, value=center_xpath)
            right = self.driver.wait_for(by=By.XPATH, value=right_xpath)

            left_num = int(left.text)
            operator = center.text
            right_num = int(right.text)

            match operator:
                case "×":
                    ans = left_num * right_num
                    regular_operator = "*"
                case "÷":
                    ans = left_num // right_num
                    regular_operator = "/"
                case _:
                    clean_exception(Exception(f"PLAY CLASS -> play({origin}) -> Cannot identify operator."))
            
            print_log(f"PLAY CLASS -> play({origin}) -> Answering question ({questions_answered}): {left_num} {regular_operator} {right_num} = {ans}")

            actions = ActionChains(self.driver)
            actions.move_to_element(in_box)
            actions.click()
            actions.send_keys(str(ans))
            actions.send_keys(Keys.RETURN)
            actions.perform()

        while True:
            start_time = time.time()
            if start_time - true_start_time > 60: #if more than 60s have passed, game over
                time_taken = start_time - true_start_time
                print_log(f"PLAY CLASS -> play({origin}) -> Game ended! Answered {questions_answered} questions in {time_taken}s, reaching {round(time_taken/questions_answered, 2)}s per question, which is {abs(round(time_taken/questions_answered, 2) - self.ideal_spq)}s off the ideal.")
                self.play_again(origin)

            questions_answered += 1
            answer_loop(questions_answered)

            answer_time = time.time() - start_time # How long it took for the question to be calculated and answered
            if answer_time > self.ideal_spq: # Answer time took longer than ideal, sleep for 0s
                print_log(f"PLAY CLASS -> play({origin}) -> Completed question in {round(answer_time, 2)} seconds. No sleep required.")
            else:
                sleep_time = self.ideal_spq - answer_time # Time to sleep to achieve ideal spq
                print_log(f"PLAY CLASS -> play({origin}) -> Completed question in {round(answer_time, 2)} seconds. Sleeping for {round(sleep_time, 2)} seconds, to achieve secs per question of {self.ideal_spq}.")
                time.sleep(sleep_time) # Sleep time to achieve ideal spq



def main():
    i_spq = Input("What speed (seconds per question) would you like to set? ")
    i_spq.add_data_type(float)
    ideal_seconds_per_question = float(i_spq.get_response())
    if ideal_seconds_per_question < 0.4:
        print_log("__main__() -> Note: Ideal seconds per question of less than 0.4s is likely impossible due to the time taken to read components.")

    i_mode = Input("Would you like to play in studio or garage mode? ")
    i_mode.add_choices(["studio", "garage"])
    mode = i_mode.get_response()


    # main
    try:
        driver = Driver()
    except FileNotFoundError:
        clean_exception(Exception("__main__() -> Chrome driver not found. Try to reinstall chrome."))

    l = Login(driver=driver)
    l.login()

    p = Play(driver=driver, ideal_seconds_per_question=ideal_seconds_per_question)

    if mode == "studio":
        p.studio()
    elif mode == "garage":
        p.garage()

if __name__ == "__main__":
    main()
