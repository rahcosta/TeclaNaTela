"""
Script utilitário para gerar o arquivo executável único (.exe) para Windows.
Utiliza o PyInstaller configurado para empacotar a aplicação completa.
"""

import sys
import subprocess
import os

def build():
    print("Iniciando a compilação do executável Teclado_Didatico_ABNT2.exe...")
    
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--clean",
        "--name", "Teclado_Didatico_ABNT2",
        "main.py"
    ]
    
    print(f"Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        exe_path = os.path.abspath(os.path.join("dist", "Teclado_Didatico_ABNT2.exe"))
        print("\n==================================================")
        print(" COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f" Executável gerado em: {exe_path}")
        print("==================================================")
    else:
        print(f"\nErro na compilação. Código de retorno: {result.returncode}")

if __name__ == "__main__":
    build()
