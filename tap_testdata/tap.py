"""TestData tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_testdata.streams import TestDataStream

class TapTestData(Tap):
    """TestData tap class."""

    name = "tap-testdata"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "records",
            th.IntegerType,
            required=True,
            description="The amount of records to generate for each stream.",
        ),
        th.Property(
            "generator_options",
            th.ObjectType(),
            required=False,
            default={},
            description="The [json-schema-faker options](https://github.com/json-schema-faker/json-schema-faker/tree/master/docs#available-options) to use when generating data.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[TestDataStream]:
        """Initialize all available streams and return them as a list.

        Returns:
            List of discovered Stream objects.
        """
        result: list[TestDataStream] = []
        for stream_name, catalog_entry in self.catalog.items():
            result.append(TestDataStream(self, catalog_entry.schema, stream_name))

        return result

if __name__ == "__main__":
    TapTestData.cli()
