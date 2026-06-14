# API Reference (summary)

Full interactive Swagger UI is auto-generated at **`/docs`** and ReDoc at **`/redoc`**.

Base prefix: `/api/v1`

## Auth
| Method | Path | Body | Notes |
|---|---|---|---|
| POST | `/auth/register` | name, email, password, role | returns JWT |
| POST | `/auth/login` | email, password | returns JWT |
| GET | `/auth/me` | — | Bearer token |

## Chat / Agent
| POST | `/chat` | message, student_id? | runs the agent, returns `{answer, tool_used, sources}` |
| GET | `/chat/history/{student_id}` | — | conversation log |

## Library MCP
`GET /library/books` · `GET /library/books/{id}` · `POST /library/books` (admin) ·
`PUT /library/books/{id}` (admin) · `DELETE /library/books/{id}` (admin)

## Events MCP
`GET /events?upcoming=true` · `GET /events/{id}` · `POST /events` (admin)

## Cafeteria MCP
`GET /cafeteria/menu?today=true&category=lunch` · `POST /cafeteria/menu` (admin)

## Academics MCP
`GET /academics/notices` · `POST /academics/notices` (admin) ·
`GET /academics/exam-schedule` · `GET /academics/attendance-rules`

## RAG
`POST /rag/upload` (multipart PDF, auth) · `POST /rag/query` (query)

## Analytics
`GET /analytics/overview` · `/most-requested-books` · `/popular-queries` ·
`/menu-popularity` · `/events-attendance`

### Example
```bash
curl -X POST localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Is the DBMS book available?"}'
# => {"answer":"...","tool_used":"search_library","sources":[]}
```
