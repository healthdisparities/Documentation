# Function to extract UK Biobank data

#### Created by: Whitney Teagle 

# Pre-requisites  
Run this before using the function. The pre-requisite code only needs to be run/loaded once per session.

### Load UKB raw dataset
```R
load("/data/teaglewl/ukbiobank/raw_data/my_ukb_data.rda") # Change filepath as needed
```

### Use ukb_df_field to create a field code-to-descriptive name key, as dataframe or named lookup vector.
```R
my_ukb_key <- ukb_df_field("ukb12345", path = "/data/teaglewl/ukbiobank/raw_data") # Change filepath and dataset number as needed
```

# Load function

### Function to extract data from the UK Biobank
```R
extract_ukb <- function(data_showcase, output_filepath, my_ukb_key, my_ukb_data) {
    
    # Create dataframe with field.showcase and col.name values
    data_key <- dplyr::filter(my_ukb_key, my_ukb_key$field.showcase %in% data_showcase)
    
    # Remove duplicate data
    data_key <- data_key[!duplicated(data_key$col.name), ]
    data_key <- data_key[,c("field.showcase", "col.name")]
    
    # Create UKB datasets
    ukb_data <- select(my_ukb_data, matches(data_key$col.name))
    
    # Save dataset as .txt file
    write.table(ukb_data, 
            file = output_filepath, 
            sep = "\t", 
            quote = FALSE, 
            row.names = FALSE)
    
    # Print completion message
    print(paste0("Data extraction complete. Data saved at ", output_filepath))
}
```
# Example of use
##### The following code extracts two variables, eid and data field #41280, from the UK Biobank

```R
data_showcase <- c("eid", "41280") # Date of first in-patient diagnosis - ICD10. Field 41280 is the date of first diagnosis of Field 41270
output_filepath <- "/data/teaglewl/ukbiobank/outputs_data/example-dataset.txt"
extract_ukb(data_showcase, output_filepath, my_ukb_key, my_ukb_data)
```
