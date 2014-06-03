# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#    
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    springgraph.py
#
#    @@@ Under development
#
from xierpa3.components.container import Container
from xierpa3.descriptors.blueprint import BluePrint

class SpringGraph(Container):

    BLUEPRINT = BluePrint(
    )
       
    def buildSpringGraph(self, id, root, width, height, **args):
        self.text("""<!--[if lte IE 8]><script type="text/javascript" src="excanvas.js"></script><![endif]-->""")
        self.script(src='http://s3.amazonaws.com/data.xierpalib.com/_root/' + self.PATH_SPRINGGRAPH_JS)
        self.script()
        self.output("""
        function init_graph_%(id)s() {
            g = new Graph(document.getElementById("_ctx"));
        """ % {'id': id})
        
        # Build the nodes, edges and set of unique node models
        nodesd, edgesjs = self.getSpringGraphNode(root, **args)

        self.output("""var nodes = {""")
        first = True
        for nodeid, nodeparams in nodesd.items():
            if not first:
                self.output(',\n')
            first = False
            self.output(""" "%s": %s""" % (nodeid, self.TX.args2JsArguments(**nodeparams)))
        self.output("""};\n""")
        
        # Generate list with edges and build list with used unique nodes
        self.output("""var edges = [""")
        first = True
        for nodeid1, nodeid2, edgeparams in edgesjs:
            if not first:
                self.output(',\n')
            first = False
            self.output("""["%s", "%s", %s]""" % (nodeid1, nodeid2, self.TX.args2JsArguments(**edgeparams)))
        self.output('];\n')

        self.output("""
            for (var id in nodes) {
                g.addNode(id, nodes[id]);
            }
            for (var i=0; i < edges.length; i++) {
                var n1 = g.nodeset[edges[i][0]];
                var n2 = g.nodeset[edges[i][1]];
                g.addEdge(n1, n2, edges[i][2]);
            }
            for (var i=0; i < g.nodes.length; i++) {
                var n = g.nodes[i];
                n.radius = n.radius + n.radius * n.weight;
            }
            for (var i=0; i < g.nodes.length; i++) {
                var e = g.nodes[i].edges();
                if (e.length == 1) {
                    e[0].length *= 8;
                }
            }
            g.prune(0);
            g.layout.k = 2.0;             // Force constant (= edge length).
            g.layout.force = 0.05;        // Repulsive strength.
            g.layout.repulsion = 150;     // Repulsive radius.
            g.betweennessCentrality();
            g.eigenvectorCentrality();
            g.loop({frames:500, fps:20, ipf:4, weighted:0.5, directed:false});
        }""")
        self._script()
        self.style()
        self.output(""".node-label { margin-left:12px;font: %(labelsize)spx sans-serif; }""" % {'labelsize': args.get('labelsize') or 11})
        self._style()

        self.div(style="width:%(width)spx; height:%(height)spx;" % {'width': width, 'height': height})
        self.canvas(id="_ctx", width=width, height=height)
        self._canvas()
        self._div()
        self.script()
        self.output('init_graph_%(id)s();' % {'id': id})
        self._script()
        
    def getSpringGraphNode(self, root, nodesd=None, edgesjs=None, **args):
        nodesd = nodesd or {}
        edgesjs = edgesjs or []
        label = root.label or root.name or root.id
        if root.isRoot():
            d = {'label': label, 'radius': args.get('rootradius', 10), 'fill': args.get('rootfill', 'rgba(240,240,240,0.7)')}
        else:
            d = {'label': label, 'radius': args.get('rootradius', 4), 'fill': args.get('fill', 'rgba(220,220,220,0.7)')}
        nodesd[root.id] = d

        for node in root.getNodes():
            edgesjs.append((root.id, node.id, {'stroke': args.get('stroke', 1)}))
            self.getSpringGraphNode(node, nodesd, edgesjs, **args)
        return nodesd, edgesjs