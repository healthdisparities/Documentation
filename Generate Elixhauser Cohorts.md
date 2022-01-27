# Create Elixhauser Cohort
The following code only needs to be run once.  

## Contents

**1. Prepare environment**  
- Load required packages  
- Load UKB data  
- Make a UKB key  

**2. Extract fields from UKB**  
- ICD-10 codes  

**4. Create and save UKB datasets**  
- Elixhauser Comorbidity Index info  

## Prepare environment

```{r prep}
rm(list = ls())
```

```{r prep2}
# Install into R folder
R_LIBS_USER="~/R/4.0/lib"
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))

# Install required packages
install.packages('ukbtools', lib = '~/R/4.0/lib')
install.packages('dplyr', lib = '~/R/4.0/lib')
install.packages('reshape2', lib = '~/R/4.0/lib')
```

```{r prep3}
# Load required packages
library('ukbtools')
library('dplyr')
library('reshape2')
```

```{r prep4}
# Load UK Biobank raw dataset
load("/data/teaglewl/ukbiobank/raw_data/my_ukb_data.rda")
```

```{r prep5}
# Make a key
my_ukb_key <- ukb_df_field("ukb12345", path = "/data/teaglewl/ukbiobank/raw_data")
```

## Extract ICD-10 fields

```{r extract}
# Create key
icdcodes_showcase <- c('eid', '41202') # "Diagnoses - ICD10" 

# Create dataframe with field.showcase and col.name values
icd_key <- dplyr::filter(my_ukb_key, my_ukb_key$field.showcase %in% icdcodes_showcase)

# Remove duplicate data
icd_key <- icd_key[!duplicated(icd_key$col.name), ]
icd_key <- icd_key[,c("field.showcase", "col.name")]

# Check key
unique(icd_key$field.showcase) # Confirm values match selected values
head(icd_key, 8)
```

## Create and format demographics datasets

```{r create}
# Create and format ICD-10 datasets
icd_data <- select(my_ukb_data, matches(icd_key$col.name))
melted_icd_data <- reshape2::melt(icd_data, id.vars = 'eid') # More info about warning message here: https://stackoverflow.com/questions/25688897/reshape2-melt-warning-message
```

```{r format}
# Compute Elixhauser comorbidity scores
elixhauser_data <- comorbidity(x = melted_icd_data, 
                          id = "eid", 
                          code = "value", 
                          score = "elixhauser", 
                          icd = "icd10", 
                          assign0 = FALSE)
melted_elixhauser_data <- reshape2::melt(elixhauser_data, id.vars = 'eid') # More info about warning message here: https://stackoverflow.com/questions/25688897/reshape2-melt-warning-message
```

## Save Elixhauser Comorbidity Index datasets
Create and save datasets.  

```{r save}
# Save Elixhauser datasets as .txt files
write.table(elixhauser_data, 
            file = "/data/teaglewl/ukbiobank/outputs_data/elixhauser-data.txt", 
            sep = "\t", 
            quote = FALSE, 
            row.names = FALSE) 

write.table(melted_elixhauser_data, 
            file = "/data/teaglewl/ukbiobank/outputs_data/melted-elixhauser-data.txt", 
            sep = "\t", 
            quote = FALSE, 
            row.names = FALSE) 
```
