install.packages("tidyverse", lib="./")
library(tidyverse)
library(ggplot2)
library(ggrepel)
library(ggforce)

#place this script at the same level with the directory containing all SG outputs (e.g. 00...AllSamples.illumina.pe)
#to run this script from the command line, enter "Rscript get_donut_plot.R" (no argument required)
#get the name of dir that contains data
#always use the 00...AllSamples group
data_dirname <- dir(path=".", pattern="^00", recursive=FALSE)

#get the fname of the relative abunance table first and check if it exist
#for now, level only takes two values: phylum or family
#organism only takes two values: prokaryote or eukaryote
get_abun_fname <- function(level, organism){
  #get search_dir
  if(organism == "prokaryote"){
    search_dir <- paste0("./", data_dirname, "/Prokaryote/AbundanceTables/")
  }
  else if(organism == "eukaryote"){
    search_dir <- paste0("./", data_dirname, "/Eukaryote/AbundanceTables/")
  }
  #get relative abundance table filename
  if(level == "phylum"){
    adun_fname <- paste0(search_dir, "2.Phylum/phylum.tsv")
  }
  else if(level == "family"){
    adun_fname <- paste0(search_dir, "4.Family/family.tsv")
  }
  return(adun_fname)
}

#get the correctly formatted df from the composition data for plotting
get_abun_df <- function(level, organism, sep="\t"){
  #get the fname of abundance table
  abun_fname <- get_abun_fname(level, organism)
  abun_df_headers <- read.csv(abun_fname, sep=sep, skip = 1, header = F, nrows = 1, as.is = T, check.names=FALSE)
  abun_df <- read.csv(abun_fname,  sep=sep, skip = 2, header = F)
  colnames(abun_df) <- abun_df_headers
  names(abun_df)[1] <- "ID"
  sample_ID <- names(abun_df)[2]
  if(level == "phylum"){
    abun_df <- separate(abun_df, ID, into=c("d","p"),sep=";",remove=TRUE)
    abun_df$percentage <- paste0(round(abun_df[,sample_ID]*100,2),"%")
    abun_df$d <- NULL
    names(abun_df)[1] <- "ID"
    abun_df$ID <- gsub("p__","",abun_df$ID)
    #get labels for the top 3 phyla (>1%)
    abun_df <-abun_df %>% arrange(desc(!!sym(sample_ID))) %>% filter(!!sym(sample_ID)>0)
    #sometimes the phylum abun df may have less than 3 rows
    #need to adjust the where to cutoff according
    cut_off_row <- min(nrow(abun_df), 3)
    cut_off <- max(abun_df[cut_off_row,sample_ID],0.01)
  }
  else if(level == "family"){
    abun_df <- separate(abun_df, ID, into=c("d","p","o","f"),sep=";",remove=TRUE)
    abun_df$percentage <- paste0(round(abun_df[,sample_ID]*100,2),"%")
    abun_df[,c("d","p","o")] <- NULL
    names(abun_df)[1] <- "ID"
    abun_df$ID <- gsub("f__","",abun_df$ID)
    #get labels for the top 5 family (>1%)
    abun_df <-abun_df %>% arrange(desc(!!sym(sample_ID))) %>% filter(!!sym(sample_ID)>0)
    cut_off_row <- min(nrow(abun_df), 5)
    cut_off <- max(abun_df[cut_off_row,sample_ID],0.01)
  }
  #get labels
  abun_df <- abun_df %>% mutate(label=ifelse(!!sym(sample_ID)>=cut_off,paste0(ID,":",percentage),NA))
  #get positions for labels
  abun_df <- abun_df %>%  mutate(end = 2 * pi * cumsum(!!sym(sample_ID))/sum(!!sym(sample_ID)),start = lag(end, default = 0),middle = 0.5 * (start + end),hjust = ifelse(middle > pi, 1, 0),vjust = ifelse(middle < pi/2 | middle > 3 * pi/2, 0, 1))
  return(abun_df)
}

#draw the donut plot and save it as png files 
get_donut_plot <- function(abun_df, output_dir="./gut_report_tmp/patient_plots/" ,output_fname){
  donut_plot <- ggplot(abun_df)+ geom_arc_bar(aes(x0 = 0, y0 = 0, r0 = 0.5, r = 1,start = start, end = end, fill = ID),color=NA) + geom_text(aes(x = 1*sin(middle), y = 1*cos(middle),label = label,hjust = hjust, vjust = vjust),size=5)+scale_x_continuous(limits = c(-2, 2),name = "", breaks = NULL, labels = NULL)+scale_y_continuous(limits = c(-1.5, 1.5),name = "", breaks = NULL, labels = NULL)+ coord_fixed() +theme_void() + theme(legend.position = "none")
  output_path <- paste0(output_dir, output_fname)
  ggsave(output_path, plot=donut_plot, device=png, height=7.5, width=10, dpi=300)
}

#plot and save the donut plots for prokaryote phylum, prokaryote family and eukaryote family abundance results(if exists) from SG pipeline
#prokaryote phylum
if(file.exists(get_abun_fname("phylum", "prokaryote"))){
  pro_p_df <- get_abun_df("phylum", "prokaryote")
  get_donut_plot(abun_df=pro_p_df, output_fname="pro_p_donut_plot.png")
}

#prokaryote family
if(file.exists(get_abun_fname("family", "prokaryote"))){
  pro_f_df <- get_abun_df("family", "prokaryote")
  get_donut_plot(abun_df=pro_f_df, output_fname="pro_f_donut_plot.png")
}

#eukaryote family
if(file.exists(get_abun_fname("family", "eukaryote"))){
  euk_f_df <- get_abun_df("family", "eukaryote")
  get_donut_plot(abun_df=euk_f_df, output_fname="euk_f_donut_plot.png")
}
