from assertpy import assert_that

from tests.utils import get_mock_flow, get_mock_request, MockFlow, MockRequest, _load_script_for_option
from tests.data_helper import TestTrackingDomainData
from src.options import get_option_by_title

PASSTHROUGH_OPTION = get_option_by_title("Passthrough")

def test_passthrough_option() -> None:
    script = _load_script_for_option(PASSTHROUGH_OPTION)

    # All headers allowed, nothing blocked
    headers = {"user-agent": "ua", "cookie": "c", "x-custom": "v"}
    flow = get_mock_flow(headers, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_NOT_TRACKING_DOMAIN_URL)
    script.request(flow)
    assert_that(flow.request.headers).contains("user-agent").contains("cookie").contains("x-custom")
    assert_that(flow.response).is_none()
    # Should not block tracker domain
    flow = get_mock_flow(headers, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_DOMAIN_URL)
    script.request(flow)
    assert_that(flow.response).is_none()
    # Should not block tracking pattern
    flow = get_mock_flow(headers, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_HOST, TestTrackingDomainData.TEST_COMMON_TRACKING_PATTERN_URL)
    script.request(flow)
    assert_that(flow.response).is_none()