from agno.knowledge.chunking.fixed import FixedSizeChunking
from agno.knowledge.reader.pdf_reader import PDFReader

from AI.config import CHUNK_OVERLAP, CHUNK_SIZE, PDF_PATH
from AI.knowledge import knowledge

def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF не найден: {PDF_PATH}")

    reader = PDFReader(
        chunking_strategy=FixedSizeChunking(
            chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP,
        )
    )

    print(f"Индексирую: {PDF_PATH}")
    knowledge.insert(
        path=str(PDF_PATH),
        reader=reader,
    )
    print("Индексация завершена.")


if __name__ == "__main__":
    main()