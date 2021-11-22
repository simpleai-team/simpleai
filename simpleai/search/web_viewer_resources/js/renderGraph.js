var treeData = {
    "nodes_count": 22,
    "max_depth": 6,
    "nodes": [
        {
            "children": [
                {
                    "children": [
                        {
                            "modifiers": ["in_fringe"],
                            "name": "((3, 7, 1), (8, 2, 0), (4, 6, 5))",
                            "tooltip": "\nCost: 2\nHeuristic: 13"
                        }
                    ],
                    "name": "((3, 7, 0), (8, 2, 1), (4, 6, 5))",
                    "tooltip": "\nCost: 1\nHeuristic: 14"
                },
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "modifiers": ["in_fringe"],
                                    "name": "((0, 2, 7), (3, 8, 1), (4, 6, 5))",
                                    "tooltip": "\nCost: 3\nHeuristic: 12"
                                },
                                {
                                    "children": [
                                        {
                                            "children": [
                                                {
                                                    "children": [
                                                        {
                                                            "modifiers": ["in_fringe"],
                                                            "name": "((3, 2, 7), (0, 4, 1), (6, 8, 5))",
                                                            "tooltip": "\nCost: 6\nHeuristic: 9"
                                                        },
                                                        {
                                                            "modifiers": ["in_fringe"],
                                                            "name": "((3, 2, 7), (4, 1, 0), (6, 8, 5))",
                                                            "tooltip": "\nCost: 6\nHeuristic: 9"
                                                        },
                                                        {
                                                            "modifiers": ["in_fringe"],
                                                            "name": "((3, 0, 7), (4, 2, 1), (6, 8, 5))",
                                                            "tooltip": "\nCost: 6\nHeuristic: 11"
                                                        }
                                                    ],
                                                    "name": "((3, 2, 7), (4, 0, 1), (6, 8, 5))",
                                                    "tooltip": "\nCost: 5\nHeuristic: 10"
                                                },
                                                {
                                                    "modifiers": ["in_fringe"],
                                                    "name": "((3, 2, 7), (4, 8, 1), (6, 5, 0))",
                                                    "tooltip": "\nCost: 5\nHeuristic: 12"
                                                }
                                            ],
                                            "name": "((3, 2, 7), (4, 8, 1), (6, 0, 5))",
                                            "tooltip": "\nCost: 4\nHeuristic: 11"
                                        }
                                    ],
                                    "name": "((3, 2, 7), (4, 8, 1), (0, 6, 5))",
                                    "tooltip": "\nCost: 3\nHeuristic: 12"
                                }
                            ],
                            "name": "((3, 2, 7), (0, 8, 1), (4, 6, 5))",
                            "tooltip": "\nCost: 2\nHeuristic: 13"
                        },
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "children": [
                                                {
                                                    "modifiers": ["in_fringe"],
                                                    "name": "((3, 1, 2), (8, 0, 7), (4, 6, 5))",
                                                    "tooltip": "\nCost: 5\nHeuristic: 10"
                                                },
                                                {
                                                    "modifiers": ["in_fringe"],
                                                    "name": "((0, 3, 2), (8, 1, 7), (4, 6, 5))",
                                                    "tooltip": "\nCost: 5\nHeuristic: 12"
                                                }
                                            ],
                                            "name": "((3, 0, 2), (8, 1, 7), (4, 6, 5))",
                                            "tooltip": "\nCost: 4\nHeuristic: 11"
                                        }
                                    ],
                                    "name": "((3, 2, 0), (8, 1, 7), (4, 6, 5))",
                                    "tooltip": "\nCost: 3\nHeuristic: 12"
                                },
                                {
                                    "children": [
                                        {
                                            "modifiers": ["in_fringe"],
                                            "name": "((3, 2, 7), (8, 1, 5), (4, 0, 6))",
                                            "tooltip": "\nCost: 4\nHeuristic: 13"
                                        }
                                    ],
                                    "name": "((3, 2, 7), (8, 1, 5), (4, 6, 0))",
                                    "tooltip": "\nCost: 3\nHeuristic: 12"
                                }
                            ],
                            "name": "((3, 2, 7), (8, 1, 0), (4, 6, 5))",
                            "tooltip": "\nCost: 2\nHeuristic: 13"
                        },
                        {
                            "modifiers": ["in_fringe"],
                            "name": "((3, 2, 7), (8, 6, 1), (4, 0, 5))",
                            "tooltip": "\nCost: 2\nHeuristic: 15"
                        }
                    ],
                    "name": "((3, 2, 7), (8, 0, 1), (4, 6, 5))",
                    "tooltip": "\nCost: 1\nHeuristic: 14"
                },
                {
                    "modifiers": ["in_fringe"],
                    "name": "((0, 3, 7), (8, 2, 1), (4, 6, 5))",
                    "tooltip": "\nCost: 1\nHeuristic: 16"
                }
            ],
            "name": "((3, 0, 7), (8, 2, 1), (4, 6, 5))",
            "tooltip": "\nCost: 0\nHeuristic: 15"
        }
    ],
};


