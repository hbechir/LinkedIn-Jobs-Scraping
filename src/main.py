from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json


def login(driver):
    # get email and password from .env
    EMAIL = 'hbechir52@gmail.com'
    PASSWORD = 'Bechir150802'
    email_input_XPATH = '//*[@id="session_key"]'
    password_input_XPATH = '//*[@id="session_password"]'
    login_button_XPATH = '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button'

    # Find the email input field
    email_input = driver.find_element('xpath', email_input_XPATH)
    email_input.send_keys(EMAIL)

    # Find the password input field
    password_input = driver.find_element('xpath', password_input_XPATH)
    password_input.send_keys(PASSWORD)

    # find the login button
    login_button = driver.find_element('xpath', login_button_XPATH)
    login_button.click()




# def search_jobs(driver, job_title):
#     # search_input_XPATH = '//*[@id="jobs-search-box-keyword-id-ember29"]' cant use xpath for this button beacause it is dynamic and changes every reload
#     # ➡️➡️➡️➡️➡️➡️ instead of using xpath we can use the url OR we can use the class name 
#     search_input = driver.find_element(By.CLASS_NAME, 'jobs-search-box__text-input').send_keys(job_title)
#     # press enter to search
#     search_input.send_keys(Keys.RETURN)

# 👆🏻👆🏻👆🏻 this function is depricated because i switched to using filter search for better results




def getEtxt(driver, element):
    """get element text by xpath"""
    return driver.find_element(By.XPATH, element).text



def getJobsCount(driver):
    """get the number of jobs found for a search or a filter"""
    return getEtxt(driver, '//*[@id="main"]/div/div[2]/div[1]/header/div[1]/small/div')


def openFilter(driver):
    """open the filter section"""
    filter_button = driver.find_element(By.CLASS_NAME, 'search-reusables__all-filters-pill-button')
    filter_button.click()

def filterByIndutries(driver):
    """filter by industries"""

    # ☢️☢️☢️☢️☢️☢️☢️☢️
    # i used this static xpath method because i tried getting the elements by getting the list and looping through
    # but it didn't work because the elements are dynamic and the xpath changes every reload
    # ☢️☢️☢️☢️☢️☢️☢️☢️

    # get the container by class
    print("loooooooool")
    container = driver.find_element(By.CLASS_NAME, 'artdeco-modal__content')

    # click radio advanced-filter-industry-4 and 96 and 6 and 3231 and 8
    filter_industry_4 = container.find_element(By.XPATH, '//label[@for="advanced-filter-industry-4"]')
    filter_industry_4.click()

    filter_industry_96 = container.find_element(By.XPATH, '//label[@for="advanced-filter-industry-96"]')
    filter_industry_96.click()

    filter_industry_6 = container.find_element(By.XPATH, '//label[@for="advanced-filter-industry-6"]')
    filter_industry_6.click()

    # filter_industry_3231 = container.find_element(By.XPATH, '//label[@for="advanced-filter-industry-3231"]')
    # filter_industry_3231.click()

    filter_industry_8 = container.find_element(By.XPATH, '//label[@for="advanced-filter-industry-8"]')
    filter_industry_8.click()



def filterByJobTitle(driver, job_title_inputclass_id):
    print("adadadada")
    container = driver.find_element(By.CLASS_NAME, 'artdeco-modal__content')
    

    filter_title_9 = container.find_element(By.XPATH, f'//label[@for="advanced-filter-title-{job_title_inputclass_id}"]')
    filter_title_9.click()

def confirmFilter(driver):
    """confirm the filter"""
    confirm_button = driver.find_element(By.CLASS_NAME, 'search-reusables__secondary-filters-show-results-button')
    confirm_button.click()


