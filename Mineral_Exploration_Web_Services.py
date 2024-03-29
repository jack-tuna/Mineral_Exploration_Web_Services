# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Mineral_Exploration_Web_Services
                                 A QGIS plugin
 This plugin connects your QGIS User Profile to many openly hosted web services related to mineral exploration. These include Country and State geological surveys that provide mapped geology and data such as mineral occurence locations, geophysics, geochemistry etc.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-03-13
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jack Maughan
        email                : jack_maughan@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, qVersion
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject, Qgis

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .Mineral_Exploration_Web_Services_dialog import Mineral_Exploration_Web_ServicesDialog
import os.path


class Mineral_Exploration_Web_Services:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Mineral_Exploration_Web_Services_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Mineral Exploration Web Services')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Mineral_Exploration_Web_Services', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Mineral_Exploration_Web_Services/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Connect to Servers'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Mineral Exploration Web Services'),
                action)
            self.iface.removeToolBarIcon(action)


    # def run(self):
    #     """Run method that performs all the real work"""

    #     # Create the dialog with elements (after translation) and keep reference
    #     # Only create GUI ONCE in callback, so that it will only load when the plugin is started
    #     if self.first_start == True:
    #         self.first_start = False
    #         self.dlg = Mineral_Exploration_Web_ServicesDialog()

    #     # show the dialog
    #     self.dlg.show()
    #     # Run the dialog event loop
    #     result = self.dlg.exec_()
    #     # See if OK was pressed
    #     if result:
    #         # Do something useful here - delete the line containing pass and
    #         # substitute with your code.
    #         pass


    def connect_all(self):
        """
        This script should be run from the Python consol inside QGIS.

        It adds online sources to the QGIS Browser.
        Each source should contain a list with the folowing items (string type):
        [sourcetype, title, authconfig, password, referer, url, username, zmax, zmin]

        You can add or remove sources from the sources section of the code.

        Script by Klas Karlsson
        Sources from https://qms.nextgis.com/

        Some services require you to supply your own API key for the services to work.

        Licence GPL-3

        Regarding the terms of use for these background maps YOU will need to verify that you
        follow the individual EULA that comes with the different services,
        Most likely they will restrict how you can use the data.
        Example:
        For Esri basemaps you will need a valid ArcGIS online subscription to use the maps.

        """


        # Sources
        sources = []

        # XYZ tile server basemaps
        sources.append(["connections-xyz","Google Maps","","","","https://mt1.google.com/vt/lyrs=m&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D","","19","0"])
        sources.append(["connections-xyz","Google Satellite", "", "", "", "https://mt1.google.com/vt/lyrs=s&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D", "", "19", "0"])
        sources.append(["connections-xyz","Google Terrain", "", "", "", "https://mt1.google.com/vt/lyrs=t&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D", "", "19", "0"])
        sources.append(["connections-xyz","Google Terrain Hybrid", "", "", "", "https://mt1.google.com/vt/lyrs=p&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D", "", "19", "0"])
        sources.append(["connections-xyz","Google Satellite Hybrid", "", "", "", "https://mt1.google.com/vt/lyrs=y&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D", "", "19", "0"])
        sources.append(["connections-xyz","Stamen Terrain", "", "", "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL", "http://tile.stamen.com/terrain/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "0"])
        sources.append(["connections-xyz","Stamen Toner", "", "", "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL", "http://tile.stamen.com/toner/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "0"])
        sources.append(["connections-xyz","Stamen Toner Light", "", "", "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL", "http://tile.stamen.com/toner-lite/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "0"])
        sources.append(["connections-xyz","Stamen Watercolor", "", "", "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL", "http://tile.stamen.com/watercolor/%7Bz%7D/%7Bx%7D/%7By%7D.jpg", "", "18", "0"])
        sources.append(["connections-xyz","Wikimedia Map", "", "", "OpenStreetMap contributors, under ODbL", "https://maps.wikimedia.org/osm-intl/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "1"])
        sources.append(["connections-xyz","Wikimedia Hike Bike Map", "", "", "OpenStreetMap contributors, under ODbL", "http://tiles.wmflabs.org/hikebike/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "17", "1"])
        sources.append(["connections-xyz","Esri Boundaries Places", "", "", "Requires ArcGIS Onlinesubscription", "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "20", "0"])
        sources.append(["connections-xyz","Esri Gray (dark)", "", "", "Requires ArcGIS Onlinesubscription", "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "16", "0"])
        sources.append(["connections-xyz","Esri Gray (light)", "", "", "Requires ArcGIS Onlinesubscription", "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "16", "0"])
        sources.append(["connections-xyz","Esri National Geographic", "", "", "Requires ArcGIS Onlinesubscription", "http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "12", "0"])
        sources.append(["connections-xyz","Esri Ocean", "", "", "Requires ArcGIS Onlinesubscription", "https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "10", "0"])
        sources.append(["connections-xyz","Esri Satellite", "", "", "Requires ArcGIS Onlinesubscription", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "17", "0"])
        sources.append(["connections-xyz","Esri Standard", "", "", "Requires ArcGIS Onlinesubscription", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "17", "0"])
        sources.append(["connections-xyz","Esri Terrain", "", "", "Requires ArcGIS Onlinesubscription", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "13", "0"])
        sources.append(["connections-xyz","Esri Topo World", "", "", "Requires ArcGIS Onlinesubscription", "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D", "", "20", "0"])
        sources.append(["connections-xyz","OpenStreetMap H.O.T.", "", "", "OpenStreetMap contributors, under ODbL", "http://tile.openstreetmap.fr/hot/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "19", "0"])
        sources.append(["connections-xyz","OpenTopoMap", "", "", "Kartendaten: © OpenStreetMap-Mitwirkende, SRTM | Kartendarstellung: © OpenTopoMap (CC-BY-SA)", "https://tile.opentopomap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "17", "1"])
        sources.append(["connections-xyz","Strava All", "", "", "OpenStreetMap contributors, under ODbL", "https://heatmap-external-b.strava.com/tiles/all/bluered/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "15", "0"])
        sources.append(["connections-xyz","Strava Run", "", "", "OpenStreetMap contributors, under ODbL", "https://heatmap-external-b.strava.com/tiles/run/bluered/%7Bz%7D/%7Bx%7D/%7By%7D.png?v=19", "", "15", "0"])
        sources.append(["connections-xyz","CartoDb Dark Matter", "", "", "Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.", "http://basemaps.cartocdn.com/dark_all/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "0"])
        sources.append(["connections-xyz","CartoDb Positron", "", "", "Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.", "http://basemaps.cartocdn.com/light_all/%7Bz%7D/%7Bx%7D/%7By%7D.png", "", "20", "0"])
        sources.append(["connections-xyz","Bing VirtualEarth", "", "", "", "http://ecn.t3.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1", "", "19", "1"])

        ## WMS AUSTRALIA
        sources.append(["connections-wms", "Geoscience Australia - Surface Geology", "", "", "", "http://services.ga.gov.au/site_1/services/GA_Surface_Geology/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Geoscience Australia - Geological Provinces", "", "", "", "http://services.ga.gov.au/site_3/services/Geological_Provinces_2013/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Geoscience Australia - Geophysical Grids", "", "", "", "http://services.ga.gov.au/site_9/services/Geophysical_Grids/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Geoscience Australia - Onshore Seismic Surveys", "", "", "", "http://services.ga.gov.au/site_9/services/Onshore_Seismic_Surveys/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Geoscience Australia - 250k Geological Maps", "", "", "", "http://services.ga.gov.au/site_9/services/Scanned_250k_Geological_Map_Index/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Geoscience Australia - Topography and Infrastructure", "", "", "", "http://services.ga.gov.au/site_7/services/Topographic_Base_Map/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "GSWA - Imagery", "", "", "", "https://public-services.slip.wa.gov.au/public/services/SLIP_Public_Services/DMIRS_Imagery_Service/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "MinRes Tasmania - Geological and Geophysical Maps", "", "", "", "http://www.mrt.tas.gov.au/erdas-iws/ogc/wms", "", "", ""])
        sources.append(["connections-wms", "GSV - Geological Maps", "", "", "", "http://geology.data.vic.gov.au/services/mapping/wms", "", "", ""])
        sources.append(["connections-wms", "GSNT - Geophysical Imagery", "", "", "", "http://geoscience.nt.gov.au/erdas-iws/ogc/wms/GIWS_NT", "", "", ""])
        sources.append(["connections-wms", "GSSA - Geophysical Imagery", "", "", "", "https://services.sarig.sa.gov.au/raster/geophysicalstateimages/wms", "", "", ""])

        ## WFS AUSTRALIA
        sources.append(["connections-wfs", "Geoscience Australia - Rock Properties", "", "", "", "http://www.ga.gov.au/geophysics-rockpropertypub-gws/ga_rock_properties_wfs/ows", "", "", ""])
        sources.append(["connections-wfs", "Geoscience Australia - Boreholes", "", "", "", "http://www.ga.gov.au/geophysics-rockpropertypub-gws/ga_rock_properties_wfs/ows", "", "", ""])
        sources.append(["connections-wfs", "Geoscience Australia - Field Geology", "", "", "", "https://services.ga.gov.au/gis/field-geology/wfs?service=wfs&request=GetCapabilities", "", "", ""])
        sources.append(["connections-wfs", "Geoscience Australia - Mines & Deposits", "", "", "", "https://services.ga.gov.au/gis/earthresource/wfs?REQUEST=GetCapabilities&SERVICE=WFS", "", "", ""])
        sources.append(["connections-wfs", "GSWA - Boreholes, Mines, Mineral Occurrences, Mineral Tenements", "", "", "", "http://geossdi.dmp.wa.gov.au/services/wfs", "", "", ""])
        sources.append(["connections-wfs", "WA Gov - Geology and Soils", "", "", "", "https://public-services.slip.wa.gov.au/public/services/SLIP_Public_Services/Geology_and_Soils_Map_WFS/MapServer/WFSServer", "", "", ""])
        sources.append(["connections-wfs", "WA Gov - Industry and Mining", "", "", "", "https://public-services.slip.wa.gov.au/public/services/SLIP_Public_Services/Industry_and_Mining_WFS/MapServer/WFSServer", "", "", ""])
        sources.append(["connections-wfs", "GSQ - Boreholes", "", "", "", "http://geology.information.qld.gov.au/geoserver/wfs", "", "", ""])
        sources.append(["connections-wfs", "MinRes Tas - Boreholes, Mines, Mineral Occurrences", "", "", "", "http://www.mrt.tas.gov.au/web-services/wfs", "", "", ""])
        sources.append(["connections-wfs", "GSV - Boreholes, Mines, Mineral Occurrences", "", "", "", "http://geology.data.vic.gov.au/nvcl/wfs", "", "", ""])
        sources.append(["connections-wfs", "GSNT - Boreholes, Mines, Mineral Occurrences", "", "", "", "http://geology.data.nt.gov.au/geoserver/wfs", "", "", ""])
        sources.append(["connections-wfs", "GSSA - Geoscience Data", "", "", "", "https://services.sarig.sa.gov.au/vector/geology/wfs", "", "", ""])
        sources.append(["connections-wfs", "GSSA - Geophysical Surveys", "", "", "", "https://services.sarig.sa.gov.au/vector/geophysical_data/wfs", "", "", ""])
        sources.append(["connections-wfs", "GSSA - Mineral Drillholes", "", "", "", "https://services.sarig.sa.gov.au/vector/drillholes/wfs", "", "", ""])
        sources.append(["connections-wfs", "GSSA - Mineral Rock Sample Sites", "", "", "", "https://services.sarig.sa.gov.au/vector/sampling_analyses/wfs", "", "", ""])
        sources.append(["connections-wfs", "GSSA - Boreholes, Mines, Mineral Occurrences", "", "", "", "https://sarigdata.pir.sa.gov.au/nvcl/geoserver/wfs", "", "", ""])
        sources.append(["connections-wfs", "GSNSW - Boreholes, Mines, Mineral Occurrences", "", "", "", "https://gs.geoscience.nsw.gov.au/geoserver/ows?service=wfs&version=2.0.0&request=GetCapabilities", "", "", ""])
        sources.append(["connections-wfs", "GSNSW - Geology", "", "", "", "https://gs-seamless.geoscience.nsw.gov.au/geoserver/onegeology/ows?service=wms&version=1.3.0&request=GetCapabilities", "", "", ""])

        # Arc Features AUSTRALIA
        sources.append(["connections-arcgisfeatureserver", "GSQ - Mines Permits", "", "", "", "https://gisservices.information.qld.gov.au/arcgis/rest/services/Economy/MinesPermitsCurrent/MapServer", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "GSQ - Geoscience Data", "", "", "", "https://gisservices.information.qld.gov.au/arcgis/rest/services/GeoscientificInformation", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "GSQ - Mines Administration", "", "", "", "https://gisservices.information.qld.gov.au/arcgis/rest/services/Boundaries/MiningAdministrativeAreas/MapServer", "", "", ""])

        # Global Geology WMS
        sources.append(["connections-wms", "Afghanistan Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_AGS_EN_Bedrock_and_Structural_Geology/wms?language=eng&", "", "", ""])
        sources.append(["connections-wms", "British GS Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_Bedrock_and_Superficial_Geology/wms?language=eng&", "", "", ""])
        sources.append(["connections-wms", "Burkina Faso Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_BUMIGEB_FR_Bedrock_Geology/wms?language=eng&", "", "", ""])
        sources.append(["connections-wms", "Falklands Island Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_FIG_Bedrock_and_Superficial_Geology/wms?language=eng&", "", "", ""])
        sources.append(["connections-wms", "Antarctica Geology - GA", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_GA_Bedrock_Geology/wms?language=eng&", "", "", ""])
        sources.append(["connections-wms", "India Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_GSI_Geology/wms?language=eng&", "", "", ""])
        sources.append(["connections-wms", "Namibia Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_GSN_Bedrock_Geology/wms?language=eng&", "", "", ""])
        sources.append(["connections-wms", "Canada Geology", "", "", "", "https://canada3d.geosciences.ca/ows/wms/getcapabilities/onegeology/GSC_EN_Geological_Formation.xml", "", "", ""])
        sources.append(["connections-wms", "Asia Geology", "", "", "", "https://onegeology-asia.org/ows/GSJ_ASIA_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "East Asia Geology", "", "", "", "https://gbank.gsj.jp/ows/GSJ_CCOP_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "Vietnam Geology", "", "", "", "http://onegeology-asia.org/ows/GSJ_DGMV_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "Myanmar Geology", "", "", "", "http://onegeology-asia.org/ows/GSJ_DGSME_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "Japan Geological Maps", "", "", "", "https://onegeology-asia.org/ows/GSJ_Geological_Maps/wms?", "", "", ""])
        sources.append(["connections-wms", "Indonesia Geology", "", "", "", "http://onegeology-asia.org/ows/GSJ_GRDC_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "Malaysia Geology", "", "", "", "http://onegeology-asia.org/ows/GSJ_JMG_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "Philippines Geology", "", "", "", "http://onegeology-asia.org/ows/GSJ_MGB_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "Papua New Guinea", "", "", "", "http://onegeology-asia.org/ows/GSJ_MRA_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "Mongolia Geology", "", "", "", "https://onegeology-asia.org/ows/GSJ_MRPAM_Combined_Bedrock_and_Superficial_Geology_and_Age/wms?", "", "", ""])
        sources.append(["connections-wms", "Sweden Geology", "", "", "", "http://resource.sgu.se/service/wms/inspire/SGU_Bedrock_Geology", "", "", ""])
        sources.append(["connections-wms", "German Geology", "", "", "", "https://services.bgr.de/wms/geologie/BGR_EN_Surface_Geology/?", "", "", ""])
        sources.append(["connections-wms", "Africa Country Geology and Groundwater", "", "", "", "https://map.bgs.ac.uk/arcgis/services/AGA/BGS_Groundwater/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "French Guiana Geology", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/BRGM_French_Guiana_Geology?", "", "", ""])
        sources.append(["connections-wms", "Antarctica Geology - SCAR", "", "", "", "https://map.bgs.ac.uk/arcgis/services/OneGeology/ATA_SCAR_GeoMAP_Geology/MapServer/WMSServer?", "", "", ""])
        sources.append(["connections-wms", "Brazil Geology", "", "", "", "https://onegeology.cprm.gov.br/geoserver/CPRM_EN_Bedrock_and_Age/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wms", "Portugal Geology", "", "", "", "https://inspire.lneg.pt/arcgis/services/CartografiaGeologica/CGP1M/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "Ireland Geology", "", "", "", "https://secure.dccae.gov.ie/arcgis/services/OneGeology/IRL_GSI_1M_OGE/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "Spain Geology", "", "", "", "http://mapas.igme.es/gis/services/oneGeology/IGME_EN_Geology/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Dominican Republic Geology", "", "", "", "http://mapas.igme.es/gis/services/PSysmin/IGME_SGN_EN_Geology/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Peru Geology", "", "", "", "http://geocatmin.ingemmet.gob.pe/ArcGIS/services/SERV_GEOLOGIA/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Korea Geology", "", "", "", "https://data.kigam.re.kr/mgeo/geoserver/OneGeology/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wms", "Slovenia Geology", "", "", "", "https://gis.geology.sk/arcgis/services/ONEGeology/GeolMap_SK_1G/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "Europe Geology", "", "", "", "https://geoserver.geo-zs.si/egdi-surface-geology/gsmlp/wms?VERSION=1.3.0", "", "", ""])
        sources.append(["connections-wms", "Europe Geology & Faults - IGME", "", "", "", "https://services.bgr.de/wms/geologie/igme5000/?service=wms&VERSION=1.3.0&request=GetCapabilities", "", "", ""])
        sources.append(["connections-wms", "Quebec Geoscience Data", "", "", "", "https://servicesvectoriels.atlas.gouv.qc.ca/IDS_SGM_EN_WMS/service.svc/get?", "", "", ""])

        ## Country Geophysics WMS
        sources.append(["connections-wms", "Sweden Magnetics", "", "", "", "https://resource.sgu.se/service/wms/130/flyggeofysik-magnet", "", "", ""])
        sources.append(["connections-wms", "Finland Geophysics", "", "", "", "https://gtkdata.gtk.fi/ArcGIS/services/Rajapinnat/GTK_Geofysiikka_WMS/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "British Geological Survey - Geophysics", "", "", "", "https://map.bgs.ac.uk/arcgis/services/GeoIndex_Onshore/geophysics/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "North Midlands of GB Geophysics", "", "", "", "https://map.bgs.ac.uk/arcgis/services/GeoIndex_Onshore/geophysics_midlands_hires/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "Portugal Radiometrics", "", "", "", "https://sig.lneg.pt/server/services/CartaRadiometrica/MapServer/WMSServer", "", "", ""])
        sources.append(["connections-wms", "Quebec Geophysics", "", "", "", "https://servicesgeo.atlas.gouv.qc.ca/ApolloCatalogWMSPublic/service.svc/get?layers=CARTE_INTERACTIVE", "", "", ""])



        # Global Geology WFS
        sources.append(["connections-wfs", "OneGeology Global Maps", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/CGMW_Bedrock_and_Structural_Geology?", "", "", ""])
        sources.append(["connections-wfs", "British Geological Survey", "", "", "", "http://ogc.bgs.ac.uk:80/digmap625k_gsml_insp_gs/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wfs", "Iran Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_GSI_EN_Bedrock_and_Structural_Geology/ows?language=eng", "", "", ""])
        sources.append(["connections-wfs", "Jamaica Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_MGD_Bedrock_Geology/ows?language=eng&", "", "", ""])
        sources.append(["connections-wfs", "France Geology", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/BRGM_1M_INSPIRE_geolUnits_geolFaults?language=eng&", "", "", ""])
        sources.append(["connections-wfs", "British Columbia Geology", "", "", "", "http://apps.empr.gov.bc.ca/geoserver/cgi/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wfs", "Africa Geology - CGMW", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/IGC35_CGMW_BRGM_Africa_Geology?", "", "", ""])
        sources.append(["connections-wfs", "Africa Geology - SIG", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/SIGAfrique_BRGM_Africa_Geology?", "", "", ""])
        sources.append(["connections-wfs", "South America Geology", "", "", "", "https://onegeology.cprm.gov.br/geoserver/tmsa/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wfs", "Belgium Geology", "", "", "", "http://www.dov.vlaanderen.be:80/geoserver/dov-pub-ALBON_DUT_Geology/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wfs", "Europe Geology", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/GISEurope_Bedrock_and_Structural_Geology?", "", "", ""])
        sources.append(["connections-wfs", "Iceland Geology", "", "", "", "http://kort.ni.is/geoserver/IINH_Geology/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wfs", "Norway Geology", "", "", "", "http://geo.ngu.no/egdi/egdi_portrayalservice/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wfs", "Cameroon Geology", "", "", "", "http://mapsrefdev.brgm.fr/wxs/1GG/IRGM_Formations_et_Geologie_Structurale?", "", "", ""])
        sources.append(["connections-wfs", "Andes Geology", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/SIGAndes_BRGM?", "", "", ""])
        sources.append(["connections-wfs", "Yemen Geology", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/YGSMRB_Bedrock_and_Structural_Geology?", "", "", ""])
        sources.append(["connections-wfs", "India Geology", "", "", "", "http://ogc.bgs.ac.uk/cgi-bin/BGS_GSI_EN_Bedrock_and_Structural_Geology/ows?language=eng&", "", "", ""])
        sources.append(["connections-wfs", "Europe Detailed Structures", "", "", "", "https://data.geus.dk/egdi/wms/?layers=hike_detail_layer&service=wms&version=1.3.0&request=GetCapabilities", "", "", ""])
        sources.append(["connections-wfs", "Finland Geology", "", "", "", "https://gtkdata.gtk.fi/arcgis/services/Rajapinnat/GTK_Kalliopera_WFS/MapServer/WFSServer?", "", "", ""])
        sources.append(["connections-wfs", "New Zealand Geology", "", "", "", "https://data.nzpam.govt.nz/hosting/services/ERM/ERM_PSC/MapServer/WFSServer", "", "", ""])
        sources.append(["connections-wfs", "New Zealand Geology - GNS", "", "", "", "https://maps.gns.cri.nz/geology/wfs", "", "", ""])

        ## Drillholes and Mines
        sources.append(["connections-wfs", "Africa Mineral Resources", "", "", "", "http://mapsref.brgm.fr/wxs/1GG/SIGAfrique_BRGM_Africa_MineralResources?", "", "", ""])
        sources.append(["connections-wfs", "Finland Mineral Occurrences", "", "", "", "http://13.95.69.121:80/geoserver/erl/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wfs", "USGS Major Mines", "", "", "", "https://mrdata.usgs.gov/services/wfs/ofr20051294?version=1.1.0", "", "", ""])
        sources.append(["connections-wms", "British Geological Survey - Boreholes", "", "", "", "https://map.bgs.ac.uk/arcgis/services/GeoIndex_Onshore/boreholes/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "British Geological Survey - Geochemistry", "", "", "", "https://map.bgs.ac.uk/arcgis/services/GeoIndex_Onshore/geochemistry/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "British Geological Survey Soil Geochemical Atlas", "", "", "", "https://map.bgs.ac.uk/arcgis/services/UKSO/UKSO_BGS_NSI/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wfs", "Europe Offshore Minerals", "", "", "", "https://drive.emodnet-geology.eu/geoserver/gsi/wms?service=wms&VERSION=1.3.0&request=GetCapabilities", "", "", ""])
        sources.append(["connections-wfs", "Europe Mineral Occurrences", "", "", "", "https://data.geus.dk/egdi/wms/?layers=egdi_mineraloccurrences_inspire&service=wms&version=1.3.0&request=GetCapabilities", "", "", ""])
        sources.append(["connections-wfs", "Europe Critical Minerals", "", "", "", "https://data.geus.dk/egdi/wms/?layers=egdi_mineraloccurr_critical_raw_materials_2023&service=wms&version=1.3.0&request=GetCapabilities", "", "", ""])
        sources.append(["connections-wfs", "Europe PROMINE", "", "", "", "http://mapsrefrec.brgm.fr/wxs/promine/wp1ogc?service=wms&VERSION=1.3.0&request=GetCapabilities", "", "", ""])
        sources.append(["connections-wfs", "Africa Artisanal Mining", "", "", "", "https://geo.ipisresearch.be/geoserver/wfs", "", "", ""])
        sources.append(["connections-wms", "Portugal Minerals", "", "", "", "https://sig.lneg.pt/server/services/OcorrenciasMinerais/MapServer/WMSServer?request=GetCapabilities&service=WMS", "", "", ""])
        sources.append(["connections-wms", "Portugal Boreholes", "", "", "", "https://sig.lneg.pt/server/services/Sondabase/MapServer/WMSServer", "", "", ""])

        sources.append(["connections-arcgisfeatureserver", "Ireland Geoscience Data", "", "", "", "https://gsi.geodata.gov.ie/server/rest/services", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "British Geological Survey Data", "", "", "", "https://map.bgs.ac.uk/arcgis/rest/services", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "Slovakia Geological Survey Data", "", "", "", "https://gis.geology.sk/arcgis/rest/services", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "Hungary Geological Survey Data", "", "", "", "https://map.mbfsz.gov.hu/arcgis/rest/services", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "North West Territories Geoscience Data", "", "", "", "https://services3.arcgis.com/GSr8HAQhtEt4sNnv/arcgis/rest/services/", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "China Geoscience Data", "", "", "", "http://219.142.81.85/arcgis/rest/services", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "NZ - Minerals Feature Service", "", "", "", "https://data.nzpam.govt.nz/arcgis/rest/services/EXTERNAL/Minerals_Feature_Service/FeatureServer", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "NZ - Minerals Map Layers", "", "", "", "https://data.nzpam.govt.nz/arcgis/rest/services/EXTERNAL/Minerals/MapServer", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "Peru Geoscience Data", "", "", "", "https://services8.arcgis.com/oTalEaSXAuyNT7xf/ArcGIS/rest/services", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "Mexico Geoscience Data", "", "", "", "https://mapasims.sgm.gob.mx/arcgis/rest/services", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "Colombia Geoscience Data", "", "", "", "https://srvags.sgc.gov.co/arcgis/rest/services", "", "", ""])
        sources.append(["connections-arcgisfeatureserver", "NOAA Global Geoscience Data", "", "", "", "https://gis.ngdc.noaa.gov/arcgis/rest/services", "", "", ""])


        ## OTHER
        sources.append(["connections-wms", "British Geological Survey - Hydrogeology", "", "", "", "https://map.bgs.ac.uk/arcgis/services/GeoIndex_Onshore/hydrogeology/MapServer/WmsServer?", "", "", ""])
        sources.append(["connections-wms", "Brazil - Hydrogeology", "", "", "", "https://onegeology.cprm.gov.br/geoserver/CPRM_EN_Hydrogeology/ows?SERVICE=WMS&", "", "", ""])
        sources.append(["connections-wms", "Japan Volcanoes", "", "", "", "https://onegeology-asia.org/ows/GSJ_Japan_Volcanoes_Geological_Maps/wms?", "", "", ""])
        sources.append(["connections-wms", "Asia Volcanic and Plutonic Rocks", "", "", "", "https://onegeology-asia.org/ows/GSJ_ASIA_Volcanic_Plutonic_Rocks/wms?", "", "", ""])


        # Add sources to browser
        for source in sources:
            connectionType = source[0]
            connectionName = source[1]
            QSettings().setValue("qgis/%s/%s/authcfg" % (connectionType, connectionName), source[2])
            QSettings().setValue("qgis/%s/%s/password" % (connectionType, connectionName), source[3])
            QSettings().setValue("qgis/%s/%s/referer" % (connectionType, connectionName), source[4])
            QSettings().setValue("qgis/%s/%s/url" % (connectionType, connectionName), source[5])
            QSettings().setValue("qgis/%s/%s/username" % (connectionType, connectionName), source[6])
            QSettings().setValue("qgis/%s/%s/zmax" % (connectionType, connectionName), source[7])
            QSettings().setValue("qgis/%s/%s/zmin" % (connectionType, connectionName), source[8])

        # Update GUI
        self.iface.reloadConnections()

      
    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = Mineral_Exploration_Web_ServicesDialog()
            # self.dlg.pushButton.clicked.connect(self.select_output_file)

        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        #result = self.dlg.exec_()
        result = self.dlg.pushButton.clicked.connect(self.connect_all)
        # See if OK was pressed
        if result:
          self.iface.messageBar().pushMessage(
            "Success", "Connected to Servers",
            level=Qgis.Success, duration=3)