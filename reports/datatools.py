#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# datatools -- reports
#
#     Copyright (C) 2021 Matteo Guadrini <matteo.guadrini@hotmail.it>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Contains all functions for data processing."""

# region Imports
from .exception import ReportDataError


# endregion

# region Functions
def select_column(data, column):
    """
    Select Dataset column

    :param data: Dataset object
    :param column: column name or index
    :return: list
    """
    # Check if dataset have a column
    if not data.headers:
        raise ReportDataError('dataset object must have the headers')
    # Select column
    if isinstance(column, int):
        return data.get_col(column)
    else:
        return data[column]


def average(data, column):
    """
    Average of list of integers or floats

    :param data: Dataset object
    :param column: column name or index
    :return: float
    """
    # Select column
    data = select_column(data, column)
    # Check if all item is integer or float
    if not all(isinstance(item, (int, float)) for item in data):
        raise ReportDataError('the column contains only int or float')
    # Calculate average
    return float(sum(data) / len(data))


def most_common(data, column):
    """
    The most common element in a column

    :param data: Dataset object
    :param column: column name or index
    :return: Any
    """
    # Select column
    data = select_column(data, column)
    return max(data, key=data.count)

# endregion
