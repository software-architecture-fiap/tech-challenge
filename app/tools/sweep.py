import fnmatch
import os
from typing import List, Optional

IGNORED_DIRS = ['node_modules', 'build', 'public', '.venv', '__pycache__', '.git', 'log', 'install']

def generate_directory_tree(root_dir: str, output_file: str, ignore_patterns: Optional[List[str]] = None) -> None:
    """Gera um arquivo com a árvore de diretórios a partir do diretório raiz especificado.

    Args:
        root_dir (str): Diretório raiz para gerar a árvore de diretórios.
        output_file (str): Caminho do arquivo de saída onde a árvore será salva.
        ignore_patterns (Optional[List[str]]): Lista de padrões para ignorar arquivos e diretórios.

    Returns:
        None
    """
    if ignore_patterns is None:
        ignore_patterns = []

    with open(output_file, 'w', encoding='utf-8') as output:
        output.write('# Directory Tree\n\n')

        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Ignora diretórios especificados
            dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
            # Filtra as pastas e arquivos ignorados pelo padrão .gitignore
            dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(d, pat) for pat in ignore_patterns)]
            filtered_filenames = [f for f in filenames if not any(fnmatch.fnmatch(f, pat) for pat in ignore_patterns)]

            depth = dirpath.count(os.sep) - root_dir.count(os.sep)
            indent = '  ' * depth

            output.write(f'{indent}- {os.path.basename(dirpath)}/\n')
            for filename in sorted(filtered_filenames):
                output.write(f'{indent}  - {filename}\n')

if __name__ == '__main__':
    root_directory = './'
    output_file = 'directory_tree.md'
    gitignore_path = os.path.join(root_directory, '.gitignore')

    ignore_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as gitignore_file:
            ignore_patterns = gitignore_file.read().splitlines()

    generate_directory_tree(root_directory, output_file, ignore_patterns)
