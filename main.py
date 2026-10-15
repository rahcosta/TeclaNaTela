"""
Ponto de entrada principal da aplicação de Teclado Didático ABNT2.
Configura suporte a telas de alta resolução (High-DPI) e inicia o loop da aplicação.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

from main_window import MainWindow


def create_app_icon():
    """Gera um ícone dinâmico nítido para a aplicação caso não exista arquivo externo."""
    pix = QPixmap(64, 64)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing, True)

    # Fundo do ícone
    painter.setBrush(QColor("#161B22"))
    painter.setPen(QColor("#FF6600"))
    painter.drawRoundedRect(4, 4, 56, 56, 12, 12)

    # Tecla em destaque
    painter.setBrush(QColor("#FF6600"))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(12, 16, 40, 20, 6, 6)

    # Barra de espaço
    painter.drawRoundedRect(16, 42, 32, 8, 4, 4)

    # Texto
    painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
    painter.setPen(QColor("#FFFFFF"))
    painter.drawText(12, 16, 40, 20, Qt.AlignCenter, "ABNT")

    painter.end()
    return QIcon(pix)


def main():
    # Habilita suporte nativo a monitores 4K / High DPI
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("TecladoDidaticoABNT2")
    app.setOrganizationName("EducacaoInformatica")
    app.setWindowIcon(create_app_icon())

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
