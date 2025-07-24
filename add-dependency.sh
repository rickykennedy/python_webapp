# This is a bit of a hack, but it works for simple cases.
# It uses 'sed' to remove version constraints so poetry can resolve the latest compatible versions.
cat requirements.txt | sed 's/==.*//' | xargs -n 1 poetry add