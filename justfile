default: lint format_check type_check test

lint:
    uv run ruff check

format_check:
    uv run ruff format --check

type_check:
    uv run pyright

test:
    uv run pytest

watch:
    # Watch for changes and run tests.
    uv run ptw sea/  

dl dataset:
    @echo "Downloading {{dataset}}..."
    uv run python main.py download {{dataset}} --format jsonl > data/{{dataset}}.jsonl

dl_building_permits:
    @just dl 'building_permits'

dl_issued_building_permits:
    @just dl 'issued_building_permits'

dl_land_use_permits:
    @just dl 'land_use_permits'

dl_trade_permits:
    @just dl 'trade_permits'

dl_electrical_permits:
    @just dl 'electrical_permits'

dl_plan_reviews:
    @just dl 'plan_reviews'

dl_plan_comments:
    @just dl 'plan_comments'

dl_all: dl_building_permits dl_issued_building_permits dl_land_use_permits dl_trade_permits dl_electrical_permits dl_plan_reviews dl_plan_comments

to_csv file:
    @echo "Converting {{file}} to CSV..."
    uv run python main.py to-csv data/{{file}}.jsonl > data/{{file}}.csv

to_csv_all:
    @just to_csv 'building_permits'
    @just to_csv 'issued_building_permits'
    @just to_csv 'land_use_permits'
    @just to_csv 'trade_permits'
    @just to_csv 'electrical_permits'
    @just to_csv 'plan_reviews'
    @just to_csv 'plan_comments'
