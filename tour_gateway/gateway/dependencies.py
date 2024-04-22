from enum import Enum

from tour_shared.responses import JSONResponse


class UninitializedRegionAction(Enum):
    RESPONSE_404 = "RESPONSE_404"  # response with 404 status code
    RESPONSE_EMPTY_LIST = "RESPONSE_EMPTY_LIST"  # response with 200 empty list
    INITIALIZE_REGION = "INITIALIZE_REGION"  # initialize region, pass the request


URA = UninitializedRegionAction


EmptyResponse = JSONResponse([], status=200)
