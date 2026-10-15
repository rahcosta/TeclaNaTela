"""
Definição geométrica e metadados do teclado padrão brasileiro ABNT2.
Contém dimensões relativas, etiquetas primárias, secundárias (Shift) e terciárias (AltGr).
Suporta modos de visualização: Completo (com Numpad e Navegação), TKL e Compacto (overlay).
"""

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class KeyDef:
    id: str
    label_main: str
    label_sub: Optional[str] = None
    label_altgr: Optional[str] = None
    display_name: Optional[str] = None
    w: float = 1.0       # Largura em unidades de tecla (1.0 = padrão)
    h: float = 1.0       # Altura em unidades de tecla
    section: str = 'main'  # 'fn', 'main', 'nav', 'numpad'
    is_spacer: bool = False

    def __post_init__(self):
        if not self.display_name:
            self.display_name = self.label_main

def create_abnt2_rows() -> List[List[KeyDef]]:
    """
    Retorna a matriz de linhas do teclado ABNT2 com todas as teclas físicas.
    """
    return [
        # Linha 0: Teclas de Função
        [
            KeyDef('KEY_ESC', 'Esc', display_name='Esc', w=1.0, section='fn'),
            KeyDef('_GAP_FN1', '', w=1.0, is_spacer=True, section='fn'),
            KeyDef('KEY_F1', 'F1', section='fn'),
            KeyDef('KEY_F2', 'F2', section='fn'),
            KeyDef('KEY_F3', 'F3', section='fn'),
            KeyDef('KEY_F4', 'F4', section='fn'),
            KeyDef('_GAP_FN2', '', w=0.5, is_spacer=True, section='fn'),
            KeyDef('KEY_F5', 'F5', section='fn'),
            KeyDef('KEY_F6', 'F6', section='fn'),
            KeyDef('KEY_F7', 'F7', section='fn'),
            KeyDef('KEY_F8', 'F8', section='fn'),
            KeyDef('_GAP_FN3', '', w=0.5, is_spacer=True, section='fn'),
            KeyDef('KEY_F9', 'F9', section='fn'),
            KeyDef('KEY_F10', 'F10', section='fn'),
            KeyDef('KEY_F11', 'F11', section='fn'),
            KeyDef('KEY_F12', 'F12', section='fn'),
            # Espaço para o bloco de navegação
            KeyDef('_GAP_FN_NAV', '', w=0.5, is_spacer=True, section='nav'),
            KeyDef('KEY_PRINTSCREEN', 'PrtSc', display_name='PrintScreen', section='nav'),
            KeyDef('KEY_SCROLLLOCK', 'ScLk', display_name='ScrollLock', section='nav'),
            KeyDef('KEY_PAUSE', 'Pause', display_name='Pause', section='nav'),
            # Espaço para o teclado numérico
            KeyDef('_GAP_FN_NUM', '', w=0.5, is_spacer=True, section='numpad'),
            KeyDef('_GAP_NUM_DUMMY1', '', w=1.0, is_spacer=True, section='numpad'),
            KeyDef('_GAP_NUM_DUMMY2', '', w=1.0, is_spacer=True, section='numpad'),
            KeyDef('_GAP_NUM_DUMMY3', '', w=1.0, is_spacer=True, section='numpad'),
            KeyDef('_GAP_NUM_DUMMY4', '', w=1.0, is_spacer=True, section='numpad'),
        ],

        # Linha 1: Números e símbolos
        [
            KeyDef('KEY_QUOTE', "'", '"', display_name="'"),
            KeyDef('KEY_1', '1', '!', '¹'),
            KeyDef('KEY_2', '2', '@', '²'),
            KeyDef('KEY_3', '3', '#', '³'),
            KeyDef('KEY_4', '4', '$', '£'),
            KeyDef('KEY_5', '5', '%', '¢'),
            KeyDef('KEY_6', '6', '¨', '¬'),
            KeyDef('KEY_7', '7', '&'),
            KeyDef('KEY_8', '8', '*'),
            KeyDef('KEY_9', '9', '('),
            KeyDef('KEY_0', '0', ')'),
            KeyDef('KEY_MINUS', '-', '_'),
            KeyDef('KEY_EQUAL', '=', '+', '§'),
            KeyDef('KEY_BACKSPACE', 'Backspace', display_name='Backspace', w=2.0),
            # Bloco de navegação
            KeyDef('_GAP_NAV_1', '', w=0.5, is_spacer=True, section='nav'),
            KeyDef('KEY_INSERT', 'Ins', display_name='Insert', section='nav'),
            KeyDef('KEY_HOME', 'Home', display_name='Home', section='nav'),
            KeyDef('KEY_PAGE_UP', 'PgUp', display_name='Page Up', section='nav'),
            # Teclado numérico
            KeyDef('_GAP_NUM_1', '', w=0.5, is_spacer=True, section='numpad'),
            KeyDef('KEY_NUMLOCK', 'Num', display_name='NumLock', section='numpad'),
            KeyDef('KEY_NUMPAD_DIVIDE', '/', display_name='Num /', section='numpad'),
            KeyDef('KEY_NUMPAD_MULTIPLY', '*', display_name='Num *', section='numpad'),
            KeyDef('KEY_NUMPAD_SUBTRACT', '-', display_name='Num -', section='numpad'),
        ],

        # Linha 2: Tab + QWERTY
        [
            KeyDef('KEY_TAB', 'Tab', display_name='Tab', w=1.5),
            KeyDef('KEY_Q', 'Q', '/'),
            KeyDef('KEY_W', 'W', '?'),
            KeyDef('KEY_E', 'E', label_altgr='€'),
            KeyDef('KEY_R', 'R'),
            KeyDef('KEY_T', 'T'),
            KeyDef('KEY_Y', 'Y'),
            KeyDef('KEY_U', 'U'),
            KeyDef('KEY_I', 'I'),
            KeyDef('KEY_O', 'O'),
            KeyDef('KEY_P', 'P'),
            KeyDef('KEY_ACUTE', '´', '`', display_name='´'),
            KeyDef('KEY_BRACKET_LEFT', '[', '{', 'ª', display_name='['),
            KeyDef('_GAP_ISO_ENTER', '', w=1.5, is_spacer=True),  # Espaço para enter ou chave
            # Bloco de navegação
            KeyDef('_GAP_NAV_2', '', w=0.5, is_spacer=True, section='nav'),
            KeyDef('KEY_DELETE', 'Del', display_name='Delete', section='nav'),
            KeyDef('KEY_END', 'End', display_name='End', section='nav'),
            KeyDef('KEY_PAGE_DOWN', 'PgDn', display_name='Page Down', section='nav'),
            # Teclado numérico
            KeyDef('_GAP_NUM_2', '', w=0.5, is_spacer=True, section='numpad'),
            KeyDef('KEY_NUMPAD_7', '7', display_name='Num 7', section='numpad'),
            KeyDef('KEY_NUMPAD_8', '8', display_name='Num 8', section='numpad'),
            KeyDef('KEY_NUMPAD_9', '9', display_name='Num 9', section='numpad'),
            KeyDef('KEY_NUMPAD_ADD', '+', display_name='Num +', h=2.0, section='numpad'),
        ],

        # Linha 3: Caps Lock + ASDFGHJKL + Ç + Enter
        [
            KeyDef('KEY_CAPSLOCK', 'Caps Lock', display_name='Caps Lock', w=1.75),
            KeyDef('KEY_A', 'A'),
            KeyDef('KEY_S', 'S'),
            KeyDef('KEY_D', 'D'),
            KeyDef('KEY_F', 'F'),
            KeyDef('KEY_G', 'G'),
            KeyDef('KEY_H', 'H'),
            KeyDef('KEY_J', 'J'),
            KeyDef('KEY_K', 'K'),
            KeyDef('KEY_L', 'L'),
            KeyDef('KEY_CEDILLA', 'Ç', display_name='Ç'),
            KeyDef('KEY_TILDE', '~', '^', display_name='~'),
            KeyDef('KEY_BRACKET_RIGHT', ']', '}', 'º', display_name=']'),
            KeyDef('KEY_ENTER', 'Enter', display_name='Enter', w=1.25),
            # Bloco de navegação (vazio nesta linha)
            KeyDef('_GAP_NAV_3', '', w=0.5, is_spacer=True, section='nav'),
            KeyDef('_GAP_NAV_3A', '', w=3.0, is_spacer=True, section='nav'),
            # Teclado numérico
            KeyDef('_GAP_NUM_3', '', w=0.5, is_spacer=True, section='numpad'),
            KeyDef('KEY_NUMPAD_4', '4', display_name='Num 4', section='numpad'),
            KeyDef('KEY_NUMPAD_5', '5', display_name='Num 5', section='numpad'),
            KeyDef('KEY_NUMPAD_6', '6', display_name='Num 6', section='numpad'),
            # (Num + ocupa o espaço vertical)
        ],

        # Linha 4: Shift L + \ | + ZXCVBNM + / ? ° + Shift R
        [
            KeyDef('KEY_LSHIFT', 'Shift', display_name='Shift (Esq)', w=1.25),
            KeyDef('KEY_BACKSLASH_ABNT', '\\', '|', display_name='\\'),
            KeyDef('KEY_Z', 'Z'),
            KeyDef('KEY_X', 'X'),
            KeyDef('KEY_C', 'C'),
            KeyDef('KEY_V', 'V'),
            KeyDef('KEY_B', 'B'),
            KeyDef('KEY_N', 'N'),
            KeyDef('KEY_M', 'M'),
            KeyDef('KEY_COMMA', ',', '<', display_name=','),
            KeyDef('KEY_PERIOD', '.', '>', display_name='.'),
            KeyDef('KEY_SEMICOLON', ';', ':', display_name=';'),
            KeyDef('KEY_SLASH_ABNT', '/', '?', '°', display_name='/'),
            KeyDef('KEY_RSHIFT', 'Shift', display_name='Shift (Dir)', w=1.75),
            # Bloco de navegação (Seta para Cima)
            KeyDef('_GAP_NAV_4', '', w=0.5, is_spacer=True, section='nav'),
            KeyDef('_GAP_NAV_4A', '', w=1.0, is_spacer=True, section='nav'),
            KeyDef('KEY_UP', '▲', display_name='Seta Cima', section='nav'),
            KeyDef('_GAP_NAV_4B', '', w=1.0, is_spacer=True, section='nav'),
            # Teclado numérico
            KeyDef('_GAP_NUM_4', '', w=0.5, is_spacer=True, section='numpad'),
            KeyDef('KEY_NUMPAD_1', '1', display_name='Num 1', section='numpad'),
            KeyDef('KEY_NUMPAD_2', '2', display_name='Num 2', section='numpad'),
            KeyDef('KEY_NUMPAD_3', '3', display_name='Num 3', section='numpad'),
            KeyDef('KEY_NUMPAD_ENTER', 'Enter', display_name='Num Enter', h=2.0, section='numpad'),
        ],

        # Linha 5: Modificadores inferiores, Barra de Espaço e Setas
        [
            KeyDef('KEY_LCTRL', 'Ctrl', display_name='Ctrl (Esq)', w=1.25),
            KeyDef('KEY_LWIN', 'Win', display_name='Win', w=1.25),
            KeyDef('KEY_LALT', 'Alt', display_name='Alt (Esq)', w=1.25),
            KeyDef('KEY_SPACE', 'Espaço', display_name='Espaço', w=6.25),
            KeyDef('KEY_ALTGR', 'AltGr', display_name='AltGr', w=1.25),
            KeyDef('KEY_RWIN', 'Win', display_name='Win (Dir)', w=1.25),
            KeyDef('KEY_APPS', 'Menu', display_name='Menu', w=1.25),
            KeyDef('KEY_RCTRL', 'Ctrl', display_name='Ctrl (Dir)', w=1.25),
            # Bloco de navegação (Setas Esquerda, Baixo, Direita)
            KeyDef('_GAP_NAV_5', '', w=0.5, is_spacer=True, section='nav'),
            KeyDef('KEY_LEFT', '◄', display_name='Seta Esquerda', section='nav'),
            KeyDef('KEY_DOWN', '▼', display_name='Seta Baixo', section='nav'),
            KeyDef('KEY_RIGHT', '►', display_name='Seta Direita', section='nav'),
            # Teclado numérico (0 amplo e vírgula decimal)
            KeyDef('_GAP_NUM_5', '', w=0.5, is_spacer=True, section='numpad'),
            KeyDef('KEY_NUMPAD_0', '0', display_name='Num 0', w=2.0, section='numpad'),
            KeyDef('KEY_NUMPAD_DECIMAL', ',', display_name='Num ,', section='numpad'),
            # (Num Enter ocupa o espaço vertical)
        ]
    ]

# Mapeamento rápido de ID para nome amigável para exibição nos atalhos
KEY_DISPLAY_NAMES = {}
for _row in create_abnt2_rows():
    for _k in _row:
        if not _k.is_spacer:
            KEY_DISPLAY_NAMES[_k.id] = _k.display_name
