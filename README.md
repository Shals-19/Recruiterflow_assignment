# Recruiterflow Assignment

I built this as a Python FastAPI service with SQLite as the persistence layer. The project follows the assignment brief by loading the recruiter bot dataset, storing it in a raw-SQL schema, and exposing ranked job/candidate matches through API endpoints.

## What this project includes

- A raw SQLite schema for jobs and candidates
- Seed data for the fictional recruiter-flow dataset from the assignment
- Matching endpoints for both directions:
  - `GET /jobs/{id}/matches`
  - `GET /candidates/{id}/matches`
- A lightweight health check and CRUD endpoints for jobs and candidates
- `sql_detective.sql` containing the SQL answers for Part 2 of the brief

## How I approached the matching logic

I weighted skill overlap the most heavily because that is the clearest and most objective signal for whether a candidate is qualified for a role. I then added an experience component to reflect whether the person meets the posted minimum, and a small culture/trait bonus to capture how well the candidate's working style matches the role. The availability signal is intentionally light, since it is useful context but should not outweigh actual skill and seniority fit.

This was a deliberate trade-off: I wanted the ranking to be explainable and interview-friendly, not a black box. When I defend the ranking later, it is easy to point to the actual criteria that drove the score.

## How to run locally

1. Open a terminal in the project root.
2. Create and activate a virtual environment:

   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Start the API:

   uvicorn app:app --reload

5. Check the app:

   curl http://127.0.0.1:8000/health

6. Example matching calls:

   curl http://127.0.0.1:8000/jobs/1/matches
   curl http://127.0.0.1:8000/candidates/1/matches

## Example payloads

Create a job:

curl -X POST http://127.0.0.1:8000/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Backend Detective",
    "required_skills": ["deduction", "pattern-recognition", "forensics"],
    "min_experience": 3,
    "culture_keywords": ["analytical", "autonomous"],
    "tagline": "We have a bug."
  }'

Create a candidate:

curl -X POST http://127.0.0.1:8000/candidates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sherlock H.",
    "skills": ["deduction", "pattern-recognition", "forensics", "research"],
    "experience_years": 8,
    "availability": "Immediate",
    "traits": ["analytical", "blunt"],
    "quirk": "Solves problems by eliminating the impossible."
  }'

## AI usage note

I used Copilot mainly as a quick-check for syntax, structure, and cleanup while I worked on the API and tests. The key decisions around the schema, scoring model, and repository structure were mine, and I reviewed every result carefully before keeping it. The project is meant to reflect my understanding of the problem and the trade-offs I made, not a fully generated solution.

## Part 2 SQL detective

The SQL answers for the hiring-ops dataset are saved in `sql_detective.sql` and are intentionally written as plain SQL queries with one question per block.
