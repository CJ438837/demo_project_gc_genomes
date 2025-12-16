from Bio import SeqIO
from pathlib import Path
import pandas as pd

def compute_gc(seq):
    seq = seq.upper()
    gc = seq.count("G") + seq.count("C")
    return (gc / len(seq)) * 100 if len(seq) > 0 else 0


def process_genomes(raw_dir, output_csv):
    records = []

    raw_dir = Path(raw_dir)

    for genus_dir in raw_dir.iterdir():
        if not genus_dir.is_dir():
            continue

        genus = genus_dir.name
        print(f"🧬 Traitement du genre : {genus}")

        for fasta_file in genus_dir.glob("*.fasta"):
            genome_id = fasta_file.stem

            total_length = 0
            total_gc = 0

            for record in SeqIO.parse(fasta_file, "fasta"):
                seq = str(record.seq)
                total_length += len(seq)
                total_gc += (seq.count("G") + seq.count("C"))

            gc_content = (total_gc / total_length) * 100 if total_length > 0 else 0

            records.append({
                "genus": genus,
                "genome_id": genome_id,
                "genome_size_bp": total_length,
                "gc_content_percent": round(gc_content, 2)
            })

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)

    print(f"\n✅ Dataset final écrit dans : {output_csv}")

  
    print(df.head())
if __name__ == "__main__":
    process_genomes(
        raw_dir="data/raw",
        output_csv="data/processed/gc_genomes.csv"
    )
