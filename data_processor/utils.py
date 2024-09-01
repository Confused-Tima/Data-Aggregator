import io
from typing import Callable

import numpy as np
import pandera as pa
import pandas as pd
from rest_framework import status
from rest_framework.response import Response
from django.db import models
from django.http.response import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from psqlextra.types import ConflictAction

from .models import ProductSalesData


def file_to_df_with_validation(file: InMemoryUploadedFile) -> pd.DataFrame:
    """Converts spreadsheets to pd.DataFrames (only supports .csv and .xlsx)

    Args:
        file (InMemoryUploadedFile):

    Returns:
        pd.DataFrame
    """

    try:
        file_content = file.read()
    except Exception as e:
        return {
            "df": None,
            "error": Response(
                {"message": f"Error while decoding file: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            ),
        }

    file_name = file.name
    error = None

    if file_name.endswith(".csv"):
        file_data = io.StringIO(file_content.decode("utf-8"))
        df = pd.read_csv(file_data)
    elif file_name.endswith(".xlsx"):
        file_data = io.BytesIO(file_content)
        df = pd.read_excel(file_data)
    else:
        df = None
        error = Response(
            {"message": "File not found in supported type, try csv or xlsx file"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return {"df": df, "error": error}


def bulk_insert_with_conflicts(df: pd.DataFrame, conflict_key: str):
    """Use this method for insertion if chances of conflicts are there

    Args:
        df (pd.DataFrame)
        conflict_key (str)

    Returns:
        dict: is_success (if insertion was successful) error (that we got)
    """

    products = df.replace({np.nan: None}).to_dict(orient="records")

    try:
        (
            ProductSalesData.objects.on_conflict(
                [conflict_key], ConflictAction.NOTHING
            ).bulk_insert(products)
        )
    except Exception as e:
        return {
            "is_success": False,
            "error": Response(
                {"error": f"Error while insertion: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            ),
        }

    return {"is_success": True, "error": None}


def convert_df_to_required_dtype(
    df: pd.DataFrame, col: str, calculator: Callable, type_converter: any
) -> bool:
    """Fixes each DataFrame column if not in correct format

    Args:
        df (pd.DataFrame)
        col (str): Column name to fix
        calculator (Callable): Function which tells what value to give if missing
        type_converter (any): Once calculated, fix all values to required data type
        (Since nan converts the entire row to float)

    Returns:
        bool: True if successful else false
    """

    if df[col].isna().all():
        return False

    nan_replacement = calculator(df[col])
    df.fillna({col: nan_replacement}, inplace=True)
    try:
        df[col] = df[col].astype(type_converter)
    except Exception:
        return False
    return True


def validate_df(
    df: pd.DataFrame, pa_schema: pa.DataFrameModel, converter: dict
) -> bool:
    """Validates the data in a df based on the converters given

    Args:
        df (pd.DataFrame):
        converter (dict):

    Returns:
        bool
    """

    is_validated = True
    try:
        pa_schema.validate(df)
    except pa.errors.SchemaError:
        return False

    for col, col_data in converter.items():
        if col_data["calc_missing"]:
            if not convert_df_to_required_dtype(
                df, col, col_data["calc_missing"], col_data["converter"]
            ):
                return False

    return is_validated


def return_csv_from_data(data: list[dict]) -> HttpResponse:
    """Takes a list of dictionaries and sends a csv file out of it

    Args:
        data (list[dict])

    Returns:
        HttpResponse
    """

    df = pd.DataFrame(data)

    # Convert DataFrame to CSV format
    csv_data = df.to_csv(index=False)  # Convert without row indices

    # Create HTTP response with CSV content
    response = HttpResponse(csv_data, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="data.csv"'

    return response


def group_up_and_calc(model: models.Model, group_by: str, subquery: dict):
    return model.objects.values(group_by).annotate(**subquery).order_by()
