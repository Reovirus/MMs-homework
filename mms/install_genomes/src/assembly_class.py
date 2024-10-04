from dataclasses import dataclass


@dataclass
class AssInfo:
    ass_acc: str
    ass_name: str
    org: str
    taxid: str
    link: str
    date: str
    linkgb: str

    @property
    def gtf(self) -> str:
        return f'{self.link}/{self.ass_acc}_{self.ass_name}_genomic.gtf.gz'

    @property
    def fasta(self) -> str:
        return f'{self.link}/{self.ass_acc}_{self.ass_name}_genomic.fna.gz'

    @property
    def ft(self) -> str:
        return f'''{self.link}/{self.ass_acc}_{'_'.join(self.ass_name.split(' '))}_feature_table.txt.gz''' if self.link else f'''{self.linkgb}/{self.ass_acc}_{'_'.join(self.ass_name.split(' '))}_feature_table.txt.gz'''

    @property
    def gbff(self) -> str:
        return f'{self.link}/{self.ass_acc}_{self.ass_name}_genomic.gbff.gz'

    @property
    def pfa(self) -> str:
        return f'{self.link}/{self.ass_acc}_{self.ass_name}_protein.faa.gz'

    @gtf.setter
    def gtfs(self, gtf: str):
        self.gtf = f'{self.link}/{self.ass_acc}_{self.ass_name}_genomic.gtf.gz'

    @fasta.setter
    def fastas(self, fasta: str):
        self.fasta = f'{self.link}/{self.ass_acc}_{self.ass_name}_genomic.fna.gz'

    @ft.setter
    def fts(self, ft: str):
        return f'''{self.link}/{self.ass_acc}_{'_'.join(self.ass_name.split(' '))}_feature_table.txt.gz''' if self.link else f'''{self.linkgb}/{self.ass_acc}_{'_'.join(self.ass_name.split(' '))}_feature_table.txt.gz'''

    @gbff.setter
    def gbffs(self, gtf: str):
        self.gtf = f'{self.link}/{self.ass_acc}_{self.ass_name}_genomic.gbff.gz'

    @pfa.setter
    def pfas(self, gtf: str):
        self.gtf = f'{self.link}/{self.ass_acc}_{self.ass_name}_protein.faa.gz'


