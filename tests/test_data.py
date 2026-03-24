def test_generate_data_shape():
    from siteofshift.data import generate_data
    df = generate_data()
    assert len(df) > 0
