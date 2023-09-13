# `tap-testdata`

A Singer tap used to generate fake data to mock other taps.
The main use case is for mocking taps in test pipelines where you don't have credentials or want to interact with sensitive data.
The tap will generate fake data that conforms the the json schema supplied by the tap being mocked.

Usually a tap is run in [discovery mode](https://hub.meltano.com/singer/spec#discovery-mode) to generate a catalog file which is then used as its own input `--catalog` when running a pipeline job.
This tap uses a catalog file from another tap to generate fake data that looks like it came from that tap.
For this tap you should instead pass the catalog file from the tap you would like to mock.

For example:

```bash
tap-github --config=gh_config.json --discover > tap_github_catalog.json
tap-testdata --config=test_data_config.json --catalog=tap_github_catalog.json
```

Built with the [Meltano Singer SDK](https://sdk.meltano.com).

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`
* `batch`

## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| records             | True     | None    | The amount of records to generate for each stream. |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas. |
| batch_config        | False    | None    |             |

A full list of supported settings and capabilities is available by running: `tap-testdata --about`

## Supported Python Versions

* 3.8
* 3.9
* 3.10
* 3.11

## Installation

This tap calls the npm package [`json-schema-faker-cli`](https://github.com/oprogramador/json-schema-faker-cli) to generate fake data.
You need to install the npm package before you run the tap.

```
npm install
```

## Usage

You can easily run `tap-testdata` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-testdata --version
tap-testdata --help
tap-testdata --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-testdata` CLI interface directly using `poetry run`:

```bash
poetry run tap-testdata --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-testdata
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-testdata --version
# OR run a test `elt` pipeline:
meltano elt tap-testdata target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
