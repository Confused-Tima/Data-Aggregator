from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import permission_classes
from django.db.models import Sum, F, Window
from django.db.models.functions import RowNumber

from .models import ProductSalesData
from .schemas import SpreadSheetSerializer, product_schema_converter, ProductSchema
from permissions.unauthenticated_user_permissions import WriteOnlyIfAuthenticated
from .utils import (
    group_up_and_calc,
    validate_df,
    return_csv_from_data,
    file_to_df_with_validation,
    bulk_insert_with_conflicts,
)


@api_view(["POST"])
@permission_classes([WriteOnlyIfAuthenticated])
def insert_csv_data(request: Request):
    """API that inserts CSV/XLSX files data into DB"""

    serializer = SpreadSheetSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    file = serializer.validated_data["file"]

    conversion = file_to_df_with_validation(file)
    if error_response := conversion["error"]:
        return error_response

    df = conversion["df"]

    is_validated = validate_df(df, ProductSchema, product_schema_converter)

    if is_validated:
        insertion_result = bulk_insert_with_conflicts(df, "product_id")
        if error_response := insertion_result["error"]:
            return error_response

    return Response(
        {
            "message": "File uploaded and processed successfully!",
            "is_validated": is_validated,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def get_products_summary(_):
    """API that aggregates data from the Database on products"""

    # Calculate total revenue per category
    revenue_by_category = group_up_and_calc(
        ProductSalesData,
        "category",
        {"total_revenue": Sum(F("price") * F("quantity_sold"))},
    )

    # Calculate top product per category
    top_products = (
        ProductSalesData.objects.annotate(
            rank=Window(
                expression=RowNumber(),
                partition_by=[F("category")],
                order_by=F("quantity_sold").desc(),
            )
        )
        .filter(rank=1)
        .values("category", "product_name", "quantity_sold")
    )

    final_ans = []
    products = {
        category_products["category"]: category_products
        for category_products in top_products
    }

    # Combine the results
    for category_data in revenue_by_category:
        category = category_data["category"]
        total_revenue = category_data["total_revenue"]

        top_product = products.get(category)
        top_product_name = top_product["product_name"] if top_product else "N/A"
        top_product_quantity_sold = top_product["quantity_sold"] if top_product else 0

        final_ans.append(
            {
                "category": category,
                "total_revenue": total_revenue,
                "top_product": top_product_name,
                "top_product_qunatity_sold": top_product_quantity_sold,
            }
        )

    return return_csv_from_data(final_ans)
