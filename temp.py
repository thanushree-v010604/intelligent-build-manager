```python
import facebook

def post_facebook(accessToken, postText, image_url = None, page_id = None):
    graph = facebook.GraphAPI(accessToken)
    
    if page_id is None:
        page_id = graph.get_object(id='me')['id']
    
    post = {
    'message': postText,
    'source': image_url
    }
    
    post_id = graph.put_object(parent_object=page_id, connection_name='feed', 
                               message=postText, link=image_url, access_token=accessToken)
    
    return print("Facebook post successful")

def get_page_access_token(page_id, accessToken):
    graph = facebook.GraphAPI(accessToken)
    page_access_token = graph.get_connections(id=page_id, connection_name='access_token')
    return page_access_token['data'][0]['access_token']

access_token = 'YOUR_FB_ACCESS_TOKEN'
page_id = 'YOUR_FB_PAGE_ID'

# Using the provided access token
post_facebook(access_token, 'Hello from Facebook!')

# or using the page access token
page_access_token = get_page_access_token(page_id, access_token)
print(page_access_token)
post_facebook(page_access_token, 'Hello from Facebook!')
```