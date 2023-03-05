import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QPropertyAnimation,QEasingCurve
from PyQt5.QtWidgets import QMainWindow, QApplication
from db import *

from Diccionario import errores

#Crearmos la clase principal de el entorno grafico
class Ventana_Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('sistema.ui', self)

        # comunicacion con la base de datos
        self.basededatos = conexion()

        #Saca Barra FEA
        window = QMainWindow()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(1) #1 es visible  0 invisible

        #sizedgrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        #Mover Ventana
        self.frame_barra.mouseevent = self.mover_ventana

        # Controles de barra
        self.b_cerrar.clicked.connect(lambda: self.close())
        self.b_minimizar.clicked.connect(self.control_minimizar)


        # Trae los datos del config.cfg
        server, base = leer_cfg()
        self.T_Server.setText (base)
        self.T_Base.setText(server)
        self.B_conexion.clicked.connect(conexion)

        # Minimizar
    def control_minimizar(self):
        self.showMinimized()

        #SizeGrip
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    # mover ventana
    def MousePressEvent(self, event):
        self.click_position = event.globalpos()

    def mover_ventana(self, event):
        print('asd')
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalpos() - self.click_position)
                self.click_position = event.globalpos()
                event.accept()
            if event.globalpos().y() <=10:
                self.showMaximized()
            else:
                self.showNormal()
    #Valores a llenar para la tabla Sistema de tecnolar.
    def completa_Sistema(self):
        Fantasia = self.T_Fantasia.text().upper()
        RazonSocial =self.T_RazonSocial.text().upper()
        Direccion = self.T_Direccion.text().upper()
        Cuit = self.T_Direccion.text().upper()
        Clienteweb = self.T_ClienteWeb.text().upper()
        Empresa = self.T_Direccion.text().upper()
        Sucursal = self.T_Sucursal.text().upper()
        cajas = self.T_Cajas.text().upper()

        #Validacion de campos.
        if Fantasia != '' or RazonSocial != '' or Direccion != '' or Cuit != '' or Clienteweb != '' or empresa != '' or Sucursal != '' or cajas != '' :

        else:
            self.T_Titulo.text = 'ERROR '







if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Ventana_Principal()
    GUI.show()
    sys.exit(app.exec())

