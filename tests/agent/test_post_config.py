

def test_serialize_log():
    from local_cloud_agent.common.configuration import serialize_log
    test_data = {'key1': 'val1', 'key2': 'val2'}
    resp = serialize_log(test_data)
    assert resp == '{\n  "key1": "val1",\n  "key2": "val2"\n}'

