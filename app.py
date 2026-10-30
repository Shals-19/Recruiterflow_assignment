import json
import sqlite3
from pathlib import Path
from typing import Any, List

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

DB_PATH = Path(__file__).resolve().parent / 'data' / 'recruiterflow.db'

app = FastAPI(title='Recruiterflow Recruiter Bot')


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except json.JSONDecodeError:
            pass
        return [part.strip() for part in value.split(',') if part.strip()]
    return []


def _seed_jobs() -> List[dict]:
    return [
        {
            'id': 1,
            'title': 'Backend Detective',
            'required_skills': ['deduction', 'pattern-recognition', 'forensics'],
            'min_experience': 3,
            'culture_keywords': ['analytical', 'autonomous'],
            'tagline': 'We have a bug. We have no leads. We have you.'
        },
        {
            'id': 2,
            'title': 'Rapid Prototyping Engineer',
            'required_skills': ['rapid-prototyping', 'systems-design'],
            'min_experience': 2,
            'culture_keywords': ['innovative', 'fast-paced'],
            'tagline': 'Ship first, document never (kidding — please document).'
        },
        {
            'id': 3,
            'title': 'Developer Relations Lead',
            'required_skills': ['public-speaking', 'research'],
            'min_experience': 2,
            'culture_keywords': ['energetic', 'curious'],
            'tagline': 'Explain complex things to confused humans, cheerfully.'
        },
        {
            'id': 4,
            'title': 'Engineering Manager, Chaos Team',
            'required_skills': ['team-building', 'stakeholder-management', 'leadership'],
            'min_experience': 5,
            'culture_keywords': ['empathetic', 'organized'],
            'tagline': 'Herd cats. The cats are senior engineers.'
        },
        {
            'id': 5,
            'title': 'Incident Commander',
            'required_skills': ['crisis-management', 'strategy', 'negotiation'],
            'min_experience': 4,
            'culture_keywords': ['decisive', 'calm-under-pressure'],
            'tagline': '3am page. You are the one who picks up.'
        },
        {
            'id': 6,
            'title': 'Sales Engineer',
            'required_skills': ['sales', 'public-speaking', 'negotiation'],
            'min_experience': 3,
            'culture_keywords': ['enthusiastic', 'persistent'],
            'tagline': 'Sell the vision, then go build it.'
        }
    ]


