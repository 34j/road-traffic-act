from road_traffic_act._main import LAW_ID, get_xml


def test_content():
    xml = get_xml(LAW_ID["道路交通法"])
    assert xml.tag == "Law"
