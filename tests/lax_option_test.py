import pytest
from assertpy import assert_that

from tests.utils import get_mock_flow, load_script_for_option, assert_headers_equal
from tests.data_helper import TestTrackingDomainData

from src.options import get_option_by_title

@pytest.fixture(scope="class")
def lax_script(request: pytest.FixtureRequest) -> None:
    return load_script_for_option(get_option_by_title("Lax"))

class TestLaxOption:
    HEADERS = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}

    def test_lax_option_no_headers_modification(self, lax_script) -> None:
        # Should not modify any headers
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)
        
        # Act
        lax_script.request(flow)

        # Assert
        assert_that(flow.response).is_none()
        assert_that(flow.request.headers).contains("user-agent").contains("cookie").contains("x-custom")
        assert_headers_equal(flow.request.headers, self.HEADERS)

    def test_lax_option_tracker_domain_blocking(self, lax_script) -> None:
        # Should block tracker domain
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_URL)
        
        # Act
        lax_script.request(flow)

        # Assert
        assert_that(flow.response).is_not_none()
        assert_that(flow.response.status_code).is_equal_to(403)

    def test_lax_option_tracker_pattern_blocking(self, lax_script) -> None:
        # Should block tracking pattern
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_URL)
        
        # Act
        lax_script.request(flow)

        # Assert
        assert_that(flow.response).is_not_none()
        assert_that(flow.response.status_code).is_equal_to(403)

    def test_lax_option_normal_domain_not_blocked(self, lax_script) -> None:
        # Should not block normal domain
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)

        # Act
        lax_script.request(flow)

        # Assert
        assert_that(flow.response).is_none()