def _seed_candidates() -> List[dict]:
    return [
        {
            'id': 1,
            'name': 'Sherlock H.',
            'skills': ['deduction', 'pattern-recognition', 'forensics', 'research'],
            'experience_years': 8,
            'availability': 'Immediate',
            'traits': ['analytical', 'blunt'],
            'quirk': 'Solves problems by eliminating the impossible.'
        },
        {
            'id': 2,
            'name': 'Hermione G.',
            'skills': ['research', 'time-management', 'public-speaking'],
            'experience_years': 4,
            'availability': '2 weeks',
            'traits': ['detail-oriented', 'overachiever'],
            'quirk': 'Reads the entire documentation before writing a single line of code.'
        },
        {
            'id': 3,
            'name': 'Tony S.',
            'skills': ['systems-design', 'rapid-prototyping', 'leadership'],
            'experience_years': 12,
            'availability': 'Not looking',
            'traits': ['confident', 'innovative'],
            'quirk': 'Ships an MVP overnight, refuses to write tests.'
        },
        {
            'id': 4,
            'name': 'Leslie K.',
            'skills': ['project-management', 'stakeholder-management', 'public-speaking'],
            'experience_years': 6,
            'availability': 'Immediate',
            'traits': ['tenacious', 'organized'],
            'quirk': 'Has a binder for everything, including the binder.'
        },
        {
            'id': 5,
            'name': 'Ron S.',
            'skills': ['woodworking', 'minimalism', 'negotiation'],
            'experience_years': 15,
            'availability': 'Not looking',
            'traits': ['stubborn', 'principled'],
            'quirk': 'Refuses to use more than one monitor.'
        },
        {
            'id': 6,
            'name': 'Rick S.',
            'skills': ['systems-design', 'rapid-prototyping', 'chemistry'],
            'experience_years': 20,
            'availability': 'Immediate',
            'traits': ['genius', 'reckless'],
            'quirk': 'Solution works; mechanism deeply concerning.'
        },
        {
            'id': 7,
            'name': 'Elle W.',
            'skills': ['persuasion', 'research', 'public-speaking'],
            'experience_years': 3,
            'availability': 'Immediate',
            'traits': ['optimistic', 'sharp'],
            'quirk': 'Underestimated in every standup, correct in every retro.'
        },
        {
            'id': 8,
            'name': 'MacGyver',
            'skills': ['rapid-prototyping', 'resourcefulness', 'chemistry', 'systems-design'],
            'experience_years': 10,
            'availability': '2 weeks',
            'traits': ['calm', 'improviser'],
            'quirk': 'Fixes production outages with duct tape and a paperclip.'
        },
        {
            'id': 9,
            'name': 'Sheldon C.',
            'skills': ['theoretical-analysis', 'pattern-recognition', 'research'],
            'experience_years': 9,
            'availability': 'Immediate',
            'traits': ['rigid', 'brilliant'],
            'quirk': 'Correct 95% of the time; insufferable 100% of the time.'
        },
        {
            'id': 10,
            'name': 'Katniss E.',
            'skills': ['precision', 'strategy', 'crisis-management'],
            'experience_years': 5,
            'availability': 'Immediate',
            'traits': ['resilient', 'decisive'],
            'quirk': 'Excellent under pressure, terrible with public speaking.'
        },
        {
            'id': 11,
            'name': 'Michael S.',
            'skills': ['sales', 'public-speaking', 'team-building'],
            'experience_years': 11,
            'availability': 'Not looking',
            'traits': ['enthusiastic', 'chaotic'],
            'quirk': 'World\'s best boss, according to a mug he bought himself.'
        },
        {
            'id': 12,
            'name': 'Olivia P.',
            'skills': ['crisis-management', 'negotiation', 'strategy', 'leadership'],
            'experience_years': 13,
            'availability': '2 weeks',
            'traits': ['decisive', 'intense'],
            'quirk': 'Handles it. Whatever it is.'
        },
        {
            'id': 13,
            'name': 'Ted L.',
            'skills': ['team-building', 'optimism', 'mentorship', 'public-speaking'],
            'experience_years': 7,
            'availability': 'Immediate',
            'traits': ['empathetic', 'persistent'],
            'quirk': 'Turns every technical setback into a folksy metaphor.'
        },
        {
            'id': 14,
            'name': 'Miranda P.',
            'skills': ['leadership', 'negotiation', 'stakeholder-management', 'precision'],
            'experience_years': 18,
            'availability': 'Not looking',
            'traits': ['demanding', 'decisive'],
            'quirk': 'Reviews every PR personally. Says nothing. Everyone panics.'
        },
        {
            'id': 15,
            'name': 'Dwight S.',
            'skills': ['sales', 'negotiation', 'security', 'loyalty'],
            'experience_years': 9,
            'availability': 'Immediate',
            'traits': ['intense', 'loyal'],
            'quirk': 'Assistant to the regional backend engineer.'
        }
    ]


def _seed_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = _connect()
    conn.execute(
        '''
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            min_experience REAL NOT NULL,
            culture_keywords TEXT NOT NULL,
            tagline TEXT
        )
        '''
    )
    conn.execute(
        '''
        CREATE TABLE candidates (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            skills TEXT NOT NULL,
            experience_years REAL NOT NULL,
            availability TEXT NOT NULL,
            traits TEXT NOT NULL,
            quirk TEXT
        )
        '''
    )

    for job in _seed_jobs():
        conn.execute(
            'INSERT INTO jobs (id, title, required_skills, min_experience, culture_keywords, tagline) VALUES (?, ?, ?, ?, ?, ?)',
            (
                job['id'],
                job['title'],
                json.dumps(job['required_skills']),
                float(job['min_experience']),
                json.dumps(job['culture_keywords']),
                job['tagline'],
            ),
        )

    for candidate in _seed_candidates():
        conn.execute(
            'INSERT INTO candidates (id, name, skills, experience_years, availability, traits, quirk) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                candidate['id'],
                candidate['name'],
                json.dumps(candidate['skills']),
                float(candidate['experience_years']),
                candidate['availability'],
                json.dumps(candidate['traits']),
                candidate['quirk'],
            ),
        )

    conn.commit()
    conn.close()


