#Kilde: https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/
import pandas as pd                 #create dataframe      Install:python -m pip install pandas 
import networkx as nx               #create kg             Install:python -m pip install networkx
import matplotlib.pyplot as plt     #display graph         Install:python -m pip install -U matplotlib

#data RDF_tuples['Subject', 'Predicate', 'Object']
RDF_tuples = [['Kate', 'is a', 'student'], 
    ['Kate', 'studies at', 'Aalborg University'], 
    ['Kate', 'is a', 'person'], 
    ['Kate', 'studies in', 'Denmark'], 
    ['Aalborg University', 'is a', 'university'], 
    ['Aalborg University', 'is located in', 'Denmark']
]

subjects = [i[0] for i in RDF_tuples]      #extract subjects       Ex: ['Kate', 'Kate', 'Kate', 'Kate', 'Aalborg University', 'Aalborg University']
predicates = [i[1] for i in RDF_tuples]    #extract predicates     Ex: ['is a', 'studies at', 'is a', 'studies in', 'is a', 'is located in']
objects = [i[2] for i in RDF_tuples]       #extract objects        Ex: ['student', 'Aalborg University', 'person', 'Denmark', 'university', 'Denmark']

#Create dataframe
kg_df = pd.DataFrame({'subjects':subjects, 'objects':objects, 'predicates':predicates})

#Create a directed-graph KG from dataframe
G=nx.from_pandas_edgelist(kg_df, "subjects", "objects", edge_attr=True, create_using=nx.MultiDiGraph())

#Draw and display KG
plt.figure(figsize=(12,12))
pos = nx.spring_layout(G, k = 0.5)
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
plt.show()