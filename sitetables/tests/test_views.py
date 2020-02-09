from sitetables.tests.testapp.models import Article
from sitetables.toolbox import Table


def test_responder(setup_articles, request_client):

    url = ('sitetables:respond', {})

    table1 = Table(
        source={
            'source': Article,
            'options': {
                'columns_add': {
                    'title_custom': 'Added Column',
                }
            },
        },
        on_server=True
    )

    client = request_client(ajax=True)
    response = client.post(url)

    assert response.status_code == 400
    assert response.json() == {'error': 'No data found for "" table'}

    setup_articles()

    response = client.post(url, data={
        'tableName': table1.name,
        'search[value]': 'my',
        'length': 9999999,
        'orderBogus': 'some',
        'order[0][column]': 0,
        'order[0][dir]': 'desc',
        'order[1][column]': 333,  # Unknown idx.

    }).json()

    assert response['recordsTotal'] == 5
    assert response['recordsFiltered'] == 5
    assert len(response['data']) == 5
    assert 'custom_my ' in response['data'][0]['title_custom']
