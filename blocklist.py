"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be imported by
app and the logout resource so that tokens can be added to the blocklist when the
user logs out.
"""

BLOCKLIST = set() # Podría ser un conjunto de Redis (ni idea que es (por ahora)), por ejemplo para hacerlo más escalable
# o tambien se puede usar una base de datos para almacenar los tokens en la lista negra