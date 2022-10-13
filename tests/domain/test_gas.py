from app.domain.model.gas import Gas


def test_gas_init():
    gas = Gas(name="NG", temperature=7.5, density=0.71)

    assert gas.name == "NG"
    assert gas.temperature == 7.5
    assert gas.density == 0.71


def test_gas_from_dict():
    init_dict = {
        "name": "NG",
        "temperature": 7.5,
        "density": 0.71,
    }

    gas = Gas.from_dict(init_dict)

    assert gas.name == "NG"
    assert gas.temperature == 7.5
    assert gas.density == 0.71


def test_gas_to_dict():
    init_dict = {
        "name": "NG",
        "temperature": 7.5,
        "density": 0.71,
    }

    gas = Gas.from_dict(init_dict)

    assert gas.to_dict() == init_dict
