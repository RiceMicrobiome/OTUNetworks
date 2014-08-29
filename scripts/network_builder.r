#############################################################
#	The purpose of this script is to take an OTU table, 
#	perform pairwise correlations between each OTU, and
#	then perform heirarchical clustering using the distance
#	matrix from the correllation matrix.  It will save the 
#	resulting tree in an R object for later analysis.
#
#	usage: HC_Tree_Builder.r otu_table.txt spearman output_file.rda
#
#	load the rda object into R, it's name is otu.hc

args <- commandArgs(TRUE)

otu.table.file = args[1]
method = args[2]
out.file = args[3]

library(dynamicTreeCut)

otu_table <- read.table(otu.table.file, header = T, row.names = 1)
otu.corr <- cor(t(otu_table), method = method)
otu.hc <- hclust(as.dist(1 - otu.corr), method = "average")

## This is a function to sum up the variance of modules where the counts have been scaled
var_dist <- function(otu_table, otus){
  module_counts = otu_table[row.names(otu_table)%in%otus,]
  scaled_module_counts = scale(module_counts)
  var_sum <- sum(apply(scaled_module_counts, 2, var))
  return(var_sum)
}

# This is an attempt to find the optimum number of modules
module_stats <- data.frame(MinSize = NA, Dist = NA, Assigned = NA, Modules = NA, VarPerMod = NA)
for (i in 10:100) {
  print(paste("On the ", i, " iteration."))
  network <- cutreeDynamicTree(otu.hc, minModuleSize = i)
  names(network) <- otu.hc$labels
  total_dist = 0
  for(j in 1:max(network)) {
    otus <- names(network[network == j])
    total_dist = total_dist + var_dist(otu_table, otus)
  }
  total_assigned = sum(table(network[network != 0]))
  num_mods <- max(network) - 1
  if (i > 10) {
    module_stats <- rbind(module_stats, c(i, total_dist, total_assigned, num_mods, total_dist / num_mods))
  } else {
    module_stats[1,] <- c(i, total_dist, total_assigned, num_mods, total_dist / num_mods)
  }
}

best_minimumModuleSize = module_stats[order(module_stats$VarPerMod),][1,1]

best_network <- cutreeDynamicTree(otu.hc, minModuleSize = best_minimumModuleSize)
names(best_network) <- otu.hc$labels
best_network_df <- data.frame(OTU = names(best_network), Module = best_network)
write.table(best_network_df, file = out.file, sep = "\t")
