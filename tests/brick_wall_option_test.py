import pytest
from typing import Dict, List
from assertpy import assert_that

from tests.utils import get_mock_flow, load_script_for_option, assert_headers_equal, get_all_header_names
from tests.data_helper import TestTrackingDomainData

from src.options import get_option_by_title

@pytest.fixture(scope="class")
def brick_wall_script(request: pytest.FixtureRequest) -> None:
    return load_script_for_option(get_option_by_title("Brick wall"))

class TestBrickWallOption:
    ALLOWED_HEADERS: List[str] = get_option_by_title("Brick wall").allowedHeaders
    OVERRIDEN_HEADERS: Dict[str, str] = get_option_by_title("Brick wall").headerOverrides
    HEADERS = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}

    def test_brick_wall_option_removes_all_headers(self, brick_wall_script) -> None:
        # Removes all headers
        # Arrange
        request_headers = {str(k): "AA" for k in get_all_header_names()}
        flow = get_mock_flow(request_headers, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)

        # Act
        brick_wall_script.request(flow)

        # Assert
        assert_that(flow.response).is_none()
        assert_that(flow.request.headers).is_empty()

    def test_brick_wall_option_tracker_domain_blocking(self, brick_wall_script) -> None:
        # Should block tracker domain
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_URL)
        
        # Act
        brick_wall_script.request(flow)

        # Assert
        assert_that(flow.response).is_not_none()
        assert_that(flow.response.status_code).is_equal_to(403)

    def test_brick_wall_option_tracker_pattern_blocking(self, brick_wall_script) -> None:
        # Should block tracking pattern
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_URL)

        # Act
        brick_wall_script.request(flow)

        # Assert
        assert_that(flow.response).is_not_none()
        assert_that(flow.response.status_code).is_equal_to(403)

    def test_brick_wall_option_normal_domain_not_blocked(self, brick_wall_script) -> None:
        # Should not block normal domain
        # Arrange
        flow = get_mock_flow(self.HEADERS, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)

        # Act
        brick_wall_script.request(flow)

        # Assert
        assert_that(flow.response).is_none()

