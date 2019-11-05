library(igraph)
library(CINNA)

# Read CSV files exported by code.py
nodes <- read.csv("Documents/ECE720/asn1/data/askerAnswerer_nodes.tsv", sep="\t")
edges <- read.csv("Documents/ECE720/asn1/data/askerAnswerer_edges.tsv", sep="\t")

# Generate graph
net <-graph.data.frame(edges, nodes, directed=T)

# Save graph to file askerAnswerer.pdf
pdf(file="Documents/ECE720/asn1/askerAnswerer.pdf")
plot(net, vertex.size=1, vertex.label=NA, edge.width=0.25, edge.arrow.size=.1, edge.arrow.width=0.5, layout=layout_components(net))
dev.off()

# Save graph to file askerAnswerer.jpg
jpeg(file="Documents/ECE720/asn1/askerAnswerer.jpg", width = 480*4, height = 480*4)
plot(net, vertex.size=1, vertex.label=NA, edge.width=0.25, edge.arrow.size=.1, edge.arrow.width=0.5, layout=layout_components(net))
dev.off()

# Get giant component of graph and save as PDF
net2 = giant_component_extract(net)
pdf(file="Documents/ECE720/asn1/askerAnswerer-giant.pdf")
plot(net2[[1]], vertex.size=1, vertex.label=NA, edge.width=0.25, edge.arrow.size=.1, edge.arrow.width=0.5, layout=layout_components(net2[[1]]))
dev.off()

# Save giant component as JPG
jpeg(file="Documents/ECE720/asn1/askerAnswerer-giant.jpg", width = 480*4, height = 480*4)
plot(net2[[1]], vertex.size=1, vertex.label=NA, edge.width=0.25, edge.arrow.size=.1, edge.arrow.width=0.5, layout=layout_components(net2[[1]]))
dev.off()

# Write giant component of graph to new TSV file
write.table(net2[[2]], file="Documents/ECE720/asn1/data/asker-answerer-giant.tsv", quote=FALSE, sep="\t", col.names=NA)
