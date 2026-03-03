#!/usr/bin/env bash
#
# Jiook Cha 논문 PDF를 dgx-spark에서 복수 에이전트로 병렬 다운로드한 뒤 로컬로 가져옵니다.
# NotebookLM 업로드용으로 docs/jiook_cha_papers/output/ 에 저장됩니다.
#
# 사용법:
#   ./scripts/fetch_jiook_cha_papers_via_dgx.sh [에이전트 수, 기본 4]
#
# 필요: ssh dgx-spark 접속 가능, 원격에 Python3 + requests, tqdm

set -e

N_AGENTS="${1:-4}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE="dgx-spark"
REMOTE_DIR="~/jiook_cha_papers_download"
REFS_FILE="${REPO_ROOT}/docs/jiook_cha_papers/refs_jiook_cha.txt"
PARTS_DIR="${REPO_ROOT}/docs/jiook_cha_papers/refs_parts"
OUTPUT_LOCAL="${REPO_ROOT}/docs/jiook_cha_papers/output"

echo "=== 에이전트 수: $N_AGENTS (병렬 다운로드) ==="

echo ""
echo "=== 1. refs를 ${N_AGENTS}개 파트로 분할 ==="
mkdir -p "$PARTS_DIR"
rm -f "${PARTS_DIR}"/refs_part*.txt
TOTAL_LINES=$(wc -l < "$REFS_FILE")
LINES_PER_PART=$(( (TOTAL_LINES + N_AGENTS - 1) / N_AGENTS ))
for (( i=1; i<=N_AGENTS; i++ )); do
  START=$(( (i-1) * LINES_PER_PART + 1 ))
  END=$(( i * LINES_PER_PART ))
  [[ $END -gt $TOTAL_LINES ]] && END=$TOTAL_LINES
  sed -n "${START},${END}p" "$REFS_FILE" > "${PARTS_DIR}/refs_part${i}.txt"
  echo "  part $i: lines $START-$END ($(wc -l < "${PARTS_DIR}/refs_part${i}.txt") entries)"
done

echo ""
echo "=== 2. dgx-spark로 스크립트·refs 파트 전송 ==="
ssh "$REMOTE" "mkdir -p $REMOTE_DIR"
rsync -avz --progress \
  "${REPO_ROOT}/scripts/download_papers.py" \
  "${PARTS_DIR}/" \
  "${REMOTE}:${REMOTE_DIR}/"

echo ""
echo "=== 3. dgx-spark에서 ${N_AGENTS}개 에이전트 병렬 실행 ==="
# 각 에이전트: refs_partN.txt → out_N, worker 4
RUN_CMD="cd $REMOTE_DIR && pip install --user -q requests tqdm 2>/dev/null; "
for (( i=1; i<=N_AGENTS; i++ )); do
  RUN_CMD+="python3 download_papers.py --input refs_part${i}.txt --output out_${i} --workers 4 & "
done
RUN_CMD+="wait; echo 'All agents done.'"
ssh "$REMOTE" "$RUN_CMD"

echo ""
echo "=== 4. 다운로드 결과를 로컬로 복사 및 병합 ==="
mkdir -p "$OUTPUT_LOCAL"
rm -rf "${OUTPUT_LOCAL}/papers" "${OUTPUT_LOCAL}/abstracts"
mkdir -p "${OUTPUT_LOCAL}/papers" "${OUTPUT_LOCAL}/abstracts"

for (( i=1; i<=N_AGENTS; i++ )); do
  rsync -a "${REMOTE}:${REMOTE_DIR}/out_${i}/papers/" "${OUTPUT_LOCAL}/papers/" 2>/dev/null || true
  rsync -a "${REMOTE}:${REMOTE_DIR}/out_${i}/abstracts/" "${OUTPUT_LOCAL}/abstracts/" 2>/dev/null || true
done

# 리포트 병합 (마지막 에이전트 것만 쓰거나, 모두 concat)
if ssh "$REMOTE" "test -f $REMOTE_DIR/out_1/download_report.csv" 2>/dev/null; then
  ssh "$REMOTE" "head -1 $REMOTE_DIR/out_1/download_report.csv" > "${OUTPUT_LOCAL}/download_report.csv"
  for (( i=1; i<=N_AGENTS; i++ )); do
    ssh "$REMOTE" "tail -n +2 $REMOTE_DIR/out_${i}/download_report.csv 2>/dev/null" >> "${OUTPUT_LOCAL}/download_report.csv" 2>/dev/null || true
  done
fi

echo ""
echo "=== 완료 ==="
echo "PDF:    $OUTPUT_LOCAL/papers/"
echo "요약:   $OUTPUT_LOCAL/abstracts/"
echo "리포트: $OUTPUT_LOCAL/download_report.csv"
echo "NotebookLM에 넣을 PDF: $OUTPUT_LOCAL/papers/"
echo "  ($(find "$OUTPUT_LOCAL/papers" -name '*.pdf' 2>/dev/null | wc -l) PDFs)"
