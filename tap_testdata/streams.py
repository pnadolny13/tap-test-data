"""Stream type classes for tap-testdata."""

from __future__ import annotations

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
        with tempfile.NamedTemporaryFile(mode="w+") as tmp:
            json.dump(self.schema, tmp)
            tmp.flush()
            npx_process = npx.Popen(['json-schema-faker-cli', tmp.name, "none", str(self.config["records"]), "none"], stdout=subprocess.PIPE)
            out, err = npx_process.communicate()
            for record in json.loads(out):
                yield record
