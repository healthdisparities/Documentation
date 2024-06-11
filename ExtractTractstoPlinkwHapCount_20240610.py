import argparse
import gzip
import zstandard as zstd
import codecs
import io
import numpy as np
from cyvcf2 import VCF

"""
USAGE:
ExtractTracts.py --msp  <an ancestral calls file produced by RFmix version 2, suffixed with .msp.tsv>
                             --vcf <VCF file suffixed with .vcf>
"""

# input is expected to be a VCF file suffixed with .vcf and an ancestral calls file produced by RFmix version 2, suffixed with .msp.tsv

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--msp', help='path stem to RFmix msp file, not including .msp.tsv', required=True)
    parser.add_argument('--vcf', help='path stem to RFmix input VCF or BCF with phased genotypes',required=True)
    parser.add_argument('--prefix', help='output prefix',required=True)
    parser.add_argument('--keep', help='samples to extract',required=False)
    parser.add_argument('--region',help='VCF query region (requires index)',required=True)
    parser.add_argument('--hds', help='Use haplotype dosage (HDS) format field instead of genotype',action='store_true',required=False)
    parser.add_argument('--freq-only',help='Output sites-only VCF with local ancestry allele frequencies only',action='store_true',required=False)
    parser.add_argument('--hapcount-vcf',help='Output haplotype counts within allele frequency VCF',action='store_true',required=False)
    parser.add_argument('--threads', help='Number of Zstandard compression threads',type=int,default=1,required=False)
    args = parser.parse_args()
    return (args)

args = parse_args()
genosfile = VCF(args.vcf,'r')
if args.keep is not None:
    with open(args.keep) as f:
        samples = {line.split()[0] for line in f}
else:
    samples = set(genosfile.samples)

# get sample maps
genosfile_samples = genosfile.samples
sample_order = np.argsort(genosfile_samples)
genosfile_sample_map = [i for i in sample_order if genosfile_samples[i] in samples]

o = open(args.prefix + '.local_anc.sites.vcf','wt')  # output dosages for each ancestry into separate files
if not args.freq_only:
    outdos0 = open(args.prefix + '.anc0.dosage.txt.zst', 'wb')  # output dosages for each ancestry into separate files
    outdos1hapcount0 = open(args.prefix + '.local_covar.txt.zst', 'wb')  # output dosages for each ancestry into separate files
    cctx0 = zstd.ZstdCompressor(threads=args.threads)
    cctx1 = zstd.ZstdCompressor(level=22,threads=args.threads)
    compressor_o0 = cctx0.stream_writer(outdos0, write_return_read=True)
    compressor_o1 = cctx1.stream_writer(outdos1hapcount0, write_return_read=True)
    b0 = io.BufferedWriter(compressor_o0)
    b1 = io.BufferedWriter(compressor_o1)
    o0 = codecs.getwriter('utf-8')(b0)
    o1 = codecs.getwriter('utf-8')(b1)

# Read through mspfile, get ancestry order, sample names, starting and ending positions
if args.msp.endswith('gz'):
    mspfile = gzip.open(args.msp, 'rt')
else:
    mspfile = open(args.msp,'rt')
for i,line in enumerate(mspfile):
    if i == 0:
        anc_keys = line.replace('#Subpopulation order/codes: ','').split()
        anc_order = [anc.split('=')[0] for anc in anc_keys]
        num_anc = len(anc_order)
    elif i == 1:
        haplotypes = line.strip().split('\t')[6:]
    elif i == 2:
        starting_pos = int(line.split('\t')[1])
    else:
        continue
ending_pos = int(line.split('\t')[2])
mspfile.close()

# Generate a mapping of the sample order in the vcf to the sample order in the msp file
sample_order = np.argsort(haplotypes)
msp_haplotypes_A_map = [i for i in sample_order if haplotypes[i].split('.')[0] in samples and haplotypes[i].endswith('.0')]
msp_haplotypes_B_map = [i for i in sample_order if haplotypes[i].split('.')[0] in samples and haplotypes[i].endswith('.1')]
num_samples = len(msp_haplotypes_A_map)

# initialization
chrom = 0; spos = 0; epos = 0
freq = np.zeros(num_anc)
rsq = np.zeros(num_anc)
frac = np.zeros(num_anc)
A = np.zeros([num_anc,num_samples],dtype=int)
B = np.zeros([num_anc,num_samples],dtype=int)
dos = np.zeros([num_anc,num_samples])
hapcount = np.zeros([num_anc,num_samples],dtype=int)
if args.msp.endswith('gz'):
    mspfile = gzip.open(args.msp, 'rt')
