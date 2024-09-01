import pandas as pd
import pandera as pa
from rest_framework import serializers


class ProductSchema(pa.DataFrameModel):
    """Used as first line of check"""

    product_id: int = pa.Field(gt=0)
    product_name: str
    category: str
    price: float = pa.Field(gt=0, nullable=True)
    quantity_sold: int = pa.Field(ge=0, nullable=True, coerce=True)
    rating: float = pa.Field(ge=0, le=5, nullable=True)
    review_count: float = pa.Field(ge=0, nullable=True, coerce=True)


def calc_df_median(df_column: pd.Series):
    return df_column.median()


def calc_df_mean(df_column: pd.Series):
    return df_column.mean()


# Final converter
product_schema_converter = {
    "product_id": {"converter": int, "calc_missing": None},
    "product_name": {"converter": str, "calc_missing": None},
    "category": {"converter": str, "calc_missing": None},
    "price": {"converter": float, "calc_missing": calc_df_median},
    "quantity_sold": {"converter": int, "calc_missing": calc_df_median},
    "rating": {"converter": float, "calc_missing": calc_df_mean},
    "review_count": {"converter": int, "calc_missing": calc_df_median},
}


class SpreadSheetSerializer(serializers.Serializer):
    file = serializers.FileField()
