from feast import Entity, FileSource, FeatureView
from feast.types import Float32, Float64
from feast.data_format import ParquetFormat
from feast.value_type import ValueType
from feast.field import Field

customer = Entity(
    name="customer_id",
    join_keys=["customer_id"],
    value_type=ValueType.STRING,
    description="Identifiant unique du client",
)

transaction_source = FileSource(
    path="../../../data/silver/transactions.parquet",
    file_format=ParquetFormat(),
    event_timestamp_column="transaction_date",
)

features_source = FileSource(
    path="../../../data/features/transactions_features.parquet",
    file_format=ParquetFormat(),
    event_timestamp_column="transaction_date",
)


transaction_features = FeatureView(
    name="transaction_features",
    entities = [customer],
    source = transaction_source,
    schema = [
        Field(name="amount", dtype=Float64),
    ],
    ttl=None,
    online=True,
    description="Features des transactions du client",
    tags={
        "team": "data",
        "domain": "transaction",
    },
)

avg_amount_7d = FeatureView(
    name="avg_amount_7d_features",
    entities=[customer],
    source=features_source,
    schema=[
        Field(name="avg_amount_7d", dtype=Float64),
    ],
    ttl=None,
    online=True,
    description="Moyenne du montant des transactions sur 7 jours precedent",
    tags={
        "team": "data",
        "domain": "transaction",
        "type": "aggregated",
        "window": "7d",
        "feature_type": "rolling",
    },
)