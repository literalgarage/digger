import csv
import json
import typing as t

Format = t.Literal["jsonl", "csv"]


def dump_data(
    items: t.Iterable[dict[str, t.Any]],
    output: t.IO[str],
    format: Format,
) -> None:
    """
    Writes an iterable of dictionaries to an output stream as either JSONL or CSV.

    For CSV writing, we do *not* assume that all dictionaries have the same keys,
    which is unfortunate -- but turns out to be quite common in Seattle's
    open data sets.
    """
    if format == "jsonl":
        for item in items:
            output.write(json.dumps(item) + "\n")
        return

    # Handle CSV writing
    def flatten_dict(d, parent_key="", sep="__"):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    # To ensure all keys are captured for the header, we need to see all items
    # before writing. This requires holding all items in memory.
    all_items = [flatten_dict(item) for item in items]

    if not all_items:
        return  # No data to write

    # Collect all unique keys across all items; use a dict as an ordered set
    all_keys: dict[str, None] = {}
    for item in all_items:
        for key in item.keys():
            all_keys[key] = None

    fieldnames = list(all_keys)
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_items)
