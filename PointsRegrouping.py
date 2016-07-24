# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PointsRegrouping
                                 A QGIS plugin
 Copies point within the polygon predetermined number of times.
                              -------------------
        begin                : 2016-07-23
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Maks Skorokhod / WB-Tech
        email                : samael500@gmail.com
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.gui import *
from qgis.core import *

from PointsRegroupingModule import PointsRegroupingProcessor

# Initialize Qt resources from file resources.py
import resources

import os.path


class PointsRegrouping:
    """QGIS Plugin Implementation."""

    _name = 'PointsRegrouping'

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
            'PointsRegrouping_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.toolbar = self.iface.addToolBar(self._name)
        self.toolbar.setObjectName(self._name)
        # clear selections
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            layer.removeSelection()

    def createToolButton(self, parent, text):
        button = QToolButton(parent)
        button.setObjectName(text)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button.setPopupMode(QToolButton.MenuButtonPopup)
        parent.addWidget(button)
        return button

    def createAction(self, icon_path, text, callback):
        action = QAction(
            QIcon(icon_path),
            text,
            self.iface.mainWindow())
        # connect the action to the run method
        action.setCheckable(True)
        action.toggled.connect(callback)
        return action

    def createClearAction(self, icon_path, text):
        action = QAction(
            QIcon(icon_path),
            text,
            self.iface.mainWindow())
        # connect the action to the run method
        action.setCheckable(False)
        action.triggered.connect(self.clear)
        return action

    def initGui(self):
        # Create action that will start plugin configuration
        self.actionRandom = self.createAction(
            ":/plugins/PointsRegrouping/icon.png",
            u"Generate Random",
            self.run_random)

        self.actionLinear = self.createAction(
            ":/plugins/PointsRegrouping/icon.png",
            u"Generate Linear",
            self.run_linear)

        # Create action that will start plugin configuration
        self.actionClear = self.createClearAction(
            ":/plugins/PointsRegrouping/icon.png",
            u"Clear selections")

        # self.tool = MultiLayerSelection(self.iface.mapCanvas(), self.actionCriar)
        self.toolRandom = PointsRegroupingProcessor(self.iface.mapCanvas(), self.actionRandom, 'random')
        self.toolLinear = PointsRegroupingProcessor(self.iface.mapCanvas(), self.actionLinear, 'linear')

        # QToolButtons
        self.selectionButton = self.createToolButton(self.toolbar, u'PointsRegroupingButton')
        self.selectionButton.addAction(self.actionLinear)
        self.selectionButton.addAction(self.actionRandom)
        self.selectionButton.addAction(self.actionClear)
        # set default active
        self.selectionButton.setDefaultAction(self.actionLinear)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.mainWindow().removeToolBar(self.toolbar)

    def clear(self):
        self.actionLinear.setChecked(False)
        self.actionRandom.setChecked(False)
        self.selectionButton.setDefaultAction(self.selectionButton.sender())
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            layer.removeSelection()

    def run_random(self, b):
        self.actionLinear.setChecked(False)
        self.selectionButton.setDefaultAction(self.selectionButton.sender())
        if b:
            self.iface.mapCanvas().setMapTool(self.toolRandom)
        else:
            self.iface.mapCanvas().unsetMapTool(self.toolRandom)

    def run_linear(self, b):
        self.actionRandom.setChecked(False)
        self.selectionButton.setDefaultAction(self.selectionButton.sender())
        if b:
            self.iface.mapCanvas().setMapTool(self.toolLinear)
        else:
            self.iface.mapCanvas().unsetMapTool(self.toolLinear)
