import json


class IConfigGetter:
    def __init__(self, config_file=None):
        self.config_file = config_file

    def get_critical_exception_list(self):
        pass


class ConfigGetterFromFile(IConfigGetter):
    def get_config(self):
        ex_list = []
        with open(self.config_file, 'r') as f:
            ex_list = json.load(f)['critical_exception_list']
        ex_list = list(map(eval, ex_list))
        return ex_list


class FakeConfigGetter(IConfigGetter):
    def get_critical_exception_list(self):
        ex_list = [TypeError, UnicodeError, ValueError]
        return ex_list


class IReportSender:
    def send_exception_report(self, e):
        return True


class FakeReportSender(IReportSender):
    def __init__(self, ret_val=True):
        self.return_value = ret_val

    def send_exception_report(self, e):
        print(str(e))
        return self.return_value


class ReportSenderFactory:
    report_sender = None

    @classmethod
    def create(cls):
        if cls.report_sender:
            return cls.report_sender
        else:
            return IReportSender()

    @classmethod
    def set_sender(cls, sender):
        cls.report_sender = sender


class MyExceptionManager:

    def __init__(self, config_getter=None):
        self.__critical_exception_counter = 0
        self.__noncritical_exception_counter = 0
        self.__send_error_counter = 0
        self.report_sender = ReportSenderFactory.create()
        self.config_getter = config_getter

    def critical_exception_counter(self):
        return self.__critical_exception_counter

    def noncritical_exception_counter(self):
        return self.__noncritical_exception_counter

    def send_error_counter(self):
        return self.__send_error_counter

    def is_critical(self, e):
        if not isinstance(e, BaseException):
            raise TypeError()

        if type(e) in self.config_getter.get_critical_exception_list():
            return True

        return False

    def proceed_exception(self, e):
        if self.is_critical(e):
            self.__critical_exception_counter += 1
            if not self.send_exception_report(e):
                self.__send_error_counter += 1
        else:
            self.__noncritical_exception_counter += 1
        return

    def send_exception_report(self, e):
        return self.report_sender.send_exception_report(e)
