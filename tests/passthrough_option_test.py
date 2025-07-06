import pytest
from typing import Dict
from assertpy import assert_that

from tests.utils import get_mock_flow, load_script_for_option, assert_headers_equal
from tests.data_helper import TestTrackingDomainData

from src.options import get_option_by_title

@pytest.fixture(scope="class")
def passthrough_script(request: pytest.FixtureRequest) -> None:
    return load_script_for_option(get_option_by_title("Passthrough"))

class TestPassthroughOption:
    HEADERS = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}

    def test_passthrough_option_no_headers_modification(self, passthrough_script) -> None:
        # All headers allowed, no modifications
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)
        
        # Act
        passthrough_script.request(flow)

        # Assert
        assert_that(flow.response).is_none()
        assert_that(flow.request.headers).contains("user-agent").contains("cookie").contains("x-custom")
        assert_headers_equal(flow.request.headers, self.HEADERS)

    def test_passthrough_option_no_domain_blocking(self, passthrough_script) -> None:
        # Should not block tracker domain
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_URL)
        
        # Act
        passthrough_script.request(flow)

        # Assert
        assert_that(flow.response).is_none()

    def test_passthrough_option_no_pattern_blocking(self, passthrough_script) -> None:
        # Should not block tracking pattern
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_URL)

        # Act
        passthrough_script.request(flow)

        # Assert
        assert_that(flow.response).is_none()

    def test_passthrough_option_normal_domain_not_blocked(self, passthrough_script) -> None:
        # Should not block normal domain
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)

        # Act
        passthrough_script.request(flow)

        # Assert
        assert_that(flow.response).is_none()