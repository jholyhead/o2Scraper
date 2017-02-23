from o2scraper.scraper import run

def test_result():
    assert run("Canada") == "The cost of calling a landline in Canada is £1.50"
    