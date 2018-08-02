from unittest.mock import MagicMock

import pytest

from extensions.booksearch.booksite import BookSite, UnSupportedSite
from extensions.booksearch.handlers import WaqfeyaHandler


def test_init(ctx):
    b = BookSite(MagicMock(spec=ctx), MagicMock(spec=WaqfeyaHandler))

    assert b is not None
    assert b.handler is not None


@pytest.mark.asyncio
async def test_convert_returns_object_if_supported_site(ctx):
    site = 'waqfeya'

    assert isinstance(await BookSite.convert(MagicMock(spec=ctx), site), BookSite)


@pytest.mark.asyncio
async def test_convert_raises_error_if_not_supported_site(ctx):
    site = 'nonexistentlibrary'

    with pytest.raises(UnSupportedSite):
        await BookSite.convert(MagicMock(spec=ctx), site)


@pytest.mark.asyncio
async def test_search_returns_embed_with_results(ctx, bookls1):
    search_url = 'uncle-google.com'
    b = BookSite(MagicMock(spec=ctx), MagicMock(spec=WaqfeyaHandler))

    async def search(query, tag):
        return bookls1, search_url

    b.handler.search = search
    b.handler.format_result = WaqfeyaHandler.format_result

    embed = await b.search('fake query', None)

    for index, field in enumerate(embed.fields):
        book = bookls1[index]

        assert book.title == field.name
        if book.author_name is not None:
            assert book.author_name in field.value
        if book.link is not None:
            assert book.link in field.value
        if book.site_link is not None:
            assert book.site_link in field.value
