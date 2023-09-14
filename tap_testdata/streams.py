"""Stream type classes for tap-testdata."""

from __future__ import annotations

import copy
import json
import subprocess
import tempfile
from typing import Iterable

from nodejs import npx
from singer_sdk.streams import Stream

class TestDataStream(Stream):
    """Stream class for TestData streams."""

    replication_method = "FULL_TABLE"

    def get_records(
        self,
        context: dict | None,  # noqa: ARG002
    ) -> Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.

        Args:
            context: Stream partition or context dictionary.

        Raises:
            NotImplementedError: If the implementation is TODO
        """
        updated_schema = copy.deepcopy(self.schema)
        required = updated_schema.get("required", [])
        for key in self.primary_keys:
            required.append(key)
        updated_schema["required"] = list(set(required))
        with tempfile.NamedTemporaryFile(mode="w+") as tmp:
            json.dump(updated_schema, tmp)
            tmp.flush()
            with tempfile.NamedTemporaryFile(mode="w+", suffix='.json') as tmp_options:
                json.dump(
                    self.config["generator_options"],
                    tmp_options
                )
                tmp_options.flush()
                npx_process = npx.Popen(['json-schema-faker-cli', tmp.name, "none", str(self.config["records"]), tmp_options.name], stdout=subprocess.PIPE)
                out, err = npx_process.communicate()
                if err:
                    raise Exception(err)
                for record in json.loads(out):
                    yield record
