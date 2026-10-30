from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_create_job_and_match_candidate_to_job():
    job_payload = {
        'title': 'Backend Detective',
        'required_skills': ['deduction', 'pattern-recognition', 'forensics'],
        'min_experience': 3,
        'culture_keywords': ['analytical', 'autonomous'],
        'tagline': 'We have a bug.'
    }
    job_response = client.post('/jobs', json=job_payload)
    assert job_response.status_code == 201
    job = job_response.json()

    candidate_payload = {
        'name': 'Sherlock H.',
        'skills': ['deduction', 'pattern-recognition', 'forensics', 'research'],
        'experience_years': 8,
        'availability': 'Immediate',
        'traits': ['analytical', 'blunt'],
        'quirk': 'Solves problems by eliminating the impossible.'
    }
    candidate_response = client.post('/candidates', json=candidate_payload)
    assert candidate_response.status_code == 201
    candidate = candidate_response.json()

    matches = client.get(f"/jobs/{job['id']}/matches")
    assert matches.status_code == 200
    body = matches.json()
    assert body['job_id'] == job['id']
    assert body['matches']
    assert body['matches'][0]['candidate_id'] == candidate['id']
    assert 'score' in body['matches'][0]
    assert 'reason' in body['matches'][0]


def test_create_candidate_and_get_reverse_matches():
    job_payload = {
        'title': 'Rapid Prototyping Engineer',
        'required_skills': ['rapid-prototyping', 'systems-design'],
        'min_experience': 2,
        'culture_keywords': ['innovative', 'fast-paced'],
        'tagline': 'Ship first.'
    }
    job_response = client.post('/jobs', json=job_payload)
    job = job_response.json()

    candidate_payload = {
        'name': 'Tony S.',
        'skills': ['systems-design', 'rapid-prototyping', 'leadership'],
        'experience_years': 12,
        'availability': 'Not looking',
        'traits': ['confident', 'innovative'],
        'quirk': 'Ships an MVP overnight.'
    }
    candidate_response = client.post('/candidates', json=candidate_payload)
    candidate = candidate_response.json()

    matches = client.get(f"/candidates/{candidate['id']}/matches")
    assert matches.status_code == 200
    body = matches.json()
    assert body['candidate_id'] == candidate['id']
    assert body['matches']
    assert body['matches'][0]['job_id'] == job['id']
