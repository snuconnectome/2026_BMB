# Jiook Cha 논문 PDF (NotebookLM용)

[Semantic Scholar – Jiook Cha](https://www.semanticscholar.org/author/Jiook-Cha/40209044) 기준 논문 목록으로, Open Access 소스(Unpaywall, arXiv, PMC 등)에서 PDF를 받습니다.

## 빠른 실행 (dgx-spark에서 받고 로컬로 복사)

```bash
# 프로젝트 루트에서
./scripts/fetch_jiook_cha_papers_via_dgx.sh
```

- `ssh dgx-spark` 접속 가능해야 합니다.
- 완료 후 PDF: `docs/jiook_cha_papers/output/papers/`
- 이 폴더의 PDF를 NotebookLM에 업로드하면 됩니다.

## 로컬에서만 다운로드

```bash
pip install requests tqdm
python3 scripts/download_papers.py \
  --input docs/jiook_cha_papers/refs_jiook_cha.txt \
  --output docs/jiook_cha_papers/output \
  --workers 8
```

## 파일

- `refs_jiook_cha.txt` – 논문 60편 참고 목록 (DOI/arXiv 포함)
- `output/papers/` – 다운로드된 PDF
- `output/abstracts/` – PDF 없을 때 저장된 초록
- `output/download_report.csv` – 논문별 다운로드 결과
