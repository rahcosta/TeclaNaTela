"""
Widget gráfico de alta performance para renderização do teclado virtual ABNT2.
Utiliza QPainter com antialiasing, gradientes modernos e visualização em tempo real de atalhos.
Suporta modos de visualização (Completo, TKL, Compacto) e paletas de cores de alto contraste.
"""

from typing import Set, List, Dict
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRectF, pyqtSlot, QTimer
from PyQt5.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush,
    QLinearGradient, QPainterPath
)

from keyboard_layout import create_abnt2_rows, KeyDef, KEY_DISPLAY_NAMES


THEMES = {
    'amber': {
        'name': 'Âmbar Vibrante (Ideal para Projetor)',
        'bg': QColor('#12151B'),
        'hud_bg': QColor('#181C24'),
        'key_bg': QColor('#20242E'),
        'key_border': QColor('#383F4E'),
        'key_text_main': QColor('#FFFFFF'),
        'key_text_sub': QColor('#A0AAB8'),
        'key_text_altgr': QColor('#6B7687'),
        # Estado Pressionado
        'active_bg_top': QColor('#FF8C00'),
        'active_bg_bottom': QColor('#FF4500'),
        'active_border': QColor('#FFC107'),
        'active_text': QColor('#FFFFFF'),
        'active_glow': QColor(255, 140, 0, 70),
        'hud_badge_bg': QColor('#FF6600'),
        'hud_badge_text': QColor('#FFFFFF'),
    },
    'cyan': {
        'name': 'Ciano Neon',
        'bg': QColor('#0D1117'),
        'hud_bg': QColor('#161B22'),
        'key_bg': QColor('#1F242C'),
        'key_border': QColor('#30363D'),
        'key_text_main': QColor('#FFFFFF'),
        'key_text_sub': QColor('#8B949E'),
        'key_text_altgr': QColor('#58A6FF'),
        'active_bg_top': QColor('#00E5FF'),
        'active_bg_bottom': QColor('#0088CC'),
        'active_border': QColor('#80D8FF'),
        'active_text': QColor('#001529'),
        'active_glow': QColor(0, 229, 255, 70),
        'hud_badge_bg': QColor('#00B4D8'),
        'hud_badge_text': QColor('#001220'),
    },
    'emerald': {
        'name': 'Verde Esmeralda',
        'bg': QColor('#0F1715'),
        'hud_bg': QColor('#152420'),
        'key_bg': QColor('#1E2E2A'),
        'key_border': QColor('#2A443D'),
        'key_text_main': QColor('#FFFFFF'),
        'key_text_sub': QColor('#95B5AB'),
        'key_text_altgr': QColor('#52B788'),
        'active_bg_top': QColor('#00E676'),
        'active_bg_bottom': QColor('#00A854'),
        'active_border': QColor('#69F0AE'),
        'active_text': QColor('#052317'),
        'active_glow': QColor(0, 230, 118, 70),
        'hud_badge_bg': QColor('#00C853'),
        'hud_badge_text': QColor('#052317'),
    }
}


