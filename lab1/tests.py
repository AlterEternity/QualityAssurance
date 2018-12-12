import unittest
# from unittest import mock
from unittest.mock import patch
from xcptnmgr import *
from parameterized import parameterized


class ExceptionmanagerInitTestCase(unittest.TestCase):
    def setUp(self):
        self.em = MyExceptionManager(FakeConfigGetter())

    def test_MyExceptionManager_Initialisation_Correct(self):
        assert self.em.noncritical_exception_counter() == 0, "noncritical_exception_counter was initialised as: %s but no 0" %\
                                                           str(self.em.noncritical_exception_counter())
        assert self.em.critical_exception_counter() == 0, "critical_exception_counter was initialised as: %s but no 0" % \
                                                        str(self.em.critical_exception_counter())


class ExceptionmanagerIsCriticalTestCase(unittest.TestCase):
    def setUp(self):
        self.em = MyExceptionManager()
        self.em.config_getter = FakeConfigGetter()

    def test_IsCritical_CriticalTypeErrorException_ReturnsTrue(self):
        e = TypeError()
        is_critical = self.em.is_critical(e)
        assert is_critical is True, "TypeError is not critical"

    def test_IsCritical_NonCriticalIndexErrorException_ReturnsFalse(self):
        e = IndexError()
        is_critical = self.em.is_critical(e)
        assert is_critical is False, "IndexError is critical"

    def test_IsCritical_InvalidType_RaiseTypeError(self):
        e = "IndexError"
        self.assertRaises(TypeError, self.em.is_critical, e)


class ExceptionmanagerProceedExceptionTestCase(unittest.TestCase):
    def setUp(self):
        pass
        # ReportSenderFactory.set_sender(FakeReportSender())
        # self.em = MyExceptionManager(FakeConfigGetter())

    @parameterized.expand([
        (TypeError(), ),
        (UnicodeError(), ),
        (ValueError(), ),
    ])
    def test_ProceedException_ProceedCriticalException_CriticalExceptionCounterIncrements(self, e=TypeError()):
        ReportSenderFactory.set_sender(FakeReportSender())
        self.em = MyExceptionManager(FakeConfigGetter())
        befor_exception_counter = self.em.critical_exception_counter()
        # e = TypeError()

        self.em.proceed_exception(e)

        assert self.em.critical_exception_counter() - befor_exception_counter == 1

    def test_ProceedException_ProceedNonCriticalException_NonCriticalExceptionCounterIncrements(self):
        ReportSenderFactory.set_sender(FakeReportSender())
        self.em = MyExceptionManager(FakeConfigGetter())
        befor_exception_counter = self.em.noncritical_exception_counter()
        e = IndexError()

        self.em.proceed_exception(e)

        assert self.em.noncritical_exception_counter() - befor_exception_counter == 1

    @parameterized.expand([
        (TypeError(),),
        (UnicodeError(),),
        (ValueError(),),
    ])
    def test_ProceedException_ProceedCriticalExceptionNoServerAnswer_ServerSendErrorCounterIncrements(self, e):
        ReportSenderFactory.set_sender(FakeReportSender(False))
        self.em = MyExceptionManager(FakeConfigGetter())

        self.em.proceed_exception(e)

        assert self.em.send_error_counter() == 1

    @parameterized.expand([
        (TypeError(),),
        (UnicodeError(),),
        (ValueError(),),
    ])
    @patch('xcptnmgr.IReportSender')
    def test_ProceedException_ProceedCriticalExceptionServerAnswerOK_ServerSendErrorCounterNotIncrements(self, e, mock_report_sender):
        mock_report_sender.send_exception_report.return_value = True
        ReportSenderFactory.set_sender(mock_report_sender)
        self.em = MyExceptionManager(FakeConfigGetter())

        self.em.proceed_exception(e)

        mock_report_sender.send_exception_report.assert_called_with(e)
        assert self.em.send_error_counter() == 0


if __name__ == '__main__':
    unittest.main()
