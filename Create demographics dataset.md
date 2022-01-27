# Create Demographics Dataset
The following code only needs to be run once.  

## Contents

**1. Prepare environment**  
- Load required packages  
- Load UKB data  
- Make a UKB key  

**2. Extract fields from UKB**  
- Demographics fields (age, sex, ethnicity, townsend deprivation index)  

**3. Format demographics datasets**  
- Rename demographics variables  
- Condense ethnic categories  

**4. Save UKB datasets**  
- Demographics (age, sex, ethnicity, townsend deprivation index) dataset  

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

## Extract demographics fields
* Ethnic group
* Age
* Sex
* Townsend deprivation index

```{r extract}
# Create key
demographics_showcase <- c("eid", 
                           "31", "21003", "34", "52", "54", "53", "21000", "189", # Primary demographic variables https://biobank.ctsu.ox.ac.uk/crystal/label.cgi?id=1001
                           "189") # Townsend deprivation index at recruitment

# Create dataframe with field.showcase and col.name values
demographics_key <- dplyr::filter(my_ukb_key, my_ukb_key$field.showcase %in% demographics_showcase)

# Remove duplicate data
demographics_key <- demographics_key[!duplicated(demographics_key$col.name), ]
demographics_key <- demographics_key[,c("field.showcase", "col.name")]

# Check key
unique(demographics_key$field.showcase) # Confirm values match selected values
head(demographics_key, 2)
```

## Create and format demographics datasets

```{r create}
# Create demographics dataset
demographics_data <- select(my_ukb_data, matches(demographics_key$col.name))
```

```{r format}
# Select variables
demographics_data <- demographics_data[c('eid', 
                                         'ethnic_background_f21000_0_0', # ethnicity
                                         'age_when_attended_assessment_centre_f21003_0_0', # age when assessed
                                         'sex_f31_0_0', # sex
                                         'townsend_deprivation_index_at_recruitment_f189_0_0')] # townsend index at assessment

# Set names
setnames(demographics_data, "ethnic_background_f21000_0_0", "ethnicity")
setnames(demographics_data, "age_when_attended_assessment_centre_f21003_0_0", "age_at_assessment")
setnames(demographics_data, "sex_f31_0_0", "sex")
setnames(demographics_data, "townsend_deprivation_index_at_recruitment_f189_0_0", "townsend_at_assessment")
```

```{r format2}
## Add top-level ethnic categories as defined by the UK Biobank
demographics_data$top_ethnicity[demographics_data$ethnicity == 'Do not know' |
                       demographics_data$ethnicity == 'Prefer not to answer' |
                       demographics_data$ethnicity == 'NA' |
                       demographics_data$ethnicity == NA |
                       is.na(demographics_data$ethnicity)] = 'Unknown'
demographics_data$top_ethnicity[demographics_data$ethnicity == 'White' |
                       demographics_data$ethnicity == 'British' |
                       demographics_data$ethnicity == 'Irish' |
                       demographics_data$ethnicity == 'Any other white background'] = 'White'
demographics_data$top_ethnicity[demographics_data$ethnicity == 'Mixed' |
                       demographics_data$ethnicity == 'White and Black Caribbean' |
                       demographics_data$ethnicity == 'White and Black African' |
                       demographics_data$ethnicity == 'White and Asian' |
                       demographics_data$ethnicity == 'Any other mixed background'] = 'Mixed'
demographics_data$top_ethnicity[demographics_data$ethnicity == 'Asian or Asian British' |
                       demographics_data$ethnicity == 'Indian' |
                       demographics_data$ethnicity == 'Pakistani' |
                       demographics_data$ethnicity == 'Bangladeshi' |
                       demographics_data$ethnicity == 'Any other Asian background'] = 'Asian'
demographics_data$top_ethnicity[demographics_data$ethnicity == 'Black or Black British' |
                       demographics_data$ethnicity == 'Caribbean' |
                       demographics_data$ethnicity == 'African' |
                       demographics_data$ethnicity == 'Any other Black background'] = 'Black'
demographics_data$top_ethnicity[demographics_data$ethnicity == 'Chinese'] = 'Chinese'
demographics_data$top_ethnicity[demographics_data$ethnicity == 'Other ethnic group'] = 'Other'
```

```{r create2}
# Create melted demographics dataset
melted_demographics_data <- reshape2::melt(demographics_data, id.vars = 'eid') # More info about warning message here: https://stackoverflow.com/questions/25688897/reshape2-melt-warning-message
```

## Save UKB datasets
Using the keys generated above, create and save datasets with UKB data of interest.  

```{r save}
# Save demographics datasets as .txt files
write.table(demographics_data, 
            file = "/data/teaglewl/ukbiobank/outputs_data/demographics-data.txt", 
            sep = "\t", 
            quote = FALSE, 
            row.names = FALSE) 

write.table(melted_demographics_data, 
            file = "/data/teaglewl/ukbiobank/outputs_data/melted-demographics-data.txt", 
            sep = "\t", 
            quote = FALSE, 
            row.names = FALSE)
```
