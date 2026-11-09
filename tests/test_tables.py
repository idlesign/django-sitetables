from sitetables.toolbox import Table


def test_tables_registry(source_listdics):

    table1 = Table(source=source_listdics, name='one')
    table2 = Table(source=source_listdics)

    registry = Table.tables_registry
    assert len(list(registry.keys())) == 2
    assert registry['one'] is table1
