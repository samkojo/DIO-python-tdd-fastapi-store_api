from typing import List
from uuid import UUID

import pytest
from store_api.core.exceptions import NotFoundException
from store_api.schemas.product import ProductOut, ProductUpdateOut
from store_api.usecases.product import product_usecase


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


# Nao consegui simular
# async def test_usecases_create_should_return_exception(product_in):
#     with pytest.raises(DBInsertException) as err:
#         await product_usecase.create(body=product_in)

#     assert (
#         err.value.message
#         == 'Fail to insert in DB'
#     )


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"))

    assert (
        err.value.message
        == "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) == 4


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_with_price_grater_than_should_return_success():
    result = await product_usecase.query(price_grater_than="5.500")

    assert isinstance(result, List)
    assert len(result) == 2


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_with_price_less_than_should_return_success():
    result = await product_usecase.query(price_less_than="10.500")

    assert isinstance(result, List)
    assert len(result) == 3


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_with_price_less_grater_should_return_success():
    result = await product_usecase.query(
        price_grater_than="5.500", price_less_than="10.500"
    )

    assert isinstance(result, List)
    assert len(result) == 1


async def test_usecases_update_should_return_success(product_up, product_inserted):
    product_up.price = "7.500"
    result: ProductUpdateOut = await product_usecase.update(
        id=product_inserted.id, body=product_up
    )

    assert isinstance(result, ProductUpdateOut)
    assert result.updated_at > product_inserted.updated_at


async def test_usecases_update_should_not_found(product_up):
    with pytest.raises(NotFoundException) as err:
        await product_usecase.update(
            id=UUID("1e4f214e-85f7-461a-89d0-a751a32e3bb9"), body=product_up
        )

    assert (
        err.value.message
        == "Product not found with filter: 1e4f214e-85f7-461a-89d0-a751a32e3bb9"
    )


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
