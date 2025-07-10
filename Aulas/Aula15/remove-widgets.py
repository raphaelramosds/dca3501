import nbformat

# Caminho para o seu notebook
notebook_path = "notebook_aula15.ipynb"

# Lê o notebook
nb = nbformat.read(notebook_path, as_version=4)

# Remove o metadata.widgets, se existir
if "widgets" in nb.metadata:
    del nb.metadata["widgets"]

# Salva o notebook limpo
nbformat.write(nb, notebook_path)

print("Metadados de widgets removidos com sucesso.")