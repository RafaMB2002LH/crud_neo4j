from py2neo import Graph, Node, Relationship
import json

# Conéctate a tu base de datos Neo4j
ruta_archivo = "C:\python\credencialesNeo4j.json"
with open(ruta_archivo, 'r') as archivo:
    datos_json = json.load(archivo)
graph = Graph("bolt://localhost:7687", auth=(datos_json['user'], datos_json['password']))

# Operación CREATE (Crear)
def create_node(label, properties):
    node = Node(label, **properties)
    graph.create(node)
    return node

# Operación READ (Leer)
def read_nodes(label):
    query = f"MATCH (n:{label}) RETURN n"
    result = graph.run(query)
    return result.data()

def read_all_nodes():
    query = "MATCH (n) RETURN n"
    result = graph.run(query)
    return result.data()

def select_node_by_id(node_id):
    query = f"MATCH (n) WHERE ID(n) = {node_id} RETURN n"
    result = graph.run(query)
    return result.data()

def update_node(node_id, properties):
    query = "MATCH (n) WHERE ID(n) = $node_id SET n += $properties RETURN n"
    result = graph.run(query, node_id=node_id, properties=properties)
    return result.data()


# Operación UPDATE (Actualizar)
def update_node(node, properties):
    query = f"MATCH (p:Persona {id: 1}) SET p.nombre = 'NuevoNombre' RETURN p;"
    result = graph.run(query)
    return result.data()

# Operación DELETE (Eliminar)
def delete_node(node):
    graph.delete(node)

def delete_node_id(node_id):
    graph.run(f"MATCH (n) WHERE ID(n) = {node_id} DETACH DELETE n")


if __name__ == "__main__":

    while True:

        print("Que quieres hacer?\n")
        print("----------------------")
        print("-1 -> Leer nodo por ID\n-2 -> Leer todos los nodos\n-3 -> Actualizar nodo por id\n-4 -> Eliminar nodo por ID\n-5 -> Crear nodo de ejemplo\n-6 -> Salir del programa")
        print("----------------------")

        inp = int(input("Escribe el numero de opcion que quiras: "))

        if inp == 1:
            id = input("Introduzca la id del nodo que quiere leer: ")
            selected_node = select_node_by_id(id)
            print(f"Nodo seleccionado por ID: {selected_node}")
            break
        elif inp == 2:
            todos_los_nodos = read_all_nodes()
            for nodo in todos_los_nodos:
                print(nodo)
            break
        elif inp == 3:
            id = input("Introduzca la id del nodo que quiere actualizar: ")
            selected_nodes = select_node_by_id(id)
    
            if selected_nodes:
                selected_node = selected_nodes[0]
                nombre_propiedad = input("Escriba el nombre de la propiedad a modificar: ")
                propiedad = input("Escriba la propiedad a modificar: ")
                a = {nombre_propiedad: propiedad}
                update_node(selected_node['n'].identity, a)
                print(f"Nodo actualizado: {read_nodes('Persona')}")
            else:
                print(f"No se encontró un nodo con la ID {id}")
            break
        elif inp == 4:
            id = input("Introduzca la id del nodo que quiere eliminar: ")
            selected_node = select_node_by_id(id)
            delete_node_id(id)
            print(f"Nodo eliminado: {read_nodes('Persona')}")
            break
        elif inp == 5:
            node_properties = {"nombre": "Ejemplo Nodo", "edad": 25}
            created_node = create_node("Persona", node_properties)
            print(f"Nodo creado: {created_node}")
            break
        elif inp == 6:
            break
        else:
            inp = int(input("Opcion no valida, esciba una valida: "))
    # Ejemplos de uso
    # Crear un nodo
    #node_properties = {"nombre": "Ejemplo Nodo", "edad": 25}
    #created_node = create_node("Persona", node_properties)
    #print(f"Nodo creado: {created_node}")

    # Leer nodos
    #nodes = read_nodes("Persona")
    #print(f"Nodos leídos: {nodes}")

    #selected_node = select_node_by_id(176)
    #print(f"Nodo seleccionado por ID: {selected_node}")

    # Actualizar nodo
    #update_node(selected_node.identity, {"edad": 26})
    #print(f"Nodo actualizado: {read_nodes('Persona')}")

    # Eliminar nodo
    #delete_node_id(177)
    #print(f"Nodo eliminado: {read_nodes('Persona')}")