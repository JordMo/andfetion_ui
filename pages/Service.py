from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec

from library.core.TestLogger import TestLogger
from pages.components.Footer import FooterPage
from datetime import datetime
from pages.contacts.Contacts import ContactsPage


class ServicePage(FooterPage):
    """主页 - 军运服务"""

    ACTIVITY = 'com.cmic.module_main.ui.activity.HomeActivity'

    __locators = {
        '军运服务': (MobileBy.XPATH, '//*[@resource-id ="com.cmic.junyuntong:id/img_logo" and @text ="军运服务"]'),
        '进度条':(MobileBy.ID,'com.cmic.junyuntong:id/progressBar_main_enterprise'),
        '应用标题':(MobileBy.ID,'com.cmic.junyuntong:id/tv_title_actionbar'),
        '展开':(MobileBy.ID,'com.cmic.junyuntong:id/tv_expanded'),
        '加载中':(MobileBy.ID,'com.cmic.junyuntong:id/img_loading')
    }

    @TestLogger.log()
    def is_on_this_page(self):
        """当前页面是否在军运服务页"""

        try:
            self.wait_until(
                timeout=15,
                auto_accept_permission_alert=True,
                condition=lambda d: self._is_element_present(self.__class__.__locators["军运服务"])
            )
            return True
        except:
            return False

    @TestLogger.log()
    def wait_for_page_load(self, timeout=30, auto_accept_alerts=True):
        """等待军运服务页面加载（自动允许权限）"""
        try:
            self.wait_until(
                timeout=timeout,
                auto_accept_permission_alert=auto_accept_alerts,
                condition=lambda d: self._is_element_present(self.__class__.__locators["军运服务"])
            )
        except:
            message = "页面在{}s内，没有加载成功".format(str(timeout))
            raise AssertionError(
                message
            )
        return self

    @TestLogger.log('打开应用通过名字')
    def open_by_name(self, name, title=''):
        app_name = (MobileBy.XPATH, '//*[@resource-id ="com.cmic.junyuntong:id/tv_name" and @text ="%s"]' % name)
        self.swipe_by_percent_on_screen(50, 30, 50, 70, 700)
        if not self._is_element_present(app_name):
            self.click_element(self.__class__.__locators['展开'])
            current = 0
            while current < 3:
                if self._is_element_present(app_name):
                    break
                current += 1
                self.swipe_by_percent_on_screen(50, 70, 50, 30, 700)
        start = datetime.now().timestamp()
        self.click_element(app_name)

        try:
            self.wait_until(
                timeout=60,
                auto_accept_permission_alert=True,
                condition=lambda d: not self._is_element_present(self.__class__.__locators["加载中"])
            )
            end = datetime.now().timestamp()
            duration = round(end - start, 3)
        except Exception as e:
            duration = 30
            print('查找进度条报错.', e)

        print('%s应用的打开时延为%s秒' % (name, duration))
        if duration == 30:
            result = 'ERROR'
        else:
            result = self.assert_title(name)

        from settings.setting import connect_db
        try:
            conn, cursor = connect_db()
        except Exception as e:
            print("connect db fail")
        sql = """
                INSERT INTO mwg_result (case_name,duration,status,remark)
                VALUES ("%s","%s","%s","%s");
                """ % (name, duration, result, '')
        print(sql)

        try:
            cursor.execute(sql)
            print("insert data success")
            conn.commit()
            cursor.close()
            conn.close()
            print("close db success")
        except Exception as e:
            print("insert data fail")
            print(e)
            cursor.close()
            conn.close()
            print("close db success")

        return result

    @TestLogger.log('断言标题是否一致')
    def assert_title(self, name):
        try:
            self.wait_until(condition=lambda d: self.get_element(self.__locators.get('应用标题')))
            return self.element_text_should_be(self.__locators.get('应用标题'), name)
        except:
            return "ERROR"


if __name__ == '__main__':
    print(datetime.now())
    import time
    time.sleep(1)
    print(datetime.now())