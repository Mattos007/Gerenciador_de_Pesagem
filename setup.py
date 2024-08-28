import sys
from cx_Freeze import setup, Executable

# Nome do ícone (para Linux, ícones normalmente são gerenciados pelos ambientes gráficos)
# Se desejar incluir ícone para Linux, precisará usar formatos .png ou .svg e adicionar manualmente ao .desktop file

# Arquivos adicionais (imagens, etc.)
includefiles = ['background.jpg', 'splash_image.png']

# Opções para a construção
build_exe_options = {
    "packages": ["os", "tkinter", "pandas", "PIL", "sqlite3", "datetime"],
    "include_files": includefiles,
    "optimize": 2,  # Otimização de bytecode
    "zip_include_packages": "*",  # Inclui todos os pacotes no arquivo zipado para evitar fácil extração
    "zip_exclude_packages": []  # Especifica pacotes a serem excluídos, se necessário
}

# Configuração do executável
executables = [
    Executable(
        script="competicao.py",  # Substitua pelo nome do seu script principal
        base=None,  # Para Linux, o terminal geralmente não é ocultado
        target_name="Competição"  # Nome do executável gerado
    )
]

setup(
    name="Controle de pesagens",
    version="1.0",
    description="Esse programa armazena dados de pesagens diárias de funcioários de uma empresa de temperos",
    options={"build_exe": build_exe_options},
    executables=executables
)
