import dlt
from opensky_source import opensky_data

pipeline = dlt.pipeline(
    pipeline_name="opensky_pipeline",
    destination='snowflake',
    dataset_name="staging",
)
load_info = pipeline.run(opensky_data())
print(load_info)


