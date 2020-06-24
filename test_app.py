import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import *


def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


JWT_MANAGER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlpNV3BPSWRVdmJVUmN1a0NkRDBiViJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS1wcm9qZWN0LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTUzNmNhNzcxYjI1MGI3NzE2NzU5MSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkyOTI1OTU1LCJleHAiOjE1OTMwMTIzNTUsImF6cCI6IjBYWlc1OTlaR25TRVcyN1E1Zzc0cnEzRFZReE9yb1U5Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cHJvamVjdHMiLCJkZWxldGU6dm9sdW50ZWVycyIsImdldDpwcm9qZWN0cyIsImdldDp2b2x1bnRlZXJzIiwicGF0Y2g6cHJvamVjdHMiLCJwYXRjaDp2b2x1bnRlZXJzIiwicG9zdDpwcm9qZWN0cyIsInBvc3Q6dm9sdW50ZWVycyJdfQ.003VO2_cEEN41NKuP_vsC1CPkT9e-I_Tsc-vK1QNNhgReCr6cE3sRSry1URpUENoHR2N4uOJ9mrkt3mfNlNscZVH8EOPNAKwEGuqJqtZ-kXCidI4gPKu-b8kqJctFjG2PVcNwQA53ypnE6jzBe3ht8hpQHIK3jYb2QHoT-dgp3N14s92CInoKQmwCgCKVKtMt4Vx2XbjP6jUQ9TKArSx8np9hGmr5O5YHamNrGynvSFKGmR2OYFEN0BV9Nv2vIg2ffIbiBPLS170EXDAZ-gaxlBMd20LYxOFirMn_5sq8oKyBbUroYmtg0Yeo9-X6GoX44sZyPSrc3qRXTNCLC7f_g'

JWT_COORDINATOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlpNV3BPSWRVdmJVUmN1a0NkRDBiViJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS1wcm9qZWN0LWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZTU4YTRkMjlhNWJhMGI2ZjU1ZmVmYyIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNTkyOTI2MDcwLCJleHAiOjE1OTMwMTI0NzAsImF6cCI6IjBYWlc1OTlaR25TRVcyN1E1Zzc0cnEzRFZReE9yb1U5Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dm9sdW50ZWVycyIsImdldDpwcm9qZWN0cyIsImdldDp2b2x1bnRlZXJzIiwicGF0Y2g6dm9sdW50ZWVycyIsInBvc3Q6dm9sdW50ZWVycyJdfQ.vp9Hz1f0jR77bhwfELxA8XJ5gHZ2GAjW0NjJpJDr78Bhw3giUbgM7VKisXUlhD2-xLadCTW2zlWsWCauk2ZTf0BbFvbJm-zGuqEo5tTEAwtYNA1ZUAxmYdhi6QglkW4yAIna-Wpoloh5IBKq1POYH4dbut4MBakI5XpHGOmjlHwHhNM4YlUwTw2cwNzwoeaiyLp1rkEdqfzJlxY5HYok5AwmB0XWndJb7ylPpLFdvIrcCGLEz2OlLJ7bp1Lq6xVA5YJY5wYy_9KHRUhnE25vHvSCwN-G715wXDtJ7g-CX6HyCqEOzxqfBfjWleF5GwZHoCNZmxo1SBNzIcKUIVbC1w'

SQLALCHEMY_DATABASE_URI = 'postgres://{}:{}@{}/{}'.format(
            'postgres', 'password', 'localhost:5432', 'capstone_db_test')


