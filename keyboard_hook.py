"""
Módulo de monitoramento de teclado 100% passivo para Windows.
Utiliza a API Win32 GetAsyncKeyState em thread dedicada a 60 FPS (~16ms).

Vantagens desta arquitetura:
1. 100% PASSIVO: NÃO instala ganchos no sistema operacional (SetWindowsHookEx),
   o que GARANTE que NENHUMA tecla seja bloqueada, atrasada ou impedida de ser digitada
   no Bloco de Notas, navegadores, Word, terminais ou outros programas.
2. SUPORTE A TECLAS MANTIDAS PRESSIONADAS: Detecta continuamente o estado elétrico/físico
   das teclas. Enquanto o professor segurar a tecla (ou combinação de teclas), ela permanece
   acesa no teclado virtual.
3. CONFIABILIDADE ABSOLUTA: Imune a timeouts de ganchos do Windows (LowLevelHooksTimeout),
   isolamento de privilégios (UIPI) ou programas executando como Administrador.
4. PRIVACIDADE: Não registra, não salva e não transmite histórico de digitação.
"""

import ctypes
from typing import Dict, Set
from PyQt5.QtCore import QThread, pyqtSignal

user32 = ctypes.windll.user32

# Mapeamento completo de Virtual-Keys (VK) para identificadores ABNT2
VK_MAP: Dict[int, str] = {
    # Modificadores individuais (Esquerda / Direita)
    0xA0: 'KEY_LSHIFT',
    0xA1: 'KEY_RSHIFT',
    0xA2: 'KEY_LCTRL',
    0xA3: 'KEY_RCTRL',
    0xA4: 'KEY_LALT',
    0xA5: 'KEY_ALTGR',
    0x5B: 'KEY_LWIN',
    0x5C: 'KEY_RWIN',
    0x5D: 'KEY_APPS',

    # Controle e navegação
    0x1B: 'KEY_ESC',
    0x08: 'KEY_BACKSPACE',
    0x09: 'KEY_TAB',
    0x14: 'KEY_CAPSLOCK',
    0x0D: 'KEY_ENTER',
    0x20: 'KEY_SPACE',
    0x2C: 'KEY_PRINTSCREEN',
    0x91: 'KEY_SCROLLLOCK',
    0x13: 'KEY_PAUSE',
    0x2D: 'KEY_INSERT',
    0x2E: 'KEY_DELETE',
    0x24: 'KEY_HOME',
    0x23: 'KEY_END',
    0x21: 'KEY_PAGE_UP',
    0x22: 'KEY_PAGE_DOWN',
    0x26: 'KEY_UP',
    0x28: 'KEY_DOWN',
    0x25: 'KEY_LEFT',
    0x27: 'KEY_RIGHT',

    # Teclas específicas do padrão brasileiro ABNT2
    0xBA: 'KEY_CEDILLA',          # Ç (VK_OEM_1 - sc 0x27)
    0xC1: 'KEY_SLASH_ABNT',       # / ? ° (VK_ABNT_C1 - sc 0x73)
    0xC2: 'KEY_NUMPAD_DECIMAL',   # Numpad , (VK_ABNT_C2 - sc 0x7E)
    0xE2: 'KEY_BACKSLASH_ABNT',   # \ | (VK_OEM_102 - sc 0x56)
    0xDE: 'KEY_TILDE',            # ~ ^ (VK_OEM_7 - sc 0x28)
    0xDB: 'KEY_ACUTE',            # ´ ` (VK_OEM_4 - sc 0x1A)
    0xDD: 'KEY_BRACKET_LEFT',     # [ { ª (VK_OEM_6 - sc 0x1B)
    0xDC: 'KEY_BRACKET_RIGHT',    # ] } º (VK_OEM_5 - sc 0x2B)
    0xBF: 'KEY_SEMICOLON',        # ; : (VK_OEM_2 - sc 0x35)
    0xC0: 'KEY_QUOTE',            # ' " (VK_OEM_3 - sc 0x29)
    0xBD: 'KEY_MINUS',            # - _ (VK_OEM_MINUS)
    0xBB: 'KEY_EQUAL',            # = + (VK_OEM_PLUS)
    0xBC: 'KEY_COMMA',            # , < (VK_OEM_COMMA)
    0xBE: 'KEY_PERIOD',           # . > (VK_OEM_PERIOD)

    # Teclado Numérico
    0x90: 'KEY_NUMLOCK',
    0x6F: 'KEY_NUMPAD_DIVIDE',
    0x6A: 'KEY_NUMPAD_MULTIPLY',
    0x6D: 'KEY_NUMPAD_SUBTRACT',
    0x6B: 'KEY_NUMPAD_ADD',
    0x6E: 'KEY_NUMPAD_DECIMAL',
}

# Letras A-Z
for code in range(0x41, 0x5B):
    VK_MAP[code] = f'KEY_{chr(code)}'

# Números 0-9 (linha superior)
for code in range(0x30, 0x3A):
    VK_MAP[code] = f'KEY_{chr(code)}'

# Teclas de Função F1-F12
for code in range(0x70, 0x7C):
    VK_MAP[code] = f'KEY_F{code - 0x70 + 1}'

# Teclado Numérico 0-9
for code in range(0x60, 0x6A):
    VK_MAP[code] = f'KEY_NUMPAD_{code - 0x60}'


class KeyboardHookThread(QThread):
    """
    Monitor contínuo passivo do estado físico do teclado.
    Emite sinais em tempo real para a interface gráfica sem NENHUMA interferência
    na digitação dos demais aplicativos do computador.
    """
    key_pressed = pyqtSignal(str, str)
    key_released = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._running = False
        self._pressed_keys: Set[str] = set()

    def run(self):
        self._running = True
        check_items = list(VK_MAP.items())

        while self._running:
            current_active: Set[str] = set()

            # 1. Consulta o estado físico de cada tecla
            for vk, kid in check_items:
                if user32.GetAsyncKeyState(vk) & 0x8000:
                    current_active.add(kid)

            # 2. Salvaguardas para teclas modificadoras genéricas
            if user32.GetAsyncKeyState(0x10) & 0x8000:  # VK_SHIFT
                if 'KEY_LSHIFT' not in current_active and 'KEY_RSHIFT' not in current_active:
                    current_active.add('KEY_LSHIFT')

            if user32.GetAsyncKeyState(0x11) & 0x8000:  # VK_CONTROL
                if 'KEY_LCTRL' not in current_active and 'KEY_RCTRL' not in current_active:
                    current_active.add('KEY_LCTRL')

            if user32.GetAsyncKeyState(0x12) & 0x8000:  # VK_MENU (Alt)
                if 'KEY_LALT' not in current_active and 'KEY_ALTGR' not in current_active:
                    current_active.add('KEY_LALT')

            # 3. Detecta teclas recém-pressionadas (aciona o destaque visual)
            newly_pressed = current_active - self._pressed_keys
            for kid in newly_pressed:
                self.key_pressed.emit(kid, kid)

            # 4. Detecta teclas soltas (remove o destaque visual)
            newly_released = self._pressed_keys - current_active
            for kid in newly_released:
                self.key_released.emit(kid)

            # 5. Atualiza o conjunto de teclas atualmente ativas
            self._pressed_keys = current_active

            # Taxa de atualização fluida (~60 FPS = 16ms) com consumo desprezível de CPU
            self.msleep(16)

    def stop(self):
        self._running = False
        self.wait(1000)
