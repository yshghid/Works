# edgeR: DE 분석

#2025-07-12

---

### 1. Load package

```R
library(edgeR)
packageVersion("edgeR")
```

###

### 2. Set path

```R
setwd("/data/home/ysh980101/2406/data-gne")
getwd()
```
```plain text
'data/home/ysh980101/2406/data-gne'
```

###

### 3. Load data, Run edgeR

```R
tissue_type <- c("G")

S1 <- "WT" 
S2 <- "GneKI"

for (tissue in tissue_type) {
    print(tissue) 
    counts <- read.csv("count.csv", header = TRUE)
    counts[, -1] <- lapply(counts[, -1], as.numeric)
    counts <- counts[rowSums(counts[, -1]) != 0, ]
    
    meta <- read.csv(paste0("mouse_meta_",tissue,".csv"), header = TRUE)
    meta <- meta[meta$Group %in% c(S1, S2), ]

    counts <- counts[, c("GeneID", unique(meta$SampleID))]
    counts <- counts[, colnames(counts) %in% c("GeneID", c("GeneID", unique(meta$SampleID)))]

    Group <- factor(meta$Group)
    Group <- relevel(Group, ref=S1)
    Group
    
    y <- DGEList(counts=counts[,2:ncol(counts)], group=Group, genes = counts[,1])
    y <- calcNormFactors(y)

    y3 <- y
    design <- model.matrix(~Group)
    rownames(design) <- colnames(y3)
    design
    
    y3 <- estimateDisp(y3, design)
    y3 <- estimateGLMRobustDisp(y3,design)
    
    fit3 <- glmFit(y3, design)
    lrt3 <- glmLRT(fit3)
    plotMD(lrt3)
    abline(h=c(-1,1), col="blue")
    
    print(summary(decideTests(lrt3)))

    result_table <- topTags(lrt3, n = nrow(lrt3$table))
    sorted_result_table <- result_table[order(result_table$table$FDR, decreasing = FALSE), ]
    filtered_result_table <- sorted_result_table[sorted_result_table$table$FDR < 0.05, ]
    write.csv(sorted_result_table, file = paste0("de-edger-",tissue,"_",S1,"-",S2,".csv"), row.names = FALSE)
    
}
```
```plain text
[1] "G"
       GroupGneKI
Down           50
NotSig      10888
Up            100
```

<img width="840" height="840" alt="image" src="https://github.com/user-attachments/assets/c51125bd-7a59-4241-b39c-da785b4dbc0e" />
