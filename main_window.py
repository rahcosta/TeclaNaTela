"""
Janela principal da aplicação de Teclado Virtual ABNT2 para Aulas e Apresentações.
Fornece controles de Always on Top (Fixar no topo), modo de visualização, temas e opacidade.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QSlider, QLabel, QFrame,
    QAction, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QFont, QCursor

from keyboard_widget import KeyboardWidget, THEMES
from keyboard_hook import KeyboardHookThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teclado Virtual ABNT2 - Modo Aula")
        self.resize(1080, 320)
        self.setMinimumSize(700, 220)

        # Estado inicial
        self._is_always_on_top = True
        self._is_frameless = False
        self._drag_pos = QPoint()

        self._setup_ui()
        self._setup_hook()
        self._apply_window_flags()

    def _setup_ui(self):
        # Estilos modernos escuros estilo Windows 11
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0E1116;
            }
            QFrame#top_bar {
                background-color: #161B22;
                border-bottom: 1px solid #30363D;
                padding: 4px 10px;
            }
            QFrame#footer_bar {
                background-color: #12151B;
                border-top: 1px solid #21262D;
                padding: 2px 10px;
            }
            QLabel {
                color: #C9D1D9;
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QLabel#title_label {
                color: #FFFFFF;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton {
                background-color: #21262D;
                color: #F0F6FC;
                border: 1px solid #30363D;
                border-radius: 5px;
                padding: 4px 8px;
                font-family: 'Segoe UI';
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #30363D;
                border-color: #8B949E;
            }
            QPushButton:pressed {
                background-color: #161B22;
            }
            QPushButton#btn_pin_active {
                background-color: #FF6600;
                color: #FFFFFF;
                border-color: #FF8C00;
                font-weight: bold;
            }
            QComboBox {
                background-color: #21262D;
                color: #F0F6FC;
                border: 1px solid #30363D;
                border-radius: 5px;
                padding: 3px 6px;
                font-family: 'Segoe UI';
                font-size: 12px;
                min-width: 70px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #161B22;
                color: #F0F6FC;
                selection-background-color: #FF6600;
                border: 1px solid #30363D;
            }
            QSlider::groove:horizontal {
                height: 4px;
                background: #30363D;
                border-radius: 2px;
            }
            QSlider::sub-page:horizontal {
                background: #FF6600;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                border: 1px solid #30363D;
                width: 14px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 7px;
            }
        """)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Barra Superior de Ferramentas
        top_bar = QFrame(self)
        top_bar.setObjectName("top_bar")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 4, 8, 4)
        top_layout.setSpacing(6)

        # Título conciso
        lbl_title = QLabel("⌨ Teclado ABNT2", self)
        lbl_title.setObjectName("title_label")
        top_layout.addWidget(lbl_title)

        top_layout.addSpacing(4)

        # Botão Always on Top
        self.btn_pin = QPushButton("📌 Topo: ON", self)
        self.btn_pin.setObjectName("btn_pin_active")
        self.btn_pin.setToolTip("Manter o teclado sempre visível por cima de outras janelas")
        self.btn_pin.clicked.connect(self._toggle_always_on_top)
        top_layout.addWidget(self.btn_pin)

        # Seletor de Modo de Layout
        top_layout.addWidget(QLabel("Layout:", self))
        self.combo_layout = QComboBox(self)
        self.combo_layout.addItems(["Completo", "TKL", "Compacto"])
        self.combo_layout.currentIndexChanged.connect(self._on_layout_changed)
        top_layout.addWidget(self.combo_layout)

        # Seletor de Temas
        top_layout.addWidget(QLabel("Tema:", self))
        self.combo_theme = QComboBox(self)
        self.combo_theme.addItem("Âmbar", "amber")
        self.combo_theme.addItem("Ciano", "cyan")
        self.combo_theme.addItem("Esmeralda", "emerald")
        self.combo_theme.currentIndexChanged.connect(self._on_theme_changed)
        top_layout.addWidget(self.combo_theme)

        # Controle de Opacidade com ícone
        lbl_op = QLabel("🌓", self)
        lbl_op.setToolTip("Ajustar opacidade e transparência")
        top_layout.addWidget(lbl_op)

        self.slider_opacity = QSlider(Qt.Horizontal, self)
        self.slider_opacity.setRange(40, 100)
        self.slider_opacity.setValue(100)
        self.slider_opacity.setFixedWidth(65)
        self.slider_opacity.setToolTip("Ajuste a transparência para não cobrir totalmente a tela")
        self.slider_opacity.valueChanged.connect(self._on_opacity_changed)
        top_layout.addWidget(self.slider_opacity)

        top_layout.addStretch()

        # Botão Ajuda
        btn_info = QPushButton("❓", self)
        btn_info.setFixedWidth(28)
        btn_info.setToolTip("Ajuda e Instruções")
        btn_info.clicked.connect(self._show_help_dialog)
        top_layout.addWidget(btn_info)

        # Botão Minimizar
        btn_min = QPushButton("🗕", self)
        btn_min.setFixedWidth(28)
        btn_min.setToolTip("Minimizar janela")
        btn_min.clicked.connect(self.showMinimized)
        top_layout.addWidget(btn_min)

        main_layout.addWidget(top_bar)

        # 2. Área do Teclado Virtual Interativo
        self.keyboard_widget = KeyboardWidget(self)
        main_layout.addWidget(self.keyboard_widget, 1)

        # 3. Rodapé com Informações de Segurança e Atalhos
        footer_bar = QFrame(self)
        footer_bar.setObjectName("footer_bar")
        footer_layout = QHBoxLayout(footer_bar)
        footer_layout.setContentsMargins(10, 3, 10, 3)

        lbl_secure = QLabel("🔒 Modo Monitoramento 100% Passivo • Nenhum dado é registrado ou salvo.", self)
        lbl_secure.setStyleSheet("color: #7D8590; font-size: 11px;")
        footer_layout.addWidget(lbl_secure)

        footer_layout.addStretch()

        lbl_hint = QLabel("Dica para aulas: Teclas e atalhos simultâneos (Ctrl+C, Ctrl+Alt+Del) são destacados em tempo real no teclado", self)
        lbl_hint.setStyleSheet("color: #58A6FF; font-size: 11px;")
        footer_layout.addWidget(lbl_hint)

        main_layout.addWidget(footer_bar)

    def _setup_hook(self):
        self.hook_thread = KeyboardHookThread()
        self.hook_thread.key_pressed.connect(self.keyboard_widget.on_key_pressed)
        self.hook_thread.key_released.connect(self.keyboard_widget.on_key_released)
        self.hook_thread.start()

    def _apply_window_flags(self):
        was_visible = self.isVisible()
        flags = Qt.Window
        if self._is_always_on_top:
            flags |= Qt.WindowStaysOnTopHint

        self.setWindowFlags(flags)
        if was_visible:
            self.show()

    def _toggle_always_on_top(self):
        self._is_always_on_top = not self._is_always_on_top
        if self._is_always_on_top:
            self.btn_pin.setText("📌 Topo: ON")
            self.btn_pin.setObjectName("btn_pin_active")
            self.btn_pin.setStyle(self.btn_pin.style())
        else:
            self.btn_pin.setText("📌 Topo: OFF")
            self.btn_pin.setObjectName("")
            self.btn_pin.setStyle(self.btn_pin.style())
        self._apply_window_flags()

    def _on_layout_changed(self, index: int):
        if index == 0:
            self.keyboard_widget.set_layout_mode('FULL')
            self.resize(1080, 320)
        elif index == 1:
            self.keyboard_widget.set_layout_mode('TKL')
            self.resize(920, 320)
        else:
            self.keyboard_widget.set_layout_mode('COMPACT')
            self.resize(780, 290)

    def _on_theme_changed(self, index: int):
        theme_key = self.combo_theme.itemData(index)
        if theme_key:
            self.keyboard_widget.set_theme(theme_key)

    def _on_opacity_changed(self, value: int):
        self.setWindowOpacity(value / 100.0)

    def _show_help_dialog(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Ajuda & Instruções de Uso")
        msg.setTextFormat(Qt.RichText)
        msg.setText("""
        <h3>⌨ Teclado Virtual Didático ABNT2</h3>
        <p>Aplicação desenvolvida para demonstração visual em tempo real durante aulas de Computação/Informática, apresentações e compartilhamento de tela.</p>
        <hr>
        <b>Recursos e Instruções de Uso:</b>
        <ul>
            <li><b>Detecção Direta no Teclado:</b> Todas as teclas físicas pressionadas são iluminadas instantaneamente no teclado virtual.</li>
            <li><b>Teclas Seguradas (Hold):</b> As teclas permanecem acesas continuamente enquanto você mantiver os dedos pressionados e apagam ao soltar.</li>
            <li><b>Atalhos Didáticos:</b> Pressione combinações como <i>Ctrl+C</i>, <i>Ctrl+Alt+Del</i>, <i>Alt+Tab</i>, <i>Shift+Setas</i> para demonstrar visualmente para os alunos.</li>
            <li><b>📌 Fixar no Topo:</b> Mantém o teclado sempre visível por cima de outros programas (Bloco de Notas, VS Code, navegadores, PowerPoint).</li>
            <li><b>Modos de Layout:</b> Alterne entre <i>Completo</i>, <i>TKL</i> (sem numérico) e <i>Compacto</i> para melhor aproveitamento do espaço de tela.</li>
            <li><b>🌓 Opacidade:</b> Ajuste a barra deslizante para deixar o teclado translúcido sobre seus slides ou código.</li>
            <li><b>🔒 100% Passivo & Seguro:</b> Não bloqueia teclas de outros aplicativos e não armazena nenhuma informação digitada.</li>
        </ul>
        """)
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox { background-color: #161B22; }
            QLabel { color: #F0F6FC; }
            QPushButton { background-color: #21262D; color: white; padding: 6px 16px; border-radius: 4px; }
        """)
        msg.exec_()

    def closeEvent(self, event):
        # Encerra o gancho do Windows e a thread com segurança
        if hasattr(self, 'hook_thread') and self.hook_thread.isRunning():
            self.hook_thread.stop()
        event.accept()