else:
    mspfile = open(args.msp,'rt')

# write VCF header
o.write('##fileformat=VCFv4.3\n')
o.write('##FILTER=<ID=PASS,Description="All filters passed">\n')
for i in list(range(1,23)) + ['X']:
    o.write(f'##contig=<ID=chr{i}>\n')
o.write('##INFO=<ID=AF,Number=1,Type=Float,Description="Allele frequency (overall)">\n')
o.write('##INFO=<ID=R2,Number=1,Type=Float,Description="Imputation R-squared (overall)">\n')
for anc in anc_order:
    o.write(f'##INFO=<ID=AF_{anc},Number=1,Type=Float,Description="Allele frequency of the {anc} tract">\n')
    o.write(f'##INFO=<ID=R2_{anc},Number=1,Type=Float,Description="Imputation R-squared of the {anc} tract">\n')
    o.write(f'##INFO=<ID=F_{anc},Number=1,Type=Float,Description="Fraction of {anc} haplotypes">\n')
if args.hapcount_vcf:
    o.write(f'##FORMAT=<ID=HC_{anc},Number=1,Type=Integer,Description="Haplotype count of the {anc} tract">\n')
if not args.freq_only:
    o.write('##INFO=<ID=FLIPPED,Number=0,Type=Float,Description="REF and ALT alleles flipped in PLINK formatted dosage/hapcount files">\n')
if args.hapcount_vcf:
    o.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT' + '\t'.join(np.array(genosfile_samples)[genosfile_sample_map]) + '\n')
else:
    o.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n')

