# -*- coding: utf-8 -*-


class Node:
    def __init__(self, id, **kwargs):
        self.id = id
        self._pressure = 0.0
        self._flow = 0.0
        self._fixed_pressure = None
        self._fixed_flow = None
        self.params = {}
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def fixed_pressure(self):
        return self._fixed_pressure

    @fixed_pressure.setter
    def fixed_pressure(self, value):
        if self._fixed_flow is None:
            self._fixed_pressure = value
            self._pressure = value
        else:
            raise Exception("Can't get node with both fixed pressure and flow.")

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, value):
        if self._fixed_pressure is None:
            self._pressure = value

    @property
    def fixed_flow(self):
        return self._fixed_flow

    @fixed_flow.setter
    def fixed_flow(self, value):
        if self._fixed_pressure is None:
            self._fixed_flow = value
            self._flow = value
        else:
            raise Exception("Can't get node with both fixed pressure and flow.")

    @property
    def flow(self):
        return self._flow

    @flow.setter
    def flow(self, value):
        if self._fixed_flow is None:
            self._flow = value

    def __getattr__(self, attribute):
        try:
            return self.__dict__[attribute]
        except KeyError:
            return self.params[attribute]

    def __setattr__(self, attr_name, attr_value):
        if attr_name in ["fixed_pressure", "fixed_flow", "flow", "pressure"]:
            super(Node, self).__setattr__(attr_name, attr_value)
        else:
            try:
                self.__dict__[attr_name] = attr_value
            except KeyError:
                self.params[attr_name] = attr_value

    def __str__(self):
        return f"Node {self.id} (Q={self.flow:.2f}; P={self.pressure:.2f})"

    def __eq__(self, other: int):
        return self.id == other

    @property
    def is_tank(self):
        if not (self.fixed_pressure is None):
            return True
        else:
            return False

    @property
    def is_customer(self):
        if not (self.fixed_flow is None):
            return True
        else:
            return False
