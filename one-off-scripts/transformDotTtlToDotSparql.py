import os
import glob
from rdflib import Graph

# Path to Turtle files
ttl_files_path = '../scholia/app/templates/*ttl'

# Get the list of .ttl files
ttl_files = glob.glob(ttl_files_path)

# Process each Turtle file
for i in ttl_files:
    # Extract the filename (fn) and create .sparql filename
    fn = os.path.basename(i)[0:-4]  # extract name without extension
    sparql = i[0:-4] + ".sparql"  # create .sparql filename

    # Open .ttl file to write
    g = Graph()
    g.parse(i)

    with open(sparql, 'w') as sparql_file:
        knows_query = """prefix sh: <http://www.w3.org/ns/shacl#>
SELECT DISTINCT ?query ?sparql
WHERE {
    ?query sh:select | sh:ask | sh:construct ?sparql .
}"""

        qres = g.query(knows_query)
        for row in qres:
            sparql_file.write(f"{row.sparql}")
