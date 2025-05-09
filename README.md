# 📦 Pyconnector 모듈 설명서

이 Python 모듈은 다음과 같은 외부 시스템과 연동하기 위한 기능을 제공합니다:
* **MySQL**: 관계형 데이터베이스 연동
* **Apache Kafka**: 메시지 큐 시스템
* **Elasticsearch**: 대용량 텍스트 기반 검색 및 분석
* **RabbitMQ**: 경량 메시지 브로커 시스템

모듈을 사용하기 전에 반드시 `settings.yml` 파일을 작성해야 하며, 시스템 접속에 필요한 정보들을 설정해야 합니다.

---

## ⚙️ 설정 파일 (`settings.yml`) 구조

아래는 `settings.yml` 파일에 포함되어야 하는 각 항목과 그 설명입니다:

| 섹션       | 속성            | 설명                                      | 예시 값        |
| -------- | ------------- | --------------------------------------- | ----------- |
| `db`     | `address`     | 데이터베이스 서버 주소                            | `127.0.0.1` |
|          | `port`        | 데이터베이스 포트 번호 (기본 MySQL: `3306`)         | `3306`      |
|          | `name`        | 접속할 데이터베이스 이름                           | `anydb`     |
|          | `username`    | 데이터베이스 사용자 이름                           | `user`      |
|          | `password`    | 데이터베이스 사용자 비밀번호                         | `pwd`       |
|          | `auto_commit` | 쿼리 실행 시 자동으로 커밋할지 여부 (`True` / `False`) | `True`      |
| `es`     | `address`     | Elasticsearch 서버 주소                     | `127.0.0.1` |
|          | `port`        | Elasticsearch 포트 번호 (기본: `9200`)        | `9200`      |
| `kafka`  | `address`     | Kafka 브로커 주소                            | `127.0.0.1` |
|          | `port`        | Kafka 브로커 포트 번호 (기본: `9092`)            | `9092`      |

---

## 🧩 주요 함수 및 기능

다음은 이 모듈에서 제공하는 핵심 기능들과 그 위치입니다:

| 모듈 위치                     | 함수                       | 설명                                     |
| ------------------------- | ------------------------ | -------------------------------------- |
| `handler.EarthlingDBPool` | `exec(...)`              | SQL 쿼리 실행 함수. SELECT, UPDATE 등의 쿼리를 실행 |
| `handler.earthling_es`    | `insert_list_to_es(...)` | 데이터 리스트를 Elasticsearch의 특정 인덱스에 저장     |
| `handler.earthling_mq`    | `consume()`              | Kafka에서 메시지를 수신하고, 파일로 저장 후 상태를 업데이트   |
| `handler.earthling_mq`    | `consume_action(...)`    | Kafka에서 수신한 메시지를 JSON 형태로 디코딩          |
| `handler.earthling_mq`    | `produce_action(...)`    | 메시지를 Kafka 전송을 위해 JSON 문자열로 직렬화        |
| `handler.earthling_mq`    | `produce(...)`           | Kafka로 메시지를 발행하는 함수                    |

---

## ✅ 사용 예시

```python
# DB 쿼리 예시
from handler.EarthlingDBPool import exec
result = exec("SELECT * FROM anytable WHERE id=1")

# Elasticsearch 저장 예시
from handler.earthling_es import insert_list_to_es
insert_list_to_es([{"field": "value"}], "my_index", "doc_type")

# Kafka 메시지 소비 예시
from handler.earthling_mq import consume
consume()

# Kafka 메시지 발행 예시
from handler.earthling_mq import produce
produce({"task_no": 1, "user_id": "john_doe"})
```

---

## 📝 비고

* `settings.yml`은 프로젝트 루트 디렉터리에 위치해야 하며, YAML 문법 오류가 없도록 주의해야 합니다.
* 데이터베이스 비밀번호, Kafka 접속 정보 등은 **환경변수 또는 보안 Vault**를 통해 관리하는 것을 권장합니다.
* Kafka 서버가 로컬이 아닌 경우, 반드시 방화벽 설정 및 인증 정책을 확인해야 합니다.