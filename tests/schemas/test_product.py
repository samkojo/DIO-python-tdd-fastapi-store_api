
from pydantic import ValidationError
import pytest
from store_api.schemas.product import ProductIn
from tests.factories import product_data


def test_schemas_validated():
    data = product_data()
    # product = ProductIn(**data)
    product = ProductIn.model_validate(data)

    assert product.name == 'iPhone 14'

def test_schemas_return_raise(snapshot):
    data = {'name':'iPhone 14', 'quantity':10, 'price':8500}

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == snapshot