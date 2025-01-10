import os
import scrapy
import time
import json
import scrapy
import re
import uuid
from scrapy.http import Response
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from spiders.util import file_util, cookie_util
from spiders.models.Course import Course
from spiders.models.Lesson import Lesson
from spiders.models.lesson_transcript import LessonTranscript
from spiders.models.lesson_note import LessonNote
from spiders.models.dialogue_data import Diaglogue
from spiders.models.dialogue_type import Dialogue_Type
from selenium import webdriver



class KoreanSpider(scrapy.Spider):
    name = 'crawl_data'
    allowed_domains = ["koreanclass101.com", "s3.amazonaws.com"]
    start_urls = [
        'https://www.koreanclass101.com'
    ]
    cookies_dict = cookie_util.get_cookies()

    def start_requests(self):
        # print(">>>CHECKING_COOKIES", self.cookies_dict)

        urls = "https://www.koreanclass101.com/lesson-library/3-minute-korean-greetings-and-useful-phrases"
        yield SeleniumRequest(url=urls,
                              callback=self.parse,
                              cookies = self.cookies_dict)

        # try:
        #     with open("cookies.json", "r") as file:
        #         cookies = json.load(file)

        #     # Convert cookies to Scrapy format
        #     scrapy_cookies = {cookie["name"]: cookie["value"] for cookie in cookies}

        #     print('chua click 1', scrapy_cookies)
        #     # scrapy_cookies = cookie_util.get_cookies()

        #     # Send request with cookies
        #     for url in urls:
        #         yield scrapy.Request(
        #             url=url,
        #             cookies=scrapy_cookies,
        #             callback=self.parse
        #         )
        # except FileNotFoundError:
        #     self.log("Cookies file not found. Please run the login spider first.")
        # except json.JSONDecodeError:
        #     self.log("Failed to load cookies. Please ensure the cookies file is valid.")

    def parse(self, response):
        # driver = response.request.meta['driver']

        driver = webdriver.Chrome()
        
        driver.get(response.url)

        for cookie in response.request.cookies:
            driver.add_cookie({
                'name': cookie,
                'value': response.request.cookies[cookie],
                'domain': response.url.split('/')[2],  # Extract domain from the URL
                'path': '/'  # Set path
            })
        #     print(f'<<<<<<< {cookie} : {response.request.cookies[cookie]} >>>>>>')
        time.sleep(3)
        driver.refresh()
        time.sleep(15)

        course_title = driver.find_element(
            By.CLASS_NAME, "_pathway__title_1o1rh_21").text

        course_description = driver.find_element(
            By.CLASS_NAME, "_pathway__subtitle_1o1rh_28").text

        course = Course(
            name=course_title, description=course_description, total_lesson=1, course_id="hehe")

        list_lesson = response.xpath(
            "//div[@class='_lesson_1h6vq_1 _is_disabled_1h6vq_14']")[:1]

        for lesson in list_lesson:
            try:
                lesson_title = lesson.xpath(".//a/div/h2/text()").get()
                lesson_description = lesson.xpath(".//a/div/p/text()").get()
                lesson_media_type = lesson.xpath(
                    ".//a/div/div/div[@class='_lesson__type_1h6vq_111']/text()").get()
                # media_length = lesson.xpath(
                #     ".//a/div/div/div[@class = '_lesson__option_1h6vq_111']/text()").get()
                # print(">>>CHECKING1:", media_length)

                lesson_url = lesson.xpath(".//a/@href").get()

                lesson = Lesson(
                    name=lesson_title,
                    description=lesson_description,
                    course_media_type=lesson_media_type
                )

                driver.get(response.urljoin(lesson_url))

                yield from self.get_dialog_korean(driver, response, lesson)
                time.sleep(10)
                # yield from self.get_lesson_transcript(driver, response, lesson)
                # time.sleep(5)
                # yield from self.get_lesson_notes(driver, response, lesson)
                # time.sleep(5)
                course.add_lesson(lesson)

            except Exception as e:
                print("Captcha HEHE")

        file_util.to_json('data.json', course)
        driver.quit()
    
    def get_dialog_korean(self, driver,response, lesson):
        print('click ALl unsuccess')
        try:
            btn_dialogue = driver.find_element(By.XPATH, '//*[@id="dialogue_tab_all_0"]')
            btn_dialogue.click()
            print('click ALl success')
        except Exception as e:
            self.logger.error(f"Dialogue button not found: {e}")

        try: 
            type_dialogs = driver.find_elements(By.XPATH, '//*[@id="dialogue_panel_all_0"]/h3')
            print(">>>CHECK", type_dialogs)
           
            list_dialogue_type = []
            for type_dialog in type_dialogs:
            # dialog
                type = type_dialog.text
                print(">>>CHECK TYPE", type)
                dialogue_type = Dialogue_Type(title=type)
                dialogs = driver.find_elements(By.XPATH, '//*[@id="dialogue_panel_all_0"]/table/tbody')
                dialogue_data = []
                for dialog in dialogs:
                    dialogue_text = dialog.find_element(By.XPATH,'.//td[contains(@class, "lsn3-lesson-dialogue__td--text")]').text
                    diaolog_url_audio = dialog.find_element(By.XPATH,'.//button[contains(@class, "js-lsn3-play-dialogue")]').get_attribute("data-src")
                    print(">>>CHECKING PLS" + dialogue_text + "\t" + diaolog_url_audio)
                    dialogue = Diaglogue(
                                            content=dialogue_text,
                                            url= diaolog_url_audio,
                                            )

                    dialogue_data.append(dialogue)

                    lesson_title = lesson.name
                    
                    file_path = os.path.join(
                        file_util.clean_title(lesson_title), "audio")
                    


                    yield {
                        'file_urls': [diaolog_url_audio],
                        'file_name': str(uuid.uuid4()) +".mp3",
                        'file_path': file_path
                    }
                
                print("<<<<<<<<<<  dialogue_data", dialogue_data)
                dialogue_type.add_dialogue(dialogue_data)
                print("<<<<<<<<<<  dialogue_type", dialogue_type)
                list_dialogue_type.append(dialogue_type)

            
            # lesson.list_dialogue = list_dialogue_type
        except Exception as e:
            print(e)
        


    def get_lesson_transcript(self, driver, response, lesson):
        try:
            pdf_url = response.urljoin(driver.find_element(
                By.XPATH, '//*[@id="lsn3_lesson_transcript_section"]/div/div/div[2]/a').get_attribute('href'))

            transcript = self.clean_text(driver.find_element(
                By.ID, "lsn3-lesson-transcript-table").get_attribute('outerHTML'))

            lesson_transcript = LessonTranscript(
                content=transcript, url=pdf_url)

            lesson.lesson_transcript = lesson_transcript

            lesson_title = lesson.name

            # Save file
            file_name = file_util.extract_pdf_file_name_from_url(pdf_url)
            file_path = os.path.join(
                file_util.clean_title(lesson_title), "pdf")

            yield {
                'file_urls': [pdf_url],
                'file_name': file_name,
                'file_path': file_path
            }
        except Exception as e:
            print("Cant find lesson transcript")

    def get_lesson_notes(self, driver, response, lesson):
        try:
            lesson_focus = self.clean_text(driver.find_element(
                By.XPATH, "//*[@id='lsn3_lesson_notes_section']/div/div[1]").get_attribute('outerHTML'))
            cultural_insight = driver.find_element(
                By.XPATH, "//*[@id='lsn3_lesson_notes_section']/div/div[2]/p").text
            pdf_url = response.urljoin(driver.find_element(
                By.XPATH, '//*[@id="lsn3_lesson_notes_section"]/div/div[3]/div/a').get_attribute('href'))

            lesson_notes = LessonNote(
                lesson_focus=lesson_focus,
                cultural_insight=cultural_insight,
                url=pdf_url
            )

            lesson.lesson_notes = lesson_notes
            lesson_title = lesson.name

            file_name = file_util.extract_pdf_file_name_from_url(pdf_url)
            file_path = os.path.join(
                file_util.clean_title(lesson_title), "pdf")

            yield {
                'file_urls': [pdf_url],
                'file_name': file_name,
                'file_path': file_path
            }
        except Exception as e:
            print("Cant find lesson notes")

    # clean text

    def clean_text(self, text):
        return re.sub(r'\s+', ' ', text).strip() if text else None
