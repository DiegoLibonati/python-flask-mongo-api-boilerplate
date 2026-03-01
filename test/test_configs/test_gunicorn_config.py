import multiprocessing

import src.configs.gunicorn_config as gunicorn_config


class TestGunicornConfigBind:
    def test_bind_is_string(self) -> None:
        assert isinstance(gunicorn_config.bind, str)

    def test_bind_value(self) -> None:
        assert gunicorn_config.bind == "0.0.0.0:5050"

    def test_bind_contains_host(self) -> None:
        assert "0.0.0.0" in gunicorn_config.bind

    def test_bind_contains_port(self) -> None:
        assert "5050" in gunicorn_config.bind


class TestGunicornConfigWorkers:
    def test_workers_is_int(self) -> None:
        assert isinstance(gunicorn_config.workers, int)

    def test_workers_formula(self) -> None:
        expected = multiprocessing.cpu_count() * 2 + 1
        assert gunicorn_config.workers == expected

    def test_workers_is_positive(self) -> None:
        assert gunicorn_config.workers > 0


class TestGunicornConfigThreads:
    def test_threads_is_int(self) -> None:
        assert isinstance(gunicorn_config.threads, int)

    def test_threads_value(self) -> None:
        assert gunicorn_config.threads == 2

    def test_threads_is_positive(self) -> None:
        assert gunicorn_config.threads > 0


class TestGunicornConfigTimeouts:
    def test_timeout_is_int(self) -> None:
        assert isinstance(gunicorn_config.timeout, int)

    def test_timeout_value(self) -> None:
        assert gunicorn_config.timeout == 120

    def test_graceful_timeout_is_int(self) -> None:
        assert isinstance(gunicorn_config.graceful_timeout, int)

    def test_graceful_timeout_value(self) -> None:
        assert gunicorn_config.graceful_timeout == 30

    def test_graceful_timeout_less_than_timeout(self) -> None:
        assert gunicorn_config.graceful_timeout < gunicorn_config.timeout


class TestGunicornConfigLogging:
    def test_accesslog_is_string(self) -> None:
        assert isinstance(gunicorn_config.accesslog, str)

    def test_accesslog_value(self) -> None:
        assert gunicorn_config.accesslog == "-"

    def test_errorlog_is_string(self) -> None:
        assert isinstance(gunicorn_config.errorlog, str)

    def test_errorlog_value(self) -> None:
        assert gunicorn_config.errorlog == "-"

    def test_loglevel_is_string(self) -> None:
        assert isinstance(gunicorn_config.loglevel, str)

    def test_loglevel_value(self) -> None:
        assert gunicorn_config.loglevel == "info"

    def test_loglevel_is_valid(self) -> None:
        valid_levels = {"debug", "info", "warning", "error", "critical"}
        assert gunicorn_config.loglevel in valid_levels


class TestGunicornConfigProcName:
    def test_proc_name_is_string(self) -> None:
        assert isinstance(gunicorn_config.proc_name, str)

    def test_proc_name_value(self) -> None:
        assert gunicorn_config.proc_name == "template-server"

    def test_proc_name_is_not_empty(self) -> None:
        assert gunicorn_config.proc_name
