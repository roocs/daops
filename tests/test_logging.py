import sys

import pytest
from daops.utils.common import _logging_examples
from daops.utils.common import enable_logging

from tests._common import ContextLogger


class TestLoggingFuncs:
    @pytest.mark.xfail(
        reason="pytest-loguru does not implement logging levels for caplog yet."
    )
    def test_logging_configuration(self, caplog):
        with ContextLogger(caplog):
            caplog.set_level("WARNING", logger="daops")

            _logging_examples()  # noqa

            assert ("daops.utils.common", 10, "1") not in caplog.record_tuples
            assert ("daops.utils.common", 40, "4") in caplog.record_tuples

    def test_disabled_enabled_logging(self, capsys):
        with ContextLogger() as _logger:
            _logger.disable("daops")

            # DAOPS disabled
            _logger.add(sys.stderr, level="WARNING")
            _logger.add(sys.stdout, level="INFO")

            _logging_examples()  # noqa

            captured = capsys.readouterr()
            assert "WARNING" not in captured.err
            assert "INFO" not in captured.out

            # re-enable DAOPS logging
            _logger.enable("daops")

            _logging_examples()  # noqa

            captured = capsys.readouterr()
            assert "INFO" not in captured.err
            assert "WARNING" in captured.err
            assert "INFO" in captured.out

    def test_logging_enabler(self, capsys):
        with ContextLogger():
            _logging_examples()  # noqa

            captured = capsys.readouterr()
            assert "WARNING" not in captured.err
            assert "INFO" not in captured.out

            enable_logging()

            _logging_examples()  # noqa

            captured = capsys.readouterr()
            assert "INFO" not in captured.err
            assert "WARNING" in captured.err
            assert "INFO" in captured.out