class KeyboardWidget(QWidget):
    """
    Componente visual do teclado que desenha o layout ABNT2 e destaca teclas ativas.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._raw_rows = create_abnt2_rows()
        self._active_keys: Set[str] = set()
        self._last_shortcut_str: str = ""
        self._layout_mode = 'FULL'  # 'FULL', 'TKL', 'COMPACT'
        self._current_theme_key = 'amber'
        self._theme = THEMES[self._current_theme_key]

        self.setMinimumSize(600, 220)
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)

    def set_theme(self, theme_key: str):
        if theme_key in THEMES:
            self._current_theme_key = theme_key
            self._theme = THEMES[theme_key]
            self.update()

    def set_layout_mode(self, mode: str):
        if mode in ('FULL', 'TKL', 'COMPACT'):
            self._layout_mode = mode
            self.update()

    @pyqtSlot(str, str)
    def on_key_pressed(self, key_id: str, _label: str):
        self._active_keys.add(key_id)
        self.update()

    @pyqtSlot(str)
    def on_key_released(self, key_id: str):
        self._active_keys.discard(key_id)
        self.update()

    def _filter_rows_for_mode(self) -> List[List[KeyDef]]:
        """Filtra as teclas conforme o modo selecionado (FULL, TKL, COMPACT)."""
        filtered = []
        for row in self._raw_rows:
            new_row = []
            for k in row:
                if self._layout_mode == 'COMPACT':
                    if k.section in ('main', 'fn') and not k.id.startswith('_GAP_FN_NAV') and not k.id.startswith('_GAP_FN_NUM'):
                        new_row.append(k)
                elif self._layout_mode == 'TKL':
                    if k.section in ('main', 'fn', 'nav') and not k.id.startswith('_GAP_FN_NUM'):
                        new_row.append(k)
                else:  # FULL
                    new_row.append(k)
            filtered.append(new_row)
        return filtered

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)

        width = self.width()
        height = self.height()
        theme = self._theme

        # Fundo da janela do teclado
        painter.fillRect(self.rect(), theme['bg'])

        # Desenho das Teclas ocupando a área útil
        padding_x = 10
        padding_y = 8
        keyboard_rect = QRectF(
            padding_x,
            padding_y,
            width - 2 * padding_x,
            height - 2 * padding_y
        )

        rows = self._filter_rows_for_mode()
        if not rows:
            return

        # Calcula a largura total em unidades da maior linha
        max_units = 0.0
        for r in rows:
            line_w = sum(k.w for k in r)
            if line_w > max_units:
                max_units = line_w

        total_rows = len(rows)
        # Linha 0 (Fn) tem altura proporcional reduzida (0.8x)
        total_unit_h = 0.8 + (total_rows - 1) * 1.0 + 0.25  # gap após a linha Fn

        unit_w = keyboard_rect.width() / max_units
        unit_h = keyboard_rect.height() / total_unit_h
        key_margin = max(1.5, min(unit_w, unit_h) * 0.06)

        cur_y = keyboard_rect.top()
        for row_idx, row in enumerate(rows):
            cur_x = keyboard_rect.left()
            row_h_mult = 0.8 if row_idx == 0 else 1.0
            cur_h = unit_h * row_h_mult

            for k in row:
                key_w = k.w * unit_w
                key_h = k.h * cur_h

                if not k.is_spacer:
                    rect_key = QRectF(
                        cur_x + key_margin,
                        cur_y + key_margin,
                        key_w - 2 * key_margin,
                        key_h - 2 * key_margin
                    )
                    is_active = k.id in self._active_keys
                    self._draw_single_key(painter, rect_key, k, is_active)

                cur_x += key_w

            cur_y += cur_h
            if row_idx == 0:
                cur_y += unit_h * 0.25  # Espaço sutil entre linha de Função e linha 1

    def _draw_single_key(self, painter: QPainter, rect: QRectF, k: KeyDef, is_active: bool):
        theme = self._theme
        radius = max(3.0, rect.height() * 0.12)

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        if is_active:
            # Gradiente vibrante para tecla ativa
            grad = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            grad.setColorAt(0.0, theme['active_bg_top'])
            grad.setColorAt(1.0, theme['active_bg_bottom'])

            # Brilho de fundo (glow sutil)
            glow_rect = rect.adjusted(-2, -2, 2, 2)
            glow_path = QPainterPath()
            glow_path.addRoundedRect(glow_rect, radius + 1, radius + 1)
            painter.fillPath(glow_path, theme['active_glow'])

            painter.fillPath(path, grad)
            painter.setPen(QPen(theme['active_border'], 1.8))
            painter.drawPath(path)
        else:
            # Estado normal
            painter.fillPath(path, theme['key_bg'])
            painter.setPen(QPen(theme['key_border'], 1.0))
            painter.drawPath(path)

            # Efeito de topo 3D sutil
            top_line_y = rect.top() + 1.2
            painter.setPen(QColor(255, 255, 255, 18))
            painter.drawLine(int(rect.left() + radius), int(top_line_y),
                             int(rect.right() - radius), int(top_line_y))

        # Renderização das Etiquetas de Texto
        # Para teclas altas (ex: Enter e + do teclado numérico), baseia a proporção na altura padrão
        normal_h = rect.height() / k.h if k.h > 1.0 else rect.height()
        font_size = max(7, int(normal_h * 0.28))

        main_font = QFont("Segoe UI", font_size, QFont.Bold if is_active else QFont.Normal)

        # Ajuste dinâmico inteligente: garante que palavras inteiras como "Enter", "Backspace", "Caps Lock"
        # caibam completamente na largura da tecla sem cortes
        max_text_width = rect.width() - 8
        painter.setFont(main_font)
        while font_size > 6 and painter.fontMetrics().horizontalAdvance(k.label_main) > max_text_width:
            font_size -= 1
            main_font.setPointSize(font_size)
            painter.setFont(main_font)

        sub_font = QFont("Segoe UI", max(6, int(font_size * 0.75)))

        if is_active:
            text_color_main = theme['active_text']
            text_color_sub = theme['active_text']
            text_color_altgr = theme['active_text']
        else:
            text_color_main = theme['key_text_main']
            text_color_sub = theme['key_text_sub']
            text_color_altgr = theme['key_text_altgr']

        pad = normal_h * 0.12

        # 1. Rótulo Secundário (Shift - Canto Superior Esquerdo)
        if k.label_sub:
            painter.setFont(sub_font)
            painter.setPen(text_color_sub)
            sub_rect = QRectF(rect.left() + pad, rect.top() + pad, rect.width() / 2, rect.height() / 2)
            painter.drawText(sub_rect, Qt.AlignLeft | Qt.AlignTop, k.label_sub)

        # 2. Rótulo Terciário (AltGr - Canto Inferior Direito)
        if k.label_altgr:
            painter.setFont(sub_font)
            painter.setPen(text_color_altgr)
            alt_rect = QRectF(rect.left() + rect.width() / 2, rect.top() + rect.height() / 2 - pad,
                              rect.width() / 2 - pad, rect.height() / 2)
            painter.drawText(alt_rect, Qt.AlignRight | Qt.AlignBottom, k.label_altgr)

        # 3. Rótulo Principal (Centro ou Inferior Esquerdo se tiver Shift)
        painter.setFont(main_font)
        painter.setPen(text_color_main)

        if k.label_sub:
            main_rect = QRectF(rect.left() + pad, rect.top() + rect.height() / 2 - pad,
                               rect.width() / 2, rect.height() / 2)
            painter.drawText(main_rect, Qt.AlignLeft | Qt.AlignBottom, k.label_main)
        else:
            painter.drawText(rect, Qt.AlignCenter, k.label_main)