def addJobs(driver, Jobs):
    """add jobs to the Jobs list"""
    
    # the sleep is to prevent the program from crashing because of the website loading time
    # and to minimize the risk of getting detected as a bot 🤖


    # pagination container artdeco-pagination__pages
    # get the pages
    
    # ⬇️ this try except is because some job title filters have only one page show the pages buttons dont show
    try:
        pages = driver.find_element(By.CLASS_NAME, 'artdeco-pagination__pages')
        pages = pages.find_elements(By.TAG_NAME, 'li')
        pagesLength = len(pages)
    except:
        pagesLength = 1
    
    for i in range(1,pagesLength+1):
        # 🐞🐞🐞🐞 this was to prevent crashing the program because of bug in the linked in website
        # the bug shows pages buttons more than the actual pages, when you reach for example page 5 it realizes that there are no more pages to show
        # the pages buttons after five desapear and the program crashes because it tries to click on the page 6 button that doesn't exist
        try:
            # get the li of data-test-pagination-page-btn="i"
            page = driver.find_element(By.XPATH, f'//li[@data-test-pagination-page-btn="{i}"]')
            page.click()
        except:
            # this is to check if the page is the last page or its just the first and last one
            if i == 1:
                pass
            else:
                break
            
        sleep(2)
        # upper jobs container that contains the jobs scroll jobs-search-results-list
        jobsUpperScrollerContainer = driver.find_element(By.CLASS_NAME, 'jobs-search-results-list')
        # scroll to the bottom of jobsUpperScrollerContainer
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", jobsUpperScrollerContainer)

        sleep(2)
        # get the jobs for the current page
        jobsContainer = driver.find_element(By.CLASS_NAME, 'scaffold-layout__list-container')

        # get the jobs li !!DIRECTLY!! inside the container by using the class jobs-search-results__list-item not the tagname 
        jobs = jobsContainer.find_elements(By.CLASS_NAME, 'jobs-search-results__list-item')
        for job in jobs:
            
            # click the job
            job.click()        
    
            while True:
                try:
                    jobsDetailsContainer = driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__primary-description-without-tagline')

                    title = driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-title-link').text

                    company = jobsDetailsContainer.text.split('·')[0]

                    location =  jobsDetailsContainer.text.split('·')[1]
                    # getting only the city
                    location = location.split(',')[0]
                    applicants = jobsDetailsContainer.text.split('·')[3]
                    condition = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/ul/li[1]/span/span[1]').text
                    condition = condition.split("\n")[0]
                    time = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[3]/ul/li[1]/span/span[2]').text
                    
                    # click the button //*[@id="how-you-match-card-container"]/section[2]/button wait for a sec and loop through the li's inside div with class job-details-skill-match-modal__content and get the text of every first div inside of the li save it in a list
                    
                    # scroll down inside the class jobs-search__job-details--wrapper
                    

                    driver.find_element(By.XPATH, '//*[@id="how-you-match-card-container"]/section[2]/div/button').click()
                    sleep(1)
                    skills = driver.find_element(By.CLASS_NAME, 'job-details-skill-match-modal__content')
                    skills = skills.find_elements(By.TAG_NAME, 'li')
                    skillsList = []
                    for skill in skills:
                        skillsList.append(skill.find_element(By.TAG_NAME, 'div').text)
                    sleep(0.5)
                    driver.find_element(By.CLASS_NAME, 'artdeco-modal__dismiss').click()
                    
                    
                    currentJobsData = {
                        'title': driver.find_element(By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-title-link').text,
                        'company': company,
                        'location': location,
                        'applicants': applicants,
                        'condition': condition,
                        'time': time,
                        'skills': skillsList
                        
                        
                    }
                    sleep(0.7)
                    break
                except:
                    continue
            print(currentJobsData)
            # scroll the length of a job  into jobsUpperScrollerContainer 
            # 🐞🐞🐞 this is to prevent a bug causing the selection of the same job twice
            driver.execute_script("arguments[0].scrollTop += 200", jobsUpperScrollerContainer)


            Jobs.append(currentJobsData)




    return Jobs




def process_job_title(driver, job_id, job_title):
    """
    This function processes a job title by applying filters, retrieving job counts, and adding jobs.

    Parameters:
    driver (webdriver instance): The webdriver instance to interact with the webpage.
    job_id (int): The id of the job title to process.
    job_title (str): The title of the job.

    Returns:
    dict: A dictionary where the keys are 'jobtitle' and 'jobs', and the values are the job title and the list of jobs, respectively.
    """
    # Open filter
    openFilter(driver)
    sleep(3)

    # Filter by job title
    filterByJobTitle(driver, job_id)
    sleep(1)
    confirmFilter(driver)
    sleep(2)

    # Get the number of jobs found after filtering
    jobs_count = getJobsCount(driver)
    jobs = addJobs(driver, [])

    # Clear the job filter
    openFilter(driver)
    sleep(2)
    filterByJobTitle(driver, job_id)
    sleep(1)
    confirmFilter(driver)
    

    return {'jobtitle': job_title, 'jobs': jobs}



def main():
    # init driver
    website = "https://www.linkedin.com"
    options=webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("user-data-dir=C:\\Users\\bechir\\AppData\\Local\\Google\\Chrome\\User Data")
    driver = webdriver.Chrome(options=options)

    # Maximize window
    driver.maximize_window()

    # wait for everything to load
    driver.get(website)

    # login

    # i skipped the login because i am using the chrome profile that is already logged in
    # login(driver)

    # go to jobs
    driver.get("https://www.linkedin.com/jobs/search/")

    # --------------------------------------------------------------------------------------------------------  #



    # a list of jobs dicts
    data = []

    
    generalData = {}
    # get the number of jobs found without filtering
    jobs_count = getJobsCount(driver)
    generalData['jobs_count'] = jobs_count

    # open filter
    # wait for the filter to load
    sleep(2)

    openFilter(driver)
    sleep(2)
    filterByIndutries(driver)
    
    confirmFilter(driver)


    # List of job title ids and corresponding titles
    # according to linkedin website html
    job_ids_titles = {
        26: "Marketing Manager",
        39: "Senior Software Engineer",
        25201: "Full Stack Engineer",
        9: "Software Engineer",
        32: "System Engineer",
        25194: "Backend Developer",
        761: "Information Technology Architect",
        1510: "Automation Engineer",
        115: "Information Technology Technology",
        369: "Technical Support Engineer"
    }

    # Process each job title
    Jobs = []
    for job_id, job_title in job_ids_titles.items():
        sleep(2)
        try:
            Jobs.append(process_job_title(driver, job_id, job_title))
        except Exception as e:
            print(f"Error processing job title '{job_title}': {str(e)}")
            continue

    # Save data to JSON file
    with open('jobs.json', 'w') as file:
        json.dump(Jobs, file, indent=4)

main()