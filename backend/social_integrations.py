"""
Social Media Integrations Module
Handles publishing to Instagram, Facebook, TikTok, YouTube, Twitter
"""

import os
import requests
import logging
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

# =========================
# INSTAGRAM INTEGRATION
# =========================

class InstagramPublisher:
    """Publish to Instagram using Graph API"""
    
    def __init__(self):
        self.access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
        self.business_account_id = os.environ.get('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def get_business_account_id(self) -> Optional[str]:
        """Get Instagram Business Account ID from token"""
        try:
            url = f"{self.base_url}/me/accounts"
            params = {'access_token': self.access_token}
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                page_id = data['data'][0]['id']
                
                # Get Instagram account linked to this page
                url = f"{self.base_url}/{page_id}"
                params = {
                    'fields': 'instagram_business_account',
                    'access_token': self.access_token
                }
                response = requests.get(url, params=params)
                ig_data = response.json()
                
                if 'instagram_business_account' in ig_data:
                    return ig_data['instagram_business_account']['id']
            
            return None
        except Exception as e:
            logger.error(f"Error getting Instagram Business Account ID: {str(e)}")
            return None
    
    def publish_photo(self, image_url: str, caption: str) -> Dict[str, Any]:
        """Publish a photo to Instagram"""
        try:
            if not self.business_account_id:
                self.business_account_id = self.get_business_account_id()
            
            if not self.business_account_id:
                return {
                    'success': False,
                    'error': 'Instagram Business Account ID not found. Please configure it.'
                }
            
            # Step 1: Create media container
            url = f"{self.base_url}/{self.business_account_id}/media"
            params = {
                'image_url': image_url,
                'caption': caption,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            data = response.json()
            
            if 'id' not in data:
                return {
                    'success': False,
                    'error': data.get('error', {}).get('message', 'Unknown error')
                }
            
            container_id = data['id']
            
            # Step 2: Publish the container
            url = f"{self.base_url}/{self.business_account_id}/media_publish"
            params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            publish_data = response.json()
            
            if 'id' in publish_data:
                return {
                    'success': True,
                    'post_id': publish_data['id'],
                    'platform': 'instagram'
                }
            else:
                return {
                    'success': False,
                    'error': publish_data.get('error', {}).get('message', 'Publishing failed')
                }
                
        except Exception as e:
            logger.error(f"Instagram publish error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def publish_carousel(self, media_urls: List[str], caption: str) -> Dict[str, Any]:
        """Publish a carousel (multiple images) to Instagram"""
        try:
            if not self.business_account_id:
                self.business_account_id = self.get_business_account_id()
            
            if not self.business_account_id:
                return {'success': False, 'error': 'Business Account ID not found'}
            
            # Step 1: Create media containers for each image
            media_ids = []
            for image_url in media_urls[:10]:  # Max 10 images in carousel
                url = f"{self.base_url}/{self.business_account_id}/media"
                params = {
                    'image_url': image_url,
                    'is_carousel_item': 'true',
                    'access_token': self.access_token
                }
                response = requests.post(url, params=params)
                data = response.json()
                
                if 'id' in data:
                    media_ids.append(data['id'])
            
            if not media_ids:
                return {'success': False, 'error': 'Failed to create carousel items'}
            
            # Step 2: Create carousel container
            url = f"{self.base_url}/{self.business_account_id}/media"
            params = {
                'caption': caption,
                'media_type': 'CAROUSEL',
                'children': ','.join(media_ids),
                'access_token': self.access_token
            }
            response = requests.post(url, params=params)
            data = response.json()
            
            if 'id' not in data:
                return {'success': False, 'error': 'Failed to create carousel'}
            
            container_id = data['id']
            
            # Step 3: Publish carousel
            url = f"{self.base_url}/{self.business_account_id}/media_publish"
            params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            response = requests.post(url, params=params)
            publish_data = response.json()
            
            if 'id' in publish_data:
                return {
                    'success': True,
                    'post_id': publish_data['id'],
                    'platform': 'instagram'
                }
            else:
                return {'success': False, 'error': 'Publishing failed'}
                
        except Exception as e:
            logger.error(f"Instagram carousel error: {str(e)}")
            return {'success': False, 'error': str(e)}


# =========================
# FACEBOOK INTEGRATION
# =========================

class FacebookPublisher:
    """Publish to Facebook using Graph API"""
    
    def __init__(self):
        self.access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        self.page_id = os.environ.get('FACEBOOK_PAGE_ID')
        self.base_url = "https://graph.facebook.com/v18.0"
    
    def get_page_id(self) -> Optional[str]:
        """Get Facebook Page ID from token"""
        try:
            url = f"{self.base_url}/me/accounts"
            params = {'access_token': self.access_token}
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                return data['data'][0]['id']
            
            return None
        except Exception as e:
            logger.error(f"Error getting Facebook Page ID: {str(e)}")
            return None
    
    def publish_text(self, message: str) -> Dict[str, Any]:
        """Publish text post to Facebook"""
        try:
            if not self.page_id:
                self.page_id = self.get_page_id()
            
            if not self.page_id:
                return {'success': False, 'error': 'Facebook Page ID not found'}
            
            url = f"{self.base_url}/{self.page_id}/feed"
            params = {
                'message': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            data = response.json()
            
            if 'id' in data:
                return {
                    'success': True,
                    'post_id': data['id'],
                    'platform': 'facebook'
                }
            else:
                return {
                    'success': False,
                    'error': data.get('error', {}).get('message', 'Unknown error')
                }
                
        except Exception as e:
            logger.error(f"Facebook publish error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def publish_photo(self, image_url: str, message: str) -> Dict[str, Any]:
        """Publish photo to Facebook"""
        try:
            if not self.page_id:
                self.page_id = self.get_page_id()
            
            if not self.page_id:
                return {'success': False, 'error': 'Facebook Page ID not found'}
            
            url = f"{self.base_url}/{self.page_id}/photos"
            params = {
                'url': image_url,
                'caption': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            data = response.json()
            
            if 'id' in data:
                return {
                    'success': True,
                    'post_id': data['id'],
                    'platform': 'facebook'
                }
            else:
                return {'success': False, 'error': data.get('error', {}).get('message', 'Unknown error')}
                
        except Exception as e:
            logger.error(f"Facebook photo error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def publish_link(self, link: str, message: str) -> Dict[str, Any]:
        """Publish link to Facebook"""
        try:
            if not self.page_id:
                self.page_id = self.get_page_id()
            
            if not self.page_id:
                return {'success': False, 'error': 'Facebook Page ID not found'}
            
            url = f"{self.base_url}/{self.page_id}/feed"
            params = {
                'link': link,
                'message': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            data = response.json()
            
            if 'id' in data:
                return {
                    'success': True,
                    'post_id': data['id'],
                    'platform': 'facebook'
                }
            else:
                return {'success': False, 'error': data.get('error', {}).get('message', 'Unknown error')}
                
        except Exception as e:
            logger.error(f"Facebook link error: {str(e)}")
            return {'success': False, 'error': str(e)}


# =========================
# UNIFIED PUBLISHER
# =========================

class SocialMediaPublisher:
    """Unified interface for all social media platforms"""
    
    def __init__(self):
        self.instagram = InstagramPublisher()
        self.facebook = FacebookPublisher()
    
    def publish(self, platform: str, content: str, media_urls: List[str] = None) -> Dict[str, Any]:
        """
        Publish content to specified platform
        
        Args:
            platform: 'instagram', 'facebook', 'tiktok', 'youtube', 'twitter'
            content: Text content/caption
            media_urls: List of image/video URLs
        
        Returns:
            Dict with success status and post_id or error
        """
        
        if not media_urls:
            media_urls = []
        
        try:
            if platform.lower() == 'instagram':
                if len(media_urls) == 0:
                    return {
                        'success': False,
                        'error': 'Instagram requires at least one image'
                    }
                elif len(media_urls) == 1:
                    return self.instagram.publish_photo(media_urls[0], content)
                else:
                    return self.instagram.publish_carousel(media_urls, content)
            
            elif platform.lower() == 'facebook':
                if len(media_urls) == 0:
                    return self.facebook.publish_text(content)
                elif len(media_urls) == 1:
                    return self.facebook.publish_photo(media_urls[0], content)
                else:
                    # Facebook doesn't have native carousel via API, post first image
                    return self.facebook.publish_photo(media_urls[0], content)
            
            elif platform.lower() == 'tiktok':
                return {
                    'success': False,
                    'error': 'TikTok integration coming soon. Requires video upload.'
                }
            
            elif platform.lower() == 'youtube':
                return {
                    'success': False,
                    'error': 'YouTube integration coming soon. Requires video upload.'
                }
            
            elif platform.lower() == 'twitter':
                return {
                    'success': False,
                    'error': 'Twitter integration coming soon. Requires Twitter API v2.'
                }
            
            else:
                return {
                    'success': False,
                    'error': f'Unknown platform: {platform}'
                }
                
        except Exception as e:
            logger.error(f"Publishing error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_platform_status(self) -> Dict[str, bool]:
        """Check which platforms are configured"""
        return {
            'instagram': bool(self.instagram.access_token),
            'facebook': bool(self.facebook.access_token),
            'tiktok': False,
            'youtube': False,
            'twitter': False
        }


# Helper function for easy import
def create_publisher() -> SocialMediaPublisher:
    """Create a social media publisher instance"""
    return SocialMediaPublisher()
