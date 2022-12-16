import pytest
from app.domain.model.node import Node

def test_create_node_new_attributes():
    n = Node(id = 12, radius = 15)
    assert n.id == 12
    assert n.radius == 15

def test_create_node_with_fixed_pressure():
    n = Node(id = 12)
    n.fixed_pressure = 0.4
    assert n.fixed_pressure == 0.4
    assert n.pressure == n.fixed_pressure
    n.fixed_pressure = 5
    assert n.fixed_pressure == 5
    assert n.pressure == n.fixed_pressure

    n2 = Node(id = 12, fixed_pressure = 0.022)
    assert n2.id == 12
    assert n2.fixed_pressure == 0.022
    assert n2.pressure == n2.fixed_pressure


def test_create_node_with_fixed_flow():
    n = Node(id = 12)
    n.fixed_flow = 0.4
    assert n.fixed_flow == 0.4
    assert n.flow == n.fixed_flow
    n.fixed_flow = 5
    assert n.fixed_flow == 5
    assert n.flow == n.fixed_flow

    n2 = Node(id = 12, fixed_flow = 0.022)
    assert n2.id == 12
    assert n2.fixed_flow == 0.022
    assert n2.flow == n2.fixed_flow

def test_fixed_pressure_node_changing_flow():
    n = Node(id = 12, fixed_pressure = 0.025)
    n.flow = 100
    assert str(n)=='Node 12 (Q=100.00; P=0.03)'

def test_try_to_change_pressure_on_fixed_pressure_node():
    n = Node(id = 12, fixed_pressure = 0.025)
    n.pressure = 12 # no impact
    assert n.pressure == 0.025
    assert n.fixed_pressure == 0.025

def test_change_flow_on_fixed_flow_node():
    n = Node(id = 12, fixed_flow = 0.025)
    n.flow = 12 # no impact
    assert n.flow == 0.025
    assert n.fixed_flow == 0.025

def test_try_to_fixe_flow_on_fixed_pressure_node():
    n = Node(id = 12, fixed_pressure = 0.025)
    with pytest.raises(Exception) as e_info:
        n.fixed_flow = 100

def test_try_to_fixe_pressure_on_fixed_flow_node():
    n = Node(id = 12, fixed_flow = 123)
    with pytest.raises(Exception) as e_info:
        n.fixed_pressure = 10