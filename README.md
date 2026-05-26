# Weathercrawler

Weathercrawler downloads weather data from `wttr.in` as JSON and stores it locally in a date-based directory structure.

## Requirements

- Python 3.12
- `uv`

## Installation

```bash
git clone https://github.com/mrcgndr/weathercrawler.git .
cd weathercrawler
uv sync
```

If you also want plotting support from `utils.visualize`, install the optional visualization dependencies:

```bash
uv sync --extra visualize
```

## Configuration

Runtime configuration lives in `config.json`.

Example:

```json
{
  "locations": ["Bonn"],
  "weatherfiledir": "./test",
  "logfilepath": "./test/log"
}
```

## Usage

Run the crawler:

```bash
uv run weathercrawler
```

Migrate existing JSON files into the new folder structure:

```bash
uv run migrate-weatherfiles ./test
```

## Storage Layout

New weather files are stored under `weatherfiledir` using this structure:

```text
<weatherfiledir>/YYYY/MM/DD/HHMM_<location>.json
```

Example:

```text
test/2026/05/26/2028_Bonn.json
```

## Notes

- The crawler uses the observation timestamp returned by `wttr.in`.
- If `localObsDateTime` is missing from the API response, the timestamp is reconstructed from `date` and `observation_time`.
- If the API response does not contain a usable weather report timestamp, the file is not written.
- `utils.weatherfilestack.WeatherFileStack` reads JSON files recursively and therefore works with the new directory structure.
