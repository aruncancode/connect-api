from .. import HOMEPAGE_LINK, By, WebDriverWait, EC
from datetime import datetime


class HomePage:
    def __init__(self, parent):
        self.__parent = parent
        self.__goToHomePage()
        self.__lastUpdate = datetime.now()

    def __goToHomePage(self):
        self.__parent.get(HOMEPAGE_LINK)

    lastUpdate = property(lambda self: self.__lastUpdate)

    def getLatestNotice(self):
        readButtonXPATH = '//*[@id="v-latestinformationportlet_WAR_connectrvportlet_INSTANCE_WqBA68MkuxAs_LAYOUT_215"]/div/div[2]/div/div[1]/div[2]/span/span'
        WebDriverWait(self.__parent.browser, 20).until(
            EC.presence_of_element_located((By.XPATH, readButtonXPATH,))
        )
        self.__parent.browser.find_element(By.XPATH, readButtonXPATH,).click()

        noticeXPATH = '//*[@id="v-latestinformationportlet_WAR_connectrvportlet_INSTANCE_WqBA68MkuxAs_LAYOUT_215-overlays"]/div[3]/div/div/div[3]/div/div/div'
        noticeBodyXPATH = f"{noticeXPATH}[1]/div/div/div"
        WebDriverWait(self.__parent.browser, 15).until(
            EC.presence_of_element_located((By.XPATH, noticeBodyXPATH))
        )
        body = self.__parent.browser.find_element(By.XPATH, noticeBodyXPATH)
        title = body.find_element(By.XPATH, "./div[1]").text
        author = body.find_element(
            By.XPATH, "./div[2]/div[1]/div[2]/div/div[1]/div[1]/div[1]",
        ).text
        authorType = body.find_element(
            By.XPATH, "./div[2]/div[1]/div[2]/div/div[1]/div[2]/div",
        ).text
        rawBody = body.find_element(
            By.XPATH, "./div[2]/div[3]/div[2]/div[1]"
        ).get_attribute("innerHTML")
        views = int(
            body.find_element(
                By.XPATH,
                "./div[2]/div[3]/div[2]/div[3]/div[1]/div[2]/div[1]/div[2]",
            ).text
        )
        from .notice import Notice

        time = Notice.parseTime(
            body.find_element(
                By.XPATH, "./div[2]/div[1]/div[2]/div/div[1]/div[1]/div[3]",
            ).text
        )
        self.__parent.browser.find_element(
            By.XPATH, f"{noticeXPATH}[3]/div[1]"
        ).click()
        WebDriverWait(self.__parent.browser, 10).until(
            EC.url_contains(
                "https://connect.det.wa.edu.au/group/students/ui/class/announcements"
            )
        )
        link = self.__parent.browser.current_url.split("#")[0]
        self.__goToHomePage()
        return Notice(title, author, authorType, rawBody, views, time, link)

    def getNextSubmissions(self):
        # TODO: FIX This will break if you don't have three submissions coming up.
        submissionsBoxXPATH = '//*[@id="v-nextsubmissionportlet_WAR_connectrvportlet_INSTANCE_hxAR8l8SbS5Q_LAYOUT_215"]/div/div[2]/div'
        submissionElementsXPATH = f"{submissionsBoxXPATH}/div[2]/div/div"

        def openMore():
            WebDriverWait(self.__parent.browser, 20).until(
                EC.presence_of_element_located((By.XPATH, submissionsBoxXPATH))
            )
            self.__parent.browser.find_element(
                By.XPATH, f"{submissionsBoxXPATH}/div[1]/div[2]"
            ).click()
            WebDriverWait(self.__parent.browser, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"{submissionElementsXPATH}[2]/div/div")
                )
            )

        openMore()
        submissions = []
        from .submission import Submission

        for i in range(2, 5):
            self.__parent.browser.find_element(
                By.XPATH, f"{submissionElementsXPATH}[{i}]/div/div"
            ).click()
            viewButtonXPATH = '//*[@id="v-nextsubmissionportlet_WAR_connectrvportlet_INSTANCE_hxAR8l8SbS5Q_LAYOUT_215-overlays"]/div[3]/div/div/div[3]/div/div/div[2]'
            WebDriverWait(self.__parent.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, viewButtonXPATH))
            )
            self.__parent.browser.find_element(
                By.XPATH, viewButtonXPATH
            ).click()
            WebDriverWait(self.__parent.browser, 20).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="v-submissionportlet_WAR_connectrvportlet_INSTANCE_IQdBhuiMMrFp_LAYOUT_248"]/div/div[2]/div[3]/div/div[2]/div[1]',
                    )
                )
            )
            submissions.append(
                Submission(
                    self.__parent,
                    self.__parent.browser.current_url.split("#")[0],
                )
            )
            self.__goToHomePage()
            openMore()

        return submissions
