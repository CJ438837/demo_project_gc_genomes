from Bio import Entrez, SeqIO
from pathlib import Path
from tqdm import tqdm
import time

# ⚠️ Obligatoire pour NCBI
Entrez.email = "ton.email@exemple.com"

def fetch_ncbi_genomes_by_genus(
    genus,
    outdir,
    max_genomes=10,
    sleep_time=0.4
):
    """
    Télécharge des génomes bactériens complets pour un genre donné.
    """

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"\n🔎 Recherche des génomes pour le genre : {genus}")

    query = f"{genus}[Organism] AND complete genome[Title]"

    handle = Entrez.esearch(
        db="nucleotide",
        term=query,
        retmax=max_genomes
    )
    record = Entrez.read(handle)
    ids = record["IdList"]

    print(f"📥 {len(ids)} génomes trouvés")

    for ncbi_id in tqdm(ids):
        fetch = Entrez.efetch(
            db="nucleotide",
            id=ncbi_id,
            rettype="fasta",
            retmode="text"
        )

        fasta_path = outdir / f"{genus}_{ncbi_id}.fasta"

        with open(fasta_path, "w") as f:
            f.write(fetch.read())

        time.sleep(sleep_time)

    print(f"✅ Téléchargement terminé pour {genus}")


if __name__ == "__main__":
    fetch_ncbi_genomes_by_genus(
        genus="Escherichia",
        outdir="data/raw/Escherichia",
        max_genomes=10
    )
