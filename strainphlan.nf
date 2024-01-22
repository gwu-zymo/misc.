#!/usr/bin/env nextflow

nextflow.enable.dsl=2

params.readsPath = '/mnt/gwu/vaginal/*_R{1,2}.fastq.gz'
params.trimmomaticPath = '/home/gwu/bin//trimmomatic.jar'
params.adaptersPath = '/home/gwu/bin/trimmomatic/adapters/NexteraPE-PE.fa'

// Define processes
process trimReads {
    input:
    tuple val(sample), path(reads)

    output:
    tuple val(sample), path('*_trimmed.fastq.gz')

    script:
    """
    java -jar ${params.trimmomaticPath} PE -phred33 \\
        ${reads[0]} ${reads[1]} \\
        ${sample}_1_trimmed.fastq.gz ${sample}_1_unpaired.fastq.gz \\
        ${sample}_2_trimmed.fastq.gz ${sample}_2_unpaired.fastq.gz \\
        ILLUMINACLIP:${params.adaptersPath}:2:30:10 SLIDINGWINDOW:4:20 MINLEN:36
    """
}

process pairReads {
    input:
    tuple val(sample), path(reads)

    output:
    tuple val(sample), path('*_paired.fastq.gz')

    script:
    """
    fastp -i ${reads[0]} -I ${reads[1]} -o ${sample}_1_paired.fastq.gz -O  ${sample}_2_paired.fastq.gz
    """
}

process metaphlan {
    container 'quay.io/biocontainers/metaphlan'
     
    input:
    tuple val(sample), path(reads)

    output:
    tuple val(sample), path("${sample}_assembled.fasta")

    script:
    """
    metaphlan reads[0],reads[1] --input_type fastq -s ${sample}.sam.bz2 --bowtie2out bowtie2/${sample}.bowtie2.bz2 -o ${sample}_profiled.tsv
    """
}

process strainphlan {
    container 'quay.io/repository/biobakery/strainphlan'
    publishDir '.', mode: 'copy', pattern: '*_assembled.fasta'
  
    input:
    tuple val(sample), path(reads)

    output:
    tuple val(sample), path("${sample}_assembled.fasta")

    script:
    """
    rnaspades.py -1 ${reads[0]} -2 ${reads[1]} -o ${sample}_spades
    mv ${sample}_spades/transcripts.fasta ${sample}_assembled.fasta
    """
}

// Define workflow
workflow {
    read_pairs = Channel.fromFilePairs(params.readsPath)

    trimmed_reads = read_pairs
        | trimReads

    paired_reads = trimmed_reads
        | pairReads

    assembled_transcripts = paired_reads
        | assembleTranscripts
   
}
