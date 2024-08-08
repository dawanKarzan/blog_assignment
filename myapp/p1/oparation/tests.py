import json
from django.test import TestCase
from rest_framework import status
from users.serializers import AuthorSerializer
class AppTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author_data = {
            "email": "dawankarzan18@gmail.com",
            "password": "12345678",
            "username": "author2",
            "phone_number": "0987654321",
            "first_name": "author",
            "last_name": "last author",
            "is_staff": False
        }
        authorSer = AuthorSerializer(data=cls.author_data)
        authorSer.is_valid(raise_exception=True)
        author = authorSer.save()
        cls.author_id = author.id
        # self.author_username = author.username
        cls.verify_code = author.verification_code
        cls.author_to_verify = {
            "email": "dawankarzan18@gmail.com",
            "verification_code": cls.verify_code
        }
        cls.post_invalid = {
            "title": "title one", 
              "html_body": "html body", 
               "tags": [
                  {
                      "name": "tag1"
                  },
                   {
                   "name": "old tag"
                  },
                   {
                      "name": "new tag"
                  } 
          ]
        }
        cls.tag = {
            "name": "new tag"
        }
        cls.tag_same = {
            "name": "new tag"
        }
        cls.tag_updated= {
            "name": "new tag 2"
        }
        cls.tag_invalid = {
        }
        cls.author_authenticated_data = {
            "email": "dawankarzan18@gmail.com",
            "password": "12345678"
        }
        cls.http = cls.client_class()
        super().setUpTestData()

    def setUp(self):
        super().setUp()
        response = self.client.post('/users/verify-email/', self.author_to_verify, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author_auth = self.client.post('/users/api/token/', data=self.__class__.author_authenticated_data)
        self.assertEqual(author_auth.status_code, status.HTTP_200_OK)
        self.author_token = author_auth.data['access']
        self.author_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.author_token}'
        }
        self.post = {
            "title": "title one", 
              "html_body": "html body", 
               "author": self.author_id, 
               "tags": [
                  {
                      "name": "tag1"
                  },
                   {
                   "name": "old tag"
                  },
                   {
                      "name": "new tag"
                  } 
          ]
        }
        self.new_post = {
            "title": "title one", 
              "html_body": "html body", 
               "tags": [
                  {
                      "name": "tag12"
                  } 
          ]
        }
        postResponse = self.client.post('/myapp/post/', self.post, content_type='application/json', headers=self.author_headers)
        self.assertEqual(postResponse.status_code, status.HTTP_201_CREATED)
        post = postResponse.data
        self.post_id = post['id']
        self.comment = {
            "post": self.post_id, 
            "body": "comment1"
        }
        commentResponse = self.client.post('/myapp/comment/', self.comment, content_type='application/json', headers=self.author_headers)
        self.assertEqual(commentResponse.status_code, status.HTTP_201_CREATED)
        comment = commentResponse.data
        self.comment_id = comment['id']
        self.comment_invalid = {
        }
        self.comment_reply = {
            "post": self.post_id, 
            "body": "comment2", 
            "author": self.author_id, 
            "parent": self.comment_id
        }

        self.like = {
            "post": self.post_id, 
        }
        self.like_invalid = {
        }
        self.favorite = {
            "post": self.post_id, 
        }
        self.favorite_invalid = {
        }
        likeResponse = self.client.post('/myapp/like/', self.like, content_type='application/json', headers=self.author_headers)
        self.assertEqual(commentResponse.status_code, status.HTTP_201_CREATED)
        like = likeResponse.data
        self.like_id = like['id']

        favoriteResponse = self.client.post('/myapp/favorite/', self.favorite, content_type='application/json', headers=self.author_headers)
        self.assertEqual(favoriteResponse.status_code, status.HTTP_201_CREATED)
        favorite = favoriteResponse.data
        self.favorite_id = favorite['id']
        
        tagsResponse = self.client.post('/myapp/tag/', self.tag, content_type='application/json', headers=self.author_headers)
        self.assertEqual(tagsResponse.status_code, status.HTTP_201_CREATED)
        tags = tagsResponse.data
        self.tags_id = tags['id']
        

    def tearDown(self) -> None:
        return super().tearDown()
    

    def test_post_not_found(self):
        res = self.client.post('/post/', self.post, content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_create_valid(self):
        post = self.new_post 
        res = self.client.post('/myapp/post/', data=post, headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_update_valid(self):
        post = json.dumps(self.post)
        res = self.client.put(f'/myapp/post/{self.post_id}/', post, headers=self.author_headers, content_type='application/json')

    def test_post_not_authorized(self):
        res = self.client.get('/myapp/post/', self.post, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_get_specific(self):
        res = self.client.get(f'/myapp/post/{self.post_id}/', headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_post_get_all(self):
        res = self.client.get('/myapp/post/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_post_delete(self):
        res = self.client.get(f'/myapp/post/{self.post_id}/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)



    def test_comment_not_found(self):
        res = self.client.post('/comment/', self.post, content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_create_valid(self):
        comment = self.comment 
        res = self.client.post('/myapp/comment/', data=comment, headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_comment_create_invalid(self):
        res = self.client.post('/myapp/comment/', self.comment_invalid, content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_create_reply(self):
        comment_reply = self.comment_reply
        res = self.client.post('/myapp/comment/', data=comment_reply, headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_comment_update_valid(self):
        comment = json.dumps(self.comment)
        res = self.client.put(f'/myapp/comment/{self.comment_id}/', comment, headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_comment_not_authorized(self):
        res = self.client.get('/myapp/comment/', data=self.comment, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_get_specific(self):
        res = self.client.get(f'/myapp/comment/{self.comment_id}/', headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_comment_get_all(self):
        res = self.client.get('/myapp/comment/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_comment_delete(self):
        res = self.client.get(f'/myapp/comment/{self.comment_id}/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)



    def test_like_not_found(self):
        res = self.client.post('/like/', self.like, content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_create_invalid(self):
        res = self.client.post('/myapp/like/', self.like_invalid, headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_update_valid(self):
        like = json.dumps(self.like)
        res = self.client.put(f'/myapp/like/{self.like_id}/', like, headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_like_not_authorized(self):
        res = self.client.get('/myapp/like/', self.like, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_get_specific(self):
        res = self.client.get(f'/myapp/like/{self.like_id}/', headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_like_get_all(self):
        res = self.client.get('/myapp/like/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_like_delete(self):
        res = self.client.get(f'/myapp/like/{self.like_id}/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)



    def test_favorite_not_found(self):
        res = self.client.post('/favorite/', self.favorite, content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_favorite_create_invalid(self):
        res = self.client.post('/myapp/like/', self.like_invalid, headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_favorite_not_authorized(self):
        res = self.client.get('/myapp/favorite/', self.favorite, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_favorite_get_specific(self):
        res = self.client.get(f'/myapp/favorite/{self.favorite_id}/', headers=self.author_headers, content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_favorite_get_all(self):
        res = self.client.get('/myapp/favorite/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_favorite_delete(self):
        res = self.client.get(f'/myapp/favorite/{self.favorite_id}/', content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)




    def test_tag_not_found(self):
        res = self.client.post('/tag/', self.tag, headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_tag_create_invalid(self):
        res = self.client.post('/myapp/tag/', self.tag_invalid, content_type='application/json', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tag_create_same(self):
        same = self.tag_same
        res = self.client.post('/myapp/tag/', data=same, headers=self.author_headers, content_type='application/json')
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_tag_update_valid(self):
        tag = json.dumps(self.tag)
        res = self.client.put(f'/myapp/tag/{self.tags_id}/', tag, headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_tag_not_authorized(self):
        res = self.client.get('/myapp/tag/', data=self.tag)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tag_get_specific(self):
        res = self.client.get(f'/myapp/tag/{self.tags_id}/', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_tag_get_all(self):
        res = self.client.get('/myapp/tag/', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_tag_delete(self):
        res = self.client.get(f'/myapp/tag/{self.tags_id}/', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_paginated_post_not_found(self):
        res = self.client.post('/paginated/post/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_paginated_post_get_all(self):
        res = self.client.get('/myapp/paginated/post')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_top_comment_get_all(self):
        res = self.client.get('/myapp/top/comment', headers=self.author_headers)
        # print('😀😀😀😀😀😀',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_top_like_get_all(self):
        res = self.client.get('/myapp/top/like', headers=self.author_headers)
        self.assertEqual(res.status_code, status.HTTP_200_OK)