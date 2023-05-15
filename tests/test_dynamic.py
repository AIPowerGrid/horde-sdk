import json
import os

import horde_shared_models.ai_horde_api as ai_horde_api
import horde_shared_models.generic_api as generic_api
import horde_shared_models.ratings_api as ratings_api
import pydantic
from horde_shared_models.generic_api.reflection import getAllRequestTypes

RATINGS_SAMPLE_DATA_FOLDER = "tests/test_data/ratings_api"
AI_HORDE_SAMPLE_DATA_FOLDER = "tests/test_data/ai_horde_api"


class Test_reflection_and_dynamic:  # noqa: D101
    def test_reflection(self) -> None:  # noqa: D102
        allRequestTypes = getAllRequestTypes(ratings_api.__name__)
        for requestType in allRequestTypes:
            assert issubclass(requestType, generic_api.BaseRequest)

    @staticmethod
    def dynamic_json_load(moduleName: str, sampleDataFolder: str) -> None:
        """Attempts to create instances of all non-abstract children of `RequestBase`."""
        # This test will do a lot of heavy lifting if you're looking to make additions/changes.
        # If you're here because it failed and you're not sure why,
        # check the implementation of `BaseRequestUserSpecific` and `UserRatingsRequest`

        allRequestTypes: list[type[generic_api.BaseRequest]] = getAllRequestTypes(moduleName)

        for requestType in allRequestTypes:
            assert issubclass(requestType, generic_api.BaseRequest)

            responseType: type[pydantic.BaseModel] = requestType.getExpectedResponseType()
            assert isinstance(responseType, type)
            assert issubclass(responseType, pydantic.BaseModel)

            targetFile = f"{sampleDataFolder}/{responseType.__name__}.json"
            assert os.path.exists(targetFile)

            with open(targetFile) as sampleFileHandle:
                sampleDataJson = json.loads(sampleFileHandle.read())
                responseType(**sampleDataJson)

    def test_horde_api(self) -> None:
        self.dynamic_json_load(ai_horde_api.__name__, AI_HORDE_SAMPLE_DATA_FOLDER)

    def test_ratings_api(self) -> None:
        self.dynamic_json_load(ratings_api.__name__, RATINGS_SAMPLE_DATA_FOLDER)
