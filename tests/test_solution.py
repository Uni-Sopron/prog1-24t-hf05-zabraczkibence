from io import StringIO
from unittest.mock import patch

import main

drinks_json = StringIO(
    '[{"name":"Csapolt Soproni","unit":"dl","price":120,"stock":300},{"name":"Soproni IPA","unit":"doboz","price":700,"stock":12},{"name":"Soproni Bivaly","unit":"üveg","price":750,"stock":5}]'
)
guests_json = StringIO(
    '[{"name":"Nagy Ivó Kálmán","balance":3000},{"name":"Seres Nikolett","balance":4400},{"name":"Bornemissza Gergely","balance":-6000}]'
)


class FakeStringIO(StringIO):
    def close(self):
        pass


def test_main():
    def fake_open(fname, mode="r", **_):
        if fname.endswith("drinks.json"):
            global drinks_json
            if "w" in mode:
                drinks_json = FakeStringIO("")
            drinks_json = FakeStringIO(drinks_json.getvalue())
            return drinks_json
        else:
            global guests_json
            if "w" in mode:
                guests_json = FakeStringIO("")
            guests_json = FakeStringIO(guests_json.getvalue())
            return guests_json

    with open("tests/input.txt", "r", encoding="utf-8") as inp:

        def fake_input(msg):
            print(msg, end="")
            answer = inp.readline().strip()
            print(answer)
            return answer

        with patch("builtins.input", fake_input):
            with patch("sys.stdout", StringIO()) as fake_out:
                with patch("builtins.open", fake_open):
                    main.run()
                    output = fake_out.getvalue()
    with open("tests/output.txt", "r", encoding="utf-8") as out:
        expected_output = out.read()
    assert output == expected_output
