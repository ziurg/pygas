def test_link_hardyCross_coefficient(basic_network):
    link = basic_network.links[60]
    link.flow = 0.4
    params = {"temperature": 25, "gas_density": 0.61, "headloss_coeff": 1.82}
    assert link.coeff(**params) == 9.756773542867552e-08
