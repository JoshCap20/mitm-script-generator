import pytest
from typing import Dict, List
from assertpy import assert_that

from tests.utils import get_mock_flow, load_script_for_option, assert_headers_equal, get_all_header_names
from tests.data_helper import TestTrackingDomainData

from src.options import get_option_by_title

@pytest.fixture(scope="class")
def fort_knox_script(request: pytest.FixtureRequest) -> None:
    return load_script_for_option(get_option_by_title("Fort Knox"))

class TestFortKnoxOption:
    ALLOWED_HEADERS: List[str] = get_option_by_title("Fort Knox").allowedHeaders
    OVERRIDEN_HEADERS: Dict[str, str] = get_option_by_title("Fort Knox").headerOverrides
    HEADERS = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}

    def test_fort_knox_option_removes_all_headers(self, fort_knox_script) -> None:
        # Removes all headers
        # Arrange
        request_headers = {str(k): "AA" for k in get_all_header_names()}
        flow = get_mock_flow(request_headers, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)

        # Act
        fort_knox_script.request(flow)

        # Assert
        assert_that(flow.request.headers).is_empty()

    def test_fort_knox_option_tracker_domain_blocking(self, fort_knox_script) -> None:
        # Should block tracker domain
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_URL)
        
        # Act
        fort_knox_script.request(flow)

        # Assert
        assert_that(flow.response).is_not_none()
        assert_that(flow.response.status_code).is_equal_to(403)

    def test_fort_knox_option_tracker_pattern_blocking(self, fort_knox_script) -> None:
        # Should block tracking pattern
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_URL)

        # Act
        fort_knox_script.request(flow)

        # Assert
        assert_that(flow.response).is_not_none()
        assert_that(flow.response.status_code).is_equal_to(403)

    def test_fort_knox_option_all_domains_blocked(self, fort_knox_script) -> None:
        # Should block all domains
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)

        # Act
        fort_knox_script.request(flow)

        # Assert
        assert_that(flow.response).is_not_none()
        assert_that(flow.response.status_code).is_equal_to(403)

