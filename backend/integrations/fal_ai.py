"""
FAL AI Wan 2.5 Integration
Video and Image Generation System
"""
import os
import requests
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import asyncio
import json

logger = logging.getLogger(__name__)


class FALAIClient:
    """
    FAL AI Wan 2.5 Client for video and image generation
    Supports: text-to-video, image-to-video, text-to-image, image-to-image
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('FAL_API_KEY')
        self.base_url = "https://queue.fal.run"
        
        if not self.api_key:
            logger.warning("FAL_API_KEY not configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with API key"""
        return {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def text_to_video(
        self,
        prompt: str,
        duration: int = 5,
        resolution: str = "720p",
        fps: int = 24,
        motion_intensity: float = 0.8,
        camera_control: Optional[Dict] = None,
        audio_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate video from text prompt
        
        Args:
            prompt: Text description of the video
            duration: Video duration in seconds (1-10)
            resolution: Video resolution (480p, 720p, 1080p)
            fps: Frames per second (24 recommended)
            motion_intensity: Motion intensity (0.0-1.0)
            camera_control: Optional camera movements
                Example: {"pan": "left", "zoom": "in", "speed": "slow"}
            audio_prompt: Optional audio description
            webhook_url: Optional webhook for completion notification
        
        Returns:
            Dict with request_id and status
        """
        if not self.api_key:
            raise ValueError("FAL_API_KEY not configured")
        
        payload = {
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution,
            "fps": fps,
            "motion_intensity": motion_intensity
        }
        
        if camera_control:
            payload["camera_control"] = camera_control
        
        if audio_prompt:
            payload["audio_prompt"] = audio_prompt
        
        if webhook_url:
            payload["webhook_url"] = webhook_url
        
        url = f"{self.base_url}/fal-ai/wan-25-preview/text-to-video"
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Text-to-video request submitted: {result.get('request_id')}")
            return result
            
        except Exception as e:
            logger.error(f"FAL AI text-to-video error: {e}")
            raise
    
    async def image_to_video(
        self,
        image_url: str,
        prompt: Optional[str] = None,
        duration: int = 5,
        resolution: str = "720p",
        motion_type: str = "smooth",
        camera_control: Optional[Dict] = None,
        audio_url: Optional[str] = None,
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate video from image
        
        Args:
            image_url: URL of the input image
            prompt: Optional text description to guide animation
            duration: Video duration in seconds
            resolution: Video resolution
            motion_type: Motion style (smooth, dynamic, cinematic)
            camera_control: Camera movements
            audio_url: Optional audio file URL
            webhook_url: Completion webhook
        
        Returns:
            Dict with request_id and status
        """
        if not self.api_key:
            raise ValueError("FAL_API_KEY not configured")
        
        payload = {
            "image_url": image_url,
            "duration": duration,
            "resolution": resolution,
            "motion_type": motion_type
        }
        
        if prompt:
            payload["prompt"] = prompt
        
        if camera_control:
            payload["camera_control"] = camera_control
        
        if audio_url:
            payload["audio_url"] = audio_url
        
        if webhook_url:
            payload["webhook_url"] = webhook_url
        
        url = f"{self.base_url}/fal-ai/wan-25-preview/image-to-video"
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Image-to-video request submitted: {result.get('request_id')}")
            return result
            
        except Exception as e:
            logger.error(f"FAL AI image-to-video error: {e}")
            raise
    
    async def text_to_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        num_images: int = 1,
        style: Optional[str] = None,
        negative_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate image from text prompt
        
        Args:
            prompt: Text description of the image
            width: Image width (256-2048)
            height: Image height (256-2048)
            num_images: Number of images to generate (1-4)
            style: Optional style (realistic, artistic, anime, etc.)
            negative_prompt: Things to avoid in image
        
        Returns:
            Dict with request_id and status
        """
        if not self.api_key:
            raise ValueError("FAL_API_KEY not configured")
        
        payload = {
            "prompt": prompt,
            "image_size": {
                "width": width,
                "height": height
            },
            "num_images": num_images
        }
        
        if style:
            payload["style"] = style
        
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        url = f"{self.base_url}/fal-ai/wan-25-preview/text-to-image"
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Text-to-image request submitted: {result.get('request_id')}")
            return result
            
        except Exception as e:
            logger.error(f"FAL AI text-to-image error: {e}")
            raise
    
    async def image_to_image(
        self,
        image_url: str,
        prompt: str,
        strength: float = 0.7,
        style: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transform image based on prompt
        
        Args:
            image_url: URL of input image
            prompt: Transformation description
            strength: Transformation strength (0.0-1.0)
            style: Optional style
        
        Returns:
            Dict with request_id and status
        """
        if not self.api_key:
            raise ValueError("FAL_API_KEY not configured")
        
        payload = {
            "image_url": image_url,
            "prompt": prompt,
            "strength": strength
        }
        
        if style:
            payload["style"] = style
        
        url = f"{self.base_url}/fal-ai/wan-25-preview/image-to-image"
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Image-to-image request submitted: {result.get('request_id')}")
            return result
            
        except Exception as e:
            logger.error(f"FAL AI image-to-image error: {e}")
            raise
    
    async def get_status(self, request_id: str) -> Dict[str, Any]:
        """
        Check status of a generation request
        
        Args:
            request_id: Request ID from submit
        
        Returns:
            Dict with status and result (if completed)
        """
        if not self.api_key:
            raise ValueError("FAL_API_KEY not configured")
        
        url = f"{self.base_url}/requests/{request_id}/status"
        
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            result = response.json()
            
            return result
            
        except Exception as e:
            logger.error(f"FAL AI status check error: {e}")
            raise
    
    async def wait_for_completion(
        self,
        request_id: str,
        timeout: int = 300,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """
        Wait for generation to complete
        
        Args:
            request_id: Request ID
            timeout: Maximum wait time in seconds
            poll_interval: Seconds between status checks
        
        Returns:
            Dict with final result
        """
        start_time = datetime.now()
        
        while True:
            status_response = await self.get_status(request_id)
            status = status_response.get('status')
            
            if status == 'COMPLETED':
                logger.info(f"Generation completed: {request_id}")
                return status_response
            
            elif status == 'FAILED':
                error = status_response.get('error', 'Unknown error')
                logger.error(f"Generation failed: {error}")
                raise Exception(f"Generation failed: {error}")
            
            # Check timeout
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > timeout:
                raise TimeoutError(f"Generation timeout after {timeout}s")
            
            # Wait before next check
            await asyncio.sleep(poll_interval)
    
    async def download_result(self, result_url: str, save_path: str) -> str:
        """
        Download generated video/image
        
        Args:
            result_url: URL of generated file
            save_path: Local path to save file
        
        Returns:
            Path to saved file
        """
        try:
            response = requests.get(result_url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Downloaded result to: {save_path}")
            return save_path
            
        except Exception as e:
            logger.error(f"Download error: {e}")
            raise


# Helper functions for common use cases

async def generate_product_video(
    fal_client: FALAIClient,
    product_name: str,
    product_description: str,
    product_image_url: Optional[str] = None,
    duration: int = 5
) -> Dict[str, Any]:
    """
    Generate marketing video for a product
    
    Args:
        fal_client: FAL AI client instance
        product_name: Product name
        product_description: Product description
        product_image_url: Optional product image
        duration: Video duration
    
    Returns:
        Dict with video URL and request details
    """
    # Create compelling prompt
    prompt = f"""
    Professional product demonstration video for {product_name}.
    {product_description}
    
    Cinematic lighting, smooth camera movements, professional product photography style.
    Show the product from multiple angles with elegant transitions.
    High quality, commercial-grade video.
    """
    
    if product_image_url:
        # Image-to-video if we have product image
        result = await fal_client.image_to_video(
            image_url=product_image_url,
            prompt=prompt,
            duration=duration,
            resolution="720p",
            motion_type="cinematic",
            camera_control={
                "zoom": "slow_in",
                "pan": "360",
                "speed": "smooth"
            }
        )
    else:
        # Text-to-video if no image
        result = await fal_client.text_to_video(
            prompt=prompt,
            duration=duration,
            resolution="720p",
            motion_intensity=0.7,
            camera_control={
                "zoom": "slow_in",
                "pan": "right_to_left",
                "speed": "smooth"
            }
        )
    
    return result


async def generate_social_media_content(
    fal_client: FALAIClient,
    product_name: str,
    platform: str = "instagram",
    style: str = "dynamic"
) -> Dict[str, Any]:
    """
    Generate social media optimized content
    
    Args:
        fal_client: FAL AI client instance
        product_name: Product name
        platform: Social media platform (instagram, tiktok, facebook)
        style: Content style
    
    Returns:
        Dict with content details
    """
    platform_specs = {
        "instagram": {"resolution": "1080p", "duration": 15, "aspect": "square"},
        "tiktok": {"resolution": "720p", "duration": 15, "aspect": "vertical"},
        "facebook": {"resolution": "720p", "duration": 30, "aspect": "landscape"}
    }
    
    specs = platform_specs.get(platform, platform_specs["instagram"])
    
    prompt = f"""
    Eye-catching {platform} video showcasing {product_name}.
    {style} style, trending format, engaging visuals.
    Perfect for {platform} feed, optimized for mobile viewing.
    Hook viewers in first 3 seconds.
    """
    
    result = await fal_client.text_to_video(
        prompt=prompt,
        duration=specs["duration"],
        resolution=specs["resolution"],
        motion_intensity=0.9 if style == "dynamic" else 0.6
    )
    
    return result


# Global FAL AI client instance
fal_client = None


def initialize_fal_client(api_key: str = None) -> FALAIClient:
    """Initialize global FAL AI client"""
    global fal_client
    fal_client = FALAIClient(api_key=api_key)
    return fal_client


def get_fal_client() -> FALAIClient:
    """Get global FAL AI client"""
    global fal_client
    if fal_client is None:
        fal_client = FALAIClient()
    return fal_client