# iterate over vcf
for variant in genosfile(args.region):
    CHROM = variant.CHROM
    POS = variant.POS
    ID = variant.ID
    if ID == None:
        ID = '.'
    REF = variant.REF
    ALT = variant.ALT[0]
    QUAL = '.'
    FILTER = '.'
    FORMAT = ':'.join([f'HC_{anc}' for anc in anc_order])

    if POS < starting_pos or POS > ending_pos:
        continue
    
    if args.hds:
        genos = variant.format('HDS')[genosfile_sample_map]
        genosA = genos[:,0]
        genosB = genos[:,1]
    else:
        genos = variant.genotypes
        genosA = np.array([gt[0] for gt in genos])[genosfile_sample_map]
        genosB = np.array([gt[1] for gt in genos])[genosfile_sample_map]

    # optimized for quicker runtime - only move to next line when out of the current msp window
    # save current line until out of window, then check next line. Input files should be in incremental order.
    while not (CHROM == chrom and (spos <= POS < epos)):
        msp_line = mspfile.readline()
        if msp_line.startswith("#"):  # skip the header lines
            continue
        if not msp_line:
            break  # when get to the end of the msp file, stop
        chrom, spos, epos, sgpos, egpos, nsnps, calls = msp_line.strip().split('\t', 6)
        spos = int(spos); epos = int(epos)
        if (CHROM == chrom and (spos <= POS < epos)):
            callsA = np.array(calls.split('\t'),dtype=int)[msp_haplotypes_A_map]
            callsB = np.array(calls.split('\t'),dtype=int)[msp_haplotypes_B_map]
            for i in range(num_anc):
                A[i,] = (callsA == i)
                B[i,] = (callsB == i)

    for i in range(num_anc):
        dos[i,] = genosA*A[i,] + genosB*B[i,]
        hapcount[i,] = A[i,] + B[i,]
        freq[i] = np.sum(dos[i,])/np.sum(hapcount[i,])
        frac[i] = np.sum(hapcount[i,])/(2*num_samples)
    freq_overall = np.sum(genosA + genosB)/(2*num_samples)

    # Generate VCF lines
    freq_keys = ['AF'] + [f'AF_{anc}' for anc in anc_order]
    freq_values = [f'{frequency:.3g}' for frequency in [freq_overall] + list(freq)]
    freq_output = ';'.join([f'{key}={value}' for key,value in zip(freq_keys,freq_values)])

    frac_keys = [f'F_{anc}' for anc in anc_order]
    frac_values = [f'{fraction:.3g}' for fraction in list(frac)]
    frac_output = ';'.join([f'{key}={value}' for key,value in zip(frac_keys,frac_values)])

    # If using haplotype dosage, calculate R-squared on each ancestry tract
    if args.hds:
        for i in range(num_anc):
            if freq[i] == 0:
                rsq[i] = 0
            else:
                rsq_sigma = np.sum((genosA[A[i,].astype(bool)]-freq[i])**2) + np.sum((genosB[B[i,].astype(bool)]-freq[i])**2)
                rsq[i] = ( 1/np.sum(hapcount[i,]) * rsq_sigma ) / ( freq[i] * (1 - freq[i]) )
        if freq_overall == 0:
            rsq_overall = 0
        else:
            rsq_sigma = np.sum((genosA-freq_overall)**2) + np.sum((genosB-freq_overall)**2)
            rsq_overall = ( 1/(2*num_samples) * rsq_sigma ) / ( freq_overall * (1 - freq_overall) )

        rsq_keys = ['R2'] + [f'R2_{anc}' for anc in anc_order]
        rsq_values = [f'{rsquared:.3g}' for rsquared in [rsq_overall] + list(rsq)]
        rsq_output = ';'.join([f'{key}={value}' for key,value in zip(rsq_keys,rsq_values)])
    
    # Write plink dosage and local covariate files
    if not args.freq_only:
        if np.min(1-freq) < np.min(freq): # flip alleles (1-dosage) if it makes the minimum frequency smaller
            for i in range(num_anc):
                dos[i,] = (1-genosA)*A[i,] + (1-genosB)*B[i,]
            FLIPPED = True
            idcols = '\t'.join([CHROM, str(POS), ID, REF, ALT]) #ALT normally goes first in PLINK-formatted dosage
        else:
            FLIPPED = False
            idcols = '\t'.join([CHROM, str(POS), ID, ALT, REF])

        interleaved = np.empty((2*(num_anc-1)*num_samples,), dtype=dos.dtype)
        for i in range(1,num_anc):
            interleaved[i-1::2*(num_anc-1)] = dos[i,]
        for i in range(0,num_anc-1):
            interleaved[num_anc-1+i::2*(num_anc-1)] = hapcount[i,]

        o0.write(idcols + '\t' + '\t'.join('%g'%i for i in dos[0,]) + '\n')
        o1.write('\t'.join('%g'%i for i in interleaved) + '\n')

    if args.hapcount_vcf:
        format_string = '\t'.join([':'.join([str(hapcount[i,j]) for i in range(num_anc)]) for j in range(num_samples)])

    idcols_vcf = '\t'.join([CHROM, str(POS), ID, REF, ALT, QUAL, FILTER])
    if args.hds:
        if args.freq_only == False and FLIPPED == True:
            if args.hapcount_vcf:
                output_string = idcols_vcf + '\t' + ';'.join([freq_output,rsq_output,frac_output,'FLIPPED']) + '\t' + FORMAT + '\t' + format_string + '\n'
            else:
                output_string = idcols_vcf + '\t' + ';'.join([freq_output,rsq_output,frac_output,'FLIPPED']) + '\n'
        else:
            if args.hapcount_vcf:
                output_string = idcols_vcf + '\t' + ';'.join([freq_output,rsq_output,frac_output]) + '\t' + FORMAT + '\t' + format_string + '\n'
            else:
                output_string = idcols_vcf + '\t' + ';'.join([freq_output,rsq_output,frac_output]) + '\n'
    else:
        if args.freq_only == False and FLIPPED == True:
            if args.hapcount_vcf:
                output_string = idcols_vcf + '\t' + ';'.join([freq_output,frac_output,'FLIPPED']) + '\t' + FORMAT + '\t' + format_string + '\n'
            else:
                output_string = idcols_vcf + '\t' + ';'.join([freq_output,frac_output,'FLIPPED']) + '\n'
        else:
            if args.hapcount_vcf:
                output_string = idcols_vcf + '\t' + ';'.join([freq_output,frac_output]) + '\t' + FORMAT + '\t' + format_string + '\n'
            else:
                output_string = idcols_vcf + '\t' + ';'.join([freq_output,frac_output]) + '\n'
    o.write(output_string)

genosfile.close()
mspfile.close()
o.close()

if not args.freq_only:
    o0.close()
    compressor_o0.close()
    outdos0.close()
    o1.close()
    compressor_o1.close()
    outdos1hapcount0.close()