class VolunteerTestCase(unittest.TestCase):
    inserted_project_id = 0
    inserted_volunteer_id = 0

    def setUp(self):
        setup_db(app, SQLALCHEMY_DATABASE_URI)

        self.app = app
        self.database_path = SQLALCHEMY_DATABASE_URI
        setup_db(self.app, self.database_path)
        self.client = self.app.test_client

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_project = {
            "name": "Hospital patients happiness program",
            "description": "Help fill up \"get well soon\" balloons, setup"
                           " flowers in beautiful arrangements, and assist in"
                           " helping the patients fell optimistic about their"
                           " health.",
            "email": "abc@def.com",
            "phone": "(123) 456-7890"
        }

        self.new_volunteer = {
            "name": "Ricky",
            "email": "abc@def.com",
            "phone": "(123) 456-7890"
        }

        self.modified_project = {
            "email": "edit@def.com",
            "phone": "(098) 765-4321"
        }

        self.modified_volunteer = {
            "email": "edit@def.com",
            "phone": "(098) 765-4321"
        }

    def tearDown(self):
        pass

    def test_aa_get_projects_manager(self):
        res = self.client().get('/projects', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('count_projects', None))
        self.assertIsNotNone(data.get('projects', None))

    def test_ab_get_volunteers_manager(self):
        res = self.client().get('/volunteers', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('count_volunteers', None))
        self.assertIsNotNone(data.get('volunteers', None))

    def test_ac_post_projects_manager(self):
        res = self.client().post('/projects', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'}, json=self.new_project)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('project', None))

        global inserted_project_id
        inserted_project_id = data['project']['id']

    def test_ad_post_volunteers_manager(self):
        res = self.client().post('/volunteers', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'}, json=self.new_volunteer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('volunteer', None))

        global inserted_volunteer_id
        inserted_volunteer_id = data['volunteer']['id']

    def test_ae_patch_projects_manager(self):
        res = self.client().patch(f'/projects/{inserted_project_id}', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'},
                                  json=self.modified_project)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('project', None))

    def test_af_patch_volunteers_manager(self):
        res = self.client().patch(f'/volunteers/{inserted_volunteer_id}',
                                  headers={
                                      'Authorization': f'Bearer {JWT_MANAGER}'},
                                  json=self.modified_volunteer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('volunteer', None))

    def test_ag_delete_projects_manager(self):
        res = self.client().delete(f'/projects/{inserted_project_id}',
                                   headers={
                                       'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('project', None))

    def test_ah_delete_volunteers_manager(self):
        res = self.client().delete(f'/volunteers/{inserted_volunteer_id}',
                                   headers={
                                       'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('volunteer', None))

    def test_ba_error_get_projects_manager(self):
        res = self.client().get('/projects/1', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method not allowed')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('count_projects', None))
        self.assertIsNone(data.get('projects', None))

    def test_bb_error_get_volunteers_manager(self):
        res = self.client().get('/volunteers/1', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method not allowed')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('count_volunteers', None))
        self.assertIsNone(data.get('volunteers', None))

    def test_bc_error_post_projects_manager(self):
        res = self.client().post('/projects', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('project', None))

    def test_bd_error_post_volunteers_manager(self):
        res = self.client().post('/volunteers', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('volunteer', None))

    def test_be_error_patch_projects_manager(self):
        res = self.client().patch('/projects/1000000', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('project', None))

    def test_bf_error_patch_volunteers_manager(self):
        res = self.client().patch('/volunteers/1000000', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('volunteer', None))

    def test_bg_error_delete_projects_manager(self):
        res = self.client().delete('/projects/1000000', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('project', None))

    def test_bh_error_delete_volunteers_manager(self):
        res = self.client().delete('/volunteers/1000000}', headers={
            'Authorization': f'Bearer {JWT_MANAGER}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('volunteer', None))

    def test_ca_get_projects_coordinator(self):
        res = self.client().get('/projects', headers={
            'Authorization': f'Bearer {JWT_COORDINATOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('count_projects', None))
        self.assertIsNotNone(data.get('projects', None))

    def test_cb_get_volunteers_coordinator(self):
        res = self.client().get('/volunteers', headers={
            'Authorization': f'Bearer {JWT_COORDINATOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('count_volunteers', None))
        self.assertIsNotNone(data.get('volunteers', None))

    def test_cc_post_projects_coordinator(self):
        res = self.client().post('/projects', headers={
            'Authorization': f'Bearer {JWT_COORDINATOR}'},
                                 json=self.new_project)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('project', None))

    def test_cd_post_volunteers_coordinator(self):
        res = self.client().post('/volunteers', headers={
            'Authorization': f'Bearer {JWT_COORDINATOR}'},
                                 json=self.new_volunteer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('volunteer', None))

        global inserted_volunteer_id
        inserted_volunteer_id = data['volunteer']['id']

    def test_ce_patch_projects_coordinator(self):
        res = self.client().patch('/projects/1000000', headers={
            'Authorization': f'Bearer {JWT_COORDINATOR}'},
                                  json=self.modified_project)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('project', None))

    def test_cf_patch_volunteers_coordinator(self):
        res = self.client().patch(f'/volunteers/{inserted_volunteer_id}',
                                  headers={
                                      'Authorization': f'Bearer {JWT_COORDINATOR}'},
                                  json=self.modified_volunteer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('volunteer', None))

    def test_cg_delete_projects_coordinator(self):
        res = self.client().delete('/projects/1000000', headers={
            'Authorization': f'Bearer {JWT_COORDINATOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], 'Permission not found')
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data.get('success', None), False)
        self.assertIsNone(data.get('project', None))

    def test_ch_delete_volunteers_coordinator(self):
        res = self.client().delete(f'/volunteers/{inserted_volunteer_id}',
                                   headers={
                                       'Authorization': f'Bearer {JWT_COORDINATOR}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success', None), True)
        self.assertIsNotNone(data.get('volunteer', None))


if __name__ == '__main__':
    unittest.main()
