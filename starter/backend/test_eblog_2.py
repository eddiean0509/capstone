import json
import unittest
from datetime import datetime

from eblog import create_app, db
from eblog.models import Post, Reply, User

BASE_URL = "http://127.0.0.1:5000/post"


# token
BLOG_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBSTlVsSEw5bVZYLUpDSTNLdVlfQSJ9.eyJlbWFpbCI6ImJsb2dAdmVyLnRlYW0iLCJuYW1lIjoiYmxvZ0B2ZXIudGVhbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2Rldi1ocHkzdzBpcWd2eGpicTBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDM2NGY5NjdiNTI1ZjEwYWU2OTJkZGUiLCJhdWQiOlsiZWJsb2ciLCJodHRwczovL2Rldi1ocHkzdzBpcWd2eGpicTBwLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODEzNzI2NTgsImV4cCI6MTY4MTQ1OTA1OCwiYXpwIjoiU0tYVkxNc2REMWNKWUVyQXpuT0dPTkZsVWFTWVU1cFQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBvc3QiLCJkZWxldGU6cmVwbHkiLCJnZXQ6cG9zdCIsImdldDpyZXBseSIsInBvc3Q6cG9zdCIsInBvc3Q6cmVwbHkiLCJwdXQ6cG9zdCIsInB1dDpyZXBseSIsInZvdGU6cG9zdCIsInZvdGU6cmVwbHkiXX0.fOAIGOpaUmiskKc1fuM3lLFOf_o06bXJQ0svhS5NGJ7ua-RZurx8rOf3muWJJJ_s0fR2hpe2pnk9EHnIEWEKM2Mz1tJYf2z3SEznKowuGtSCC-nxu24OvCws6JIJU15GQU4ZY9QH4XfnkqtesRlvQJRfGxwAv3d9G3RccnVcZQeaxg3urWyEjSRQpOF40wBtfBSWe8RWvtWinq2SFoaqB3d0k8TbBid6pfDGEAz5Qic81Vidgr3-aNrPAzK2HR2TzXkMenphVo4psms2wQa3WLPunr2RPJbwrxgpTKBgzi8m5c0ql-s9ghnrgr1iHzz8JhUrwYYVNldx2jzGBez6zA"
NEIGHBOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBSTlVsSEw5bVZYLUpDSTNLdVlfQSJ9.eyJlbWFpbCI6Im5laWdoYm9yQHZlci50ZWFtIiwibmFtZSI6Im5laWdoYm9yQHZlci50ZWFtIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vZGV2LWhweTN3MGlxZ3Z4amJxMHAudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0MzY1MDBjNjY5YzZhMjY2Y2JhNGEzYyIsImF1ZCI6WyJlYmxvZyIsImh0dHBzOi8vZGV2LWhweTN3MGlxZ3Z4amJxMHAudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4MTM3MjYwMCwiZXhwIjoxNjgxNDU5MDAwLCJhenAiOiJTS1hWTE1zZEQxY0pZRXJBem5PR09ORmxVYVNZVTVwVCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cmVwbHkiLCJnZXQ6cmVwbHkiLCJwb3N0OnJlcGx5IiwicHV0OnJlcGx5Iiwidm90ZTpwb3N0Iiwidm90ZTpyZXBseSJdfQ.u3YCRqDOMc_Q7qzRZHdusmQeP3edBbwmh9naAVzbNZWqX7q3zLqnUlwb9wuzEvvnuuan9a5hw0b29oKl--j5R-4-5kqtFuFJqkn6W8DnssYSksPrQWlRZrxj9xgRkvEgut2N02Id5ueqvSJCphj-YpjgyT8HQqVvUse5Hzkpb1aRFZBsejly_0onT1AY8sudaTyxy7Qrl7WUwnWZSO4Sj6QEfrKXyHUP31nbK2xwfxRLd1Rk9FNC0PUT7JTW3_IiyzjXSVA05Cr5gGMHm1DWIO980i5jxexObHmnkMRj8jIDspWSgKx43HXXQCHGMs1sRe97L-Nrb8jQrKg1R0vYZQ"


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app(SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.client = self.app.test_client

    def tearDown(self):
        pass

    def test_posts(self):
        response = self.client().get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_read(self):
        self.create_post(username="blog", email="blog@ver.team")

        post_id = 1
        response = self.client().get(f"{BASE_URL}/{post_id}/")
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        self.create_post(username="blog", email="blog@ver.team")

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BLOG_TOKEN}"}
        data = {"subject": "Test Post", "content": "This is a test post."}
        response = self.client().post(BASE_URL, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

        # 404, empty data
        invalid_url = "http://127.0.0.1:5000/q"
        response = self.client().post(invalid_url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_post_modify(self):
        self.create_post(username="blog", email="blog@ver.team")

        post_id = 1
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BLOG_TOKEN}"}
        data = {
            "subject": "Modified Test Post",
            "content": "This is a modified test post.",
        }
        response = self.client().put(
            f"{BASE_URL}/{post_id}/", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)

        # 404, invalid_post
        invalid_post = 9999
        response = self.client().put(
            f"{BASE_URL}/{invalid_post}/", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 404)

    def test_post_delete(self):
        self.create_post(username="blog", email="blog@ver.team")

        post_id = 1
        headers = {"Authorization": f"Bearer {BLOG_TOKEN}"}
        response = self.client().delete(f"{BASE_URL}/{post_id}", headers=headers)
        self.assertEqual(response.status_code, 200)

        # 404, invalid_post
        invalid_post = 9999
        response = self.client().delete(
            f"{BASE_URL}/{invalid_post}/", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_post_vote(self):
        self.create_post(username="blog", email="blog@ver.team")
        self.create_post(username="neighbor", email="neighbor@ver.team")

        # blog vote to neighbor's post
        post_id = 2
        headers = {"Authorization": f"Bearer {BLOG_TOKEN}"}
        response = self.client().post(f"{BASE_URL}/{post_id}/vote", headers=headers)
        self.assertEqual(response.status_code, 200)

        # 404, invalid_post
        invalid_post = 9999
        headers = {"Authorization": f"Bearer {BLOG_TOKEN}"}
        response = self.client().post(f"{BASE_URL}/{invalid_post}/vote", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_reply_read(self):
        self.create_post(username="neighbor", email="neighbor@ver.team")

        post_id = 1
        reply_id = 1
        response = self.client().get(f"{BASE_URL}/{post_id}/reply/{reply_id}")
        self.assertEqual(response.status_code, 200)

        # 404, invalid post
        invalid_post = 9999
        response = self.client().get(f"{BASE_URL}/{invalid_post}/reply/{reply_id}")
        self.assertEqual(response.status_code, 200)

    def test_reply_modify(self):
        self.create_post(username="blog", email="blog@ver.team")

        post_id = 1
        reply_id = 1
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BLOG_TOKEN}"}
        data = {"content": "This is a modified test reply."}
        response = self.client().put(
            f"{BASE_URL}/{post_id}/reply/{reply_id}", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)

        # 404, invalid reply
        invalid_reply = 9999
        response = self.client().put(
            f"{BASE_URL}/{post_id}/reply/{invalid_reply}", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 404)

    def test_reply_create(self):
        self.create_post(username="neighbor", email="neighbor@ver.team")

        post_id = 1
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BLOG_TOKEN}"}
        data = {"content": "This is a test reply."}
        response = self.client().post(
            f"{BASE_URL}/{post_id}/reply", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)

        # 404, invalid post
        invalid_post = 9999
        response = self.client().post(
            f"{BASE_URL}/{invalid_post}/reply", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 404)

    def test_reply_delete(self):
        self.create_post(username="blog", email="blog@ver.team")

        post_id = 1
        reply_id = 1
        headers = {"Authorization": f"Bearer {BLOG_TOKEN}"}
        response = self.client().delete(
            f"{BASE_URL}/{post_id}/reply/{reply_id}", headers=headers
        )
        self.assertEqual(response.status_code, 200)

        # 404, invalid reply
        invalid_reply = 9999
        response = self.client().delete(
            f"{BASE_URL}/{post_id}/reply/{invalid_reply}", headers=headers
        )
        self.assertEqual(response.status_code, 404)

    def test_permission(self):
        self.create_post(username="blog", email="blog@ver.team")

        post_id = 1
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BLOG_TOKEN}"}
        data = {"content": "This is a test post."}
        response = self.client().post(
            f"{BASE_URL}/{post_id}/reply", headers=headers, data=json.dumps(data)
        )

        # neighbor does not have "post:post" permission
        self.assertEqual(response.status_code, 403)

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BLOG_TOKEN}"}
        data = {"content": "This is a test post."}
        response = self.client().post(
            f"{BASE_URL}/{post_id}", headers=headers, data=json.dumps(data)
        )

        # blog has "post:reply" permission
        self.assertEqual(response.status_code, 200)

    def create_post(self, username, email):
        # test user
        user = User(username=username, email=email, password="password")
        db.session.add(user)
        db.session.commit()

        # test post
        post = Post(
            subject="hello world", content="hello content", create_date=datetime.now(), user=user
        )
        db.session.add(post)
        db.session.commit()

        # test.reply
        reply = Reply(
            content="hello reply", user=user, post=post, create_date=datetime.now()
        )
        db.session.add(reply)
        db.session.commit()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
