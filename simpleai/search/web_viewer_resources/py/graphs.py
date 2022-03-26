from browser import ajax, window


# javascript "imports"
d3 = window.d3
jq = window.jQuery

node_radius = 30

def render_graph(root_nodes, nodes_count, max_depth):
    """
    Render a graph or tree, starting from a list of root nodes.
    Nodes
    """
    jq("#graph-image").html("")


    if not root_nodes:
        return
    
    width = 1900 
    height = 1000

    # initialize a d3 nodes hierarchy
    treemap = d3.tree().size([height, width])\
        .separation(lambda a, b: 10)
    nodes = d3.hierarchy(root_nodes[0], lambda d: d.children)  # TODO what if more than one root?
    nodes = treemap(nodes)

    # zoom
    zoom = d3.zoom()\
        .on('zoom', handle_zoom)

    # initialize the svg to draw on it with d3
    svg = d3.select("#graph-image").append("svg")\
            .attr("width", width)\
            .attr("height", height)\
            .attr("viewbox", f"{width / 2 } {max_depth * 150} 0 0")

    # attach d3.zoom to svg figure
    graph = svg.call(zoom)\
        .append("g")\
    

    # draw the links between nodes (before the nodes themselves, so the nodes come on top)
    links = graph.selectAll(".link")\
         .data(nodes.descendants()[1:])\
         .enter().append("path")\
         .attr("class", "link")\
         .attr("d", get_curved_path)
    
    # tie all the nodes to their data
    node = graph.selectAll(".node")\
                .data(nodes.descendants())\
                .enter().append("g")\
                .attr("class", get_node_class)\
                .attr("transform", translate_to_position)

    # draw the circles for each node
    node.append("circle")\
        .attr("r", node_radius)

    # draw the labels for each node
    node.append("text")\
        .text(get_node_name)

    return


def handle_zoom(e, *args):
    d3.select("g").attr("transform", e.transform)


def get_node_class(d, *args):
    """
    Get the d3 node classes from the node data.
    """
    return " ".join(["node"] + d.data.modifiers)


def get_node_name(d, *args):
    """
    Get the d3 node name from the node data.
    """
    return d.data.name


def translate_to_position(d, *args):
    """
    Translate a d3 element to the position of its related node.
    """
    y = d.depth * 150
    x = d.x + (window.innerWidth / 2)
    return f"translate({d.x},{y})"


def get_curved_path(d, *args):
    """
    Get the parameters required for a curved path in a link.
    """
    parent_y = d.parent.depth * 150
    parent_x = d.parent.x 
    y = d.depth * 150
    x = d.x 

    return (
        f"M{x},{y}" 
        f"C{x}, {(y + parent_y) / 2}"
        f" {parent_x}, {(y + parent_y) / 2}"
        f" {parent_x},{parent_y}"
    )