_seed_database()


@app.on_event('startup')
def startup_event() -> None:
    _seed_database()


@app.get('/health')
def health() -> dict:
    return {'status': 'ok'}


@app.get('/jobs')
def list_jobs() -> List[dict]:
    conn = _connect()
    rows = conn.execute('SELECT * FROM jobs ORDER BY id').fetchall()
    conn.close()
    return [
        {
            'id': row['id'],
            'title': row['title'],
            'required_skills': _as_list(row['required_skills']),
            'min_experience': float(row['min_experience']),
            'culture_keywords': _as_list(row['culture_keywords']),
            'tagline': row['tagline'],
        }
        for row in rows
    ]


@app.post('/jobs', status_code=status.HTTP_201_CREATED)
def create_job(payload: dict) -> dict:
    title = (payload.get('title') or '').strip()
    required_skills = _as_list(payload.get('required_skills'))
    min_experience = payload.get('min_experience')
    culture_keywords = _as_list(payload.get('culture_keywords'))
    tagline = (payload.get('tagline') or '').strip()

    if not title or not required_skills or min_experience is None:
        raise HTTPException(status_code=400, detail='title, required_skills, and min_experience are required')

    conn = _connect()
    cursor = conn.execute(
        'INSERT INTO jobs (title, required_skills, min_experience, culture_keywords, tagline) VALUES (?, ?, ?, ?, ?)',
        (title, json.dumps(required_skills), float(min_experience), json.dumps(culture_keywords), tagline),
    )
    job_id = cursor.lastrowid
    job_row = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    conn.commit()
    conn.close()

    return {
        'id': job_row['id'],
        'title': job_row['title'],
        'required_skills': _as_list(job_row['required_skills']),
        'min_experience': float(job_row['min_experience']),
        'culture_keywords': _as_list(job_row['culture_keywords']),
        'tagline': job_row['tagline'],
    }


@app.get('/candidates')
def list_candidates() -> List[dict]:
    conn = _connect()
    rows = conn.execute('SELECT * FROM candidates ORDER BY id').fetchall()
    conn.close()
    return [
        {
            'id': row['id'],
            'name': row['name'],
            'skills': _as_list(row['skills']),
            'experience_years': float(row['experience_years']),
            'availability': row['availability'],
            'traits': _as_list(row['traits']),
            'quirk': row['quirk'],
        }
        for row in rows
    ]


@app.post('/candidates', status_code=status.HTTP_201_CREATED)
def create_candidate(payload: dict) -> dict:
    name = (payload.get('name') or '').strip()
    skills = _as_list(payload.get('skills'))
    experience_years = payload.get('experience_years')
    availability = (payload.get('availability') or '').strip()
    traits = _as_list(payload.get('traits'))
    quirk = (payload.get('quirk') or '').strip()

    if not name or not skills or experience_years is None or not availability:
        raise HTTPException(status_code=400, detail='name, skills, experience_years, and availability are required')

    conn = _connect()
    cursor = conn.execute(
        'INSERT INTO candidates (name, skills, experience_years, availability, traits, quirk) VALUES (?, ?, ?, ?, ?, ?)',
        (name, json.dumps(skills), float(experience_years), availability, json.dumps(traits), quirk),
    )
    candidate_id = cursor.lastrowid
    row = conn.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,)).fetchone()
    conn.commit()
    conn.close()

    return {
        'id': row['id'],
        'name': row['name'],
        'skills': _as_list(row['skills']),
        'experience_years': float(row['experience_years']),
        'availability': row['availability'],
        'traits': _as_list(row['traits']),
        'quirk': row['quirk'],
    }


