from uuid import UUID

import pytest
from store_api.core.exceptions import NotFoundException
from store_api.schemas.product import ProductOut, ProductUpdateOut
from store_api.usecases.product import product_usecase
from tests.factories import product_data
# from tests.factories import product_data

async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == product_data()['name']

async def test_usecases_get_should_return_success(product_id):
    result = await product_usecase.get(id=product_id)

    assert isinstance(result, ProductOut)
    assert result.name == product_data()['name']

async def test_usecases_get_should_not_found():
    
    with pytest.raises(Exception) as err:
        await product_usecase.get(id=UUID('123ad3a9-3b07-4ee3-baa8-2df6fcb074ce'))

    assert err.value.message == 'Product not found with filter: 123ad3a9-3b07-4ee3-baa8-2df6fcb074ce'

@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, list)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_up, product_inserted):
    product_up.price = "7.500"
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


async def test_usecases_delete_should_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"))

    assert (
        err.value.message
        == "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"
    )