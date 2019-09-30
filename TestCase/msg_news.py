from library.core.TestCase import TestCase
from pages import MessagePage, SingleChatPage
from pages.Service import ServicePage
from pages.components import BaseChatPage
from preconditions.BasePreconditions import LoginPreconditions, SelectLocalContactsPage
from library.core.utils.applicationcache import *
from time import sleep

class Preconditions(LoginPreconditions):

    @staticmethod
    def enter_single_chat_page(name):
        """进入单聊聊天会话页面"""
        mp = MessagePage()
        mp.wait_for_page_load()
        # 点击发起聊天
        mp.click_add_icon()
        # 点击搜索
        slc = SelectLocalContactsPage()
        slc.wait_for_page_load()
        # 进入单聊会话页面
        slc.input_search_keyword(name)
        slc.selecting_local_contacts_by_name(name)
        scp = SingleChatPage()
        # 等待单聊会话页面加载
        scp.wait_for_page_load()


class MWGMsgNewsTest(TestCase):
    """消息"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile("Android-移动")
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    def default_setUp(self):
        """确保每个用例运行前在消息页面"""
        mess = MessagePage()
        if mess.is_on_this_page():
            return
        else:
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    def test_C001_is_install(self):
        is_install=current_mobile().is_app_installed("com.cmic.junyuntong")
        self.assertEqual(True,is_install)

    def test_C002_open_service(self):
        """打开军运服务"""
        msgp= MessagePage()
        msgp.open_workbench_page()
        sleep(3)
        self.assertEqual(True,msgp.is_element_exit_("军运服务"))

class MWGServiceTest(TestCase):
    """军运服务"""

    @classmethod
    def setUpClass(cls):
        Preconditions.select_mobile("Android-移动")
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    def default_setUp(self):
        """确保每个用例运行前在军运服务页面"""
        serp = ServicePage()
        messp = MessagePage()

        if serp.is_on_this_page():
            return
        else:
            if messp.is_on_this_page():
                serp.open_workbench_page()
                return
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()


    def test_C001_ZCJY(self):
        """智闯军运"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('智闯军运'))
        serp.click_back_by_android()

    def test_C002_ZXYXH(self):
        """知行英雄汇"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('知行英雄汇'))
        serp.click_back_by_android()

    def test_C003_JYZAS(self):
        """军运障碍赛"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('军运障碍赛'))
        serp.click_back_by_android()

    def test_C004_MORE(self):
        """更多好玩"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('更多好玩'))
        serp.click_back_by_android()

    def test_C005_WHTQ(self):
        """武汉天气"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('武汉天气'))
        serp.click_back_by_android()

    def test_C006_JTZY(self):
        """交通指引"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('交通指引'))
        serp.click_back_by_android()

    def test_C007_CYZY(self):
        """餐饮指引"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('餐饮指引'))
        serp.click_back_by_android()

    def test_C008_WZWH(self):
        """玩转武汉"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('玩转武汉'))
        serp.click_back_by_android()

    def test_C009_HMNC(self):
        """和玛挪车"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('和玛挪车'))
        serp.click_back_by_android()

    def test_C010_JYLY(self):
        """军运留言"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('军运留言'))
        serp.click_back_by_android()

    def test_C012_5GKYH(self):
        """5G看樱花"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('5G看樱花'))
        serp.click_back_by_android()

    def test_C013_HSH(self):
        """和生活"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('和生活'))
        serp.click_back_by_android()

    def setUp_test_C014_FWTT(self):
        """展开"""
        serp = ServicePage()
        messp = MessagePage()

        if serp.is_on_this_page():
            return
        else:
            if messp.is_on_this_page():
                serp.open_workbench_page()
                return
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()

    def test_C014_FWTT(self):
        """飞闻头条"""
        serp = ServicePage()
        self.assertEqual(True,serp.open_by_name('飞闻头条'))
        serp.click_back_by_android()

class SinglechatTest(TestCase):
    """消息-单聊"""

    def default_setUp(self):
        """确保每个用例运行前在单聊会话页面"""
        name = "Jord5477"
        mp = MessagePage()
        scp = SingleChatPage()
        if scp.is_on_this_page():
            current_mobile().hide_keyboard_if_display()
        else:
            if mp.is_on_this_page():
                Preconditions.enter_single_chat_page(name)
                return
            current_mobile().launch_app()
            Preconditions.make_already_in_message_page()
            Preconditions.enter_single_chat_page(name)

    @classmethod
    def setUpClass(cls) -> None:
        Preconditions.select_mobile("Android-移动")
        current_mobile().hide_keyboard_if_display()
        Preconditions.make_already_in_message_page()

    def test_C001_send_text(self):
        """发送文本"""
        text='哈'*100
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.input_message(text)
        # 发送消息
        scp.send_message()

    def test_C002_send_expression(self):
        """发送表情"""
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.select_expression(5)
        scp.close_chat_expression()
        scp.send_message()

    def test_C003_send_pic(self):
        """发送图片"""
        scp = SingleChatPage()
        scp.wait_for_page_load()
        scp.click_picture()
        scp.select_items_by_given_orders(1,2)
        scp.click_element_('发送')