def _match_score(job: dict, candidate: dict) -> tuple[int, str]:
    required_skills = set(skill.lower() for skill in _as_list(job['required_skills']))
    candidate_skills = set(skill.lower() for skill in _as_list(candidate['skills']))
    overlap = sorted(required_skills & candidate_skills)
    skill_score = len(overlap) * 50

    candidate_experience = float(candidate['experience_years'])
    required_experience = float(job['min_experience'])
    if candidate_experience >= required_experience:
        exp_gap = candidate_experience - required_experience
        experience_score = min(40, 20 + int(exp_gap * 10))
    else:
        exp_gap = required_experience - candidate_experience
        experience_score = max(-35, -int(exp_gap * 15))

    job_keywords = set(keyword.lower() for keyword in _as_list(job['culture_keywords']))
    candidate_traits = set(trait.lower() for trait in _as_list(candidate['traits']))
    culture_overlap = sorted(job_keywords & candidate_traits)
    culture_score = len(culture_overlap) * 12

    availability = str(candidate['availability']).lower()
    if 'immediate' in availability:
        availability_score = 8
    elif '2 weeks' in availability or 'weeks' in availability:
        availability_score = 4
    else:
        availability_score = 2

    total = skill_score + experience_score + culture_score + availability_score

    reason_parts = []
    if overlap:
        reason_parts.append(f"skill overlap ({len(overlap)}/{len(required_skills)})")
    else:
        reason_parts.append('no direct skill overlap')
    if candidate_experience >= required_experience:
        reason_parts.append(f"experience exceeds minimum by {candidate_experience - required_experience:.1f} years")
    else:
        reason_parts.append(f"experience is {required_experience - candidate_experience:.1f} years below minimum")
    if culture_overlap:
        reason_parts.append(f"culture match: {', '.join(culture_overlap[:2])}")
    if availability_score:
        reason_parts.append(f"availability: {candidate['availability']}")

    reason = '; '.join(reason_parts)
    return total, reason


@app.get('/jobs/{job_id}/matches')
def job_matches(job_id: int) -> dict:
    conn = _connect()
    job_row = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    if not job_row:
        conn.close()
        raise HTTPException(status_code=404, detail='Job not found')

    job = {
        'id': job_row['id'],
        'title': job_row['title'],
        'required_skills': _as_list(job_row['required_skills']),
        'min_experience': float(job_row['min_experience']),
        'culture_keywords': _as_list(job_row['culture_keywords']),
        'tagline': job_row['tagline'],
    }
    candidate_rows = conn.execute('SELECT * FROM candidates ORDER BY id').fetchall()
    conn.close()

    ranked = []
    for row in candidate_rows:
        candidate = {
            'id': row['id'],
            'name': row['name'],
            'skills': _as_list(row['skills']),
            'experience_years': float(row['experience_years']),
            'availability': row['availability'],
            'traits': _as_list(row['traits']),
            'quirk': row['quirk'],
        }
        score, reason = _match_score(job, candidate)
        ranked.append({
            'candidate_id': candidate['id'],
            'candidate_name': candidate['name'],
            'score': score,
            'reason': reason,
        })

    ranked.sort(key=lambda item: (-item['score'], -item['candidate_id']))
    return {'job_id': job['id'], 'job_title': job['title'], 'matches': ranked}


@app.get('/candidates/{candidate_id}/matches')
def candidate_matches(candidate_id: int) -> dict:
    conn = _connect()
    candidate_row = conn.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,)).fetchone()
    if not candidate_row:
        conn.close()
        raise HTTPException(status_code=404, detail='Candidate not found')

    candidate = {
        'id': candidate_row['id'],
        'name': candidate_row['name'],
        'skills': _as_list(candidate_row['skills']),
        'experience_years': float(candidate_row['experience_years']),
        'availability': candidate_row['availability'],
        'traits': _as_list(candidate_row['traits']),
        'quirk': candidate_row['quirk'],
    }
    job_rows = conn.execute('SELECT * FROM jobs ORDER BY id').fetchall()
    conn.close()

    ranked = []
    for row in job_rows:
        job = {
            'id': row['id'],
            'title': row['title'],
            'required_skills': _as_list(row['required_skills']),
            'min_experience': float(row['min_experience']),
            'culture_keywords': _as_list(row['culture_keywords']),
            'tagline': row['tagline'],
        }
        score, reason = _match_score(job, candidate)
        ranked.append({
            'job_id': job['id'],
            'job_title': job['title'],
            'score': score,
            'reason': reason,
        })

    ranked.sort(key=lambda item: (-item['score'], -item['job_id']))
    return {'candidate_id': candidate['id'], 'candidate_name': candidate['name'], 'matches': ranked}


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)
