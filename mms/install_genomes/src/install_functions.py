import subprocess
import shutil
import warnings

import urllib.request as request

from contextlib import closing
from Bio import (
    Entrez,
    SeqIO
)

from .multithreading_decorator import multithreadizer
from .assembly_class import AssInfo


@multithreadizer()
def download_ftp(ftp_path, out_path):
    print(f'Downloading {ftp_path}')
    with closing(request.urlopen(ftp_path)) as ftp_blean:
        with open(out_path, 'wb') as file_blean:
            shutil.copyfileobj(ftp_blean, file_blean)
    print(f'{ftp_path} succefully downloaded')
    return


def get_ftp(orgname):
    ftw = ['AssemblyAccession',
           'AssemblyName',
           'Organism',
           'SpeciesTaxid',
           'FtpPath_RefSeq',
           'AsmReleaseDate_GenBank',
           'FtpPath_GenBank']
    handle = Entrez.esearch(db="assembly",
                            term=f"{orgname}[ORGN]",
                            idtype="acc")
    ids = Entrez.read(handle)['IdList']
    answ = []
    for i in ids:
        rec = Entrez.efetch(db="assembly",
                            id=i,
                            retmode="xml",
                            rettype='docsum')
        rec = Entrez.read(rec, validate=False)
        ans = [rec['DocumentSummarySet']['DocumentSummary'][0][i] for i in ftw]
        answ.append(AssInfo(*ans))
    if not answ:
        warnings.warn(f'No DocumentSummarySet for genome {orgname}. Unable to download') 
    return answ


def get_latest(assinfos):
    last = ''
    ans = None
    for i in assinfos:
        if i.date > last and i.link:
            last = i.date
            ans = i
    return ans


def get_infolist(orgnames):
    ans = [get_latest(get_ftp(i)) for i in orgnames]
    return ans


def open_fasta(filename):
    ans = SeqIO.parse(filename, 'fasta')
    return ans


def down_org(orgnames,
             dirname: str = 'data',
             fasta: bool = True,
             gtf: bool = True,
             gbff: bool = True,
             ft: bool = True,
             proteins: bool = True,
             unzip: bool = True):
    all_about_orgs = get_infolist(orgnames)
    p = subprocess.Popen(f'mkdir {dirname}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    ftp_set_fasta = []
    ftp_set_gtf = []
    ftp_set_ft = []
    ftp_set_gbff = []
    ftp_prot_fa = []
    for i in all_about_orgs:
        if not i:
            warnings.warn('Some missing genome can\'t be downloaded')
            continue
        if fasta:
            ftp_set_fasta.append((i.fasta, f'{dirname}/{i.ass_acc}_{i.ass_name}.fasta.gz'))
            download_ftp(ftp_set_fasta)
        if gtf:
            ftp_set_gtf.append((i.gtf, f'{dirname}/{i.ass_acc}_{i.ass_name}.gtf.gz'))
            download_ftp(ftp_set_gtf)
        if ft:
            ftp_set_ft.append((i.ft, f'{dirname}/{i.ass_acc}_{i.ass_name}.ft.gz'))
            download_ftp(ftp_set_ft)
        if gbff:
            ftp_set_gbff.append((i.gbff, f'{dirname}/{i.ass_acc}_{i.ass_name}.gbff.gz'))
            download_ftp(ftp_set_gbff)
        if proteins:
            ftp_prot_fa.append((i.pfa, f'{dirname}/{i.ass_acc}_{i.ass_name}.prot_fasta.faa.gz'))
            download_ftp(ftp_prot_fa)
        if unzip:
            p = subprocess.Popen(f'gunzip {dirname}/*.gz', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
    return all_about_orgs


def get_seqs(orgnames_info, dirname='data'):
    id_to_len = dict()
    id_to_ac = dict()
    org_seqs = dict()
    ac_to_spi = dict()
    for i in orgnames_info:
        for j in open_fasta(f'{dirname}/{i.ass_acc}_{i.ass_name}.fasta'):
            id_to_len[j.id] = len(j.seq)
            id_to_ac[j.id] = f'{i.ass_acc}_{i.ass_name}'
            org_seqs[j.id] = j.seq
            ac_to_spi[j.id] = i.org
    return id_to_len, id_to_ac, org_seqs, ac_to_spi
