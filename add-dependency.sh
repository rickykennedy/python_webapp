# This is a bit of a hack, but it works for simple cases.
# It uses 'sed' to remove version constraints so poetry can resolve the latest compatible versions.
cat requirements.txt | sed 's/==.*//' | xargs -n 1 poetry add

#alternatively, you can use pip to freeze the current environment and then add those packages to poetry.
# This will create a temporary requirements file, add it to poetry, and then clean up.
pip freeze > temp-requirements.txt
poetry add $(cat temp-requirements.txt)

# If you want to add all dependencies from a requirements.txt file to a Poetry project,
# you can use the following command:
poetry add $(pip freeze | grep -v 'pkg-resources==')  # optional if no requirements.txt
# or directly:
poetry add $(cat requirements.txt)