// ************** Generate the tree diagram	 *****************

var margin = { top: 20, right: 120, bottom: 20, left: 120 },
    width = (treeData.nodes_count * 50) - margin.right - margin.left,
    height = (treeData.max_depth * 200) - margin.top - margin.bottom;

var i = 0,
    duration = 0,
    root;

var tree = d3.layout.tree().size([width, height]);

var diagonal = d3.svg.diagonal().projection(function (d) { return [d.x, d.y]; });

var svg = d3.select("#graph-image").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function update(source) {
    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function (d) { d.y = d.depth * 180; });

    // Update the nodes…
    var node = svg.selectAll("g.node").data(nodes, function (d) {
        return d.id || (d.id = ++i);
    });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", function (d) {
            let classesCss = ""
            d.modifiers?.forEach(modifier => {
                switch (modifier) {
                    case modifier === "choosen":
                        classesCss += "choosen"
                    case modifier === "newly":
                        classesCss += "newly"
                    case modifier === "goal":
                        classesCss += "goal"
                    case modifier === "visited":
                        classesCss += "visited"
                    default:
                        classesCss += "newly"
                }
            })
            return `node ${classesCss}`
        })
        .attr("transform", function (d) { return "translate(" + source.x0 + "," + source.y0 + ")"; })
        .on("click", click);

    nodeEnter.append("circle")
        .attr("r", 1e-6)
        .style("fill", function (d) { return d._children ? "lightsteelblue" : "#fff"; })
        .on("mouseenter", function(d){
            d3.select(this.parentNode).select("text").style("visibility", "visible");
        })
        .on("mouseleave", function(d){
            d3.select(this.parentNode).select("text").style("visibility", "hidden");
        });

    nodeEnter.append("text")
        .attr("x", function (d) { return d.children || d._children ? -13 : 13; })
        .attr("dy", ".35em")
        .attr("text-anchor", function (d) { return d.children || d._children ? "end" : "start"; })
        .text(function (d) { return `${d.name.slice(0, 10)}...`; })
        .style("fill-opacity", 1e-6)
        .style("visibility", "hidden")

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; });

    nodeUpdate.select("circle")
        .attr("r", 10)
        .style("fill", function (d) { return d._children ? "lightsteelblue" : "#fff"; });

    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function (d) { return "translate(" + source.x + "," + source.y + ")"; })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links…
    var link = svg.selectAll("path.link")
        .data(links, function (d) { return d.target.id; });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function (d) {
            var o = { x: source.x0, y: source.y0 };
            return diagonal({ source: o, target: o });
        });

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function (d) {
            var o = { x: source.x, y: source.y };
            return diagonal({ source: o, target: o });
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function (d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

// Toggle children on click.
function click(d) {
    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
    update(d);
}

function renderGraph() {
    root = treeData.nodes[0];
    root.x0 = height / 2;
    root.y0 = 0;
    update(root);
    d3.select(self.frameElement).style("height", "500px");
}
/*
-Blue border, white background: nodes that are currently part of the fringe (waiting to be visited).
-Blue border, blue background: current node, being analyzed or expanded.
-Orange border, white background: newly created nodes, after expanding a parent node.
-Black border, green background: the solution node (goal for traditional search, or best node for local search).
-Black border, white background: the rest of the nodes kept in memory, needed to keep the search tree from the fringe to the initial node.
*/