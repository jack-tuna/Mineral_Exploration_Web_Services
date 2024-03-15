# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Mineral_Exploration_Web_Services
                                 A QGIS plugin
 This plugin connects your QGIS User Profile to many openly hosted web services related to mineral exploration. These include Country and State geological surveys that provide mapped geology and data such as mineral occurence locations, geophysics, geochemistry etc.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-03-13
        copyright            : (C) 2024 by Jack Maughan
        email                : jack_maughan@hotmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Mineral_Exploration_Web_Services class from file Mineral_Exploration_Web_Services.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Mineral_Exploration_Web_Services import Mineral_Exploration_Web_Services
    return Mineral_Exploration_Web_Services(iface)
