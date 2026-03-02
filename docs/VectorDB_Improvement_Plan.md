# 2026 BMB Vector DB Improvement Plan

## 1. 개요 (Overview)

현재 `scripts/build_vector_db.py`에 구현된 Vector DB는 FAISS와 `all-MiniLM-L6-v2` 모델을 기반으로 하며, 단순 텍스트 분할(`RecursiveCharacterTextSplitter`)을 사용하고 있습니다.
이 방식은 로컬 프로토타이핑에는 적합하지만, 2026년 기준 최고 성능(SOTA)을 달성하기에는 다음과 같은 한계가 있습니다.

## 2. 한계점 및 개선 방향 (Room for Improvement)

1. **단순 청킹(Chunking)으로 인한 문맥 파괴**: 엑셀 표와 같은 구조화된 데이터를 단순 글자 수 기준으로 자르면 데이터의 속성(시간, 교수명 등)이 소실됩니다.
   -> **개선**: 표 데이터는 속성(Metadata)을 보존하는 방식으로, 마크다운은 헤더 기반으로 논리적으로 분할(Semantic/Structured Chunking)합니다.
2. **소형 임베딩 모델의 한계**: `all-MiniLM-L6-v2`는 가볍지만 한국어 및 복잡한 BMB(뇌/마음/행동) 도메인 지식의 미세한 뉘앙스를 포착하기 어렵습니다.
   -> **개선**: 높은 해상도의 다국어 지원 임베딩 모델(오픈소스 SOTA 또는 OpenAI 수준) 혹은 DGX-Spark의 GPU 자원을 활용할 수 있는 고성능 임베딩 모델로 교체합니다.
3. **FAISS의 검색 한계**: FAISS는 순수 벡터 유사도만 검색하며, 키워드나 메타데이터를 결합한 하이브리드 검색이 기본적으로 어렵습니다.
   -> **개선**: Qdrant 등 메타데이터 필터링 및 하이브리드 검색(Dense + Sparse)을 네이티브로 지원하는 최신 Vector DB 엔진으로 전환합니다.
4. **Ingestion 성능 저하**: 단일 프로세스로 문서를 임베딩하면 속도가 현저히 느립니다.
   -> **개선**: DGX-Spark의 강력한 멀티 GPU 리소스와 다중 워커(Multi-processing/Multi-threading)를 활용한 병렬 병렬 Ingestion 파이프라인(Batched GPU Inference)을 구축합니다.

## 3. GPU 기반 병렬 Ingestion 아키텍처 설계

* **Batched Inference**: 데이터를 청크 단위로 나눈 뒤, 배치(Batch)로 묶어 GPU 메모리에 올리고 병렬로 임베딩을 추출합니다.
* **Multiprocessing**: 문서 전처리(Loading, Chunking) 단계는 CPU 멀티프로세싱을 사용하여 IO 바운드 작업을 가속화합니다.
* **DB Client Batch Upload**: 추출된 벡터를 Vector DB 서버(예: Qdrant)에 비동기/배치로 업로드하여 네트워크 병목을 최소화합니다.
